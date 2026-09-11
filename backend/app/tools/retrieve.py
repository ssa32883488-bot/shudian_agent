# -*- coding: utf-8 -*-
"""检索类工具实现（题库 / 图谱 / 教材RAG+插图占位）。"""

from __future__ import annotations

import asyncio
import concurrent.futures
import logging
from typing import Any

from sqlalchemy.orm import Session

from app.config import get_settings
from app.services.figure_blocks import (
    extract_figures_from_chunk,
    figures_to_llm_appendix,
)
from app.services.graph_kg import knowledge_network, recommend_path
from app.services.question_bank import search_question_bank
from app.services.rag import TextbookRAG

logger = logging.getLogger(__name__)


def _run_coro(coro: Any) -> Any:
    """在可能已有事件循环的上下文中跑协程（工具多为同步入口）。"""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result(timeout=60)


async def _validate_bank_hit(
    user_query: str,
    bank_content: str,
    bank_answer: str,
    *,
    retrieval_score: float,
) -> dict[str, Any]:
    """校验：是否同一道题，且题库答案能否解决用户问题。"""
    from app.services.mimo import get_mimo
    from app.services.question_slots import hard_reject_bank_match

    hard = hard_reject_bank_match(user_query, bank_content)
    if hard:
        return {"usable": False, "reason": hard, "score": 0.0}

    mimo = get_mimo()
    match = await mimo.judge_question_match(
        user_query,
        bank_content,
        retrieval_score=retrieval_score,
    )
    if not match.get("matched"):
        return {
            "usable": False,
            "reason": match.get("reason") or "与用户题不是同一道",
            "score": float(match.get("score") or 0.0),
        }

    ans = (bank_answer or "").strip()
    if not ans:
        return {
            "usable": False,
            "reason": "题库条目无答案",
            "score": float(match.get("score") or 0.0),
        }

    if mimo.mock:
        return {
            "usable": True,
            "reason": f"Mock：同题匹配通过；{match.get('reason')}",
            "score": float(match.get("score") or 0.0),
        }

    import json
    import re

    prompt = (
        "用户问题与题库题已判定为同一道。请再判断【题库答案】是否足以直接回答用户所问。\n"
        "若答案缺失关键步骤/所求量，或答非所问 → usable=false。\n"
        '只输出 JSON：{"usable":true/false,"reason":"一句中文"}\n\n'
        f"【用户问题】\n{user_query[:1500]}\n\n"
        f"【题库答案】\n{ans[:2000]}"
    )
    try:
        content = await mimo.chat(
            [
                {
                    "role": "system",
                    "content": "你只做质检，输出严格 JSON。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        m = re.search(r"\{[\s\S]*\}", content or "")
        if not m:
            return {
                "usable": False,
                "reason": "答案质检无结构化结果，不放行",
                "score": float(match.get("score") or 0.0),
            }
        obj = json.loads(m.group(0))
        usable = bool(obj.get("usable"))
        return {
            "usable": usable,
            "reason": str(obj.get("reason") or ("答案可用" if usable else "答案不足")),
            "score": float(match.get("score") or 0.0),
        }
    except Exception as exc:  # noqa: BLE001
        logger.warning("bank answer usable check failed: %s", exc)
        return {
            "usable": False,
            "reason": f"答案质检异常，不放行：{exc}",
            "score": float(match.get("score") or 0.0),
        }


def format_bank_hit_answer(hit: dict[str, Any]) -> str:
    """原题直出：题库答案 + 可选解析，少包装。"""
    answer = (hit.get("answer") or "").strip()
    analysis = (hit.get("analysis") or "").strip()
    parts = ["**【题库原题解答】**", "", answer or "（题库无答案正文）"]
    if analysis and analysis != answer:
        parts.extend(["", "**【解析】**", "", analysis])
    return "\n".join(parts).strip()


def tool_search_question_bank(
    db: Session,
    query: str,
    top_k: int = 3,
) -> dict[str, Any]:
    """题库工具：题干 → 向量检索（≥阈值）→ 候选瀑布同题+答案校验。

    校验通过才返回题干+答案；否则 hit=false / message=无。
    """
    from app.services.embedding import get_embedding_service
    from app.services.rerank import get_rerank_service

    q = (query or "").strip()
    if db is None:
        return {
            "ok": False,
            "hit": False,
            "message": "无",
            "error": "数据库会话不可用",
        }
    if not q:
        return {
            "ok": True,
            "hit": False,
            "message": "无",
            "reason": "查询题干为空",
        }

    settings = get_settings()
    th = float(settings.hit_score_threshold)
    try:
        rows = search_question_bank(db, q, top_k=max(3, int(top_k or 3)))
    except Exception as exc:  # noqa: BLE001
        logger.warning("search_question_bank failed: %s", exc)
        return {
            "ok": True,
            "hit": False,
            "message": "无",
            "reason": f"检索异常：{exc}",
        }

    qualified = [r for r in rows if float(r.get("score") or 0.0) >= th]
    if not qualified:
        top_score = float(rows[0]["score"]) if rows else 0.0
        return {
            "ok": True,
            "hit": False,
            "message": "无",
            "reason": f"无达到阈值 {th:.2f} 的题库命中（最高 {top_score:.3f}）",
            "meta": {
                "threshold": th,
                "top_score": top_score,
                "embed_mode": get_embedding_service().mode,
                "rerank_mode": get_rerank_service().mode,
            },
        }

    last_reject: dict[str, Any] = {}
    for cand in qualified:
        score = float(cand.get("score") or 0.0)
        try:
            verdict = _run_coro(
                _validate_bank_hit(
                    q,
                    str(cand.get("content") or ""),
                    str(cand.get("answer") or ""),
                    retrieval_score=score,
                )
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("bank validate failed: %s", exc)
            last_reject = {
                "reason": f"同题校验失败：{exc}",
                "candidate_id": cand.get("question_id"),
                "candidate_score": score,
            }
            continue

        if not verdict.get("usable"):
            last_reject = {
                "reason": verdict.get("reason") or "同题/答案校验未通过",
                "candidate_id": cand.get("question_id"),
                "candidate_score": score,
                "match_score": verdict.get("score"),
            }
            continue

        return {
            "ok": True,
            "hit": True,
            "message": "命中题库原题（已校验同题且答案可用）",
            "question_id": cand.get("question_id"),
            "score": score,
            "content": cand.get("content") or "",
            "answer": cand.get("answer") or "",
            "analysis": cand.get("analysis") or "",
            "knowledge_tags": cand.get("knowledge_tags"),
            "source": cand.get("source"),
            "match_reason": verdict.get("reason") or "",
            "meta": {
                "threshold": th,
                "embed_mode": get_embedding_service().mode,
                "rerank_mode": get_rerank_service().mode,
            },
        }

    return {
        "ok": True,
        "hit": False,
        "message": "无",
        "reason": last_reject.get("reason") or "候选均未通过同题/答案校验",
        "meta": {
            "threshold": th,
            "tried": len(qualified),
            **{k: v for k, v in last_reject.items() if k != "reason"},
        },
    }


def tool_graph_query(concept: str, top_k: int = 6) -> dict[str, Any]:
    """知识图谱：路径推荐 + 逻辑链 + 相关题。"""
    concept = (concept or "").strip()
    if not concept:
        return {"ok": False, "error": "concept 为空"}
    path = recommend_path(concept)
    net = knowledge_network(text=concept, top_k=top_k, problems_per_concept=4)
    from app.services.graph_kg import _load_graph

    g = _load_graph()
    kg_engine = g.get("_engine") or "json"
    return {
        "ok": True,
        "tier": "runtime",
        "engine": f"kg_{kg_engine}",
        "path": {
            "target": path.get("target") or path.get("resolved"),
            "resolved": path.get("resolved"),
            "direct_prerequisites": path.get("direct_prerequisites") or [],
            "missing_prerequisites": path.get("missing_prerequisites") or [],
            "all_prerequisites": (path.get("all_prerequisites") or [])[:20],
            "suggestion": path.get("suggestion"),
            "path": path.get("path") or path.get("learning_chain") or [],
        },
        "network": {
            "keywords": net.get("keywords") or [],
            "learning_chain": net.get("learning_chain") or [],
            "related_problems": (net.get("related_problems") or [])[:10],
            "prompt_block": (net.get("prompt_block") or "")[:600],
        },
        "meta": {
            "concept": concept,
            "top_k": top_k,
            "kg_engine": kg_engine,
            "kg_source": g.get("_source"),
            "ui_hint": "学生可在 /kg 可视化页查看同一图谱，并一键带到答疑。",
        },
    }


def tool_retrieve_multi_rerank(question: str, top_k: int = 4) -> dict[str, Any]:
    """教材召回 + 精排；chunk 内凡有「图x…」则捞齐插图，以 FIGURE 文字块交给 LLM。"""
    question = (question or "").strip()
    if not question:
        return {"ok": False, "error": "question 为空", "hits": []}
    from app.services.embedding import get_embedding_service
    from app.services.rerank import get_rerank_service

    settings = get_settings()
    media_base = (settings.media_base_url or "").rstrip("/")
    min_score = float(settings.textbook_rag_score_threshold)
    fetch_k = max(top_k * 3, 8)
    rag = TextbookRAG()
    raw = rag.search(question, top_k=fetch_k, min_score=min_score)
    hits = []
    figures: list[dict[str, Any]] = []
    seen_fig: set[str] = set()
    for h in raw[:top_k]:
        chunk = h.get("text") or h.get("content") or ""
        hits.append(
            {
                "text": chunk[:800],
                "score": h.get("score"),
                "source": h.get("source"),
            }
        )
        for fig in extract_figures_from_chunk(chunk, media_base=media_base):
            key = fig.get("path") or fig.get("id") or ""
            if key and key not in seen_fig:
                seen_fig.add(key)
                figures.append(fig)
    appendix = figures_to_llm_appendix(figures)
    llm_context = "\n\n".join(
        f"[{i+1}] score={h.get('score')} {(h.get('text') or '')[:400]}"
        for i, h in enumerate(hits)
    )
    if appendix:
        llm_context = (llm_context + "\n\n" + appendix).strip()
    return {
        "ok": True,
        "hits": hits,
        "figures": figures,
        "llm_context": llm_context[:4000],
        "meta": {
            "top_k": top_k,
            "min_score": min_score,
            "embed_mode": get_embedding_service().mode,
            "rerank_mode": get_rerank_service().mode,
        },
    }

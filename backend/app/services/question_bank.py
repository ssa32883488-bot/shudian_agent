"""题库检索：向量召回 → 轻量精排 → 回填 SQL 权威答案。

刻意保持简单：只服务「是否原题」判断，不做教材级多路召回。
阈值分只认向量相似度（精排只重排，不抬分）。
"""

from __future__ import annotations

import logging
import re
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import QuestionBank
from app.services.chromadb_client import get_chroma_store
from app.services.rerank import get_rerank_service

logger = logging.getLogger(__name__)


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", (text or "").strip())


def _near_exact(query: str, content: str) -> bool:
    """冷启动兜底：题干几乎一字不差才算原题候选。"""
    a, b = _norm(query), _norm(content)
    if not a or not b:
        return False
    if a == b:
        return True
    # 短查询整段落在长题干里（用户贴了题干片段）
    if len(a) >= 24 and (a in b or b in a):
        return True
    return False


def search_question_bank(
    db: Session, query: str, top_k: int = 5
) -> list[dict[str, Any]]:
    """向量召回为主；Chroma 空时仅近原题文本兜底。score = 向量分。"""
    q = (query or "").strip()
    if not q:
        return []

    chroma_hits = get_chroma_store().search(q, top_k=max(top_k * 2, 6))
    candidates: dict[int, dict[str, Any]] = {}
    for h in chroma_hits:
        raw_id = h.get("question_id")
        if raw_id is None:
            continue
        qid = int(raw_id)
        candidates[qid] = {
            "question_id": qid,
            "content": h.get("content") or "",
            "score": float(h.get("score") or 0.0),
        }

    # 冷启动：向量库空时，只收近原题文本，给满分便于过阈值
    if not candidates:
        needle = q[:48]
        rows = db.scalars(
            select(QuestionBank)
            .where(QuestionBank.status == "active")
            .where(QuestionBank.content.ilike(f"%{needle}%"))
            .limit(top_k)
        ).all()
        for row in rows:
            if _near_exact(q, row.content):
                candidates[row.id] = {
                    "question_id": row.id,
                    "content": row.content,
                    "score": 1.0,
                }

    if not candidates:
        return []

    docs = [c["content"] for c in candidates.values()]
    ids = list(candidates.keys())
    ranked = get_rerank_service().rerank(q, docs, top_k=top_k)

    results: list[dict[str, Any]] = []
    for idx, _rr in ranked:
        qid = ids[idx]
        row = db.get(QuestionBank, qid)
        if not row or row.status != "active":
            continue
        results.append(
            {
                "question_id": row.id,
                "content": row.content,
                "answer": row.answer,
                "analysis": row.analysis,
                "knowledge_tags": row.knowledge_tags,
                "source": row.source,
                # 阈值只看向量分，不用精排分抬高假命中
                "score": float(candidates[qid]["score"]),
            }
        )
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def find_near_duplicates(
    db: Session,
    query: str,
    *,
    threshold: Optional[float] = None,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """入库前近重提示：score ≥ threshold 视为相近。"""
    settings = get_settings()
    th = float(threshold if threshold is not None else settings.hit_score_threshold)
    results = search_question_bank(db, (query or "").strip(), top_k=max(3, top_k))
    out: list[dict[str, Any]] = []
    for r in results:
        score = float(r.get("score") or 0.0)
        if score < th:
            continue
        out.append(
            {
                "question_id": r["question_id"],
                "content": r.get("content") or "",
                "answer": r.get("answer") or "",
                "source": r.get("source"),
                "score": score,
            }
        )
    return out[:top_k]


def sync_question_to_chroma(row: QuestionBank) -> None:
    """active → upsert；非 active → 从向量库删除。"""
    store = get_chroma_store()
    if (row.status or "").lower() != "active":
        store.delete_question(row.id)
        return
    store.upsert_question(
        question_id=row.id,
        content=row.content,
        metadata={"source": row.source or "", "status": row.status or "active"},
    )

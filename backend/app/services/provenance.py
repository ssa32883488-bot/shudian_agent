# -*- coding: utf-8 -*-
"""解题溯源：把「答案怎么来的」整理成可展示结构。"""

from __future__ import annotations

from typing import Any

# tool_trace 中的工具名 → 学生可读说明
_TOOL_LABELS: dict[str, str] = {
    "search_question_bank": "题库检索",
    "retrieve_multi_rerank": "教材知识库检索",
    "graph_query": "知识图谱查询",
    "draw_with_workflow": "绘图工作流",
    "draw_truth_table": "真值表",
    "draw_kmap": "卡诺图",
    "draw_logic": "逻辑图",
    "draw_wave": "波形图",
    "draw_state": "状态图",
    "read_profile": "学情画像",
    "memory_search": "长期记忆检索",
    "memory_upsert": "写入长期记忆",
    "memory_forget": "删除长期记忆",
}


def _tool_names(tool_trace: list[str] | None) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for raw in tool_trace or []:
        s = str(raw)
        name = ""
        if s.startswith("call:"):
            # call:foo args=...
            body = s[5:]
            name = body.split(" ", 1)[0].split("=", 1)[0].strip()
        elif s.startswith("result:"):
            name = s[7:].strip()
        elif "search_question_bank" in s:
            name = "search_question_bank"
        if not name or name in seen:
            continue
        seen.add(name)
        names.append(name)
    return names


def _friendly_tools(names: list[str]) -> list[str]:
    out: list[str] = []
    for n in names:
        if n.startswith("search_question_bank"):
            label = _TOOL_LABELS["search_question_bank"]
        else:
            label = _TOOL_LABELS.get(n, n)
        if label not in out:
            out.append(label)
    return out


def _kg_chapters(kg: dict[str, Any] | None) -> list[str]:
    if not kg:
        return []
    chapters: list[str] = []
    seen: set[str] = set()

    def add(ch: str) -> None:
        t = (ch or "").strip()
        if not t or t in seen:
            return
        seen.add(t)
        chapters.append(t)

    for key in ("chapters",):
        for ch in kg.get(key) or []:
            add(str(ch))

    for m in kg.get("matched") or []:
        if isinstance(m, dict):
            add(str(m.get("chapter") or ""))

    for p in kg.get("paths") or []:
        if isinstance(p, dict):
            add(str(p.get("chapter") or ""))

    for p in kg.get("related_problems") or []:
        if isinstance(p, dict):
            add(str(p.get("chapter_id") or p.get("chapter") or ""))

    # 从知识点名推断「第N章」样式（若图谱已写入 chapter 字段）
    return chapters[:8]


def build_solve_provenance(state: dict[str, Any]) -> dict[str, Any]:
    """从 SolveState 汇总溯源，供前端「溯源」区展示。"""
    intent = str(state.get("intent") or "").lower()
    plan = state.get("decision_plan") or {}
    if isinstance(plan, dict) and not intent:
        intent = str(plan.get("intent") or "").lower()

    hit = bool(state.get("hit"))
    tool_trace = list(state.get("tool_trace") or [])
    tool_names = _tool_names(tool_trace)
    tools = _friendly_tools(tool_names)
    kg = state.get("kg_context") if isinstance(state.get("kg_context"), dict) else None
    keywords = list((kg or {}).get("keywords") or [])[:8]
    chapters = _kg_chapters(kg)
    textbook_hits = list(state.get("textbook_hits") or [])
    textbook_chapters: list[str] = []
    for h in textbook_hits:
        if isinstance(h, dict):
            ch = str(h.get("chapter") or "").strip()
            if ch and ch not in textbook_chapters:
                textbook_chapters.append(ch)
    textbook_chapters = textbook_chapters[:6]

    bank_checked = hit or any(
        "search_question_bank" in str(t) for t in tool_trace
    )

    bank: dict[str, Any] | None = None
    if hit:
        qid = state.get("hit_question_id")
        score = state.get("hit_score")
        payload = state.get("hit_payload") if isinstance(state.get("hit_payload"), dict) else {}
        bank = {
            "id": qid,
            "score": float(score) if score is not None else None,
            "reason": state.get("match_reason") or payload.get("match_reason") or "",
            "label": payload.get("source") or payload.get("message") or "正式题库",
            "tags": payload.get("knowledge_tags") or [],
        }

    if hit:
        origin = "question_bank"
        score_s = ""
        if bank and bank.get("score") is not None:
            score_s = f"，相似度 {float(bank['score']):.3f}"
        summary = f"正式题库命中原题#{bank['id'] if bank else '?'}{score_s}"
    elif intent in {"chat", "smalltalk", "greeting"}:
        origin = "system"
        summary = "系统对话说明（非标准解题结论）"
    elif intent in {"study_plan", "syllabus"}:
        origin = "system"
        summary = "学习规划 / 大纲导引（结合知识图谱）"
    else:
        origin = "ai_solve"
        bits = ["AI 现解（仅供参考"]
        if bank_checked:
            bits.append("，题库未命中原题")
        if textbook_chapters or "教材知识库检索" in tools:
            bits.append("，并参考了教材摘录")
        elif keywords:
            bits.append("，并锚定了知识图谱考点")
        bits.append("）")
        summary = "".join(bits)

    return {
        "origin": origin,
        "summary": summary,
        "intent": intent or None,
        "bank_checked": bank_checked,
        "bank": bank,
        "knowledge_graph": {
            "keywords": keywords,
            "chapters": chapters,
            "related_problems": [
                str(p.get("problem_id"))
                for p in ((kg or {}).get("related_problems") or [])
                if isinstance(p, dict) and p.get("problem_id")
            ][:8],
            "learning_chain": list((kg or {}).get("learning_chain") or [])[:8],
            "source": (kg or {}).get("source"),
        }
        if (keywords or chapters or kg)
        else None,
        "textbook": {
            "chapters": textbook_chapters,
            "hit_count": len(textbook_hits),
        }
        if (textbook_chapters or any("retrieve_multi" in str(t) for t in tool_trace))
        else None,
        "tools": tools,
    }

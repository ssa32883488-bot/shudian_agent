"""LangGraph：决策者规划 → 题库预检索（原题直出）→ 未命中再 ReAct。"""

from __future__ import annotations

import logging
from typing import Any, Literal, Optional, TypedDict

from langgraph.graph import END, StateGraph
from sqlalchemy.orm import Session

from app.agents.decision_maker import DecisionPlan, make_decision, plan_from_dict
from app.services.graph_kg import assist_complex, knowledge_network
from app.services.mimo import get_mimo
from app.services.reflow import write_reflow

logger = logging.getLogger(__name__)


class SolveState(TypedDict, total=False):
    text: Optional[str]
    image_base64: Optional[str]
    reflow_stem: Optional[str]
    reflow_image_path: Optional[str]
    db: Any
    user_id: Optional[int]
    thread_id: Optional[str]
    memory_brief: Optional[str]
    profile_snapshot: Optional[dict[str, Any]]
    question_text: str
    source: Literal["text", "image", "mixed"]
    decision_plan: dict[str, Any]
    intent: str
    hit: bool
    hit_payload: Optional[dict[str, Any]]
    match_passed: bool
    match_score: float
    match_reason: str
    ai_answer: str
    ai_analysis: str
    validate_passed: bool
    validate_score: float
    validate_reason: str
    kg_context: Optional[dict[str, Any]]
    images: list[str]
    scope_notice: str
    task_heavy: bool
    trust_level: Literal["authoritative", "ai_reference"]
    trust_label: str
    answer: str
    analysis: Optional[str]
    hit_question_id: Optional[int]
    hit_score: Optional[float]
    reflowed: bool
    reflow_id: Optional[int]
    tool_trace: list[str]
    bank_prefetch_note: str
    trace: list[str]


def _trace(state: SolveState, msg: str) -> list[str]:
    t = list(state.get("trace") or [])
    t.append(msg)
    logger.info("[solve_graph] %s", msg)
    return t


def _plan(state: SolveState) -> DecisionPlan:
    return plan_from_dict(state.get("decision_plan")) or DecisionPlan(
        intent="solve",
        summary="默认解题规划",
        steps=[],
        needs_drawing=False,
        allow_bank_answer=True,
    )


def node_normalize(state: SolveState) -> dict[str, Any]:
    text = (state.get("text") or "").strip()
    image = state.get("image_base64")
    if image and text:
        source: Literal["text", "image", "mixed"] = "mixed"
    elif image:
        source = "image"
    else:
        source = "text"
    return {
        "question_text": text,
        "source": source,
        "trace": _trace(state, f"输入归一 source={source}"),
        "reflowed": False,
        "reflow_id": None,
        "hit": False,
        "hit_payload": None,
        "hit_question_id": None,
        "hit_score": None,
        "match_passed": False,
        "bank_prefetch_note": "",
    }


async def node_ocr_or_text(state: SolveState) -> dict[str, Any]:
    text = state.get("question_text") or ""
    image = state.get("image_base64")
    if image:
        ocr_text = await get_mimo().ocr_extract_question(image)
        merged = ocr_text if not text else f"{text}\n{ocr_text}"
        return {"question_text": merged.strip(), "trace": _trace(state, "OCR/视模型识别完成")}
    if not text:
        return {"question_text": "", "trace": _trace(state, "无文本无图片，题面为空")}
    return {"question_text": text, "trace": _trace(state, "使用文本题面")}


async def node_decide(state: SolveState) -> dict[str, Any]:
    q = state.get("question_text") or ""
    plan = await make_decision(q, has_image=bool(state.get("image_base64")))
    return {
        "decision_plan": plan.to_dict(),
        "intent": plan.intent,
        "trace": _trace(state, f"决策者 intent={plan.intent} | {plan.status_line()}"),
    }


def node_scope_task(state: SolveState) -> dict[str, Any]:
    """题量分流：解题链路始终评估。"""
    from app.agents.guardrails import estimate_and_scope_question

    scope = estimate_and_scope_question(state.get("question_text") or "")
    if not scope.is_heavy:
        return {
            "scope_notice": "",
            "task_heavy": False,
            "trace": _trace(state, f"题量评估轻量 items≈{scope.estimated_items}"),
        }
    return {
        "question_text": scope.scoped_text,
        "scope_notice": scope.notice,
        "task_heavy": True,
        "trace": _trace(
            state,
            f"题量过重裁剪 estimated={scope.estimated_items} answered={scope.answered_items}",
        ),
    }


def node_bank_prefetch(state: SolveState) -> dict[str, Any]:
    """解题意图：进 ReAct 前查一次题库；命中则权威直出，省掉后续 LLM。"""
    from app.tools.retrieve import format_bank_hit_answer, tool_search_question_bank

    plan = _plan(state)
    intent = (plan.intent or state.get("intent") or "").lower()
    if intent != "solve":
        return {
            "hit": False,
            "bank_prefetch_note": "",
            "trace": _trace(state, f"非解题意图，跳过题库预检索 intent={intent}"),
        }

    q = (state.get("question_text") or "").strip()
    db = state.get("db")
    if not q or db is None:
        return {
            "hit": False,
            "bank_prefetch_note": "题库预检索：无（题面或库不可用）",
            "trace": _trace(state, "题库预检索跳过（无题面/无库）"),
        }

    result = tool_search_question_bank(db, q, top_k=3)
    if not result.get("hit"):
        note = "题库预检索：无命中原题，请直接解题，不必再调 search_question_bank。"
        return {
            "hit": False,
            "hit_payload": None,
            "bank_prefetch_note": note,
            "tool_trace": ["search_question_bank:miss"],
            "trace": _trace(
                state,
                f"题库预检索未命中 reason={result.get('reason') or result.get('message')}",
            ),
        }

    answer = format_bank_hit_answer(result)
    notice = (state.get("scope_notice") or "").strip()
    if notice and notice not in answer:
        answer = notice + answer
    qid = result.get("question_id")
    score = float(result.get("score") or 0.0)
    analysis = (
        f"**来源**：题库原题#{qid}（向量分 {score:.3f}）\n"
        f"**校验**：{result.get('match_reason') or '同题且答案可用'}"
    )
    return {
        "hit": True,
        "hit_payload": result,
        "hit_question_id": int(qid) if qid is not None else None,
        "hit_score": score,
        "match_passed": True,
        "match_score": score,
        "match_reason": str(result.get("match_reason") or ""),
        "trust_level": "authoritative",
        "trust_label": "题库原题·权威解答",
        "ai_answer": answer,
        "ai_analysis": analysis,
        "answer": answer,
        "analysis": analysis,
        "images": [],
        "validate_passed": True,
        "validate_score": 1.0,
        "validate_reason": "题库原题，跳过 AI 评审",
        "reflowed": False,
        "reflow_id": None,
        "tool_trace": [f"search_question_bank:hit:{qid}"],
        "bank_prefetch_note": "",
        "trace": _trace(state, f"题库原题直出 id={qid} score={score:.3f}"),
    }


def route_after_bank(state: SolveState) -> Literal["bank_done", "kg_ground"]:
    return "bank_done" if state.get("hit") else "kg_ground"


def node_bank_done(state: SolveState) -> dict[str, Any]:
    return {"trace": _trace(state, "题库命中交付，跳过图谱/ReAct/回流")}


def node_kg_ground(state: SolveState) -> dict[str, Any]:
    plan = _plan(state)
    q = state.get("question_text") or ""
    if not q:
        return {"kg_context": None, "trace": _trace(state, "跳过图谱锚定（无题面）")}
    if plan.intent == "chat":
        return {"kg_context": None, "trace": _trace(state, "寒暄跳过图谱")}
    try:
        if plan.intent in {"study_plan", "syllabus"}:
            net = assist_complex(text=q, goal=plan.intent)
        else:
            net = knowledge_network(text=q, top_k=6, problems_per_concept=3)
        return {
            "kg_context": net,
            "trace": _trace(state, f"图谱/计划锚定 keywords={len(net.get('keywords') or [])}"),
        }
    except Exception as exc:
        logger.warning("图谱锚定失败: %s", exc)
        return {"kg_context": None, "trace": _trace(state, f"图谱锚定失败: {exc}")}


async def node_ai_solve(state: SolveState) -> dict[str, Any]:
    from app.agents.tutor_react import run_tutor_react

    q = state.get("question_text") or ""
    kg = state.get("kg_context") or {}
    plan = _plan(state)
    result = await run_tutor_react(
        q,
        db=state.get("db"),
        kg_context=kg.get("prompt_block"),
        memory_brief=state.get("memory_brief"),
        user_id=state.get("user_id"),
        bank_prefetch_note=state.get("bank_prefetch_note") or "",
    )
    analysis = f"**决策规划**：{plan.summary}\n\n" + (result.get("analysis") or "")
    if kg.get("keywords"):
        analysis = (
            f"**考点**：{'、'.join(kg['keywords'])}\n"
            f"**逻辑链**：{' → '.join((kg.get('learning_chain') or [])[:10])}\n\n{analysis}"
        )
    answer = result["answer"]
    notice = (state.get("scope_notice") or "").strip()
    if notice and notice not in answer:
        answer = notice + answer
    images = list(result.get("images") or [])
    tool_trace = list(state.get("tool_trace") or [])
    tool_trace.extend(str(t) for t in (result.get("tool_trace") or []))
    return {
        "trust_level": "ai_reference",
        "trust_label": "AI解答，仅供参考·不一定准确",
        "ai_answer": answer,
        "ai_analysis": analysis.strip(),
        "answer": answer,
        "analysis": analysis.strip(),
        "images": images,
        "tool_trace": tool_trace,
        "trace": _trace(state, f"ReAct 完成 tools={len(tool_trace)}"),
    }


async def node_validate(state: SolveState) -> dict[str, Any]:
    from app.services.draw_blocks import drawing_requirement_met, wants_drawing_tools

    q = state.get("question_text") or ""
    ans = state.get("ai_answer") or state.get("answer") or ""
    result = await get_mimo().validate_authority(q, ans)
    reason = str(result.get("reason") or "")
    score = float(result["score"])
    passed = bool(result["passed"])

    if wants_drawing_tools(q) and not drawing_requirement_met(q, ans):
        score = min(score, 0.35)
        passed = False
        note = "题面要求配图，但解答中未见工具产物图"
        reason = f"{note}；{reason}".strip("；")
        analysis_extra = f"\n\n> **配图检查未通过**：{note}"
    else:
        analysis_extra = ""

    analysis = (state.get("analysis") or "").rstrip()
    if "权威评审" not in analysis:
        analysis += (
            f"\n\n---\n**权威评审**：{'通过' if passed else '未通过'}（{score:.2f}）\n{reason}"
        )
    analysis += analysis_extra
    return {
        "validate_passed": passed,
        "validate_score": score,
        "validate_reason": reason,
        "analysis": analysis,
        "ai_analysis": analysis,
        "trace": _trace(state, f"权威评审 passed={passed} score={score:.3f}"),
    }


def route_after_validate(state: SolveState) -> Literal["reflow", "skip_reflow"]:
    from app.services.draw_blocks import drawing_requirement_met, wants_drawing_tools

    if state.get("hit"):
        return "skip_reflow"
    intent = (state.get("intent") or "").lower()
    if intent in {
        "explain",
        "study_plan",
        "syllabus",
        "chat",
        "greeting",
        "knowledge_query",
    }:
        return "skip_reflow"
    ans = (state.get("ai_answer") or state.get("answer") or "").strip()
    q = (state.get("question_text") or "").strip()
    if not ans or not q:
        return "skip_reflow"
    if wants_drawing_tools(q) and not drawing_requirement_met(q, ans):
        return "skip_reflow"
    return "reflow"


def node_reflow(state: SolveState) -> dict[str, Any]:
    stem = (state.get("reflow_stem") or state.get("question_text") or "").strip()
    if stem.startswith("【当前子任务】"):
        parts = stem.split("【完整识读文本", 1)
        stem = parts[0].replace("【当前子任务】", "", 1).strip()
    item = write_reflow(
        state["db"],
        question=stem,
        ai_answer=state.get("ai_answer") or state.get("answer") or "",
        validate_score=float(state.get("validate_score") or 0.0),
        source=state.get("source") or "text",
        image_base64=state.get("image_base64"),
        image_path=state.get("reflow_image_path"),
    )
    return {
        "reflowed": True,
        "reflow_id": item.id,
        "trace": _trace(state, f"回流待审 id={item.id} stem_len={len(stem)}"),
    }


def node_skip_reflow(state: SolveState) -> dict[str, Any]:
    from app.services.draw_blocks import drawing_requirement_met, wants_drawing_tools

    if state.get("hit"):
        return {
            "reflowed": False,
            "reflow_id": None,
            "trace": _trace(state, "跳过回流（题库原题）"),
        }
    q = (state.get("question_text") or "").strip()
    ans = (state.get("ai_answer") or state.get("answer") or "").strip()
    reason = "跳过回流"
    if q and wants_drawing_tools(q) and not drawing_requirement_met(q, ans):
        reason = "跳过回流（题面要图但解答缺工具配图）"
    return {"reflowed": False, "reflow_id": None, "trace": _trace(state, reason)}


def build_solve_graph():
    """归一 → OCR → 决策 → 题量 → 题库预检索（命中直出）→ 否则图谱+ReAct → 评审 → 回流。"""
    g = StateGraph(SolveState)
    g.add_node("normalize", node_normalize)
    g.add_node("ocr_or_text", node_ocr_or_text)
    g.add_node("decide", node_decide)
    g.add_node("scope_task", node_scope_task)
    g.add_node("bank_prefetch", node_bank_prefetch)
    g.add_node("bank_done", node_bank_done)
    g.add_node("kg_ground", node_kg_ground)
    g.add_node("ai_solve", node_ai_solve)
    g.add_node("validate", node_validate)
    g.add_node("reflow", node_reflow)
    g.add_node("skip_reflow", node_skip_reflow)

    g.set_entry_point("normalize")
    g.add_edge("normalize", "ocr_or_text")
    g.add_edge("ocr_or_text", "decide")
    g.add_edge("decide", "scope_task")
    g.add_edge("scope_task", "bank_prefetch")
    g.add_conditional_edges(
        "bank_prefetch",
        route_after_bank,
        {"bank_done": "bank_done", "kg_ground": "kg_ground"},
    )
    g.add_edge("bank_done", END)
    g.add_edge("kg_ground", "ai_solve")
    g.add_edge("ai_solve", "validate")
    g.add_conditional_edges(
        "validate",
        route_after_validate,
        {"reflow": "reflow", "skip_reflow": "skip_reflow"},
    )
    g.add_edge("reflow", END)
    g.add_edge("skip_reflow", END)
    return g.compile()


_graph = None


def get_solve_graph():
    global _graph
    if _graph is None:
        _graph = build_solve_graph()
    return _graph


def reset_solve_graph() -> None:
    global _graph
    _graph = None


def _inject_memory(db: Session, user_id: Optional[int]) -> dict[str, Any]:
    if not user_id:
        return {}
    try:
        from app.services.long_term_memory import build_memory_brief

        brief = build_memory_brief(db, int(user_id))
        out: dict[str, Any] = {"memory_brief": brief or None}
        if brief:
            out["trace"] = [f"注入 memory_brief ({len(brief)} chars)"]
        return out
    except Exception as exc:  # noqa: BLE001
        logger.warning("build_memory_brief failed: %s", exc)
        return {}


def _solve_config(thread_id: Optional[str], user_id: Optional[int]) -> dict:
    """LangGraph 一旦 compile(checkpointer=...)，调用时必须带 thread_id。"""
    import uuid

    tid = (thread_id or "").strip() or f"auto-{uuid.uuid4().hex[:12]}"
    key = f"solve:{user_id or 0}:{tid}"
    return {"configurable": {"thread_id": key}}


async def run_solve(
    db: Session,
    *,
    text: Optional[str] = None,
    image_base64: Optional[str] = None,
    reflow_stem: Optional[str] = None,
    reflow_image_path: Optional[str] = None,
    user_id: Optional[int] = None,
    thread_id: Optional[str] = None,
) -> SolveState:
    reset_solve_graph()
    mem = _inject_memory(db, user_id)
    payload: dict[str, Any] = {
        "text": text,
        "image_base64": image_base64,
        "reflow_stem": reflow_stem,
        "reflow_image_path": reflow_image_path,
        "db": db,
        "user_id": user_id,
        "thread_id": thread_id,
        "trace": list(mem.pop("trace", [])),
        **mem,
    }
    cfg = _solve_config(thread_id, user_id)
    graph = get_solve_graph()
    result = await graph.ainvoke(payload, config=cfg)
    return result  # type: ignore[return-value]


async def run_solve_stream(
    db: Session,
    *,
    text: Optional[str] = None,
    image_base64: Optional[str] = None,
    reflow_stem: Optional[str] = None,
    reflow_image_path: Optional[str] = None,
    user_id: Optional[int] = None,
    thread_id: Optional[str] = None,
):
    from app.agents.tutor_react import stream_tutor_react
    from app.tools import set_tool_db

    set_tool_db(db, user_id=user_id)
    mem = _inject_memory(db, user_id)
    state: SolveState = {
        "text": text,
        "image_base64": image_base64,
        "reflow_stem": reflow_stem,
        "reflow_image_path": reflow_image_path,
        "db": db,
        "user_id": user_id,
        "thread_id": thread_id,
        "trace": list(mem.pop("trace", [])),
        "images": [],
        **mem,
    }
    memory_brief = state.get("memory_brief") or None

    def _emit_status(msg: str) -> dict[str, Any]:
        return {"type": "status", "message": msg}

    state.update(node_normalize(state))
    yield _emit_status("正在接收题目…")
    state.update(await node_ocr_or_text(state))
    yield _emit_status("正在识别题目…" if state.get("image_base64") else "正在理解输入…")
    if not (state.get("question_text") or "").strip():
        yield {"type": "error", "message": "未能得到有效题面"}
        return

    yield _emit_status("决策者正在规划任务…")
    state.update(await node_decide(state))
    plan = _plan(state)
    yield _emit_status(f"规划：{plan.summary}")

    if plan.has("scope") or plan.intent == "solve" or not plan.steps:
        yield _emit_status("执行：scope — 检查题量")
        state.update(node_scope_task(state))
        if state.get("task_heavy"):
            yield _emit_status("检测到多题/整卷，本轮只详解前几道…")

    yield _emit_status("执行：bank — 题库原题预检索")
    state.update(node_bank_prefetch(state))
    if state.get("hit"):
        yield _emit_status("题库命中原题，直接交付权威解答")
        ans = state.get("answer") or ""
        if ans:
            yield {"type": "delta", "text": ans}
        state.update(node_bank_done(state))
        yield {"type": "final", "state": {k: v for k, v in dict(state).items() if k != "db"}}
        return

    yield _emit_status("执行：graph — 关联知识点（可选）")
    state.update(node_kg_ground(state))
    kg = state.get("kg_context") or {}
    if kg.get("keywords"):
        yield {
            "type": "kg",
            "keywords": kg.get("keywords") or [],
            "learning_chain": (kg.get("learning_chain") or [])[:10],
        }

    yield _emit_status("执行：solve — ReAct（教材/绘图等工具）")
    q = state.get("question_text") or ""
    scope_notice = (state.get("scope_notice") or "").strip()
    if scope_notice:
        yield {"type": "delta", "text": scope_notice}

    react_result = None
    async for ev in stream_tutor_react(
        q,
        db=db,
        kg_context=(kg.get("prompt_block") if isinstance(kg, dict) else None),
        memory_brief=memory_brief,
        user_id=user_id,
        bank_prefetch_note=state.get("bank_prefetch_note") or "",
    ):
        if ev.get("type") == "react_done":
            react_result = ev.get("result")
            continue
        if ev.get("type") == "error":
            yield ev
            return
        yield ev
    if not react_result:
        yield {"type": "error", "message": "AI 解题未返回结果"}
        return

    analysis = f"**决策规划**：{plan.summary}\n\n" + (react_result.get("analysis") or "")
    if kg.get("keywords"):
        analysis = (
            f"**考点**：{'、'.join(kg['keywords'])}\n"
            f"**逻辑链**：{' → '.join((kg.get('learning_chain') or [])[:10])}\n\n{analysis}"
        )
    answer = react_result["answer"]
    if scope_notice and scope_notice not in answer:
        answer = scope_notice + answer
    tool_trace = list(state.get("tool_trace") or [])
    tool_trace.extend(str(t) for t in (react_result.get("tool_trace") or []))
    state.update(
        {
            "trust_level": "ai_reference",
            "trust_label": "AI解答，仅供参考·不一定准确",
            "ai_answer": answer,
            "ai_analysis": analysis.strip(),
            "answer": answer,
            "analysis": analysis.strip(),
            "images": list(react_result.get("images") or []),
            "tool_trace": tool_trace,
            "trace": _trace(state, "ReAct 完成"),
        }
    )
    yield _emit_status("正在整理解答…")
    if plan.has("validate") or not plan.steps:
        yield _emit_status("执行：validate — 权威评审")
        state.update(await node_validate(state))
        yield _emit_status(
            "评审通过，准备交付…"
            if state.get("validate_passed")
            else "评审未达标，仍作参考交付…"
        )
    if route_after_validate(state) == "reflow":
        state.update(node_reflow(state))
        yield _emit_status("已写入回流待审，供管理员入库…")
    else:
        state.update(node_skip_reflow(state))
        yield _emit_status("即将完成…")
    yield {"type": "final", "state": {k: v for k, v in dict(state).items() if k != "db"}}

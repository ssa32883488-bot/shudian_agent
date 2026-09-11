"""Agent 流程 trace 落库（题面/答案摘要 + 节点与工具链，无完整对话原文）。"""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.models_ext import AgentTrace


def _derive_status(
    *,
    hit: bool,
    validate_passed: bool | None,
    error: str | None,
    trust_level: str | None,
) -> str:
    if error:
        return "error"
    if hit:
        return "bank_hit"
    if validate_passed is False:
        return "validate_fail"
    if trust_level == "ai_reference":
        return "ai_reference"
    return "ok"


def _build_detail_from_state(state: dict[str, Any] | None, error: str | None = None) -> dict[str, Any]:
    state = state or {}
    answer = str(state.get("answer") or state.get("ai_answer") or "").strip()
    preview = answer.replace("\n", " ")[:480]
    tool_trace = [str(x)[:300] for x in (state.get("tool_trace") or [])][:60]
    validate_passed = state.get("validate_passed")
    if validate_passed is not None:
        validate_passed = bool(validate_passed)
    score = state.get("validate_score")
    try:
        score_f = float(score) if score is not None else None
    except (TypeError, ValueError):
        score_f = None
    detail: dict[str, Any] = {
        "intent": state.get("intent"),
        "trust_level": state.get("trust_level"),
        "trust_label": state.get("trust_label"),
        "validate_passed": validate_passed,
        "validate_score": score_f,
        "validate_reason": (str(state.get("validate_reason") or "")[:400] or None),
        "answer_preview": preview or None,
        "tool_trace": tool_trace,
        "hit_question_id": state.get("hit_question_id"),
        "hit_score": state.get("hit_score"),
        "match_score": state.get("match_score"),
        "match_reason": (str(state.get("match_reason") or "")[:240] or None),
        "reflow_id": state.get("reflow_id"),
        "reflowed": bool(state.get("reflowed")),
        "source": state.get("source"),
        "error": (error[:500] if error else None),
    }
    return {k: v for k, v in detail.items() if v is not None and v != [] and v != ""}


def record_trace(
    db: Session,
    *,
    student_id: int | None,
    thread_id: str | None,
    question_text: str,
    steps: list[str] | None,
    hit: bool,
    state: dict[str, Any] | None = None,
    error: str | None = None,
) -> AgentTrace | None:
    steps = [str(s)[:240] for s in (steps or [])][:100]
    if not steps and not question_text and not error:
        return None
    preview = (question_text or "").strip().replace("\n", " ")[:240]
    detail = _build_detail_from_state(state, error=error)
    status = _derive_status(
        hit=bool(hit),
        validate_passed=detail.get("validate_passed"),
        error=error,
        trust_level=detail.get("trust_level"),
    )
    detail["status"] = status
    row = AgentTrace(
        student_id=student_id,
        thread_id=(thread_id or None),
        question_preview=preview or ("（流程异常）" if error else "（无题面预览）"),
        steps=steps,
        hit=bool(hit),
        status=status,
        detail=detail,
    )
    db.add(row)
    try:
        db.commit()
        db.refresh(row)
        return row
    except Exception:
        db.rollback()
        return None


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, str) and value.strip():
        try:
            import json

            parsed = json.loads(value)
            return dict(parsed) if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


def _serialize(r: AgentTrace, db: Session, *, include_detail: bool = True) -> dict[str, Any]:
    nick = None
    if r.student_id:
        u = db.get(User, r.student_id)
        nick = u.nickname if u else None
    detail = _as_dict(getattr(r, "detail", None))
    status = getattr(r, "status", None) or detail.get("status") or ("bank_hit" if r.hit else "ok")
    item: dict[str, Any] = {
        "id": r.id,
        "student_id": r.student_id,
        "nickname": nick,
        "thread_id": r.thread_id,
        "question_preview": r.question_preview,
        "steps": r.steps or [],
        "hit": r.hit,
        "status": status,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "answer_preview": detail.get("answer_preview"),
        "intent": detail.get("intent"),
        "validate_passed": detail.get("validate_passed"),
        "validate_score": detail.get("validate_score"),
    }
    if include_detail:
        item["detail"] = detail
        item["tool_trace"] = detail.get("tool_trace") or []
        item["trust_label"] = detail.get("trust_label")
        item["error"] = detail.get("error")
    return item


def list_traces(
    db: Session,
    *,
    limit: int = 50,
    student_id: int | None = None,
    status: str | None = None,
    q: str | None = None,
) -> list[dict[str, Any]]:
    limit = max(1, min(200, int(limit)))
    stmt = select(AgentTrace).order_by(AgentTrace.created_at.desc()).limit(limit)
    if student_id:
        stmt = stmt.where(AgentTrace.student_id == student_id)
    if status:
        stmt = stmt.where(AgentTrace.status == status)
    rows = list(db.scalars(stmt).all())
    needle = (q or "").strip().lower()
    out: list[dict[str, Any]] = []
    for r in rows:
        item = _serialize(r, db, include_detail=False)
        if needle:
            blob = f"{item.get('question_preview') or ''} {item.get('nickname') or ''} {item.get('thread_id') or ''}".lower()
            if needle not in blob:
                continue
        out.append(item)
    return out


def get_trace(db: Session, trace_id: int) -> dict[str, Any] | None:
    row = db.get(AgentTrace, trace_id)
    if not row:
        return None
    return _serialize(row, db, include_detail=True)

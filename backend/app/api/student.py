"""学生端 API：解题 / 搜题。"""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import require_student
from app.db import get_db
from app.db.models import User
from app.graphs.solve_graph import run_solve, run_solve_stream
from app.schemas.student import SearchResponse, SolveRequest, SolveResponse
from app.services import chat_history as chat_svc
from app.services.profile import bump_after_solve

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/student", tags=["学生·解题"])


def _state_to_response(state: dict[str, Any]) -> SolveResponse:
    return SolveResponse(
        trust_level=state.get("trust_level") or "ai_reference",
        trust_label=state.get("trust_label")
        or "AI解答，仅供参考·不一定准确",
        question_text=state.get("question_text") or "",
        answer=state.get("answer") or "",
        analysis=state.get("analysis"),
        hit=bool(state.get("hit")),
        hit_question_id=state.get("hit_question_id"),
        hit_score=state.get("hit_score"),
        reflowed=bool(state.get("reflowed")),
        reflow_id=state.get("reflow_id"),
        validate_passed=state.get("validate_passed"),
        validate_score=state.get("validate_score"),
        source=state.get("source") or "text",
        trace=list(state.get("trace") or []),
        kg_context=state.get("kg_context"),
        images=list(state.get("images") or []),
    )


def _sse_pack(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False, default=str)}\n\n"


def _persist_user_turn(
    db: Session,
    *,
    user_id: Optional[int],
    thread_id: Optional[str],
    text: Optional[str],
    image: Optional[str],
    client_message_id: Optional[str],
) -> Optional[str]:
    if not user_id or not thread_id:
        return None
    try:
        attachments = None
        if image:
            attachments = [{"type": "image", "ref": "inline"}]
        chat_svc.append_message(
            db,
            user_id=int(user_id),
            thread_id=thread_id,
            role="user",
            content=(text or "").strip() or ("[图片提问]" if image else ""),
            attachments=attachments,
            client_message_id=client_message_id,
            touch_title=True,
        )
        return thread_id
    except PermissionError:
        logger.warning("persist user turn denied thread=%s user=%s", thread_id, user_id)
        return None
    except Exception as exc:  # noqa: BLE001
        logger.warning("persist user turn failed: %s", exc)
        return None


def _persist_assistant_turn(
    db: Session,
    *,
    user_id: Optional[int],
    thread_id: Optional[str],
    state: dict[str, Any],
) -> None:
    if not user_id or not thread_id:
        return
    answer = (state.get("answer") or "").strip()
    if not answer:
        return
    images = list(state.get("images") or [])
    attachments = [{"type": "image", "url": u} for u in images[:12]] or None
    try:
        chat_svc.append_message(
            db,
            user_id=int(user_id),
            thread_id=thread_id,
            role="assistant",
            content=answer,
            attachments=attachments,
            trust_label=state.get("trust_label"),
            client_message_id=None,
            touch_title=False,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("persist assistant turn failed: %s", exc)


@router.post("/solve", response_model=SolveResponse)
async def solve(
    req: SolveRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_student),
) -> SolveResponse:
    """发文字/拍照 → 搜题 → 命中权威 / 未命中 AI 解题 → 校验 → 回流。"""
    if not (req.text and req.text.strip()) and not req.resolved_image():
        raise HTTPException(status_code=400, detail="请提供 text 或 image_base64")

    sid = user.id
    tid = _persist_user_turn(
        db,
        user_id=sid,
        thread_id=req.thread_id,
        text=req.text,
        image=req.resolved_image(),
        client_message_id=req.client_message_id,
    )

    try:
        state = await run_solve(
            db,
            text=req.text,
            image_base64=req.resolved_image(),
            reflow_stem=req.reflow_stem,
            reflow_image_path=req.reflow_image_path,
            user_id=int(sid),
            thread_id=tid or req.thread_id,
        )
    except Exception as exc:
        logger.exception("解题流程失败")
        try:
            from app.services.agent_trace import record_trace

            record_trace(
                db,
                student_id=int(sid),
                thread_id=tid or req.thread_id,
                question_text=(req.text or "")[:240],
                steps=[f"解题异常: {exc}"],
                hit=False,
                error=str(exc),
            )
        except Exception as trace_exc:  # noqa: BLE001
            logger.warning("record_trace(error) failed: %s", trace_exc)
        raise HTTPException(status_code=500, detail=f"解题失败: {exc}") from exc

    q = state.get("question_text") or ""
    if not q:
        raise HTTPException(status_code=400, detail="未能得到有效题面")

    tags = None
    if state.get("hit_payload"):
        tags = (state["hit_payload"].get("knowledge_tags") or {}).get("tags")
    bump_after_solve(db, int(sid), hit=bool(state.get("hit")), tags=tags)
    _persist_assistant_turn(
        db, user_id=int(sid), thread_id=tid or req.thread_id, state=dict(state)
    )
    try:
        from app.services.agent_trace import record_trace

        record_trace(
            db,
            student_id=int(sid),
            thread_id=tid or req.thread_id,
            question_text=q,
            steps=list(state.get("trace") or []),
            hit=bool(state.get("hit")),
            state=dict(state),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("record_trace failed: %s", exc)

    return _state_to_response(dict(state))


@router.post("/solve/stream")
async def solve_stream(
    req: SolveRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_student),
):
    """SSE 流式解题：status / delta / tool_* / final / error。"""
    if not (req.text and req.text.strip()) and not req.resolved_image():
        raise HTTPException(status_code=400, detail="请提供 text 或 image_base64")

    sid = user.id
    tid = _persist_user_turn(
        db,
        user_id=sid,
        thread_id=req.thread_id,
        text=req.text,
        image=req.resolved_image(),
        client_message_id=req.client_message_id,
    )

    async def event_gen():
        try:
            async for ev in run_solve_stream(
                db,
                text=req.text,
                image_base64=req.resolved_image(),
                reflow_stem=req.reflow_stem,
                reflow_image_path=req.reflow_image_path,
                user_id=int(sid),
                thread_id=tid or req.thread_id,
            ):
                et = ev.get("type")
                if et == "final":
                    state = ev.get("state") or {}
                    tags = None
                    hit_payload = state.get("hit_payload")
                    if isinstance(hit_payload, dict):
                        tags = (hit_payload.get("knowledge_tags") or {}).get("tags")
                    try:
                        bump_after_solve(
                            db, int(sid), hit=bool(state.get("hit")), tags=tags
                        )
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("bump_after_solve failed: %s", exc)
                    _persist_assistant_turn(
                        db,
                        user_id=int(sid),
                        thread_id=tid or req.thread_id,
                        state=state,
                    )
                    try:
                        from app.services.agent_trace import record_trace

                        record_trace(
                            db,
                            student_id=int(sid),
                            thread_id=tid or req.thread_id,
                            question_text=str(state.get("question_text") or ""),
                            steps=list(state.get("trace") or []),
                            hit=bool(state.get("hit")),
                            state=dict(state),
                        )
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("record_trace failed: %s", exc)
                    slim = {
                        k: v
                        for k, v in state.items()
                        if k
                        not in (
                            "db",
                            "hit_payload",
                            "text",
                            "image_base64",
                            "ai_answer",
                            "ai_analysis",
                        )
                    }
                    resp = _state_to_response(slim)
                    yield _sse_pack({"type": "final", "result": resp.model_dump()})
                else:
                    yield _sse_pack(ev)
        except Exception as exc:
            logger.exception("流式解题失败")
            try:
                from app.services.agent_trace import record_trace

                record_trace(
                    db,
                    student_id=int(sid),
                    thread_id=tid or req.thread_id,
                    question_text=(req.text or "")[:240],
                    steps=[f"流式解题异常: {exc}"],
                    hit=False,
                    error=str(exc),
                )
            except Exception as trace_exc:  # noqa: BLE001
                logger.warning("record_trace(error) failed: %s", trace_exc)
            yield _sse_pack({"type": "error", "message": f"解题失败: {exc}"})

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, description="搜题关键词/题面"),
    top_k: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    _user: User = Depends(require_student),
) -> SearchResponse:
    """题库检索（只读）。"""
    from app.services.question_bank import search_question_bank

    results = search_question_bank(db, q, top_k=top_k)
    return SearchResponse(query=q, results=results)

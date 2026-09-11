"""管理·系统观测（Agent 轨迹列表与详情）。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db import get_db
from app.db.models import User
from app.services.agent_trace import get_trace, list_traces

router = APIRouter(prefix="/api/admin/traces", tags=["管理·可观测"])


@router.get("")
def traces(
    limit: int = Query(50, ge=1, le=200),
    student_id: int | None = None,
    status: str | None = Query(None, description="ok|bank_hit|validate_fail|error|ai_reference"),
    q: str | None = Query(None, description="题面/昵称/thread 关键词"),
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    _ = user
    items = list_traces(db, limit=limit, student_id=student_id, status=status, q=q)
    return {
        "ok": True,
        "items": items,
        "privacy_note": "含题面与答案摘要、图节点与工具链；不含完整学生对话原文。",
    }


@router.get("/{trace_id}")
def trace_detail(
    trace_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    _ = user
    item = get_trace(db, trace_id)
    if not item:
        raise HTTPException(status_code=404, detail="轨迹不存在")
    return {"ok": True, "item": item}

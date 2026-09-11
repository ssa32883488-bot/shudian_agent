"""管理·回流审核 API。"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db import get_db
from app.db.models import User
from app.services.reflow_review import approve, list_pending, reject

router = APIRouter(prefix="/api/admin/reflow", tags=["管理·回流"])


class ApproveBody(BaseModel):
    """force=true：已确认近重提示后仍入库。"""

    force: bool = False


@router.get("/list")
def pending_list(
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    with_near_dup: bool = Query(True, description="是否附带题库近重提示"),
    source: Optional[str] = Query(
        None, description="筛选：memory_summary / 其它前缀；空=全部"
    ),
):
    items = list_pending(db, with_near_dup=with_near_dup)
    if source:
        key = source.strip()
        items = [x for x in items if (x.get("source") or "").startswith(key)]
    return {"ok": True, "items": items}


@router.post("/{reflow_id}/approve")
def approve_item(
    reflow_id: int,
    body: ApproveBody | None = None,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    force = bool(body.force) if body else False
    try:
        result = approve(db, reflow_id, force=force)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    if result.get("needs_confirm"):
        return result
    return result


@router.post("/{reflow_id}/reject")
def reject_item(
    reflow_id: int, user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    try:
        reject(db, reflow_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"ok": True}

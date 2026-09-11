"""学生·学情画像 API（公开画像，非摘要隐私）。"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import require_student
from app.db import get_db
from app.db.models import User
from app.services.memory import REBUILD_COOLDOWN_SEC, profile_public_dict, rebuild_student_profile
from app.services.profile import get_or_create_profile
from app.services.profile_export import export_student_profile_word

router = APIRouter(prefix="/api/student", tags=["学生·画像"])


@router.get("/profile")
def get_profile(user: User = Depends(require_student), db: Session = Depends(get_db)):
    p = get_or_create_profile(db, user.id)
    return profile_public_dict(user, p)


@router.get("/profile/export-word")
def export_profile_word(
    user: User = Depends(require_student), db: Session = Depends(get_db)
):
    """导出个人学情 Word（不含对话摘要原文）。"""
    p = get_or_create_profile(db, user.id)
    payload = profile_public_dict(user, p)
    try:
        data = export_student_profile_word(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return Response(
        content=data,
        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        headers={"Content-Disposition": 'attachment; filename="learning_profile.docx"'},
    )


@router.post("/profile/rebuild")
def rebuild_profile(user: User = Depends(require_student), db: Session = Depends(get_db)):
    """学情总览「更新学情」：与夜间 03:00 同一套 rebuild。限流 1 次 / 10 分钟。"""
    p = get_or_create_profile(db, user.id)
    if p.rebuild_status == "running":
        raise HTTPException(status_code=409, detail="学情正在更新中，请稍后再试")
    last = p.last_rebuild_at
    if last is not None:
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        elapsed = (datetime.now(timezone.utc) - last).total_seconds()
        if elapsed < REBUILD_COOLDOWN_SEC:
            wait = int(REBUILD_COOLDOWN_SEC - elapsed)
            raise HTTPException(
                status_code=429,
                detail=f"更新过于频繁，请 {wait} 秒后再试",
            )
    try:
        p = rebuild_student_profile(db, user.id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"学情更新失败: {exc}") from exc
    return profile_public_dict(user, p)

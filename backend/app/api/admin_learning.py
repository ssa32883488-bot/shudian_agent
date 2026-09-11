"""管理·学情总览：个人画像可读；对话摘要不可读。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.config import get_settings
from app.db import get_db
from app.db.models import ClassRoom, User
from app.services.class_export import export_class_learning_word
from app.services.memory import get_class_rollup, profile_public_dict
from app.services.profile import get_or_create_profile

router = APIRouter(prefix="/api/admin/learning", tags=["管理·学情"])


def _default_class(admin: User, class_code: str | None, db: Session) -> str:
    code = (class_code or "").strip().upper()
    if code:
        return code
    owned = db.scalar(
        select(ClassRoom)
        .where(ClassRoom.owner_id == admin.id, ClassRoom.status == "active")
        .order_by(ClassRoom.created_at.desc())
    )
    if owned:
        return owned.class_code
    return get_settings().demo_class_code.strip()


def _signals(rollup) -> tuple[list, dict]:
    sig = rollup.exam_signals or {}
    if not isinstance(sig, dict):
        return [], {}
    mistake_top = sig.get("mistake_top") or []
    practice = sig.get("practice") or {}
    return mistake_top, practice


def _learning_payload(db: Session, code: str, *, refresh: bool) -> dict:
    rollup = get_class_rollup(db, code, refresh=refresh)
    students = list(
        db.scalars(
            select(User).where(User.role == "student", User.class_code == code)
        ).all()
    )
    roster = []
    for s in students:
        p = get_or_create_profile(db, s.id)
        roster.append(
            {
                "student_id": s.id,
                "nickname": s.nickname,
                "weak_points": p.weak_points or [],
                "mastery_avg": round(
                    sum(float(v) for v in (p.mastery or {}).values())
                    / max(1, len(p.mastery or {})),
                    3,
                )
                if p.mastery
                else 0,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            }
        )
    mistake_top, practice = _signals(rollup)
    return {
        "ok": True,
        "class_code": code,
        "n_students": rollup.n_students,
        "mastery_avg": rollup.mastery_avg or {},
        "weak_top": rollup.weak_top or [],
        "progress": rollup.progress or {},
        "mistake_top": mistake_top,
        "practice": practice,
        "exam_signals": rollup.exam_signals or {},
        "computed_at": rollup.computed_at.isoformat() if rollup.computed_at else None,
        "roster": roster,
    }


@router.get("/class")
def class_learning(
    class_code: str | None = None,
    refresh: bool = False,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    code = _default_class(user, class_code, db)
    return _learning_payload(db, code, refresh=refresh)


@router.get("/class/export-word")
def export_class_word(
    class_code: str | None = None,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    code = _default_class(user, class_code, db)
    payload = _learning_payload(db, code, refresh=False)
    data = export_class_learning_word(payload)
    filename = f"class_learning_{code}.docx"
    return Response(
        content=data,
        media_type=(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/student/{student_id}")
def student_learning(
    student_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """管理员查看学生学情：与学生端同构，不含对话摘要。"""
    student = db.get(User, student_id)
    if not student or student.role != "student":
        raise HTTPException(404, detail="学生不存在")
    demo = get_settings().demo_class_code
    owned_codes = {
        r.class_code
        for r in db.scalars(
            select(ClassRoom).where(ClassRoom.owner_id == user.id)
        ).all()
    }
    allowed = {demo, *owned_codes}
    if student.class_code and student.class_code not in allowed and user.phone != "13900000001":
        raise HTTPException(403, detail="仅可查看授权范围内学生学情")
    p = get_or_create_profile(db, student.id)
    data = profile_public_dict(student, p)
    data["privacy_note"] = "对话摘要属隐私，管理员不可见；本页仅学情画像。"
    return data


@router.get("/rollup")
def rollup_summary(
    class_code: str | None = None,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """班级学情聚合。"""
    code = _default_class(user, class_code, db)
    payload = _learning_payload(db, code, refresh=False)
    payload.pop("roster", None)
    return payload

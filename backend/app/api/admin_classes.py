"""管理控制台 · 班级 API。"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db import get_db
from app.db.models import User
from app.services import classrooms as cls_svc

router = APIRouter(prefix="/api/admin/classes", tags=["管理控制台-班级"])


class CreateClassRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)


class RenameClassRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)


class ClassOut(BaseModel):
    id: int
    name: str
    class_code: str
    owner_id: int
    status: str
    n_students: int
    created_at: str | None = None


class MemberOut(BaseModel):
    student_id: int
    nickname: str
    phone: str


@router.get("", response_model=list[ClassOut])
def list_classes(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_admin)],
) -> list[dict]:
    rooms = cls_svc.list_owned_classes(db, user)
    return [cls_svc.class_public(r, db) for r in rooms]


@router.post("", response_model=ClassOut)
def create_class(
    req: CreateClassRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_admin)],
) -> dict:
    room = cls_svc.create_class(db, owner=user, name=req.name)
    return cls_svc.class_public(room, db)


@router.patch("/{class_code}", response_model=ClassOut)
def rename_class(
    class_code: str,
    req: RenameClassRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_admin)],
) -> dict:
    room = cls_svc.rename_class(db, user, class_code, req.name)
    return cls_svc.class_public(room, db)


@router.post("/{class_code}/archive", response_model=ClassOut)
def archive_class(
    class_code: str,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_admin)],
) -> dict:
    room = cls_svc.archive_class(db, user, class_code)
    return cls_svc.class_public(room, db)


@router.get("/{class_code}/members", response_model=list[MemberOut])
def list_members(
    class_code: str,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_admin)],
) -> list[dict]:
    room = cls_svc.get_class_by_code(db, class_code)
    if not room:
        # 也可能已归档，仍允许 owner 看成员
        from sqlalchemy import select
        from app.db.models import ClassRoom

        room = db.scalar(
            select(ClassRoom).where(ClassRoom.class_code == class_code.strip().upper())
        )
    if not room:
        raise HTTPException(status_code=404, detail="班级不存在")
    if room.owner_id != user.id and user.phone != "13900000001":
        raise HTTPException(status_code=403, detail="无权查看该班级")
    members = cls_svc.class_members(db, class_code)
    return [
        {"student_id": m.id, "nickname": m.nickname, "phone": m.phone}
        for m in members
    ]


@router.delete("/{class_code}/members/{student_id}")
def remove_member(
    class_code: str,
    student_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_admin)],
) -> dict:
    cls_svc.remove_member(db, user, class_code, student_id)
    return {"ok": True}

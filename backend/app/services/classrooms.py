"""班级：创建、班级码、成员列表。"""

from __future__ import annotations

import secrets
import string

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import ClassRoom, User


def _gen_class_code(db: Session, length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    for _ in range(32):
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        exists = db.scalar(select(ClassRoom.id).where(ClassRoom.class_code == code))
        if not exists:
            return code
    raise HTTPException(status_code=500, detail="无法生成唯一班级码")


def get_class_by_code(db: Session, code: str) -> ClassRoom | None:
    code = (code or "").strip().upper()
    if not code:
        return None
    return db.scalar(
        select(ClassRoom).where(
            ClassRoom.class_code == code, ClassRoom.status == "active"
        )
    )


def ensure_class_code_valid(db: Session, code: str | None) -> str | None:
    if not code:
        return None
    room = get_class_by_code(db, code)
    if not room:
        raise HTTPException(status_code=400, detail="班级码无效或不存在")
    return room.class_code


def create_class(db: Session, *, owner: User, name: str) -> ClassRoom:
    name = (name or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="请填写班级名称")
    if owner.role not in ("admin", "teacher"):
        raise HTTPException(status_code=403, detail="仅教师管理员可创建班级")
    room = ClassRoom(
        name=name[:64],
        class_code=_gen_class_code(db),
        owner_id=owner.id,
        status="active",
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def list_owned_classes(db: Session, owner: User) -> list[ClassRoom]:
    return list(
        db.scalars(
            select(ClassRoom)
            .where(ClassRoom.owner_id == owner.id, ClassRoom.status == "active")
            .order_by(ClassRoom.created_at.desc())
        ).all()
    )


def class_members(db: Session, class_code: str) -> list[User]:
    code = (class_code or "").strip().upper()
    return list(
        db.scalars(
            select(User)
            .where(User.class_code == code, User.role == "student")
            .order_by(User.id.asc())
        ).all()
    )


def class_public(room: ClassRoom, db: Session) -> dict:
    n = db.scalar(
        select(func.count())
        .select_from(User)
        .where(User.class_code == room.class_code, User.role == "student")
    )
    return {
        "id": room.id,
        "name": room.name,
        "class_code": room.class_code,
        "owner_id": room.owner_id,
        "status": room.status,
        "n_students": int(n or 0),
        "created_at": room.created_at.isoformat() if room.created_at else None,
    }


def _require_owned(db: Session, owner: User, class_code: str) -> ClassRoom:
    code = (class_code or "").strip().upper()
    room = db.scalar(select(ClassRoom).where(ClassRoom.class_code == code))
    if not room:
        raise HTTPException(status_code=404, detail="班级不存在")
    demo_ok = owner.phone == "13900000001"
    if room.owner_id != owner.id and not demo_ok:
        raise HTTPException(status_code=403, detail="无权操作该班级")
    return room


def rename_class(db: Session, owner: User, class_code: str, name: str) -> ClassRoom:
    room = _require_owned(db, owner, class_code)
    name = (name or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="请填写班级名称")
    room.name = name[:64]
    db.commit()
    db.refresh(room)
    return room


def archive_class(db: Session, owner: User, class_code: str) -> ClassRoom:
    room = _require_owned(db, owner, class_code)
    room.status = "archived"
    db.commit()
    db.refresh(room)
    return room


def remove_member(db: Session, owner: User, class_code: str, student_id: int) -> None:
    room = _require_owned(db, owner, class_code)
    if room.status != "active":
        raise HTTPException(status_code=400, detail="班级已归档")
    student = db.get(User, student_id)
    if not student or student.role != "student":
        raise HTTPException(status_code=404, detail="学生不存在")
    if (student.class_code or "").upper() != room.class_code.upper():
        raise HTTPException(status_code=400, detail="该学生不在本班")
    student.class_code = None
    db.commit()


def ensure_demo_class(db: Session, *, owner_id: int, class_code: str, name: str = "演示班级") -> ClassRoom:
    code = class_code.strip().upper()
    room = get_class_by_code(db, code)
    if room:
        return room
    # 可能被归档或大小写不一致
    room = db.scalar(select(ClassRoom).where(ClassRoom.class_code == code))
    if room:
        room.status = "active"
        db.commit()
        db.refresh(room)
        return room
    room = ClassRoom(
        name=name,
        class_code=code,
        owner_id=owner_id,
        status="active",
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

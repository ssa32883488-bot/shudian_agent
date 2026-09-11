"""认证：昵称 + 手机号 + 密码（无短信）；学生可选班级码。"""

from __future__ import annotations

import hashlib
import secrets
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, UserPublic
from app.services.classrooms import ensure_class_code_valid
from app.services.redis_client import get_redis

# 进程内回退（无 Redis / Redis 宕机）
_TOKEN_STORE: dict[str, int] = {}
_TOKEN_KEY = "shudian:auth:token:"
_TOKEN_TTL_SEC = 7 * 24 * 3600  # 7 天


def hash_password(password: str) -> str:
    settings = get_settings()
    raw = f"{settings.auth_salt}:{password}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def issue_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    r = get_redis()
    if r is not None:
        try:
            r.setex(f"{_TOKEN_KEY}{token}", _TOKEN_TTL_SEC, str(user_id))
            return token
        except Exception:
            pass
    _TOKEN_STORE[token] = user_id
    return token


def resolve_token(token: str) -> Optional[int]:
    r = get_redis()
    if r is not None:
        try:
            raw = r.get(f"{_TOKEN_KEY}{token}")
            if raw is not None:
                return int(raw)
        except Exception:
            pass
    return _TOKEN_STORE.get(token)


def revoke_token(token: str) -> None:
    r = get_redis()
    if r is not None:
        try:
            r.delete(f"{_TOKEN_KEY}{token}")
        except Exception:
            pass
    _TOKEN_STORE.pop(token, None)


def _normalize_role(role: str | None) -> str:
    r = (role or "student").strip().lower()
    if r in ("teacher", "admin", "teacher_admin"):
        return "admin"
    return "student"


def user_to_public(user: User) -> UserPublic:
    return UserPublic(
        id=user.id,
        nickname=user.nickname,
        phone=user.phone,
        class_code=user.class_code,
        role=user.role,
    )


def register_student(db: Session, req: RegisterRequest) -> User:
    exists = db.scalar(select(User).where(User.phone == req.phone))
    if exists:
        raise HTTPException(status_code=400, detail="该手机号已注册，请直接登录")

    role = _normalize_role(req.role)
    class_code = None
    if role == "student":
        class_code = ensure_class_code_valid(db, req.class_code)
    elif req.class_code:
        raise HTTPException(status_code=400, detail="教师管理员注册无需填写班级码")

    user = User(
        nickname=req.nickname.strip(),
        phone=req.phone.strip(),
        password_hash=hash_password(req.password),
        class_code=class_code,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_student(db: Session, req: LoginRequest) -> User:
    user = db.scalar(select(User).where(User.phone == req.phone))
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误",
        )
    return user


def bind_class_code(db: Session, user: User, class_code: str) -> User:
    if user.role != "student":
        raise HTTPException(status_code=400, detail="仅学生可加入班级")
    code = ensure_class_code_valid(db, class_code)
    user.class_code = code
    db.commit()
    db.refresh(user)
    return user

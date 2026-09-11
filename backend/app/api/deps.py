"""API 依赖：Token 鉴权与角色校验；支持 auth_disabled 演示身份。"""

from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.db.models import User
from app.services.auth import hash_password, resolve_token

_bearer = HTTPBearer(auto_error=False)

DEMO_STUDENT_PHONE = "13800000001"
DEMO_ADMIN_PHONE = "13900000001"


def _persona_user(db: Session, persona: Optional[str]) -> User:
    ensure_demo_users(db)
    role = (persona or "student").strip().lower()
    if role in ("admin", "teacher"):
        phone = DEMO_ADMIN_PHONE
    else:
        phone = DEMO_STUDENT_PHONE
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=500, detail="演示用户初始化失败")
    return user


def get_current_user(
    creds: Annotated[Optional[HTTPAuthorizationCredentials], Depends(_bearer)],
    db: Session = Depends(get_db),
    x_dev_persona: Annotated[Optional[str], Header(alias="X-Dev-Persona")] = None,
) -> User:
    settings = get_settings()
    # 有 Token 优先走真实登录（即便仍开着演示开关）
    if creds and creds.credentials:
        uid = resolve_token(creds.credentials)
        if uid is not None:
            user = db.get(User, uid)
            if user:
                return user
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")
        if not settings.auth_disabled:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录已失效")

    if settings.auth_disabled:
        return _persona_user(db, x_dev_persona)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录")


def ensure_demo_users(db: Session) -> None:
    """无登录模式下确保演示学生与管理员存在；并保证演示班级码可用。"""
    settings = get_settings()
    class_code = settings.demo_class_code

    def _upsert(phone: str, nickname: str, role: str, with_class: bool) -> User:
        u = db.query(User).filter(User.phone == phone).first()
        if u:
            changed = False
            target = "admin" if role == "admin" else role
            if role == "admin" and u.role in ("teacher", "admin"):
                if u.role != "admin":
                    u.role = "admin"
                    changed = True
            elif u.role != target:
                u.role = target
                changed = True
            if with_class and not (u.class_code or "").strip():
                # 仅补空；勿覆盖学生后补绑班
                u.class_code = class_code
                changed = True
            if phone == DEMO_ADMIN_PHONE and u.nickname in ("陈老师", "演示管理员", "系统管理员"):
                if u.nickname != "系统管理员":
                    u.nickname = "系统管理员"
                    changed = True
            if changed:
                db.commit()
                db.refresh(u)
            return u
        u = User(
            nickname=nickname,
            phone=phone,
            password_hash=hash_password("123456"),
            role=role,
            class_code=class_code if with_class else None,
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        return u

    admin = _upsert(DEMO_ADMIN_PHONE, "系统管理员", "admin", False)
    _upsert(DEMO_STUDENT_PHONE, "演示同学", "student", True)
    _upsert("13800000002", "演示同学乙", "student", True)
    try:
        from app.services.classrooms import ensure_demo_class

        ensure_demo_class(db, owner_id=admin.id, class_code=class_code, name="演示班级")
    except Exception:
        pass


def require_student(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role != "student":
        raise HTTPException(status_code=403, detail="需要学生身份")
    return user


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role not in ("admin", "teacher"):
        raise HTTPException(status_code=403, detail="需要管理员身份")
    return user


require_teacher = require_admin


def optional_user(
    creds: Annotated[Optional[HTTPAuthorizationCredentials], Depends(_bearer)],
    db: Session = Depends(get_db),
    x_dev_persona: Annotated[Optional[str], Header(alias="X-Dev-Persona")] = None,
) -> Optional[User]:
    settings = get_settings()
    if creds and creds.credentials:
        uid = resolve_token(creds.credentials)
        if uid is not None:
            return db.get(User, uid)
    if settings.auth_disabled:
        return _persona_user(db, x_dev_persona)
    return None

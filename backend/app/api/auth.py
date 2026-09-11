"""学生注册 / 登录（无短信验证）。"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_student
from app.db import get_db
from app.db.models import User
from app.schemas.auth import (
    AuthResponse,
    BindClassRequest,
    LoginRequest,
    RegisterRequest,
    UserPublic,
)
from app.services.auth import (
    bind_class_code,
    issue_token,
    login_student,
    register_student,
    user_to_public,
)

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """注册：学生=昵称+手机+密码+可选班级码；教师管理员=昵称+手机+密码。"""
    user = register_student(db, req)
    token = issue_token(user.id)
    return AuthResponse(user=user_to_public(user), token=token)


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """登录：手机号 + 密码。"""
    user = login_student(db, req)
    token = issue_token(user.id)
    return AuthResponse(user=user_to_public(user), token=token)


@router.get("/me", response_model=UserPublic)
def me(user: Annotated[User, Depends(get_current_user)]) -> UserPublic:
    return user_to_public(user)


@router.post("/bind-class", response_model=UserPublic)
def bind_class(
    req: BindClassRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(require_student)],
) -> UserPublic:
    user = bind_class_code(db, user, req.class_code)
    return user_to_public(user)

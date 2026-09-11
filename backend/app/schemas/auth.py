"""认证相关 Schema。"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RegisterRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=32, description="昵称")
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    password: str = Field(..., min_length=6, max_length=64, description="密码")
    class_code: Optional[str] = Field(None, max_length=32, description="班级码（选填）")
    role: str = Field(default="student", description="student | teacher | admin")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not (v.isdigit() and len(v) == 11):
            raise ValueError("手机号须为 11 位数字")
        return v

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        return v.strip()

    @field_validator("class_code")
    @classmethod
    def normalize_class_code(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v or None


class LoginRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6, max_length=64)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not (v.isdigit() and len(v) == 11):
            raise ValueError("手机号须为 11 位数字")
        return v


class BindClassRequest(BaseModel):
    class_code: str = Field(..., min_length=2, max_length=32)


class UserPublic(BaseModel):
    id: int
    nickname: str
    phone: str
    class_code: Optional[str] = None
    role: str = "student"


class AuthResponse(BaseModel):
    ok: bool = True
    user: UserPublic
    token: str

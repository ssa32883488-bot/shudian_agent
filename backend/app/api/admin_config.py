"""管理·基础配置（只读：参数已写死在 Settings，不可热改）。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db import get_db
from app.db.models import User
from app.services.runtime_config import get_runtime_config

router = APIRouter(prefix="/api/admin/config", tags=["管理·配置"])


@router.get("")
def get_config(
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    _ = user
    cfg = get_runtime_config(db)
    return {
        "ok": True,
        "config": cfg,
        "mutable": False,
        "note": "回流/记忆/权威阈值已写死在服务端配置，管理端不再提供热改。",
    }

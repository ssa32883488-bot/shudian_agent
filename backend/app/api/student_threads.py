"""学生短期会话 API：线程列表 / 消息 / 同步（服务端权威）。"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import require_student
from app.db import get_db
from app.db.models import User
from app.services import chat_history as chat_svc

router = APIRouter(prefix="/api/student/threads", tags=["学生·会话记忆"])


class ThreadCreateIn(BaseModel):
    id: Optional[str] = Field(None, description="客户端线程 id；缺省由服务端生成")
    title: str = "新会话"


class ThreadPatchIn(BaseModel):
    title: Optional[str] = None
    archived: Optional[bool] = None
    summarized_until: Optional[int] = None


class MessageIn(BaseModel):
    role: str = "user"
    content: str = ""
    content_format: str = "md"
    attachments: list[Any] = Field(default_factory=list)
    trust_label: Optional[str] = None
    client_message_id: Optional[str] = None


class SyncIn(BaseModel):
    thread_id: str
    title: Optional[str] = None
    summarized_until: Optional[int] = None
    messages: list[MessageIn] = Field(default_factory=list)


@router.get("")
def list_my_threads(
    include_archived: bool = Query(False),
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    rows = chat_svc.list_threads(db, user.id, include_archived=include_archived)
    return {"ok": True, "items": [chat_svc.thread_public_dict(t) for t in rows]}


@router.post("")
def create_thread(
    body: ThreadCreateIn,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    try:
        row = chat_svc.ensure_thread(
            db, user_id=user.id, thread_id=body.id, title=body.title
        )
    except PermissionError:
        raise HTTPException(403, detail="线程不属于当前用户") from None
    return {"ok": True, "thread": chat_svc.thread_public_dict(row)}


@router.get("/{thread_id}")
def get_thread(
    thread_id: str,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    row = chat_svc.get_thread(db, user.id, thread_id)
    if not row:
        raise HTTPException(404, detail="线程不存在")
    return {"ok": True, "thread": chat_svc.thread_public_dict(row)}


@router.patch("/{thread_id}")
def patch_thread(
    thread_id: str,
    body: ThreadPatchIn,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    row = chat_svc.update_thread(
        db,
        user.id,
        thread_id,
        title=body.title,
        archived=body.archived,
        summarized_until=body.summarized_until,
    )
    if not row:
        raise HTTPException(404, detail="线程不存在")
    return {"ok": True, "thread": chat_svc.thread_public_dict(row)}


@router.delete("/{thread_id}")
def remove_thread(
    thread_id: str,
    hard: bool = Query(False),
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    ok = chat_svc.delete_thread(db, user.id, thread_id, hard=hard)
    if not ok:
        raise HTTPException(404, detail="线程不存在")
    return {"ok": True}


@router.get("/{thread_id}/messages")
def get_messages(
    thread_id: str,
    after_id: Optional[int] = Query(None),
    limit: int = Query(500, ge=1, le=1000),
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    if not chat_svc.get_thread(db, user.id, thread_id):
        raise HTTPException(404, detail="线程不存在")
    rows = chat_svc.list_messages(
        db, user.id, thread_id, limit=limit, after_id=after_id
    )
    return {"ok": True, "items": [chat_svc.message_public_dict(m) for m in rows]}


@router.post("/{thread_id}/messages")
def post_message(
    thread_id: str,
    body: MessageIn,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    try:
        row = chat_svc.append_message(
            db,
            user_id=user.id,
            thread_id=thread_id,
            role=body.role,
            content=body.content,
            content_format=body.content_format,
            attachments=body.attachments or None,
            trust_label=body.trust_label,
            client_message_id=body.client_message_id,
            touch_title=body.role == "user",
        )
    except PermissionError:
        raise HTTPException(403, detail="线程不属于当前用户") from None
    return {"ok": True, "message": chat_svc.message_public_dict(row)}


@router.post("/sync")
def sync_thread(
    body: SyncIn,
    user: User = Depends(require_student),
    db: Session = Depends(get_db),
):
    try:
        result = chat_svc.sync_messages(
            db,
            user_id=user.id,
            thread_id=body.thread_id,
            title=body.title,
            summarized_until=body.summarized_until,
            messages=[m.model_dump() for m in body.messages],
        )
    except PermissionError:
        raise HTTPException(403, detail="线程不属于当前用户") from None
    return {"ok": True, **result}

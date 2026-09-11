"""短期记忆：会话线程 / 消息（服务端权威）。"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models_ext import ChatMessageRecord, ChatThread


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_thread_id() -> str:
    return f"chat_{uuid.uuid4().hex[:16]}"


def ensure_thread(
    db: Session,
    *,
    user_id: int,
    thread_id: Optional[str] = None,
    title: str = "新会话",
    agent: str = "student",
) -> ChatThread:
    tid = (thread_id or "").strip() or _new_thread_id()
    row = db.get(ChatThread, tid)
    if row:
        if row.user_id != user_id:
            raise PermissionError("thread belongs to another user")
        if row.archived:
            row.archived = False
            row.updated_at = _now()
            db.commit()
            db.refresh(row)
        return row
    row = ChatThread(
        id=tid,
        user_id=user_id,
        agent=agent,
        title=(title or "新会话")[:256],
        archived=False,
        summarized_until=0,
        created_at=_now(),
        updated_at=_now(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_threads(
    db: Session,
    user_id: int,
    *,
    include_archived: bool = False,
    limit: int = 100,
) -> list[ChatThread]:
    q = select(ChatThread).where(ChatThread.user_id == user_id)
    if not include_archived:
        q = q.where(ChatThread.archived.is_(False))
    q = q.order_by(ChatThread.updated_at.desc()).limit(limit)
    return list(db.scalars(q).all())


def get_thread(db: Session, user_id: int, thread_id: str) -> Optional[ChatThread]:
    row = db.get(ChatThread, thread_id)
    if not row or row.user_id != user_id:
        return None
    return row


def update_thread(
    db: Session,
    user_id: int,
    thread_id: str,
    *,
    title: Optional[str] = None,
    archived: Optional[bool] = None,
    summarized_until: Optional[int] = None,
) -> Optional[ChatThread]:
    row = get_thread(db, user_id, thread_id)
    if not row:
        return None
    if title is not None:
        row.title = title[:256]
    if archived is not None:
        row.archived = bool(archived)
    if summarized_until is not None:
        row.summarized_until = max(0, int(summarized_until))
    row.updated_at = _now()
    db.commit()
    db.refresh(row)
    return row


def delete_thread(db: Session, user_id: int, thread_id: str, *, hard: bool = False) -> bool:
    row = get_thread(db, user_id, thread_id)
    if not row:
        return False
    if hard:
        from sqlalchemy import delete

        db.execute(
            delete(ChatMessageRecord).where(ChatMessageRecord.thread_id == thread_id)
        )
        db.delete(row)
    else:
        row.archived = True
        row.updated_at = _now()
    db.commit()
    return True


def list_messages(
    db: Session,
    user_id: int,
    thread_id: str,
    *,
    limit: int = 500,
    after_id: Optional[int] = None,
) -> list[ChatMessageRecord]:
    thread = get_thread(db, user_id, thread_id)
    if not thread:
        return []
    q = select(ChatMessageRecord).where(ChatMessageRecord.thread_id == thread_id)
    if after_id is not None:
        q = q.where(ChatMessageRecord.id > int(after_id))
    q = q.order_by(ChatMessageRecord.id.asc()).limit(limit)
    return list(db.scalars(q).all())


def _find_by_client_id(
    db: Session, thread_id: str, client_message_id: Optional[str]
) -> Optional[ChatMessageRecord]:
    cid = (client_message_id or "").strip()
    if not cid:
        return None
    return db.scalars(
        select(ChatMessageRecord)
        .where(
            ChatMessageRecord.thread_id == thread_id,
            ChatMessageRecord.client_message_id == cid,
        )
        .limit(1)
    ).first()


def append_message(
    db: Session,
    *,
    user_id: int,
    thread_id: str,
    role: str,
    content: str,
    content_format: str = "md",
    attachments: Optional[list] = None,
    trust_label: Optional[str] = None,
    client_message_id: Optional[str] = None,
    touch_title: bool = False,
) -> ChatMessageRecord:
    thread = ensure_thread(db, user_id=user_id, thread_id=thread_id)
    existing = _find_by_client_id(db, thread.id, client_message_id)
    if existing:
        return existing

    row = ChatMessageRecord(
        thread_id=thread.id,
        role=(role or "user")[:16],
        content=content or "",
        content_format=(content_format or "md")[:16],
        attachments=attachments,
        trust_label=(trust_label or None),
        client_message_id=(client_message_id or None),
        created_at=_now(),
    )
    db.add(row)
    thread.updated_at = _now()
    if touch_title and role == "user" and (thread.title in ("", "新会话")):
        text = (content or "").strip()
        if text:
            thread.title = (text[:28] + ("…" if len(text) > 28 else ""))
        elif attachments:
            thread.title = "图片提问"
    db.commit()
    db.refresh(row)
    return row


def sync_messages(
    db: Session,
    *,
    user_id: int,
    thread_id: str,
    messages: list[dict[str, Any]],
    title: Optional[str] = None,
    summarized_until: Optional[int] = None,
) -> dict[str, Any]:
    """前端推送本地缓存消息；按 client_message_id 幂等。"""
    thread = ensure_thread(db, user_id=user_id, thread_id=thread_id, title=title or "新会话")
    if title:
        thread.title = title[:256]
    if summarized_until is not None:
        thread.summarized_until = max(0, int(summarized_until))

    saved = 0
    skipped = 0
    for m in messages:
        role = str(m.get("role") or "user")
        content = str(m.get("content") or "")
        cid = m.get("client_message_id") or m.get("id")
        if _find_by_client_id(db, thread.id, str(cid) if cid else None):
            skipped += 1
            continue
        append_message(
            db,
            user_id=user_id,
            thread_id=thread.id,
            role=role,
            content=content,
            content_format=str(m.get("content_format") or "md"),
            attachments=m.get("attachments") if isinstance(m.get("attachments"), list) else None,
            trust_label=m.get("trust_label"),
            client_message_id=str(cid) if cid else None,
            touch_title=False,
        )
        saved += 1

    thread.updated_at = _now()
    db.commit()
    db.refresh(thread)
    return {
        "thread_id": thread.id,
        "saved": saved,
        "skipped": skipped,
        "updated_at": thread.updated_at.isoformat() if thread.updated_at else None,
        "summarized_until": thread.summarized_until,
    }


def thread_public_dict(t: ChatThread) -> dict[str, Any]:
    return {
        "id": t.id,
        "title": t.title,
        "agent": t.agent,
        "archived": t.archived,
        "summarized_until": t.summarized_until,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "updated_at": t.updated_at.isoformat() if t.updated_at else None,
        "updated_at_ms": int(t.updated_at.timestamp() * 1000) if t.updated_at else 0,
    }


def message_public_dict(m: ChatMessageRecord) -> dict[str, Any]:
    return {
        "id": m.id,
        "thread_id": m.thread_id,
        "role": m.role,
        "content": m.content,
        "content_format": m.content_format,
        "attachments": m.attachments or [],
        "trust_label": m.trust_label,
        "client_message_id": m.client_message_id,
        "created_at": m.created_at.isoformat() if m.created_at else None,
        "created_at_ms": int(m.created_at.timestamp() * 1000) if m.created_at else 0,
    }

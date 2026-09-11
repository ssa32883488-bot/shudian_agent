"""回流问答表写入。"""

from __future__ import annotations

import base64
import logging
import re
import uuid
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import QuestionBank, ReflowQueue
from app.services.question_bank import sync_question_to_chroma
from app.tools.gateway import artifact_dir

logger = logging.getLogger(__name__)


def _strip_data_url(image_base64: str) -> tuple[str, str]:
    """返回 (raw_b64, ext)。"""
    raw = (image_base64 or "").strip()
    ext = "jpg"
    m = re.match(r"^data:image/([\w+.-]+);base64,(.+)$", raw, re.DOTALL)
    if m:
        mime = m.group(1).lower()
        raw = m.group(2)
        if "png" in mime:
            ext = "png"
        elif "webp" in mime:
            ext = "webp"
        elif "gif" in mime:
            ext = "gif"
        else:
            ext = "jpg"
    return raw, ext


def save_reflow_stem_image(image_base64: Optional[str]) -> Optional[str]:
    """保存用户上传题干图，返回可访问路径 /media/artifacts/..."""
    if not image_base64 or not str(image_base64).strip():
        return None
    try:
        raw, ext = _strip_data_url(str(image_base64))
        data = base64.b64decode(raw, validate=False)
        if len(data) < 32:
            return None
        name = f"reflow_{uuid.uuid4().hex[:16]}.{ext}"
        path = artifact_dir() / name
        path.write_bytes(data)
        return f"/media/artifacts/{name}"
    except Exception:
        return None


def write_reflow(
    db: Session,
    *,
    question: str,
    ai_answer: str,
    validate_score: float,
    source: str,
    image_base64: Optional[str] = None,
    image_path: Optional[str] = None,
    knowledge_tags: Optional[dict[str, Any]] = None,
) -> ReflowQueue:
    settings = get_settings()
    from app.services.graph_kg import resolve_knowledge_tags
    from app.services.runtime_config import get_runtime_config

    runtime = get_runtime_config(db)
    reflow_mode = runtime.get("reflow_mode") or settings.reflow_mode
    img = image_path or save_reflow_stem_image(image_base64)
    q = (question or "").strip()
    ans = (ai_answer or "").strip()
    if "\n### 溯源" in ans:
        ans = ans.split("\n### 溯源", 1)[0].rstrip()

    tags = knowledge_tags
    if not tags:
        tags = resolve_knowledge_tags(None, stem=q, source="solve_reflow")

    if reflow_mode == "auto":
        content = q
        if img and img not in content:
            content = f"![题干原图]({img})\n\n{q}"
        qb = QuestionBank(
            content=content,
            answer=ans,
            analysis=None,
            knowledge_tags=tags,
            source="ai_reflow_auto",
            status="active",
        )
        db.add(qb)
        db.flush()
        sync_question_to_chroma(qb)
        item = ReflowQueue(
            question=q,
            ai_answer=ans,
            validate_status="auto_imported",
            validate_score=str(validate_score),
            source=source,
            image_path=img,
            knowledge_tags=tags,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    item = ReflowQueue(
        question=q,
        ai_answer=ans,
        validate_status="pending",
        validate_score=str(validate_score),
        source=source,
        image_path=img,
        knowledge_tags=tags,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def _normalize_stem(text: str) -> str:
    return re.sub(r"\s+", "", (text or "").strip().lower())


def enqueue_memory_qa_pairs(
    db: Session,
    pairs: list[dict[str, Any]],
    *,
    summary_id: Optional[int] = None,
    session_id_client: str = "",
) -> list[ReflowQueue]:
    """记忆压缩旁路抽出的题干+答案 → 回流候选（始终 pending，不走 auto 入库）。"""
    from app.services.graph_kg import resolve_knowledge_tags

    created: list[ReflowQueue] = []
    if not pairs:
        return created

    pending = list(
        db.scalars(
            select(ReflowQueue).where(ReflowQueue.validate_status == "pending")
        ).all()
    )
    pending_norms = {_normalize_stem(p.question) for p in pending if p.question}

    for raw in pairs:
        if not isinstance(raw, dict):
            continue
        q = str(raw.get("question") or raw.get("stem") or "").strip()
        ans = str(raw.get("answer") or "").strip()
        if len(q) < 8 or len(ans) < 2:
            continue
        try:
            conf = float(raw.get("confidence") if raw.get("confidence") is not None else 0.7)
        except (TypeError, ValueError):
            conf = 0.7
        if conf < 0.45:
            continue
        if "\n### 溯源" in ans:
            ans = ans.split("\n### 溯源", 1)[0].rstrip()
        norm = _normalize_stem(q)
        if norm in pending_norms:
            continue
        pending_norms.add(norm)

        src = "memory_summary"
        if summary_id is not None:
            src = f"memory_summary:{summary_id}"
        elif session_id_client:
            src = f"memory_summary:{session_id_client[:32]}"

        pair_tags = raw.get("tags") or []
        if not isinstance(pair_tags, list):
            pair_tags = [pair_tags] if pair_tags else []
        tags = resolve_knowledge_tags(
            [str(t) for t in pair_tags if str(t).strip()],
            stem=q,
            source="memory_summary",
        )

        item = ReflowQueue(
            question=q[:8000],
            ai_answer=ans[:12000],
            validate_status="pending",
            validate_score=f"{conf:.3f}",
            source=src[:64],
            image_path=None,
            knowledge_tags=tags,
        )
        db.add(item)
        created.append(item)

    if created:
        db.commit()
        for item in created:
            db.refresh(item)
        logger.info("memory QA → reflow_queue: +%s", len(created))
    return created

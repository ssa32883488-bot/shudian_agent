"""学生·附件解析（MinerU）。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.deps import require_student
from app.config import get_settings
from app.db.models import User
from app.services.mineru_parse import mineru_kind_from_name, parse_upload_to_markdown

router = APIRouter(prefix="/api/student", tags=["学生·附件解析"])


@router.post("/parse-file")
async def parse_file(
    file: UploadFile = File(...),
    _user: User = Depends(require_student),
):
    """上传 Word/PDF/PPT/图片等，经 MinerU 解析为 Markdown 正文。"""
    settings = get_settings()
    filename = (file.filename or "upload.bin").strip() or "upload.bin"
    raw = await file.read()
    max_bytes = int(settings.mineru_max_file_mb) * 1024 * 1024
    if len(raw) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"文件不能超过 {settings.mineru_max_file_mb}MB",
        )
    result = parse_upload_to_markdown(filename, raw)
    if not result.get("ok"):
        raise HTTPException(
            status_code=400,
            detail=result.get("error") or "解析失败",
        )
    return {
        "ok": True,
        "filename": filename,
        "kind": result.get("kind") or mineru_kind_from_name(filename),
        "engine": result.get("engine"),
        "chars": result.get("chars") or 0,
        "text": result.get("text") or "",
    }

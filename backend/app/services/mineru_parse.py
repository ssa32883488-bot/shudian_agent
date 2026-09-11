# -*- coding: utf-8 -*-
"""MinerU 文档解析：Word/PDF/PPT/图片 → Markdown（LangChain MinerULoader）。"""

from __future__ import annotations

import logging
import re
import tempfile
from pathlib import Path
from typing import Any

from app.config import get_settings

logger = logging.getLogger(__name__)

# precision 支持；flash 略少（无老 .doc）
_MINERU_SUFFIXES = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".gif",
    ".html",
    ".htm",
}
_PLAIN_SUFFIXES = {".txt", ".md", ".csv"}


def mineru_kind_from_name(filename: str) -> str | None:
    name = (filename or "").lower()
    if name.endswith((".docx", ".doc")):
        return "docx"
    if name.endswith(".pdf"):
        return "pdf"
    if name.endswith((".ppt", ".pptx")):
        return "ppt"
    if name.endswith((".txt", ".md", ".csv")):
        return "txt"
    if name.endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")):
        return "image"
    return None


def needs_mineru(filename: str) -> bool:
    suf = Path(filename or "").suffix.lower()
    return suf in _MINERU_SUFFIXES


def _safe_suffix(filename: str) -> str:
    suf = Path(filename or "upload.bin").suffix.lower()
    if re.fullmatch(r"\.[a-z0-9]{1,8}", suf or ""):
        return suf
    return ".bin"


def parse_upload_to_markdown(
    filename: str,
    raw: bytes,
    *,
    mode: str | None = None,
) -> dict[str, Any]:
    """解析上传文件为 Markdown 文本。

    返回: {ok, text, kind, engine, error?, chars}
    """
    settings = get_settings()
    name = (filename or "upload.bin").strip() or "upload.bin"
    kind = mineru_kind_from_name(name) or "file"
    data = raw or b""
    max_bytes = int(settings.mineru_max_file_mb) * 1024 * 1024
    if len(data) > max_bytes:
        return {
            "ok": False,
            "text": "",
            "kind": kind,
            "engine": "none",
            "error": f"文件超过 {settings.mineru_max_file_mb}MB 上限",
            "chars": 0,
        }
    if not data:
        return {
            "ok": False,
            "text": "",
            "kind": kind,
            "engine": "none",
            "error": "空文件",
            "chars": 0,
        }

    suf = Path(name).suffix.lower()
    if suf in _PLAIN_SUFFIXES:
        text = data.decode("utf-8", errors="ignore").strip()
        return {
            "ok": bool(text),
            "text": text,
            "kind": "txt",
            "engine": "local_text",
            "error": None if text else "文本为空",
            "chars": len(text),
        }

    if not needs_mineru(name):
        # 未知类型尝试文本
        try:
            text = data.decode("utf-8", errors="ignore").strip()
        except Exception:
            text = ""
        if text:
            return {
                "ok": True,
                "text": text,
                "kind": kind,
                "engine": "local_text",
                "error": None,
                "chars": len(text),
            }
        return {
            "ok": False,
            "text": "",
            "kind": kind,
            "engine": "none",
            "error": f"不支持的文件类型：{suf or 'unknown'}",
            "chars": 0,
        }

    use_mode = (mode or settings.mineru_mode or "precision").strip().lower()
    if use_mode not in {"flash", "precision"}:
        use_mode = "precision"
    token = (settings.mineru_token or "").strip()
    if use_mode == "precision" and not token:
        return {
            "ok": False,
            "text": "",
            "kind": kind,
            "engine": "mineru",
            "error": "未配置 MINERU_TOKEN，无法使用 precision 解析",
            "chars": 0,
        }

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix="mineru_",
            suffix=_safe_suffix(name),
            delete=False,
        ) as tmp:
            tmp.write(data)
            tmp_path = Path(tmp.name)

        from langchain_mineru import MinerULoader

        # flash 模式对 formula/table 参数敏感：precision 才传开关
        kwargs: dict[str, Any] = {
            "source": str(tmp_path),
            "language": "ch",
            "timeout": int(settings.mineru_timeout_sec or 600),
            "mode": use_mode,
            "token": token or None,
        }
        if use_mode == "precision":
            kwargs.update({"ocr": True, "formula": True, "table": True})

        loader = MinerULoader(**kwargs)
        docs = loader.load()
        parts = [str(d.page_content or "").strip() for d in docs if d.page_content]
        text = "\n\n".join(p for p in parts if p).strip()
        if not text:
            return {
                "ok": False,
                "text": "",
                "kind": kind,
                "engine": f"mineru:{use_mode}",
                "error": "MinerU 返回空正文",
                "chars": 0,
            }
        # 截断保护（与 plan file_text 上限对齐）
        max_chars = 180_000
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n…（正文过长已截断）"
        return {
            "ok": True,
            "text": text,
            "kind": kind,
            "engine": f"mineru:{use_mode}",
            "error": None,
            "chars": len(text),
        }
    except Exception as exc:  # noqa: BLE001
        logger.exception("MinerU 解析失败 name=%s", name)
        return {
            "ok": False,
            "text": "",
            "kind": kind,
            "engine": f"mineru:{use_mode}",
            "error": f"MinerU 解析失败：{exc}",
            "chars": 0,
        }
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:  # noqa: BLE001
                pass

"""教材图片：MinIO（可选）→ 本地目录回退；Agent 绘图产物本地 artifacts。"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response

from app.services.object_store import get_object_bytes
from app.tools.gateway import artifact_dir

router = APIRouter(prefix="/media", tags=["媒体"])

_here = Path(__file__).resolve()
_REPO_CANDIDATES = [
    p for depth in (4, 3, 2) if depth < len(_here.parents) for p in (_here.parents[depth],)
]
_IMAGE_DIRS: list[Path] = [
    Path("/app/media/chapters"),
    Path("/app/media/guide"),
]
for _repo in _REPO_CANDIDATES:
    for _book_root in (
        _repo / "课本" / "课本加习题册" / "markdown_云端解析",
        _repo / "_archive" / "课本" / "课本加习题册" / "markdown_云端解析",
    ):
        _IMAGE_DIRS.extend(
            [
                _book_root / "按章节拆分" / "images",
                _book_root / "学习辅导按章节拆分" / "images",
            ]
        )


def _find_file(name: str) -> Path | None:
    name = Path(name).name
    for d in _IMAGE_DIRS:
        p = d / name
        if p.is_file():
            return p
    return None


@router.get("/{prefix}/{filename}")
def get_media(prefix: str, filename: str):
    """chapters/guide 教材图；artifacts 为绘图产物与回流题干图。"""
    name = Path(filename).name
    if prefix == "artifacts":
        path = artifact_dir() / name
        if not path.is_file():
            raise HTTPException(status_code=404, detail="产物不存在")
        mime, _ = mimetypes.guess_type(name)
        return FileResponse(path, media_type=mime or "application/octet-stream")
    if prefix not in ("chapters", "guide", "local"):
        raise HTTPException(status_code=404, detail="未知前缀")

    # 1) MinIO（若已配置且有对象）
    if prefix in ("chapters", "guide"):
        data = get_object_bytes(f"{prefix}/{name}")
        if data:
            mime, _ = mimetypes.guess_type(name)
            return Response(content=data, media_type=mime or "image/jpeg")

    # 2) 本地目录
    path = _find_file(name)
    if not path:
        raise HTTPException(status_code=404, detail="图片不存在")
    mime, _ = mimetypes.guess_type(path.name)
    return FileResponse(path, media_type=mime or "image/jpeg")

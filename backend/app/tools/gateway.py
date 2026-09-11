"""统一工具出参与产物落盘（对齐工具层设计门面）。"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from app.config import get_settings

# backend/data/artifacts
_ARTIFACT_ROOT = Path(__file__).resolve().parents[2] / "data" / "artifacts"


@dataclass
class ToolResult:
    ok: bool
    artifact: Optional[str] = None  # SVG 字符串或空
    artifact_url: Optional[str] = None  # 对外可访问 URL
    meta: dict[str, Any] = field(default_factory=dict)
    engine: str = ""
    tier: str = ""  # A | B | C
    warnings: list[str] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_tool_message(self) -> str:
        """给 ReAct LLM 看的紧凑 JSON（artifact 过长则只留 URL）。"""
        payload = self.to_dict()
        if payload.get("artifact") and len(payload["artifact"]) > 800:
            payload["artifact"] = f"<svg omitted len={len(self.artifact or '')}>"
        # 提示模型：在正文对应步骤写 DRAW 占位，勿手写 URL、勿堆文末
        kind = str(
            (self.meta or {}).get("draw_kind")
            or (self.meta or {}).get("prefix")
            or "auto"
        )
        if self.ok and self.artifact_url:
            from app.services.draw_blocks import make_draw_marker, normalize_draw_kind

            nk = normalize_draw_kind(kind)
            desc = str((self.meta or {}).get("title") or (self.meta or {}).get("desc") or "本题配图")
            payload["embed_hint"] = (
                f"请在最终解答「该图应出现的步骤」原样写入占位（不要手写图片 URL、不要堆到文末）："
                f"{make_draw_marker(nk, desc)}"
            )
        return json.dumps(payload, ensure_ascii=False)


def artifact_dir() -> Path:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    return _ARTIFACT_ROOT


def save_svg_artifact(svg: str, *, prefix: str = "draw") -> tuple[str, str]:
    """保存 SVG，返回 (filename, public_url)。"""
    name = f"{prefix}_{uuid.uuid4().hex[:12]}.svg"
    path = artifact_dir() / name
    path.write_text(svg, encoding="utf-8")
    base = get_settings().media_base_url.rstrip("/")
    # MEDIA_BASE_URL 形如 http://127.0.0.1:8000/media → /media/artifacts/xxx.svg
    url = f"{base}/artifacts/{name}"
    return name, url


def wrap_ok(
    *,
    svg: str,
    tier: str,
    engine: str,
    meta: Optional[dict[str, Any]] = None,
    warnings: Optional[list[str]] = None,
    prefix: str = "draw",
) -> ToolResult:
    _, url = save_svg_artifact(svg, prefix=prefix)
    meta_out = dict(meta or {})
    meta_out.setdefault("draw_kind", prefix)
    meta_out.setdefault("prefix", prefix)
    return ToolResult(
        ok=True,
        artifact=svg,
        artifact_url=url,
        meta=meta_out,
        engine=engine,
        tier=tier,
        warnings=warnings or [],
    )


def wrap_err(msg: str, *, tier: str = "", engine: str = "") -> ToolResult:
    return ToolResult(ok=False, error=msg, tier=tier, engine=engine, warnings=[msg])

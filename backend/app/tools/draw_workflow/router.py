# -*- coding: utf-8 -*-
"""路由：diagram_kind 优先；否则按 brief/slots 关键词打分。"""

from __future__ import annotations

from typing import Any, Optional

from app.tools.draw_workflow.catalog import KINDS, KindSpec, get_kind


def resolve_kind(
    diagram_kind: str,
    brief: str = "",
    slots: Optional[dict[str, Any]] = None,
) -> Optional[str]:
    slots = slots or {}
    raw = (diagram_kind or "").strip().lower()
    if raw:
        spec = get_kind(raw)
        return spec.kind if spec else None

    sk = str(slots.get("kind") or slots.get("diagram_kind") or "").strip().lower()
    if sk:
        spec = get_kind(sk)
        if spec:
            return spec.kind

    blob = f"{brief}\n{slots}".lower()
    scored: list[tuple[int, str]] = []
    for spec in KINDS.values():
        score = 0
        for kw in spec.keywords:
            if kw.lower() in blob:
                score += 2 if len(kw) >= 3 else 1
        if score:
            scored.append((score, spec.kind))
    if not scored:
        return None
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][1]


def list_kinds() -> list[dict[str, str]]:
    return [
        {
            "kind": s.kind,
            "title": s.title_zh,
            "desc": s.description,
        }
        for s in KINDS.values()
    ]

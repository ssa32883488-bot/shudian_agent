# -*- coding: utf-8 -*-
"""绘图工作流：入参 → 路由 → Skill+LLM → 出图 → 最多 3 次自检。

对外唯一入口：`draw_with_workflow(...)`
权威说明：`docs/定稿-绘图子系统.md`
"""

from __future__ import annotations

from typing import Any, Optional

from app.tools.draw_workflow.loop import run_draw_loop
from app.tools.draw_workflow.router import resolve_kind, list_kinds
from app.tools.gateway import ToolResult, wrap_err


def draw_with_workflow(
    *,
    diagram_kind: str = "",
    brief: str = "",
    slots: Optional[dict[str, Any]] = None,
    script: Optional[str] = None,
    max_retries: int = 3,
) -> ToolResult:
    """
    Parameters
    ----------
    diagram_kind:
        logic_dag | timing_wave | state_machine | truth_table | kmap |
        seven_seg | char_curve | msi_design；空则按 brief 路由。
    brief:
        自然语言需求。
    slots:
        结构化槽位。
    script:
        已有合法 IR/参数 JSON 时跳过首次 LLM 生成。
    max_retries:
        尝试上限（默认 3，含首次；硬限制 1..3）。
    """
    slots = dict(slots or {})
    brief = (brief or "").strip()
    kind = resolve_kind(diagram_kind, brief, slots)
    if not kind:
        return wrap_err(
            "无法路由图类。请指定 diagram_kind 为："
            + " / ".join(k["kind"] for k in list_kinds()),
            tier="W",
            engine="draw_workflow",
        )
    return run_draw_loop(
        kind=kind,
        brief=brief,
        slots=slots,
        script=script,
        max_retries=max(1, min(int(max_retries), 3)),
    )


__all__ = ["draw_with_workflow", "list_kinds", "resolve_kind"]

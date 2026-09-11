# -*- coding: utf-8 -*-
"""timing_wave 确定性兜底：常见题型在 LLM 不可用/失败时仍能出图。"""

from __future__ import annotations

import json
import re
from typing import Any, Optional


def _blob(*parts: str) -> str:
    return "\n".join(p for p in parts if p)


def _is_jk_toggle(text: str) -> bool:
    t = text or ""
    if "JK" not in t.upper() and "J-K" not in t.upper():
        return False
    compact = re.sub(r"\s+", "", t)
    if re.search(r"J\s*=\s*K\s*=\s*1", t, flags=re.I) or "J=K=1" in compact:
        return True
    if "翻转" in t or "T触发" in t or "接成T" in t or "计数状态" in t:
        return True
    return False


def _rising_edge(text: str) -> bool:
    t = text or ""
    if "上升沿" in t:
        return True
    if "下降沿" in t:
        return False
    # 「无小圆圈」= 上升沿；「有/带小圆圈」= 下降沿（勿用裸「小圆圈」误伤）
    if "无小圆圈" in t:
        return True
    if "有小圆圈" in t or "带小圆圈" in t or "均带小圆圈" in t:
        return False
    return True


def _initial_q0(text: str) -> bool:
    t = text or ""
    if re.search(r"Q\s*=\s*0", t):
        return True
    if re.search(r"Q\s*=\s*1", t):
        return False
    return True


def _edges_count(text: str, default: int = 5) -> int:
    t = text or ""
    m = re.search(r"(\d+)\s*个?\s*(?:上升|下降)?沿", t)
    if m:
        return max(3, min(int(m.group(1)), 8))
    m = re.search(r"(\d+)\s*个?\s*时钟", t)
    if m:
        return max(3, min(int(m.group(1)), 8))
    return default


def build_jk_toggle_wave_ir(
    *,
    brief: str = "",
    slots: Optional[dict[str, Any]] = None,
    rising: Optional[bool] = None,
    q0: Optional[bool] = None,
    edges: Optional[int] = None,
) -> Optional[dict[str, Any]]:
    """JK 且 J=K=1 时生成 CLK/Q/Q' 波形 IR；非该类题返回 None。"""
    text = _blob(brief, str(slots or ""))
    if not _is_jk_toggle(text):
        return None

    is_rising = _rising_edge(text) if rising is None else bool(rising)
    q = 0 if _initial_q0(text) else 1
    if q0 is not None:
        q = 0 if q0 else 1
    n_edges = edges if edges is not None else _edges_count(text, 5)

    # 无效电平 → 有效电平 = 触发沿；再回到无效电平
    inactive = 0 if is_rising else 1
    active = 1 - inactive

    clk: list[str] = [str(inactive)]
    q_wave: list[str] = [str(q)]
    qp_wave: list[str] = [str(1 - q)]

    for _ in range(n_edges):
        # 进入有效电平：产生触发沿，JK(J=K=1) 翻转
        clk.append(str(active))
        q = 1 - q
        q_wave.append(str(q))
        qp_wave.append(str(1 - q))
        # 回到无效电平：输出保持
        clk.append(str(inactive))
        q_wave.append(str(q))
        qp_wave.append(str(1 - q))

    edge_name = "上升沿" if is_rising else "下降沿"
    return {
        "schema_version": "wave_ir_v1",
        "diagram_type": "waveform",
        "title": f"JK边沿触发器(J=K=1,{edge_name}) CLK/Q/Q'",
        "signals": [
            {"name": "CLK", "wave": "".join(clk)},
            {"name": "Q", "wave": "".join(q_wave)},
            {"name": "Q'", "wave": "".join(qp_wave)},
        ],
    }


def fallback_timing_wave_script(
    *,
    brief: str = "",
    slots: Optional[dict[str, Any]] = None,
) -> Optional[str]:
    """返回可直接 parse 的 JSON 字符串；无匹配题型则 None。"""
    ir = build_jk_toggle_wave_ir(brief=brief, slots=slots)
    if not ir:
        return None
    return json.dumps(ir, ensure_ascii=False)

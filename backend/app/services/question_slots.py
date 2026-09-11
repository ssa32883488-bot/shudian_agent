"""题面关键槽位抽取与硬否决：防止「考点相近」的题库误当权威答案。

典型误配：JK 下降沿 + 仅 CLK 波形，被向量检索拉到 D 触发器 + CLK/D 波形题。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FlipFlopSlots:
    """触发器波形类题的关键槽。unknown 表示题面未明确写出，不强行否决。"""

    device: str  # d | jk | sr | t | unknown
    edge: str  # rising | falling | unknown
    has_d_input: bool
    has_jk_pins: bool
    waveform_only_clk: bool  # 题面只交代 CLK 波形、未给数据端波形


def _norm(text: str) -> str:
    s = (text or "").lower()
    s = (
        s.replace("′", "'")
        .replace("＇", "'")
        .replace("‾", "")
        .replace("＝", "=")
        .replace("－", "-")
    )
    s = re.sub(r"\s+", "", s)
    return s


def extract_flipflop_slots(text: str) -> FlipFlopSlots:
    t = _norm(text)

    has_jk_pins = bool(
        re.search(r"jk触发|jk触发器|j-?k触发", t)
        or re.search(r"j\s*=\s*k\s*=", t)
        or ("j=1" in t and "k=1" in t)
        or ("1j" in t and "1k" in t)
        or (re.search(r"(?<![a-z0-9])j(?![a-z0-9])", t) and re.search(r"(?<![a-z0-9])k(?![a-z0-9])", t))
    )
    has_d_input = bool(
        re.search(r"d触发|d触发器|输入端d|输入d|1d|端d|信号d", t)
        or re.search(r"d和时钟|d与时钟|时钟信号clk.*d|输入端d和", t)
    )

    device = "unknown"
    if has_jk_pins or "jk" in t:
        device = "jk"
    elif re.search(r"sr触发|rs触发|sr触发器|rs触发器", t):
        device = "sr"
    elif re.search(r"t触发|t触发器", t) or re.search(r"(?<![a-z0-9])t=1", t):
        device = "t"
    elif has_d_input or "d触发" in t:
        device = "d"

    edge = "unknown"
    if any(k in t for k in ("下降沿", "负跳变", "下跳沿", "后沿触发", "负边沿")):
        edge = "falling"
    elif any(k in t for k in ("上升沿", "正跳变", "上跳沿", "前沿触发", "正边沿")):
        edge = "rising"

    mentions_clk = "clk" in t or "时钟" in t
    # 只画 Q/Q'，且题面未出现 D/J/K 数据波形描述
    asks_q_wave = bool(re.search(r"画出.*[qQ]|输出端.*波形|电压波形", t))
    waveform_only_clk = bool(
        asks_q_wave
        and mentions_clk
        and not has_d_input
        and not re.search(r"d的电压|输入d.*如图|如图.*输入d", t)
    )

    return FlipFlopSlots(
        device=device,
        edge=edge,
        has_d_input=has_d_input,
        has_jk_pins=has_jk_pins,
        waveform_only_clk=waveform_only_clk,
    )


def hard_reject_bank_match(user_text: str, bank_text: str) -> Optional[str]:
    """若关键槽冲突，返回否决理由；否则 None（交给 LLM 细判）。"""
    u = extract_flipflop_slots(user_text)
    b = extract_flipflop_slots(bank_text)

    if u.device != "unknown" and b.device != "unknown" and u.device != b.device:
        return f"器件类型不一致（用户={u.device.upper()}，题库={b.device.upper()}）"

    if u.edge != "unknown" and b.edge != "unknown" and u.edge != b.edge:
        return f"触发沿不一致（用户={u.edge}，题库={b.edge}）"

    if u.has_jk_pins and b.device == "d":
        return "用户含 J/K 条件，题库为 D 触发器题"

    if u.device == "jk" and b.has_d_input:
        return "用户为 JK 题，题库题面含 D 输入条件"

    if u.has_d_input and b.device == "jk":
        return "用户为 D 输入波形题，题库为 JK 题"

    # 用户只给 CLK、题库明确还有 D 输入波形 → 不是同一道
    if u.waveform_only_clk and b.has_d_input and u.device in {"jk", "unknown"}:
        return "用户题仅给 CLK 波形，题库另含 D 输入波形（非同一题）"

    return None

# -*- coding: utf-8 -*-
"""logic_dag 确定性兜底：从中文简述解析简单门级网表。"""

from __future__ import annotations

import json
import re
from typing import Any, Optional


_GATE_WORDS = (
    ("与非", "NAND"),
    ("或非", "NOR"),
    ("异或", "XOR"),
    ("同或", "XNOR"),
    ("与门", "AND"),
    ("或门", "OR"),
    ("非门", "NOT"),
    ("反相", "NOT"),
    ("与", "AND"),
    ("或", "OR"),
    ("非", "NOT"),
)


def _find_gate_type(text: str) -> Optional[str]:
    for word, gtype in _GATE_WORDS:
        if word in text:
            return gtype
    return None


def _split_inputs(blob: str) -> list[str]:
    """从『A、B』『A和B』『A,B』等切出信号名。"""
    s = (blob or "").strip()
    if not s:
        return []
    s = s.replace("和", "、").replace(",", "、").replace("，", "、").replace("&", "、")
    parts = [p.strip() for p in re.split(r"[、/\s]+", s) if p.strip()]
    out: list[str] = []
    for p in parts:
        m = re.match(r"^([A-Za-z][A-Za-z0-9_]*|~?[A-Za-z]\w*|Y\d+)$", p)
        if m:
            out.append(m.group(1))
    return out


def fallback_logic_dag_script(*, brief: str, slots: dict[str, Any] | None = None) -> Optional[str]:
    """从题面/desc 抽简单『A、B 经与门 → Y1；Y1 与 C 经或非 → Y』类结构。

    返回 logic_ir_v1 JSON 字符串；无法识别则 None。
    """
    _ = slots
    text = (brief or "").replace("\n", " ")
    if not text.strip():
        return None

    # 模式1：A、B经与门得Y1，Y1与C经或非门输出Y
    step_re = re.compile(
        r"(?P<ins>[A-Za-z0-9_~、和,\s]+?)"
        r"(?:经|通过|进|送)"
        r"(?P<body>.{0,12}?)"
        r"(?:门)?"
        r"(?:得|得到|产生|输出|出)\s*"
        r"(?P<out>[A-Za-z][A-Za-z0-9_]*)",
        re.I,
    )
    steps = list(step_re.finditer(text))
    if not steps:
        # 模式2：与门(A,B)->Y1 / AND(A,B)=Y
        step_re2 = re.compile(
            r"(?P<body>与非|或非|异或|同或|与门|或门|非门|与|或|非|AND|OR|NOT|NAND|NOR|XOR|XNOR)"
            r"\s*[\(（]\s*(?P<ins>[^)）]+)\s*[\)）]"
            r"\s*(?:->|→|=|得|输出)?\s*"
            r"(?P<out>[A-Za-z][A-Za-z0-9_]*)",
            re.I,
        )
        steps = list(step_re2.finditer(text))

    if not steps:
        return None

    gates: dict[str, Any] = {}
    inputs: list[str] = []
    seen_in: set[str] = set()
    last_out = "Y"
    gid = 0

    for m in steps[:8]:
        gtype = _find_gate_type(m.group("body") or "")
        if not gtype:
            raw = (m.group("body") or "").upper()
            for t in ("NAND", "NOR", "XNOR", "XOR", "AND", "OR", "NOT"):
                if t in raw:
                    gtype = t
                    break
        if not gtype:
            continue
        outs = (m.group("out") or "Y").strip()
        ins = _split_inputs(m.group("ins") or "")
        if gtype == "NOT":
            ins = ins[:1]
        if not ins and gtype != "NOT":
            continue
        if gtype == "NOT" and not ins:
            continue
        gid += 1
        name = outs if outs not in gates else f"G{gid}"
        # 输出名若与输入重名，用门 id
        if name in seen_in or name in inputs:
            name = f"G{gid}"
        gates[name] = {"type": gtype, "inputs": ins}
        for sig in ins:
            if sig not in gates and sig not in seen_in:
                seen_in.add(sig)
                inputs.append(sig)
        last_out = outs if outs in gates or outs == name else name

    if not gates:
        return None

    # 最终输出：优先文中「输出 Y」
    final = last_out
    m_out = re.search(r"(?:输出|得)\s*([A-Za-z][A-Za-z0-9_]*)\s*$", text)
    if m_out and (m_out.group(1) in gates or m_out.group(1) == last_out):
        final = m_out.group(1) if m_out.group(1) in gates else last_out

    ir = {
        "schema_version": "logic_ir_v1",
        "diagram_type": "logic",
        "style": "iec",
        "title": "logic_example",
        "inputs": inputs or ["A", "B"],
        "gates": gates,
        "outputs": {final if final.isidentifier() else "Y": final if final in gates else next(iter(gates))},
    }
    # 规范化 outputs value 必须是门 id
    out_name = next(iter(ir["outputs"]))
    out_src = ir["outputs"][out_name]
    if out_src not in gates:
        ir["outputs"] = {"Y": next(iter(gates))}
    return json.dumps(ir, ensure_ascii=False)

# -*- coding: utf-8 -*-
"""结构校验：解析 JSON + 按 kind 检查必填字段。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class VerifyResult:
    ok: bool
    data: Optional[dict[str, Any]] = None
    feedback: str = ""


def parse_script(script: str) -> VerifyResult:
    try:
        data = json.loads(script)
    except json.JSONDecodeError as e:
        return VerifyResult(ok=False, feedback=f"JSON 解析失败：{e}")
    if not isinstance(data, dict):
        return VerifyResult(ok=False, feedback="脚本必须是 JSON 对象")
    return VerifyResult(ok=True, data=data)


def verify_structure(kind: str, data: dict[str, Any]) -> VerifyResult:
    if kind == "logic_dag":
        if data.get("schema_version") not in (None, "logic_ir_v1"):
            return VerifyResult(ok=False, feedback="logic 需 schema_version=logic_ir_v1")
        if not data.get("inputs") or not data.get("gates"):
            return VerifyResult(ok=False, feedback="logic_ir 需含 inputs 与 gates")
        if not data.get("outputs"):
            return VerifyResult(ok=False, feedback="logic_ir 需含 outputs")
        data.setdefault("schema_version", "logic_ir_v1")
        data.setdefault("diagram_type", "logic")
        return VerifyResult(ok=True, data=data)

    if kind == "timing_wave":
        data.setdefault("schema_version", "wave_ir_v1")
        data.setdefault("diagram_type", "waveform")
        sigs = data.get("signals")
        if not isinstance(sigs, list) or not sigs:
            return VerifyResult(ok=False, feedback="wave_ir 需 signals 非空数组")
        for s in sigs:
            if not isinstance(s, dict) or not s.get("name") or not s.get("wave"):
                return VerifyResult(ok=False, feedback="每个 signal 需 name 与 wave")
        return VerifyResult(ok=True, data=data)

    if kind == "state_machine":
        data.setdefault("schema_version", "state_ir_v1")
        data.setdefault("diagram_type", "state")
        if not data.get("states") or not data.get("transitions"):
            return VerifyResult(ok=False, feedback="state_ir 需 states 与 transitions")
        return VerifyResult(ok=True, data=data)

    if kind == "truth_table":
        if not data.get("inputs") or not data.get("outputs") or not data.get("rows"):
            return VerifyResult(
                ok=False, feedback="truth_table 需 inputs/outputs/rows"
            )
        return VerifyResult(ok=True, data=data)

    if kind == "kmap":
        if not data.get("minterms"):
            return VerifyResult(ok=False, feedback="kmap 需 minterms 列表")
        vc = int(data.get("var_count") or 4)
        if vc not in (2, 3, 4):
            return VerifyResult(ok=False, feedback="kmap var_count 仅支持 2/3/4")
        data["var_count"] = vc
        return VerifyResult(ok=True, data=data)

    if kind == "seven_seg":
        digit = data.get("digit", 8)
        try:
            digit = int(digit)
        except (TypeError, ValueError):
            return VerifyResult(ok=False, feedback="digit 须为 0-9 整数")
        if digit < 0 or digit > 9:
            return VerifyResult(ok=False, feedback="digit 须为 0-9")
        data["digit"] = digit
        return VerifyResult(ok=True, data=data)

    if kind == "char_curve":
        curve = str(data.get("curve") or "ttl_vtc")
        if curve not in ("ttl_vtc", "cmos_vtc"):
            return VerifyResult(
                ok=False, feedback="curve 仅支持 ttl_vtc 或 cmos_vtc"
            )
        data["curve"] = curve
        return VerifyResult(ok=True, data=data)

    if kind == "msi_design":
        data.setdefault("schema_version", "digital_msi_v1")
        data.setdefault("diagram_type", "msi_design")
        from app.tools.draw.digital_dig import normalize_ir
        from app.tools.draw.digital_dig.methodology import validate_logic_first

        data = normalize_ir(data)
        errs = validate_logic_first(data)
        if errs:
            return VerifyResult(ok=False, feedback="；".join(errs))
        if not data.get("components") or not data.get("connections"):
            return VerifyResult(
                ok=False,
                feedback="须含 components 与 connections 完整网表（禁止只用 template 占位）",
            )
        return VerifyResult(ok=True, data=data)

    return VerifyResult(ok=False, feedback=f"未知 kind={kind}")

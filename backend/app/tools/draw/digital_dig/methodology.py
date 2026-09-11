# -*- coding: utf-8 -*-
"""设计电路：逻辑先行校验（全类型：74 MSI / 555 / CMOS / DAC·ADC / PLD）。"""

from __future__ import annotations

import re
from typing import Any

from app.tools.draw.digital_dig.pin_library import (
    resolve_chip,
    resolve_pin_name,
    validate_netlist_pins,
)


SUPPORTED_METHODS = (
    "sync_clear",
    "sync_load",
    "decoder_sop",
    "mux",
    "timer_555",
    "monostable",
    "astable",
    "schmitt",
    "cmos_gate",
    "ripple_counter",
    "dac_circuit",
    "adc_circuit",
    "pld_structure",
    "shift_register",
    "comparator_arith",
    "generic_netlist",
)


def _norm_method(raw: str) -> str:
    m = (raw or "").strip().lower()
    aliases = {
        "置零法": "sync_clear",
        "同步清零": "sync_clear",
        "sync_clear": "sync_clear",
        "clear": "sync_clear",
        "加载法": "sync_load",
        "同步加载": "sync_load",
        "sync_load": "sync_load",
        "load": "sync_load",
        "decoder_sop": "decoder_sop",
        "译码": "decoder_sop",
        "138": "decoder_sop",
        "mux": "mux",
        "151": "mux",
        "数据选择": "mux",
        # 555 / 波形
        "timer_555": "timer_555",
        "555": "timer_555",
        "ne555": "timer_555",
        "定时器": "timer_555",
        "monostable": "monostable",
        "单稳": "monostable",
        "astable": "astable",
        "多谐": "astable",
        "多谐振荡": "astable",
        "schmitt": "schmitt",
        "施密特": "schmitt",
        # CMOS
        "cmos_gate": "cmos_gate",
        "cmos": "cmos_gate",
        "反相器振荡": "cmos_gate",
        # 异步计数
        "ripple_counter": "ripple_counter",
        "异步计数": "ripple_counter",
        "ripple": "ripple_counter",
        # DAC/ADC
        "dac_circuit": "dac_circuit",
        "dac": "dac_circuit",
        "数模": "dac_circuit",
        "ad7520": "dac_circuit",
        "adc_circuit": "adc_circuit",
        "adc": "adc_circuit",
        "模数": "adc_circuit",
        # PLD
        "pld_structure": "pld_structure",
        "gal": "pld_structure",
        "pld": "pld_structure",
        # 移位 / 运算
        "shift_register": "shift_register",
        "移位": "shift_register",
        "194": "shift_register",
        "comparator_arith": "comparator_arith",
        "比较器": "comparator_arith",
        "加法器": "comparator_arith",
        # 兜底：任意正确网表
        "generic_netlist": "generic_netlist",
        "generic": "generic_netlist",
        "自定义": "generic_netlist",
        "组合": "generic_netlist",
        "分析电路": "generic_netlist",
    }
    return aliases.get(m, m)


def validate_logic_first(data: dict[str, Any]) -> list[str]:
    """返回错误列表；空列表表示通过。"""
    errors: list[str] = []
    lf = data.get("logic_first")
    if not isinstance(lf, dict) or not lf:
        errors.append("缺少 logic_first：必须先写方法/芯片/目标，再连线")
        return errors

    method = _norm_method(str(lf.get("method") or ""))
    if not method:
        errors.append("logic_first.method 不能为空")
    chip = str(lf.get("chip") or lf.get("device") or "").strip()
    if not chip:
        errors.append("logic_first.chip 不能为空")
    goal = str(lf.get("goal") or "").strip()
    if not goal:
        errors.append("logic_first.goal 不能为空")

    checkers = {
        "sync_clear": lambda: _check_sync_clear(lf, data),
        "sync_load": lambda: _check_sync_load(lf),
        "decoder_sop": lambda: _check_decoder(lf, data),
        "mux": lambda: _check_mux(lf, data),
        "timer_555": lambda: _check_timer_555(lf),
        "monostable": lambda: _check_monostable(lf),
        "astable": lambda: _check_astable(lf),
        "schmitt": lambda: _check_schmitt(lf),
        "cmos_gate": lambda: _check_cmos(lf),
        "ripple_counter": lambda: _check_ripple(lf),
        "dac_circuit": lambda: _check_dac(lf),
        "adc_circuit": lambda: _check_adc(lf),
        "pld_structure": lambda: _check_pld(lf),
        "shift_register": lambda: _check_shift(lf),
        "comparator_arith": lambda: _check_arith(lf),
        "generic_netlist": lambda: _check_generic(lf),
    }
    if method in checkers:
        errors.extend(checkers[method]())
    elif method:
        errors.append(
            "未知 method=%s；支持 %s" % (method, "|".join(SUPPORTED_METHODS))
        )

    # 全 method 通用：禁止教材脚名解析失败后静默出图
    errors.extend(validate_netlist_pins(data))

    rules = data.get("rules") if isinstance(data.get("rules"), dict) else {}
    layout = rules.get("layout")
    if layout is not None and not isinstance(layout, list):
        errors.append("rules.layout 须为字符串数组")

    return errors


def _check_sync_clear(lf: dict[str, Any], data: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    mod = lf.get("modulus")
    det = lf.get("detect_state")
    if mod is not None:
        try:
            mod_i = int(mod)
        except (TypeError, ValueError):
            errs.append("modulus 须为整数")
            mod_i = None
        else:
            if det is None:
                errs.append("sync_clear 须给 detect_state（同步清零 = N-1）")
            else:
                try:
                    det_i = int(det)
                except (TypeError, ValueError):
                    errs.append("detect_state 须为整数")
                else:
                    if det_i != mod_i - 1:
                        errs.append(
                            f"同步置零法 detect_state 应为 N-1={mod_i - 1}，"
                            f"不能是 {det_i}（检 N 会多计一拍）"
                        )
    clear_expr = str(lf.get("clear_expr") or "")
    carry_expr = str(lf.get("carry_expr") or "")
    if not clear_expr:
        errs.append("sync_clear 须写 clear_expr")
    if not carry_expr:
        errs.append("sync_clear 须写 carry_expr（显式进位，禁止省略）")
    if re.search(r"NOT\s*\(\s*~?R", carry_expr, re.I) or "not(~r)" in carry_expr.lower():
        errs.append("禁止用 NOT(~R) 冒充进位；须显式 AND/等价门")
    conns = data.get("connections") or []
    if conns and "163" in str(lf.get("chip") or ""):
        from app.tools.draw.digital_dig.emit_mod7 import validate as validate_mod7_net

        if any(str(c.get("to", "")).startswith("G1.") for c in conns if isinstance(c, dict)):
            errs.extend(validate_mod7_net(data))
    return errs


def _check_sync_load(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("load_expr") and not lf.get("detect_expr"):
        errs.append("sync_load 须写 load_expr 或 detect_expr")
    if lf.get("preset") is None and lf.get("Dn") is None:
        errs.append("sync_load 须写 preset 或 Dn 预置数")
    return errs


def _check_decoder(lf: dict[str, Any], data: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("function") and not lf.get("minterms") and not lf.get("expr"):
        errs.append("decoder_sop 须写 function / minterms / expr 之一")
    chip = str(lf.get("chip") or "")
    cmap = resolve_chip(chip)
    if not cmap:
        return errs
    enable_pins = [
        p
        for p in ("G", "~GA", "~GB", "~1G", "~2G", "1G", "2G")
        if p in cmap.pins
    ]
    if not enable_pins:
        return errs
    driven = {leaf for leaf, _val in _const_and_conn_leaves(data)}
    # 归一后的叶名也算
    driven_real = set()
    for leaf in driven:
        driven_real.add(resolve_pin_name(chip, leaf).upper())
        driven_real.add(leaf.upper())
    if not any(p.upper() in driven_real for p in enable_pins):
        errs.append(
            "decoder_sop 须配置使能脚（如 74138：G=HIGH 且 ~GA/~GB=LOW；"
            "可用教材名 G1/~G2A，系统会映射）"
        )
    return errs


def _const_and_conn_leaves(data: dict[str, Any]) -> list[tuple[str, str]]:
    """返回 (pin_leaf, value_or_empty)。value 仅 constants 有。"""
    out: list[tuple[str, str]] = []
    for c in data.get("constants") or []:
        if not isinstance(c, dict) or not c.get("pin"):
            continue
        leaf = str(c["pin"]).split(".")[-1]
        out.append((leaf, str(c.get("value") or "").upper()))
    for c in data.get("connections") or []:
        if not isinstance(c, dict):
            continue
        for key in ("from", "to"):
            ep = str(c.get(key) or "")
            if "." in ep:
                out.append((ep.split(".")[-1], ""))
    return out


def _check_mux(lf: dict[str, Any], data: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("select_vars") and not lf.get("data_map"):
        errs.append("mux 须写 select_vars 或 data_map")

    chip = str(lf.get("chip") or "74151")
    cmap = resolve_chip(chip)

    # 选通必须有效（151/150：S；157：G；153：1G 与 2G）
    if cmap:
        if "1G" in cmap.pins and "2G" in cmap.pins:
            needed_en = ["1G", "2G"]
        elif "S" in cmap.pins:
            needed_en = ["S"]
        elif "G" in cmap.pins:
            needed_en = ["G"]
        else:
            needed_en = []
        if needed_en:
            driven_low: set[str] = set()
            for leaf, val in _const_and_conn_leaves(data):
                real = resolve_pin_name(chip, leaf)
                if real in needed_en and val in ("LOW", "0", "GND"):
                    driven_low.add(real)
            for c in data.get("connections") or []:
                if not isinstance(c, dict):
                    continue
                fr, to = str(c.get("from") or ""), str(c.get("to") or "")
                for a, b in ((fr, to), (to, fr)):
                    if "GND" not in a.upper():
                        continue
                    leaf = b.split(".")[-1] if "." in b else ""
                    real = resolve_pin_name(chip, leaf) if leaf else ""
                    if real in needed_en:
                        driven_low.add(real)
            missing = [p for p in needed_en if p not in driven_low]
            if missing:
                errs.append(
                    "mux 须将选通/使能接 LOW（缺："
                    + ",".join(missing)
                    + "；74151/150 可用教材名 ~G→S；74157 用 G；74153 用 1G 与 2G）"
                )

    # 有正输出 Y 时，禁止只从互补端 W 出（除非 goal 明示反相/互补）
    goal = str(lf.get("goal") or "").lower()
    want_comp = any(k in goal for k in ("反相", "互补", "complement", "~y", "w输出"))
    if cmap and "Y" in cmap.pins and not want_comp:
        from_y = False
        from_w = False
        for c in data.get("connections") or []:
            if not isinstance(c, dict):
                continue
            fr = str(c.get("from") or "")
            if "." not in fr:
                continue
            leaf = fr.split(".")[-1]
            real = resolve_pin_name(chip, leaf)
            if real == "Y":
                from_y = True
            if real == "W":
                from_w = True
        if from_w and not from_y:
            errs.append(
                "mux 正逻辑输出应从 Y 引出，不要从互补端 W/~Y（题面要反相时在 goal 写明）"
            )
    return errs


def _check_timer_555(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    mode = str(lf.get("mode") or lf.get("goal") or "").lower()
    if not any(k in mode for k in ("schmitt", "施密特", "mono", "单稳", "astable", "多谐", "timer")):
        if not lf.get("mode"):
            errs.append("timer_555 须写 mode：schmitt|monostable|astable")
    chip = str(lf.get("chip") or "").upper()
    if chip and "555" not in chip and "556" not in chip:
        errs.append("timer_555 的 chip 应为 NE555/555/NE556")
    # 关键 RC 可写在 timing / components
    if not lf.get("timing") and not lf.get("R") and not lf.get("C") and not lf.get("expr"):
        errs.append("timer_555 建议写 timing 或 R/C/expr（周期公式）")
    return errs


def _check_monostable(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("trigger") and not lf.get("expr") and not lf.get("timing"):
        errs.append("monostable 须写 trigger / timing / expr 之一")
    return errs


def _check_astable(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("timing") and not lf.get("freq") and not lf.get("expr") and not (
        lf.get("R") or lf.get("C")
    ):
        errs.append("astable 须写 timing / freq / expr 或 R、C")
    return errs


def _check_schmitt(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("thresholds") and not lf.get("expr") and not lf.get("VT+") and not lf.get("VT-"):
        errs.append("schmitt 须写 thresholds 或 VT+/VT-")
    return errs


def _check_cmos(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("topology") and not lf.get("expr") and not lf.get("role"):
        errs.append("cmos_gate 须写 topology / expr / role（如 inverter_osc）")
    return errs


def _check_ripple(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if lf.get("modulus") is None and not lf.get("stages") and not lf.get("goal"):
        errs.append("ripple_counter 须写 modulus 或 stages")
    return errs


def _check_dac(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("bits") and not lf.get("VREF") and not lf.get("expr") and not lf.get("topology"):
        errs.append("dac_circuit 须写 bits / VREF / expr / topology 之一")
    chip = str(lf.get("chip") or "").upper()
    if chip and not any(x in chip for x in ("7520", "DAC", "0808", "0830")):
        # 允许与计数器拼波形：chip 可写 AD7520+74161
        pass
    return errs


def _check_adc(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("bits") and not lf.get("topology") and not lf.get("expr"):
        errs.append("adc_circuit 须写 bits / topology / expr 之一")
    return errs


def _check_pld(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("device") and not lf.get("chip"):
        errs.append("pld_structure 须写 chip/device（如 GAL16V8）")
    if not lf.get("role") and not lf.get("notes") and not lf.get("goal"):
        errs.append("pld_structure 须写 goal 或 role（结构说明）")
    return errs


def _check_shift(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("mode") and not lf.get("S0_S1") and not lf.get("expr"):
        errs.append("shift_register 须写 mode（移位/并行）或 S0_S1 / expr")
    return errs


def _check_arith(lf: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not lf.get("op") and not lf.get("expr") and not lf.get("function"):
        errs.append("comparator_arith 须写 op / function / expr")
    return errs


def _check_generic(lf: dict[str, Any]) -> list[str]:
    """兜底：只要求能说明目标；具体靠完整网表。"""
    errs: list[str] = []
    if not lf.get("goal") and not lf.get("notes"):
        errs.append("generic_netlist 须写 goal 或 notes")
    return errs


def match_gold_template(brief: str, data: dict[str, Any]) -> str | None:
    """命中已注册金标则返回 template id。"""
    tpl = str(data.get("template") or data.get("gold") or "").strip().lower()
    if tpl in ("mod7_74163", "mod7", "74163_mod7"):
        return "mod7_74163"
    blob = f"{brief}\n{data}".lower()
    keys_mod7 = ("模7", "七进制", "mod7", "mod-7", "modulus\": 7", "modulus\":7")
    keys_163 = ("74163", "74ls163", "74hc163", "163")
    keys_clear = ("置零", "同步清零", "sync_clear", "清零法")
    if any(k in blob for k in keys_mod7) and any(k in blob for k in keys_163):
        return "mod7_74163"
    if any(k in blob for k in keys_mod7) and any(k in blob for k in keys_clear):
        if "160" not in blob and "161" not in blob and "138" not in blob:
            return "mod7_74163"
    return None

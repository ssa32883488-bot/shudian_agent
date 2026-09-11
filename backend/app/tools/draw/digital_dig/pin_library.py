# -*- coding: utf-8 -*-
"""器件库：教材全类型引脚几何 + 考试符号。

- Digital 官方 DIL（74xx / CMOS 怪异命名 / EPROM）
- custom_devices 考试外壳：555、CC4xxx、AD7520、DAC/ADC、缺失 74、GAL…
- 别名：74LS/HC、CC/CD、NE555→555、功能代用
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

_PKG = Path(__file__).resolve().parent
_JSON = _PKG / "chip_pinmaps.json"


@dataclass(frozen=True)
class ChipPinMap:
    element: str
    width: int
    pins: dict[str, tuple[int, int]]
    family: str = "74xx"
    origin: str = "digital_lib"


# 金标考试符号（与 emit_mod7 / 用户认可图一致）
_74163_EXAM = ChipPinMap(
    element="74163_exam.dig",
    width=120,
    pins={
        "~R": (0, 0),
        "CLK": (0, 40),
        "D0": (0, 80),
        "D1": (0, 120),
        "D2": (0, 160),
        "D3": (0, 200),
        "EP": (0, 240),
        "GND": (0, 280),
        "VCC": (120, 0),
        "C": (120, 40),
        "Q0": (120, 80),
        "Q1": (120, 120),
        "Q2": (120, 160),
        "Q3": (120, 200),
        "ET": (120, 240),
        "~LD": (120, 280),
    },
    family="74xx",
    origin="exam_gold",
)

CHIP_LIBRARY: dict[str, ChipPinMap] = {
    "74163_exam": _74163_EXAM,
}

CHIP_ALIASES: dict[str, str] = {}
CHIP_FAMILIES: dict[str, list[str]] = {}

# Digital 官方脚名 ← 教材/IR 常用别名（按芯片族）
PIN_ALIASES: dict[str, dict[str, str]] = {
    "74163": {
        "~R": "~SR",
        "R": "~SR",
        "~CLR": "~SR",
        "CLR": "~SR",
        "D0": "P0",
        "D1": "P1",
        "D2": "P2",
        "D3": "P3",
        "A": "P0",
        "B": "P1",
        "C": "P2",
        "D": "P3",
        "EP": "CEP",
        "ENP": "CEP",
        "ET": "CET",
        "ENT": "CET",
        "~LD": "~PE",
        "LD": "~PE",
        "~PE": "~PE",
        "C_out": "TC",
        "RCO": "TC",
        "CO": "TC",
        "CLK": "CLK",
    },
    "74161": {
        "~R": "~CLR",
        "~SR": "~CLR",
        "~CLR": "~CLR",
        "D0": "A",
        "D1": "B",
        "D2": "C",
        "D3": "D",
        "P0": "A",
        "P1": "B",
        "P2": "C",
        "P3": "D",
        "EP": "ENP",
        "CEP": "ENP",
        "ET": "ENT",
        "CET": "ENT",
        "~LD": "~LD",
        "~PE": "~LD",
        "Q0": "QA",
        "Q1": "QB",
        "Q2": "QC",
        "Q3": "QD",
        "C_out": "RCO",
        "RCO": "RCO",
        "TC": "RCO",
        "C": "RCO",
        "CO": "RCO",
    },
    "74160": {
        "~R": "~CLR",
        "R": "~CLR",
        "~SR": "~CLR",
        "D0": "A",
        "D1": "B",
        "D2": "C",
        "D3": "D",
        "P0": "A",
        "P1": "B",
        "P2": "C",
        "P3": "D",
        "EP": "ENP",
        "CEP": "ENP",
        "ET": "ENT",
        "CET": "ENT",
        "Q0": "QA",
        "Q1": "QB",
        "Q2": "QC",
        "Q3": "QD",
        "C": "RCO",
        "TC": "RCO",
        "CO": "RCO",
    },
    "74162": {
        "~R": "~CLR",
        "D0": "A",
        "D1": "B",
        "D2": "C",
        "D3": "D",
        "EP": "ENP",
        "ET": "ENT",
        "Q0": "QA",
        "Q1": "QB",
        "Q2": "QC",
        "Q3": "QD",
        "C": "RCO",
        "TC": "RCO",
    },
    "74138": {
        "G1": "G",
        "S1": "G",
        "~G2A": "~GA",
        "~G2B": "~GB",
        "S2": "~GA",
        "S3": "~GB",
        "~G2": "~GA",
        "G2A": "~GA",
        "G2B": "~GB",
        "Y0": "~Y0",
        "Y1": "~Y1",
        "Y2": "~Y2",
        "Y3": "~Y3",
        "Y4": "~Y4",
        "Y5": "~Y5",
        "Y6": "~Y6",
        "Y7": "~Y7",
    },
    # 8 选 1：教材 Ḡ/A2A1A0/Ȳ ↔ Digital S/C,B,A/W
    "74151": {
        "~G": "S",
        "G": "S",
        "G'": "S",
        "/G": "S",
        "Ḡ": "S",
        "STROBE": "S",
        "~S": "S",
        "S'": "S",
        "/S": "S",
        "~Y": "W",
        "Y'": "W",
        "/Y": "W",
        "Ȳ": "W",
        "YBAR": "W",
        "A0": "A",
        "A1": "B",
        "A2": "C",
    },
    # 16 选 1：输出常为 W，选通为 S
    "74150": {
        "~G": "S",
        "G": "S",
        "G'": "S",
        "/G": "S",
        "Ḡ": "S",
        "STROBE": "S",
        "~S": "S",
        "~Y": "W",
        "Y": "W",
        "Y'": "W",
        "Ȳ": "W",
        "A0": "A",
        "A1": "B",
        "A2": "C",
        "A3": "D",
    },
    # 双 4 选 1
    "74153": {
        "~1G": "1G",
        "1G'": "1G",
        "/1G": "1G",
        "~2G": "2G",
        "2G'": "2G",
        "/2G": "2G",
        "G1": "1G",
        "G2": "2G",
        "A0": "A",
        "A1": "B",
        "S0": "A",
        "S1": "B",
    },
    # 四 2 选 1：S=选择，G=使能（低有效习惯写作 ~G）
    "74157": {
        "~G": "G",
        "G'": "G",
        "/G": "G",
        "Ḡ": "G",
        "STROBE": "G",
        "~S": "S",
    },
    "74139": {
        "1G": "~1G",
        "2G": "~2G",
        "~G1": "~1G",
        "~G2": "~2G",
        "1Y0": "~1Y0",
        "1Y1": "~1Y1",
        "1Y2": "~1Y2",
        "1Y3": "~1Y3",
        "2Y0": "~2Y0",
        "2Y1": "~2Y1",
        "2Y2": "~2Y2",
        "2Y3": "~2Y3",
    },
    # 555 教材脚名
    "NE555": {
        "TRIGGER": "TRIG",
        "THRESHOLD": "THRES",
        "DISCHARGE": "DISCH",
        "CONTROL": "CTRL",
        "CV": "CTRL",
        "vI1": "THRES",
        "vI2": "TRIG",
        "vO": "OUT",
        "vOD": "DISCH",
        "~R": "RESET",
    },
    "555": {
        "TRIGGER": "TRIG",
        "THRESHOLD": "THRES",
        "DISCHARGE": "DISCH",
        "CONTROL": "CTRL",
        "CV": "CTRL",
    },
    # AD7520 教材 d9..d0 ↔ DB1..DB10（MSB=DB1）
    "AD7520": {
        "d9": "DB1",
        "d8": "DB2",
        "d7": "DB3",
        "d6": "DB4",
        "d5": "DB5",
        "d4": "DB6",
        "d3": "DB7",
        "d2": "DB8",
        "d1": "DB9",
        "d0": "DB10",
        "D9": "DB1",
        "D8": "DB2",
        "D7": "DB3",
        "D6": "DB4",
        "D5": "DB5",
        "D4": "DB6",
        "D3": "DB7",
        "D2": "DB8",
        "D1": "DB9",
        "D0": "DB10",
        "Iout1": "OUT1",
        "Iout2": "OUT2",
        "I_out1": "OUT1",
        "RF": "RFB",
        "R_FB": "RFB",
    },
    "OPAMP": {
        "-": "IN-",
        "+": "IN+",
        "VIN-": "IN-",
        "VIN+": "IN+",
        "VOUT": "OUT",
    },
}


def _load_generated() -> None:
    if not _JSON.is_file():
        return
    data = json.loads(_JSON.read_text(encoding="utf-8"))
    CHIP_ALIASES.clear()
    CHIP_ALIASES.update({str(k): str(v) for k, v in (data.get("aliases") or {}).items()})
    CHIP_FAMILIES.clear()
    CHIP_FAMILIES.update({str(k): list(v) for k, v in (data.get("families") or {}).items()})

    for chip, meta in (data.get("chips") or {}).items():
        pins = {k: (int(v[0]), int(v[1])) for k, v in meta["pins"].items()}
        cmap = ChipPinMap(
            element=meta["element"],
            width=int(meta["width"]),
            pins=pins,
            family=str(meta.get("family") or "other"),
            origin=str(meta.get("origin") or "digital_lib"),
        )
        CHIP_LIBRARY[chip] = cmap
        CHIP_LIBRARY[f"{chip}.dig"] = cmap
        # 系列别名（74）
        if chip.startswith("74") and len(chip) > 2 and chip[2].isdigit():
            num = chip[2:]
            for pref in ("74LS", "74HC", "74HCT", "SN74", "SN74LS", "SN74HC"):
                CHIP_LIBRARY[f"{pref}{num}"] = cmap


_load_generated()

# 考试符号优先（教材网表脚名 ~R/D0/EP）
CHIP_LIBRARY["74163_exam"] = _74163_EXAM
CHIP_LIBRARY["74163_exam.dig"] = _74163_EXAM
for k in ("74163", "74LS163", "74HC163", "SN74163", "SN74LS163"):
    CHIP_LIBRARY[k] = _74163_EXAM

# 部分官方计数器 dig 未声明 CLK（DIP 脚2）；补几何供布线
for _chip in ("74160", "74161", "74162", "74190", "74191", "74193"):
    _cmap = CHIP_LIBRARY.get(_chip)
    if _cmap and "CLK" not in _cmap.pins:
        _pins = dict(_cmap.pins)
        _pins["CLK"] = (0, 40)
        _new = ChipPinMap(
            element=_cmap.element,
            width=_cmap.width,
            pins=_pins,
            family=_cmap.family,
            origin=_cmap.origin,
        )
        CHIP_LIBRARY[_chip] = _new
        _num = _chip[2:]
        for _pref in ("74LS", "74HC", "74HCT", "SN74", "SN74LS", "SN74HC"):
            CHIP_LIBRARY[f"{_pref}{_num}"] = _new
        CHIP_LIBRARY[f"{_chip}.dig"] = _new

GATE_TYPES = {
    "NOT": ("Not", 0),
    "INV": ("Not", 0),
    "NAND2": ("NAnd", 2),
    "NAND3": ("NAnd", 3),
    "NAND4": ("NAnd", 4),
    "AND2": ("And", 2),
    "AND3": ("And", 3),
    "AND4": ("And", 4),
    "OR2": ("Or", 2),
    "OR3": ("Or", 3),
    "NOR2": ("NOr", 2),
    "NOR3": ("NOr", 3),
    "XOR2": ("XOr", 2),
    "XNOR2": ("XOr", 2),
}

# 无源/模拟（Digital 内建名；几何由布局器按默认处理）
PASSIVE_TYPES = {
    "RESISTOR": "Resistor",
    "R": "Resistor",
    "CAPACITOR": "Capacitor",
    "C": "Capacitor",
    "DIODE": "DiodeForward",
    "GROUND": "Ground",
    "GND": "Ground",
    "VDD": "Vdd",
    "VCC": "Vdd",
}


def _norm_type(type_name: str) -> str:
    t = (type_name or "").strip()
    if t.endswith(".dig"):
        t = t[: -len(".dig")]
    return t


def _canonical(type_name: str) -> str:
    t = _norm_type(type_name)
    # 别名表（chip_pinmaps.aliases）
    if t in CHIP_ALIASES:
        return CHIP_ALIASES[t]
    tu = t.upper()
    for k, v in CHIP_ALIASES.items():
        if k.upper() == tu:
            return v
    # CC4069 ↔ 已入库名
    if tu.startswith("CD") and tu[2:].isdigit():
        alt = "CC" + tu[2:]
        if alt in CHIP_LIBRARY:
            return alt
        if alt in CHIP_ALIASES:
            return CHIP_ALIASES[alt]
    if tu.startswith("CC") and ("CC" + tu[2:]) in CHIP_LIBRARY:
        return "CC" + tu[2:]
    return t


def resolve_chip(type_name: str) -> Optional[ChipPinMap]:
    t = _canonical(type_name)
    if t in CHIP_LIBRARY:
        return CHIP_LIBRARY[t]
    if t in ("74163", "74LS163", "74HC163", "SN74163"):
        return _74163_EXAM
    # 大小写不敏感
    for k, v in CHIP_LIBRARY.items():
        if k.upper() == t.upper():
            return v
    return None


def _alias_table_key(chip_type: str) -> str:
    t = _canonical(chip_type)
    for key in PIN_ALIASES:
        if key.upper() == t.upper() or t.upper().endswith(key.upper()) or key.upper() in t.upper():
            return key
    if t.upper() in ("555", "NE555", "LMC555"):
        return "NE555"
    if t.upper() == "AD7520":
        return "AD7520"
    return t


def _normalize_pin_token(pin: str) -> str:
    """教材常见上划线/撇号 → ASCII。"""
    p = (pin or "").strip()
    repl = {
        "Ḡ": "~G",
        "Ȳ": "~Y",
        "Ā": "~A",
        "′": "'",
        "’": "'",
    }
    for a, b in repl.items():
        p = p.replace(a, b)
    return p


def _generic_pin_fallback(pin: str, pins: set[str]) -> Optional[str]:
    """无专用别名表时：按库内实脚做保守推断（避免 151 的 ~G 静默丢失）。"""
    p = _normalize_pin_token(pin)
    pu = p.upper()
    pin_set = {x.upper(): x for x in pins}

    def has(*names: str) -> Optional[str]:
        for n in names:
            if n.upper() in pin_set:
                return pin_set[n.upper()]
        return None

    # 低有效选通/使能
    if pu in {"~G", "G'", "/G", "GBAR", "G_BAR", "STROBE", "~S", "S'", "/S"}:
        hit = has("S", "~G", "G", "~GA", "1G", "~1G")
        if hit:
            return hit
    if pu in {"~Y", "Y'", "/Y", "YBAR", "Y_BAR"}:
        hit = has("W", "~Y")
        if hit:
            return hit
    # 地址：A0/A1/A2(/A3) → A/B/C(/D)
    addr = {"A0": "A", "A1": "B", "A2": "C", "A3": "D", "S0": "A", "S1": "B", "S2": "C"}
    if pu in addr:
        hit = has(addr[pu])
        if hit:
            return hit
    return None


def resolve_pin_name(chip_type: str, pin: str) -> str:
    """IR 脚名 → 库内实际 Label。"""
    t = _canonical(chip_type)
    pin_n = _normalize_pin_token(pin)
    if "exam" in t.lower() or (resolve_chip(t) is _74163_EXAM and "163" in t):
        cmap = resolve_chip(t)
        if cmap and pin_n in cmap.pins:
            return pin_n
    base = _alias_table_key(t)
    aliases = PIN_ALIASES.get(base) or {}
    mapped = aliases.get(pin_n, pin_n)
    if mapped == pin_n and pin_n not in aliases:
        for ak, av in aliases.items():
            if ak.upper() == pin_n.upper():
                mapped = av
                break
    cmap = resolve_chip(t)
    pins = set(cmap.pins.keys()) if cmap else set()
    if cmap and mapped in cmap.pins:
        return mapped
    if cmap and pin_n in cmap.pins:
        return pin_n
    # 通用回退（仅当映射结果仍不在库内）
    if cmap:
        fb = _generic_pin_fallback(pin_n, pins)
        if fb and fb in cmap.pins:
            return fb
    return mapped


def pin_exists(chip_type: str, pin: str) -> bool:
    cmap = resolve_chip(chip_type)
    if not cmap:
        return False
    real = resolve_pin_name(chip_type, pin)
    return real in cmap.pins


def _parse_pin_path(path: str) -> tuple[str, str]:
    raw = (path or "").strip()
    if "." not in raw:
        return raw, ""
    cid, pin = raw.split(".", 1)
    return cid.strip(), pin.strip()


def rewrite_ir_pin_names(data: dict) -> dict:
    """把 connections/constants 里的教材脚名改写成库内实脚（全图种通用）。"""
    ir = dict(data or {})
    comps = [c for c in (ir.get("components") or []) if isinstance(c, dict)]
    by_id = {str(c.get("id")): c for c in comps if c.get("id")}

    def fix_endpoint(ep: str) -> str:
        cid, pin = _parse_pin_path(ep)
        if not cid or not pin or cid not in by_id:
            return ep
        ctype = str(by_id[cid].get("type") or "")
        if resolve_gate(ctype) or resolve_passive(ctype):
            return ep
        if ctype in ("Clock", "Out", "In", "Probe"):
            return ep
        if not resolve_chip(ctype):
            return ep
        real = resolve_pin_name(ctype, pin)
        return f"{cid}.{real}"

    consts = []
    for c in ir.get("constants") or []:
        if not isinstance(c, dict):
            continue
        row = dict(c)
        if row.get("pin"):
            row["pin"] = fix_endpoint(str(row["pin"]))
        consts.append(row)
    if consts:
        ir["constants"] = consts

    conns = []
    for c in ir.get("connections") or []:
        if not isinstance(c, dict):
            continue
        row = dict(c)
        if row.get("from"):
            row["from"] = fix_endpoint(str(row["from"]))
        if row.get("to"):
            row["to"] = fix_endpoint(str(row["to"]))
        conns.append(row)
    if conns:
        ir["connections"] = conns
    return ir


def validate_netlist_pins(data: dict) -> list[str]:
    """所有芯片端点必须能解析到库内实脚；否则明确报错（禁止静默丢脚）。"""
    errors: list[str] = []
    comps = [c for c in (data.get("components") or []) if isinstance(c, dict)]
    by_id = {str(c.get("id")): c for c in comps if c.get("id")}

    def check_path(path: str, *, where: str) -> None:
        cid, pin = _parse_pin_path(path)
        if not cid or not pin:
            return
        owner = by_id.get(cid)
        if not owner:
            errors.append(f"{where} 引用未知器件 {cid}（{path}）")
            return
        ctype = str(owner.get("type") or "")
        if resolve_gate(ctype) or resolve_passive(ctype) or ctype in (
            "Clock",
            "Out",
            "In",
            "Probe",
        ):
            return
        cmap = resolve_chip(ctype)
        if not cmap:
            errors.append(f"{where} 器件类型未入库：{cid}:{ctype}")
            return
        real = resolve_pin_name(ctype, pin)
        if real not in cmap.pins:
            sample = "、".join(list(cmap.pins.keys())[:12])
            errors.append(
                f"{where} 脚名无法解析：{path}（{ctype} 无「{pin}」→「{real}」；"
                f"库内示例：{sample}…）"
            )

    for c in data.get("constants") or []:
        if isinstance(c, dict) and c.get("pin"):
            check_path(str(c["pin"]), where="constants")
    for c in data.get("connections") or []:
        if not isinstance(c, dict):
            continue
        if c.get("from"):
            check_path(str(c["from"]), where="connections")
        if c.get("to"):
            check_path(str(c["to"]), where="connections")
    return errors


def resolve_gate(type_name: str) -> Optional[tuple[str, int]]:
    t = (type_name or "").strip().upper()
    return GATE_TYPES.get(t)


def resolve_passive(type_name: str) -> Optional[str]:
    t = (type_name or "").strip().upper()
    return PASSIVE_TYPES.get(t)


def list_chips(family: Optional[str] = None) -> list[str]:
    if family:
        return list(CHIP_FAMILIES.get(family) or [])
    keys = set()
    for k in CHIP_LIBRARY:
        if k.endswith(".dig"):
            continue
        if any(x in k for x in ("LS", "HC", "HCT", "SN")):
            continue
        keys.add(k)
    return sorted(keys)


def list_families() -> dict[str, list[str]]:
    return dict(CHIP_FAMILIES)


def missing_textbook_chips() -> list[str]:
    if not _JSON.is_file():
        return []
    return list(json.loads(_JSON.read_text(encoding="utf-8")).get("missing_textbook") or [])

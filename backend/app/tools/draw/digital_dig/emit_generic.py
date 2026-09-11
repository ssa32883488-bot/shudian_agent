# -*- coding: utf-8 -*-
"""通用 IR → Digital .dig 布局器。

输入：digital_msi_v1 网表（LLM 按方法论 skill 生成）
输出：遵守布线硬规则的 .dig（线不穿符号、门左侧进线、长回授可用 Tunnel）

不是「每题模板」：同一套算法服务任意连线；缺芯片引脚库时明确报错。
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any, Optional

from app.tools.draw.digital_dig.pin_library import (
    resolve_chip,
    resolve_gate,
    resolve_passive,
    resolve_pin_name,
)


def visual(parent, name, x, y, entries=None):
    ve = ET.SubElement(parent, "visualElement")
    ET.SubElement(ve, "elementName").text = name
    ea = ET.SubElement(ve, "elementAttributes")
    for item in entries or []:
        e = ET.SubElement(ea, "entry")
        ET.SubElement(e, "string").text = item[0]
        k = item[1]
        if k == "string":
            ET.SubElement(e, "string").text = item[2]
        elif k == "int":
            ET.SubElement(e, "int").text = str(item[2])
        elif k == "long":
            ET.SubElement(e, "long").text = str(item[2])
        elif k == "rotation":
            rot = ET.SubElement(e, "rotation")
            rot.set("rotation", str(item[2]))
        elif k == "testData":
            td = ET.SubElement(e, "testData")
            ET.SubElement(td, "dataString").text = item[2]
    pos = ET.SubElement(ve, "pos")
    pos.set("x", str(x))
    pos.set("y", str(y))


def W(parent, x1, y1, x2, y2):
    if (x1, y1) == (x2, y2):
        return
    if (x1, y1) > (x2, y2):
        x1, y1, x2, y2 = x2, y2, x1, y1
    w = ET.SubElement(parent, "wire")
    p1 = ET.SubElement(w, "p1")
    p1.set("x", str(x1))
    p1.set("y", str(y1))
    p2 = ET.SubElement(w, "p2")
    p2.set("x", str(x2))
    p2.set("y", str(y2))


def tunnel_entries(net: str, rotation: int = 0) -> list:
    ents = []
    if rotation:
        ents.append(("rotation", "rotation", rotation))
    ents.append(("NetName", "string", net))
    return ents


@dataclass
class Placed:
    id: str
    kind: str  # chip|gate|clock|out|const|gnd
    element: str
    x: int
    y: int
    inputs: int = 0
    label: str = ""
    pins: dict[str, tuple[int, int]] = field(default_factory=dict)  # absolute


def _parse_endpoint(ep: str) -> tuple[str, str]:
    ep = (ep or "").strip()
    if "." not in ep:
        return ep, ""
    a, b = ep.split(".", 1)
    return a, b


def _gate_pin_abs(p: Placed, pin: str) -> tuple[int, int]:
    """Not: IN left / OUT right+40；NAnd/And: A/B/C… 左，OUT 右。"""
    pin_u = pin.upper()
    if p.element == "Not":
        if pin_u in ("IN", "A", "I"):
            return p.x, p.y
        return p.x + 40, p.y
    n = max(p.inputs, 2)
    # 输入脚垂直间距 20
    if pin_u in ("OUT", "Y", "O"):
        # NAnd out ≈ +(80, 20) for 3in mid; And ≈ +(60, 20)
        dx = 80 if p.element == "NAnd" else 60
        if p.element in ("Or", "NOr"):
            dx = 80
        return p.x + dx, p.y + (n - 1) * 10
    # A,B,C or IN0…
    idx = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}.get(pin_u)
    if idx is None and pin_u.startswith("IN"):
        try:
            idx = int(pin_u[2:] or "0")
        except ValueError:
            idx = 0
    if idx is None:
        idx = 0
    return p.x, p.y + idx * 20


def validate_ir_for_layout(spec: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    comps = spec.get("components") or []
    if not comps:
        errs.append("components 为空，无法布局")
    for c in comps:
        if not isinstance(c, dict) or not c.get("id") or not c.get("type"):
            errs.append("每个 component 需要 id 与 type")
            continue
        t = str(c["type"])
        if resolve_chip(t) or resolve_gate(t) or resolve_passive(t) or t in (
            "Clock",
            "Out",
            "Const",
            "Ground",
            "VDD",
            "In",
            "Probe",
        ):
            continue
        # 允许带 .dig
        if t.endswith(".dig") and resolve_chip(t.replace(".dig", "")):
            continue
        errs.append(
            f"未知器件 type={t}（见 LIBRARY.md：74/CMOS/555/DAC/ADC/GAL/门/R/C）"
        )
    if not (spec.get("connections") or []):
        errs.append("connections 为空")
    return errs


def emit_dig(spec: dict[str, Any]) -> tuple[ET.ElementTree, list[str]]:
    """
    返回 (tree, warnings)。
    失败时抛 ValueError(消息)。
    """
    errs = validate_ir_for_layout(spec)
    if errs:
        raise ValueError("；".join(errs))

    c = ET.Element("circuit")
    ET.SubElement(c, "version").text = "1"
    attrs = ET.SubElement(c, "attributes")
    e = ET.SubElement(attrs, "entry")
    ET.SubElement(e, "string").text = "Description"
    desc = str(spec.get("description") or spec.get("circuit_name") or "msi_design")
    ET.SubElement(e, "string").text = desc[:200]

    ve = ET.SubElement(c, "visualElements")
    wires = ET.SubElement(c, "wires")
    warnings: list[str] = []

    comps = [x for x in (spec.get("components") or []) if isinstance(x, dict)]
    by_id = {str(x["id"]): x for x in comps}
    placed: dict[str, Placed] = {}

    # —— 放置主芯片（第一个可解析芯片）+ 其余库内芯片 ——
    chip_origin = (280, 80)
    chip_id = None
    chip_map = None
    chip_comps = []
    for x in comps:
        cm = resolve_chip(str(x["type"]).replace(".dig", ""))
        if cm:
            chip_comps.append((x, cm))
            if chip_id is None:
                chip_id = str(x["id"])
                chip_map = cm
    if not chip_id or not chip_map:
        raise ValueError("IR 中需要至少一颗库内芯片（如 74163_exam / NE555 / AD7520）")

    ox, oy = chip_origin
    cursor_x = ox
    for x, cm in chip_comps:
        cid = str(x["id"])
        visual(ve, cm.element, cursor_x, oy)
        pins_abs_i = {n: (cursor_x + d[0], oy + d[1]) for n, d in cm.pins.items()}
        chip_type_i = str(x["type"])
        extra_alias: dict[str, tuple[int, int]] = {}
        for want in list(cm.pins.keys()) + [
            "~R",
            "~CLR",
            "D0",
            "D1",
            "D2",
            "D3",
            "EP",
            "ET",
            "ENP",
            "ENT",
            "~LD",
            "Q0",
            "Q1",
            "Q2",
            "Q3",
            "TRIG",
            "THRES",
            "OUT",
            "DISCH",
            "CTRL",
            "RESET",
            "OUT1",
            "OUT2",
            "VREF",
            "RFB",
            "IN-",
            "IN+",
        ]:
            real = resolve_pin_name(chip_type_i, want)
            if real in pins_abs_i and want not in pins_abs_i:
                extra_alias[want] = pins_abs_i[real]
        pins_abs_i.update(extra_alias)
        placed[cid] = Placed(
            id=cid,
            kind="chip",
            element=cm.element,
            x=cursor_x,
            y=oy,
            pins=pins_abs_i,
        )
        cursor_x += cm.width + 200

    pins_abs = placed[chip_id].pins
    chip_type = str(by_id[chip_id]["type"])
    ox, oy = placed[chip_id].x, placed[chip_id].y
    chip_map = resolve_chip(chip_type) or chip_map


    # —— 常数脚（任意已放置芯片）——
    const_vals = {
        str(c["pin"]): str(c["value"]).upper()
        for c in (spec.get("constants") or [])
        if isinstance(c, dict) and c.get("pin")
    }
    for pin_path, val in const_vals.items():
        cid, pin = _parse_endpoint(pin_path)
        if cid not in placed or placed[cid].kind != "chip":
            raise ValueError(f"未知常数脚（器件未放置）：{pin_path}")
        pabs = placed[cid].pins
        # 脚名映射
        real = resolve_pin_name(str(by_id.get(cid, {}).get("type") or ""), pin)
        if real not in pabs and pin not in pabs:
            raise ValueError(
                f"未知常数脚：{pin_path}（映射为 {real}，不在芯片引脚库；"
                "请用库内脚名或已登记教材别名，禁止静默丢弃）"
            )
        use = real if real in pabs else pin
        px, py = pabs[use]
        is_high = val in ("HIGH", "1", "VDD", "VCC")
        if use.upper() in ("GND", "VSS") or (
            val in ("GND", "0", "LOW") and use.upper() in ("GND", "VSS")
        ):
            visual(ve, "Ground", px - 100, py + 40)
            W(wires, px - 100, py, px, py)
            W(wires, px - 100, py, px - 100, py + 40)
            continue
        if pabs[use][0] <= placed[cid].x:
            cx = px - 140
            visual(ve, "Const", cx, py, [("Value", "long", 1 if is_high else 0)])
            W(wires, cx, py, px, py)
        else:
            cx = px + 60
            visual(ve, "Const", cx, py, [("Value", "long", 1 if is_high else 0)])
            W(wires, px, py, cx, py)

    # —— Clock / Out / Gate / Passiveive ——
    clocks = [x for x in comps if str(x["type"]) == "Clock"]
    outs = [x for x in comps if str(x["type"]) == "Out"]
    gates = [x for x in comps if resolve_gate(str(x["type"]))]
    passives = [x for x in comps if resolve_passive(str(x["type"]))]

    # 无源：放在芯片下方
    pass_y = oy + max((len(p) for p in (chip_map.pins if chip_map else {})), default=8) * 40 + 80
    for i, pcomp in enumerate(passives):
        pid = str(pcomp["id"])
        el = resolve_passive(str(pcomp["type"])) or "Resistor"
        px = ox + i * 120
        visual(ve, el, px, pass_y)
        # Resistor/Capacitor：近似两端
        placed[pid] = Placed(
            id=pid,
            kind="passive",
            element=el,
            x=px,
            y=pass_y,
            pins={"A": (px, pass_y), "B": (px + 40, pass_y), "IN": (px, pass_y), "OUT": (px + 40, pass_y)},
        )

    # Clock → 接 U1.CLK
    for cl in clocks:
        cid = str(cl["id"])
        lab = str(cl.get("label") or "CLK")
        clk_pin = pins_abs.get("CLK", (ox, oy + 40))
        visual(ve, "Clock", clk_pin[0] - 140, clk_pin[1], [("Label", "string", lab)])
        W(wires, clk_pin[0] - 140, clk_pin[1], clk_pin[0], clk_pin[1])
        placed[cid] = Placed(
            id=cid,
            kind="clock",
            element="Clock",
            x=clk_pin[0] - 140,
            y=clk_pin[1],
            pins={"OUT": (clk_pin[0] - 140, clk_pin[1])},
        )

    # Out 探针：贴在源脚同侧短引出（禁止左脚 Y 飞线穿壳到右侧）
    # 默认右列仅作无源脚回退；74163 Q* 在右、74151 Y/W 在左，各自就近。
    default_probe_x = ox + chip_map.width + 80
    PROBE_OFFSET = 80
    max_right_probe_x = default_probe_x
    for o in outs:
        oid = str(o["id"])
        lab = str(o.get("label") or oid)
        # 找连到该 Out 的来源
        src_pin = None
        for conn in spec.get("connections") or []:
            if str(conn.get("to", "")).startswith(oid + "."):
                src_pin = str(conn.get("from"))
                break
        y = oy + 80
        probe_x = default_probe_x
        if src_pin:
            sc, sp = _parse_endpoint(src_pin)
            if sc == chip_id:
                owner = by_id.get(chip_id) or {}
                real = resolve_pin_name(str(owner.get("type") or ""), sp)
                use = real if real in pins_abs else (sp if sp in pins_abs else "")
                if use:
                    px, py = pins_abs[use]
                    y = py
                    if px <= ox:
                        # 左脚：探针在左侧，短线探针→脚（与 Const 同侧策略一致）
                        probe_x = px - PROBE_OFFSET
                        W(wires, probe_x, y, px, y)
                    else:
                        probe_x = ox + chip_map.width + PROBE_OFFSET
                        W(wires, px, y, probe_x, y)
                        max_right_probe_x = max(max_right_probe_x, probe_x)
        visual(ve, "Out", probe_x, y, [("Label", "string", lab)])
        placed[oid] = Placed(
            id=oid,
            kind="out",
            element="Out",
            x=probe_x,
            y=y,
            label=lab,
            pins={"IN": (probe_x, y)},
        )

    # 门：Not 靠近右侧探针列，组合门更右（左脚 Out 不参与右列推进）
    nots = [g for g in gates if resolve_gate(str(g["type"]))[0] == "Not"]
    combos = [g for g in gates if resolve_gate(str(g["type"]))[0] != "Not"]

    not_x = max_right_probe_x + 40
    for i, g in enumerate(nots):
        gid = str(g["id"])
        el, nin = resolve_gate(str(g["type"]))
        # 尽量与其输入 Q 同行
        gy = oy + 80 + i * 40
        for conn in spec.get("connections") or []:
            if str(conn.get("to", "")).startswith(gid + ".") and "OUT" not in str(
                conn.get("to", "")
            ).upper():
                sc, sp = _parse_endpoint(str(conn.get("from")))
                if sc == chip_id and sp in pins_abs:
                    gy = pins_abs[sp][1]
                elif sc in placed and placed[sc].kind == "out":
                    gy = placed[sc].y
                break
        visual(ve, el, not_x, gy)
        placed[gid] = Placed(
            id=gid, kind="gate", element=el, x=not_x, y=gy, inputs=1
        )

    combo_x = not_x + 180
    # 组合门垂直排列，间距足够避免穿线
    base_y = oy + 40
    for i, g in enumerate(combos):
        gid = str(g["id"])
        el, nin = resolve_gate(str(g["type"]))
        gy = base_y + i * 160
        entries = [("Inputs", "int", nin)] if nin >= 2 else None
        visual(ve, el, combo_x, gy, entries)
        placed[gid] = Placed(
            id=gid, kind="gate", element=el, x=combo_x, y=gy, inputs=nin
        )

    # CO 类 Out 若未从 Q 接上，放在组合门右侧
    for o in outs:
        oid = str(o["id"])
        if oid not in placed:
            continue
        # 已放置
        pass
    # 重新处理：连到门输出的 Out
    for conn in spec.get("connections") or []:
        fr, to = str(conn.get("from", "")), str(conn.get("to", ""))
        tc, tp = _parse_endpoint(to)
        if tc in placed and placed[tc].kind == "out":
            fc, fp = _parse_endpoint(fr)
            if fc in placed and placed[fc].kind == "gate" and fp.upper() in (
                "OUT",
                "Y",
                "O",
                "",
            ):
                # 把门输出接到该 Out：移动 Out 到门右侧
                gp = placed[fc]
                ox_, oy_ = _gate_pin_abs(gp, "OUT")
                # 删不了已画 Out，再画一个并改 placed（Digital 允许多 Out）——改为只拉线到已有位置
                # 若 Out 仍在 Q 列且 label 像 CO，挪线到门输出
                lab = placed[tc].label.upper()
                if lab in ("CO", "Cout", "CARRY") or "CO" in lab:
                    visual(ve, "Out", ox_ + 100, oy_, [("Label", "string", placed[tc].label)])
                    W(wires, ox_, oy_, ox_ + 100, oy_)
                    placed[tc].x, placed[tc].y = ox_ + 100, oy_
                    placed[tc].pins = {"IN": (ox_ + 100, oy_)}

    def endpoint_xy(ep: str) -> Optional[tuple[int, int]]:
        cid, pin = _parse_endpoint(ep)
        if cid not in placed:
            return None
        p = placed[cid]
        if p.kind == "chip":
            if pin not in p.pins:
                # 再试脚名映射
                owner = by_id.get(cid) or {}
                real = resolve_pin_name(str(owner.get("type") or ""), pin)
                if real in p.pins:
                    return p.pins[real]
                return None
            return p.pins[pin]
        if p.kind == "gate":
            return _gate_pin_abs(p, pin or "OUT")
        if p.kind == "clock":
            return p.pins.get("OUT")
        if p.kind == "out":
            return p.pins.get("IN")
        if p.kind == "passive":
            key = (pin or "A").upper()
            return p.pins.get(key) or p.pins.get("A")
        return None

    # —— 连线 ——
    tunnel_i = 0
    wire_fails: list[str] = []
    for conn in spec.get("connections") or []:
        fr, to = str(conn.get("from", "")), str(conn.get("to", ""))
        a = endpoint_xy(fr)
        b = endpoint_xy(to)
        if a is None or b is None:
            wire_fails.append(f"无法布线 {fr} → {to}（端点脚名无法解析）")
            continue
        fc, fp = _parse_endpoint(fr)
        tc, tp = _parse_endpoint(to)

        # 时钟已布
        if fc in placed and placed[fc].kind == "clock":
            continue
        # Out 从芯片 Q：已在放置时布了探针短线
        if tc in placed and placed[tc].kind == "out" and fc == chip_id:
            continue
        # Out 从门 OUT 且已为 CO 特殊处理
        if (
            tc in placed
            and placed[tc].kind == "out"
            and fc in placed
            and placed[fc].kind == "gate"
        ):
            # 若已在 CO 分支拉过，跳过重复；简单再拉一次短线安全否？
            # 对普通 Out 拉线
            if placed[tc].label.upper() in ("CO", "COUT", "CARRY") or "CO" in placed[
                tc
            ].label.upper():
                continue

        # 回授到芯片左侧脚 → Tunnel，避免穿壳
        if tc == chip_id and tp in pins_abs and pins_abs[tp][0] <= ox:
            tunnel_i += 1
            net = f"t{tunnel_i}"
            # 源侧
            visual(ve, "Tunnel", a[0] + 40, a[1], tunnel_entries(net))
            W(wires, a[0], a[1], a[0] + 40, a[1])
            # 汇侧
            bx, by = b
            visual(ve, "Tunnel", bx - 40, by, tunnel_entries(net, rotation=2))
            W(wires, bx - 40, by, bx, by)
            continue

        # 一般：正交，先水平后垂直；若目标是门输入，保证从左侧进
        ax, ay = a
        bx, by = b
        if tc in placed and placed[tc].kind == "gate" and tp.upper() not in (
            "OUT",
            "Y",
            "O",
        ):
            # 门输入：水平接到 bx
            if ax != bx:
                # 若需上绕避免穿其它门，先垂直到 by 再水平——当 ax < bx 时
                mid_x = min(ax, bx - 20)
                if ay != by:
                    W(wires, ax, ay, mid_x, ay)
                    W(wires, mid_x, ay, mid_x, by)
                    W(wires, mid_x, by, bx, by)
                else:
                    W(wires, ax, ay, bx, by)
            else:
                W(wires, ax, ay, bx, by)
            continue

        # 默认曼哈顿
        if ay == by or ax == bx:
            W(wires, ax, ay, bx, by)
        else:
            W(wires, ax, ay, bx, ay)
            W(wires, bx, ay, bx, by)

    # Testcase
    tc = spec.get("testcase") or {}
    if tc.get("data"):
        visual(
            ve,
            "Testcase",
            100,
            oy + 400,
            [
                ("Label", "string", tc.get("label", "T")),
                ("Testdata", "testData", tc.get("data", "")),
            ],
        )

    ET.SubElement(c, "measurementOrdering")
    if wire_fails:
        raise ValueError("；".join(wire_fails[:8]))
    return ET.ElementTree(c), warnings


def analyze_no_through_gates(path) -> list[str]:
    """静检：水平线不得穿 And/NAnd 壳。"""
    notes = []
    root = ET.parse(path).getroot()
    boxes = []
    for ve in root.findall("./visualElements/visualElement"):
        name = ve.findtext("elementName")
        pos = ve.find("pos")
        if pos is None or name not in ("NAnd", "And", "Or", "NOr", "Not"):
            continue
        x, y = int(pos.get("x")), int(pos.get("y"))
        w = 40 if name == "Not" else (80 if name in ("NAnd", "Or", "NOr") else 60)
        h = 40 if name != "Not" else 20
        boxes.append((name, x, y, x + w, y + h))
    through = []
    for name, x0, y0, x1, y1 in boxes:
        for w in root.findall("./wires/wire"):
            p1, p2 = w.find("p1"), w.find("p2")
            wx1, wy1 = int(p1.get("x")), int(p1.get("y"))
            wx2, wy2 = int(p2.get("x")), int(p2.get("y"))
            if wy1 != wy2:
                continue
            if not (y0 < wy1 < y1):
                continue
            lo, hi = sorted((wx1, wx2))
            if lo < x0 + 8 and hi > x1 - 8:
                through.append(f"{name}@{x0},{y0}")
    if through:
        notes.append("FAIL wire through gate: " + ",".join(through))
    else:
        notes.append("OK no wire through gate symbols")
    return notes

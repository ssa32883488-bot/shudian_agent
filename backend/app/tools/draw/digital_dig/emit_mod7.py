#!/usr/bin/env python3
"""JSON IR → validate → .dig（74163 置零法模7 金标布局 v8）。

工作流包内模块；CLI 入口仍可用于本地调试。
"""
from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

_PKG = Path(__file__).resolve().parent
JSON_PATH = _PKG / "gold" / "mod7_74163.json"
DIG_PATH = _PKG / "gold" / "_emit_mod7.dig"


def validate(spec: dict) -> list[str]:
    errors: list[str] = []
    conns = spec.get("connections", [])
    consts = {c["pin"]: c["value"] for c in spec.get("constants", [])}

    g1_ins = [c["from"] for c in conns if c["to"].startswith("G1.")]
    g2_ins = [c["from"] for c in conns if c["to"].startswith("G2.")]
    if "U1.Q3" in g1_ins or "U1.Q3" in g2_ins:
        errors.append("FATAL: Q3 must NOT feed clear/carry decode")
    if "U1.Q0" in g1_ins or "U1.Q0" in g2_ins:
        errors.append("FATAL: Q0 must go through NOT (detect 110 not 111)")
    if "INV0.OUT" not in g1_ins:
        errors.append("MISSING INV0.OUT → clear NAND")
    if "INV0.OUT" not in g2_ins:
        errors.append("MISSING INV0.OUT → carry AND")
    for need in ("U1.Q1", "U1.Q2"):
        if need not in g1_ins:
            errors.append(f"MISSING clear input {need}")
        if need not in g2_ins:
            errors.append(f"MISSING carry input {need}")
    if not any(c["from"] == "U1.Q0" and c["to"] == "INV0.IN" for c in conns):
        errors.append("MISSING U1.Q0 → INV0")
    if not any(c["from"] == "G1.OUT" and c["to"] == "U1.~R" for c in conns):
        errors.append("MISSING G1.OUT → U1.~R")
    if not any(c["from"] == "G2.OUT" and c["to"] == "CO.IN" for c in conns):
        errors.append("MISSING G2.OUT → CO")
    if any(c["from"] == "U1.C" for c in conns):
        errors.append("FATAL: do not use chip C as mod-7 carry")
    for pin, val in (
        ("U1.EP", "HIGH"),
        ("U1.ET", "HIGH"),
        ("U1.~LD", "HIGH"),
        ("U1.D0", "LOW"),
        ("U1.D1", "LOW"),
        ("U1.D2", "LOW"),
        ("U1.D3", "LOW"),
    ):
        if consts.get(pin) != val:
            errors.append(f"CONST {pin} want {val} got {consts.get(pin)}")
    return errors


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


def emit_dig(spec: dict) -> ET.ElementTree:
    """
    Gold layout v8 (user-accepted):
      ~R = NAND(Q2, Q1, ~Q0)   detect state 6
      CO = AND(Q2, Q1, ~Q0)    explicit AND (not NOT of ~R)
      Q0 through inverter; Q3 probe only; chip C unused
      Solid wires Q→gates; Tunnel only for ~R (nR); AND right of wrap, enter from left
      Never route wires through chip/gate symbols
    """
    c = ET.Element("circuit")
    ET.SubElement(c, "version").text = "1"
    attrs = ET.SubElement(c, "attributes")
    e = ET.SubElement(attrs, "entry")
    ET.SubElement(e, "string").text = "Description"
    ET.SubElement(e, "string").text = (
        "mod7 sync-clear detect6: ~R=NAND(Q2,Q1,~Q0); CO=AND(Q2,Q1,~Q0)"
    )

    ve = ET.SubElement(c, "visualElements")
    wires = ET.SubElement(c, "wires")

    # —— chip + controls ——
    visual(ve, "74163_exam.dig", 280, 80)

    visual(ve, "Clock", 140, 120, [("Label", "string", "CLK")])
    W(wires, 140, 120, 280, 120)

    for y in (160, 200, 240, 280):
        visual(ve, "Const", 140, y, [("Value", "long", 0)])
        W(wires, 140, y, 280, y)

    visual(ve, "Const", 140, 320, [("Value", "long", 1)])
    W(wires, 140, 320, 280, 320)

    visual(ve, "Ground", 180, 400)
    W(wires, 180, 360, 280, 360)
    W(wires, 180, 360, 180, 400)

    visual(ve, "Const", 460, 80, [("Value", "long", 1)])
    W(wires, 400, 80, 460, 80)
    visual(ve, "Const", 460, 320, [("Value", "long", 1)])
    W(wires, 400, 320, 460, 320)
    visual(ve, "Const", 460, 360, [("Value", "long", 1)])
    W(wires, 400, 360, 460, 360)

    # —— Q probes（Q3 只探针）——
    for y, lab in ((160, "Q0"), (200, "Q1"), (240, "Q2"), (280, "Q3")):
        visual(ve, "Out", 480, y, [("Label", "string", lab)])
        W(wires, 400, y, 480, y)

    # Q0 → Not；左侧实线进 NAND；绕行后从左侧进 AND（禁止线穿门符号）
    visual(ve, "Not", 520, 160)
    W(wires, 480, 160, 520, 160)
    # Not 出 ≈ (560,160)

    nx, ny = 700, 160  # NAnd in 160/180/200 → out 780,180
    # AND 放在绕行列右侧，输入只从左侧进入，线不会穿符号
    ax, ay = 980, 280  # And in 280/300/320 → out 1040,300

    visual(ve, "NAnd", nx, ny, [("Inputs", "int", 3)])
    visual(ve, "And", ax, ay, [("Inputs", "int", 3)])

    visual(
        ve,
        "Text",
        520,
        100,
        [
            ("Description", "string", "~R=NAND(Q2,Q1,~Q0) detect state 6"),
            ("FontSize", "int", 14),
        ],
    )
    visual(
        ve,
        "Text",
        980,
        360,
        [
            ("Description", "string", "CO=AND(Q2,Q1,~Q0)"),
            ("FontSize", "int", 14),
        ],
    )

    # 左侧 → NAND（Q1 水平止于 x=640，避免与 Q2 在 (660,200) 短路）
    W(wires, 560, 160, 670, 160)
    W(wires, 670, 160, nx, 160)  # ~Q0
    W(wires, 480, 200, 640, 200)
    W(wires, 640, 180, 640, 200)
    W(wires, 640, 180, nx, 180)  # Q1
    W(wires, 480, 240, 660, 240)
    W(wires, 660, 200, 660, 240)
    W(wires, 660, 200, nx, 200)  # Q2

    # 上绕 → 竖槽 → 从左侧短接到 AND（竖槽 x < ax，绝不穿 And/NAnd 壳）
    # ~Q0 @670 → 槽 860
    W(wires, 670, 120, 670, 160)
    W(wires, 670, 120, 860, 120)
    W(wires, 860, 120, 860, 280)
    W(wires, 860, 280, ax, 280)
    # Q1 @640 → 槽 880
    W(wires, 640, 100, 640, 180)
    W(wires, 640, 100, 880, 100)
    W(wires, 880, 100, 880, 300)
    W(wires, 880, 300, ax, 300)
    # Q2 @660 → 槽 900
    W(wires, 660, 80, 660, 200)
    W(wires, 660, 80, 900, 80)
    W(wires, 900, 80, 900, 320)
    W(wires, 900, 320, ax, 320)

    # CO ← AND（右侧引出）
    and_out = (ax + 60, ay + 20)  # (1040, 300)
    visual(ve, "Out", and_out[0] + 80, and_out[1], [("Label", "string", "CO")])
    W(wires, and_out[0], and_out[1], and_out[0] + 80, and_out[1])

    # 仅 ~R 用 Tunnel（NAND 右侧，勿与绕行槽重叠）
    nand_out = (nx + 80, ny + 20)  # (780, 180)
    visual(ve, "Tunnel", 820, 180, tunnel_entries("nR"))
    W(wires, nand_out[0], nand_out[1], 820, 180)
    visual(ve, "Tunnel", 240, 80, tunnel_entries("nR", rotation=2))
    W(wires, 240, 80, 280, 80)

    tc = spec.get("testcase", {})
    visual(
        ve,
        "Testcase",
        100,
        480,
        [
            ("Label", "string", tc.get("label", "MOD7")),
            ("Testdata", "testData", tc.get("data", "")),
        ],
    )

    ET.SubElement(c, "measurementOrdering")
    return ET.ElementTree(c)


def analyze_dig(path: Path) -> list[str]:
    notes = []
    root = ET.parse(path).getroot()
    nand_inputs = and_inputs = None
    not_count = 0
    tunnel_nets = set()
    for ve in root.findall("./visualElements/visualElement"):
        name = ve.findtext("elementName")
        if name == "Not":
            not_count += 1
        if name == "Tunnel":
            for entry in ve.findall("./elementAttributes/entry"):
                kids = list(entry)
                if kids and kids[0].text == "NetName":
                    tunnel_nets.add(kids[1].text)
        for entry in ve.findall("./elementAttributes/entry"):
            kids = list(entry)
            if kids and kids[0].text == "Inputs":
                n = int(kids[1].text)
                if name == "NAnd":
                    nand_inputs = n
                elif name == "And":
                    and_inputs = n

    if nand_inputs != 3:
        notes.append(f"FAIL NAnd Inputs={nand_inputs}")
    else:
        notes.append("OK NAnd Inputs=3")
    if and_inputs != 3:
        notes.append(f"FAIL And Inputs={and_inputs}")
    else:
        notes.append("OK And Inputs=3 (explicit CO)")
    if not_count < 1:
        notes.append("FAIL missing Not on Q0")
    else:
        notes.append("OK Not on Q0")

    if "nR" not in tunnel_nets:
        notes.append("FAIL missing Tunnel nR for ~R")
    else:
        notes.append("OK Tunnel nR only for ~R feedback")
    extra = tunnel_nets - {"nR"}
    if extra:
        notes.append(f"WARN extra tunnels (prefer wires): {sorted(extra)}")

    # Q3：芯片→探针段不得延伸进译码区（仅查 x∈[400,600] 的探针行）
    bad = []
    for w in root.findall("./wires/wire"):
        p1, p2 = w.find("p1"), w.find("p2")
        x1, y1 = int(p1.get("x")), int(p1.get("y"))
        x2, y2 = int(p2.get("x")), int(p2.get("y"))
        if y1 == 280 and y2 == 280:
            lo, hi = sorted((x1, x2))
            if lo <= 480 and hi > 520:
                bad.append((lo, hi))
    if bad:
        notes.append(f"FAIL Q3 row extends into decode at {bad}")
    else:
        notes.append("OK Q3 stops at probe")

    # 硬规则：水平线不得穿过 NAnd/And 符号外壳
    def gate_boxes():
        boxes = []
        for ve in root.findall("./visualElements/visualElement"):
            name = ve.findtext("elementName")
            pos = ve.find("pos")
            if pos is None or name not in ("NAnd", "And"):
                continue
            x, y = int(pos.get("x")), int(pos.get("y"))
            # NAnd 宽约 80；And 宽约 60；三输入高约 40
            w = 80 if name == "NAnd" else 60
            boxes.append((name, x, y, x + w, y + 40))
        return boxes

    through = []
    for name, x0, y0, x1, y1 in gate_boxes():
        for w in root.findall("./wires/wire"):
            p1, p2 = w.find("p1"), w.find("p2")
            wx1, wy1 = int(p1.get("x")), int(p1.get("y"))
            wx2, wy2 = int(p2.get("x")), int(p2.get("y"))
            if wy1 != wy2:
                continue  # 只查水平穿壳
            if not (y0 < wy1 < y1):
                continue
            lo, hi = sorted((wx1, wx2))
            # 线段同时覆盖符号左缘内侧与右缘内侧 → 穿心
            if lo < x0 + 10 and hi > x1 - 10:
                through.append(f"{name}@{x0},{y0} wire y={wy1} [{lo},{hi}]")
    if through:
        notes.append("FAIL wire through gate symbol: " + "; ".join(through))
    else:
        notes.append("OK no horizontal wire through NAnd/And body")

    const0_ys = set()
    for ve in root.findall("./visualElements/visualElement"):
        if ve.findtext("elementName") != "Const":
            continue
        pos = ve.find("pos")
        val = None
        for entry in ve.findall("./elementAttributes/entry"):
            kids = list(entry)
            if kids and kids[0].text == "Value":
                val = int(kids[1].text)
        if val == 0 and pos is not None:
            const0_ys.add(int(pos.get("y")))
    need_low = {160, 200, 240, 280}
    if not need_low.issubset(const0_ys):
        notes.append(f"FAIL D-pin Const0 missing at y={sorted(need_low - const0_ys)}")
    else:
        notes.append("OK D0..D3 tied via Const 0")
    return notes


def main() -> int:
    spec = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    errs = validate(spec)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        return 2
    print("validation OK")

    tree = emit_dig(spec)
    try:
        ET.indent(tree, space="  ")
    except AttributeError:
        pass
    tree.write(DIG_PATH, encoding="utf-8", xml_declaration=True)
    print(f"wrote {DIG_PATH}")
    for n in analyze_dig(DIG_PATH):
        print(n)
        if n.startswith("FAIL"):
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

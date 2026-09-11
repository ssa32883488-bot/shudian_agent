# -*- coding: utf-8 -*-
"""从 Digital 官方 lib + 自定义考试外壳 → chip_pinmaps.json

覆盖：全部 DIL 74xx / CMOS 怪异命名 / EPROM / 教材 555·CMOS·DAC·ADC·PLD·缺失74。
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from custom_devices import (
    CUSTOM_DEVICES,
    DIGITAL_CMOS_ALIASES,
    FUNCTIONAL_SUBSTITUTES,
    emit_all_shells,
)

LIB_ROOT = Path(r"F:\code\digital-circuit-poc\digital\lib\DIL Chips")
PKG = Path(__file__).resolve().parent
COMPONENTS = PKG / "components"
OUT_JSON = PKG / "chip_pinmaps.json"
OUT_PY = PKG / "_generated_chip_maps.py"
OUT_LIST = PKG / "_lib_chips.txt"

PITCH = 40  # Digital DIL 实测脚间距


def find_all_digs() -> list[Path]:
    hits = []
    for p in LIB_ROOT.rglob("*.dig"):
        stem = p.stem.lower()
        if "real" in stem or "inc" in stem:
            continue
        hits.append(p)
    return sorted(hits)


def parse_dil(path: Path) -> dict:
    root = ET.parse(path).getroot()
    width = 5
    for entry in root.findall("./attributes/entry"):
        kids = list(entry)
        if len(kids) >= 2 and kids[0].text == "Width":
            width = int(kids[1].text)

    pins: dict[str, int] = {}
    for ve in root.findall("./visualElements/visualElement"):
        name = ve.findtext("elementName")
        if name not in ("In", "Out"):
            continue
        label = None
        pin_no = None
        for entry in ve.findall("./elementAttributes/entry"):
            kids = list(entry)
            if len(kids) < 2:
                continue
            if kids[0].text == "Label":
                label = kids[1].text
            elif kids[0].text == "pinNumber":
                pin_no = int(kids[1].text)
        if label and pin_no is not None:
            pins[label] = pin_no

    if not pins:
        raise ValueError(f"no pins in {path}")

    max_pin = max(pins.values())
    n = max_pin if max_pin % 2 == 0 else max_pin + 1
    half = n // 2
    width_px = width * 20 + 20

    def pin_to_xy(num: int) -> tuple[int, int]:
        if 1 <= num <= half:
            return (0, (num - 1) * PITCH)
        idx_from_top = n - num
        return (width_px, idx_from_top * PITCH)

    rel = {lab: pin_to_xy(num) for lab, num in pins.items()}
    try:
        src = str(path.relative_to(LIB_ROOT)).replace("\\", "/")
    except ValueError:
        src = str(path.name)
    return {
        "element": f"{path.stem}.dig",
        "width": width_px,
        "max_pin": n,
        "pins": {k: list(v) for k, v in sorted(rel.items(), key=lambda x: pins[x[0]])},
        "pin_numbers": pins,
        "source": src,
        "origin": "digital_lib" if path.is_relative_to(LIB_ROOT) else "custom_shell",
    }


def meta_from_custom(name: str, meta: dict) -> dict:
    """不经 .dig 也可从 CUSTOM_DEVICES 算几何（与 dig 一致）。"""
    width = int(meta.get("width") or 5)
    pin_numbers = {p["label"]: int(p["num"]) for p in meta["pins"]}
    max_pin = max(pin_numbers.values())
    n = max_pin if max_pin % 2 == 0 else max_pin + 1
    half = n // 2
    width_px = width * 20 + 20

    def pin_to_xy(num: int) -> tuple[int, int]:
        if 1 <= num <= half:
            return (0, (num - 1) * PITCH)
        return (width_px, (n - num) * PITCH)

    rel = {lab: list(pin_to_xy(num)) for lab, num in pin_numbers.items()}
    return {
        "element": f"{name}.dig",
        "width": width_px,
        "max_pin": n,
        "pins": dict(sorted(rel.items(), key=lambda x: pin_numbers[x[0]])),
        "pin_numbers": pin_numbers,
        "source": f"components/{name}.dig",
        "origin": "custom_shell",
        "family": meta.get("family"),
        "desc": meta.get("desc"),
    }


def main() -> int:
    COMPONENTS.mkdir(parents=True, exist_ok=True)
    shells = emit_all_shells(COMPONENTS)

    found: dict[str, dict] = {}
    errors: list[str] = []

    for path in find_all_digs():
        try:
            found[path.stem] = parse_dil(path)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{path.stem}({e})")

    # 自定义外壳（覆盖同名）
    for name, meta in CUSTOM_DEVICES.items():
        found[name] = meta_from_custom(name, meta)

    # 别名表
    aliases: dict[str, str] = {}
    for alias, target in DIGITAL_CMOS_ALIASES.items():
        aliases[alias] = target
    for alias, target in FUNCTIONAL_SUBSTITUTES.items():
        # 若已有自定义外壳，优先外壳，不强制代用
        if alias not in found:
            aliases[alias] = target

    for name, meta in CUSTOM_DEVICES.items():
        for a in meta.get("aliases") or []:
            aliases[a] = name
        # 系列前缀
        if name.startswith("74") and len(name) >= 4:
            num = name[2:]
            for pref in ("74LS", "74HC", "74HCT", "SN74", "SN74LS", "SN74HC"):
                aliases[f"{pref}{num}"] = name

    # 官方 74 系列别名
    for chip in list(found):
        if chip.startswith("74") and chip[2:3].isdigit():
            num = chip[2:]
            for pref in ("74LS", "74HC", "74HCT", "SN74", "SN74LS", "SN74HC"):
                aliases.setdefault(f"{pref}{num}", chip)

    # DAC 别名已在 CUSTOM 里；AD7520 数据脚教材 d0..d9
    families: dict[str, list[str]] = {}
    for chip, data in found.items():
        fam = data.get("family")
        if not fam:
            if chip.startswith("74") or chip.startswith("27") or chip.startswith("28"):
                fam = "74xx" if chip.startswith("74") else "memory"
            elif chip.startswith("A"):
                fam = "memory"
            else:
                fam = "other"
        families.setdefault(fam, []).append(chip)

    # 教材清单覆盖检查
    textbook_want = sorted(
        set(CUSTOM_DEVICES)
        | set(DIGITAL_CMOS_ALIASES)
        | {
            "7400", "7402", "7403", "7404", "7407", "7410", "7413", "7420", "7427",
            "74125", "74138", "74139", "74147", "74148", "74151", "74153", "74154",
            "74160", "74161", "74162", "74163", "74175", "74190", "74191", "74193",
            "74194", "74283", "7442", "7448", "7483", "7485", "7490", "7493",
            "NE555", "555", "CC4069", "CC4007", "CC4027", "CC40106", "CC4024",
            "CC4510", "CC40192", "AD7520", "DAC0808", "ADC0820", "GAL16V8", "2114",
        }
    )
    missing_textbook = []
    for t in textbook_want:
        if t in found or t in aliases or (aliases.get(t) in found):
            continue
        missing_textbook.append(t)

    payload = {
        "chips": found,
        "aliases": aliases,
        "families": {k: sorted(v) for k, v in sorted(families.items())},
        "custom_shells": sorted(shells),
        "missing_textbook": missing_textbook,
        "parse_errors": errors,
        "notes": [
            "脚间距 pitch=40；宽度 Width*20+20",
            "custom_shell 多为考试黑盒，CLI 向量可能无法测通，出图仍可用",
            "FUNCTIONAL_SUBSTITUTES 仅在无专用外壳时启用",
        ],
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_LIST.write_text("\n".join(sorted(found)) + "\n", encoding="utf-8")

    # 轻量 py 片段（可选）
    lines = [
        "# Auto-generated — do not edit",
        f"# chips={len(found)} aliases={len(aliases)} customs={len(shells)}",
        "CHIP_COUNT = %d" % len(found),
        "ALIAS_COUNT = %d" % len(aliases),
        "",
    ]
    OUT_PY.write_text("\n".join(lines), encoding="utf-8")

    print(f"ok chips={len(found)} aliases={len(aliases)} shells={len(shells)}")
    print("families:", {k: len(v) for k, v in families.items()})
    if missing_textbook:
        print("missing_textbook:", ", ".join(missing_textbook))
    if errors:
        print("errors:", ", ".join(errors[:10]))
    print("wrote", OUT_JSON)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

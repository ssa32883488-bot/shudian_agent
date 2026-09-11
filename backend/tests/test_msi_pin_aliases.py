# -*- coding: utf-8 -*-
"""MSI 脚名别名 / 未知脚硬失败 / mux 使能校验（全图种回归）。"""

from __future__ import annotations

import pytest

from app.tools.draw.digital_dig import normalize_ir, draw_digital_msi
from app.tools.draw.digital_dig.methodology import validate_logic_first
from app.tools.draw.digital_dig.pin_library import (
    resolve_pin_name,
    rewrite_ir_pin_names,
    validate_netlist_pins,
)


@pytest.mark.parametrize(
    "chip,raw,expect",
    [
        ("74151", "~G", "S"),
        ("74HC151", "Ḡ", "S"),
        ("74151", "STROBE", "S"),
        ("74151", "~Y", "W"),
        ("74151", "A0", "A"),
        ("74151", "A2", "C"),
        ("74150", "~G", "S"),
        ("74150", "Y", "W"),
        ("74138", "G1", "G"),
        ("74138", "~G2A", "~GA"),
        ("74138", "Y0", "~Y0"),
        ("74157", "~G", "G"),
        ("74153", "~1G", "1G"),
        ("NE555", "TRIGGER", "TRIG"),
    ],
)
def test_resolve_textbook_pin_aliases(chip: str, raw: str, expect: str):
    assert resolve_pin_name(chip, raw) == expect


def test_rewrite_ir_maps_enable_before_emit():
    ir = rewrite_ir_pin_names(
        {
            "components": [{"id": "U1", "type": "74151"}],
            "constants": [{"pin": "U1.~G", "value": "LOW"}],
            "connections": [{"from": "U1.Y", "to": "Y.IN"}],
        }
    )
    assert ir["constants"][0]["pin"] == "U1.S"


def test_unknown_pin_fails_validation():
    ir = {
        "logic_first": {
            "method": "mux",
            "chip": "74151",
            "goal": "f",
            "data_map": {"D0": "0"},
        },
        "components": [{"id": "U1", "type": "74151"}, {"id": "Y", "type": "Out"}],
        "connections": [{"from": "U1.Y", "to": "Y.IN"}],
        "constants": [{"pin": "U1.NOT_A_REAL_PIN", "value": "LOW"}],
    }
    errs = validate_netlist_pins(normalize_ir(ir))
    assert errs and "无法解析" in "".join(errs)


def test_mux_rejects_missing_strobe():
    ir = normalize_ir(
        {
            "logic_first": {
                "method": "mux",
                "chip": "74151",
                "goal": "odd_parity",
                "select_vars": ["A", "B", "C"],
                "data_map": {"D0": "0"},
            },
            "components": [
                {"id": "U1", "type": "74151"},
                {"id": "Y", "type": "Out", "label": "Y"},
            ],
            "connections": [{"from": "U1.Y", "to": "Y.IN"}],
            "constants": [{"pin": "U1.D0", "value": "LOW"}],
        }
    )
    errs = validate_logic_first(ir)
    assert any("选通" in e or "使能" in e for e in errs)


def test_mux_rejects_output_from_w_only():
    ir = normalize_ir(
        {
            "logic_first": {
                "method": "mux",
                "chip": "74151",
                "goal": "odd_parity",
                "select_vars": ["A", "B", "C"],
                "data_map": {"D1": "1"},
            },
            "components": [
                {"id": "U1", "type": "74151"},
                {"id": "Y", "type": "Out", "label": "Y"},
            ],
            "connections": [{"from": "U1.W", "to": "Y.IN"}],
            "constants": [{"pin": "U1.~G", "value": "LOW"}],
        }
    )
    errs = validate_logic_first(ir)
    assert any("Y 引出" in e or "互补" in e for e in errs)


def test_mux_accepts_textbook_strobe_and_draws():
    ir = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "circuit_name": "odd_parity_151",
        "logic_first": {
            "method": "mux",
            "chip": "74151",
            "goal": "odd_parity",
            "select_vars": ["A", "B", "C"],
            "data_map": {
                "D0": "0",
                "D1": "1",
                "D2": "1",
                "D3": "0",
                "D4": "1",
                "D5": "0",
                "D6": "0",
                "D7": "1",
            },
        },
        "components": [
            {"id": "U1", "type": "74151"},
            {"id": "Y", "type": "Out", "label": "Y"},
        ],
        "connections": [{"from": "U1.Y", "to": "Y.IN"}],
        "constants": [
            {"pin": "U1.~G", "value": "LOW"},
            {"pin": "U1.D0", "value": "LOW"},
            {"pin": "U1.D1", "value": "HIGH"},
            {"pin": "U1.D2", "value": "HIGH"},
            {"pin": "U1.D3", "value": "LOW"},
            {"pin": "U1.D4", "value": "HIGH"},
            {"pin": "U1.D5", "value": "LOW"},
            {"pin": "U1.D6", "value": "LOW"},
            {"pin": "U1.D7", "value": "HIGH"},
        ],
    }
    # 逻辑校验应通过（~G 已能映射）
    assert validate_logic_first(normalize_ir(ir)) == []
    res = draw_digital_msi(ir)
    assert res.ok, res.error
    meta = res.meta or {}
    warns = " ".join(meta.get("warnings") or [])
    assert "跳过未知常数脚" not in warns
    assert "U1.~G" not in warns


def test_74151_y_out_probe_stays_on_left():
    """左脚 Y 的 Out 探针必须同侧短引出，禁止穿壳飞到芯片右侧。"""
    import xml.etree.ElementTree as ET

    from app.tools.draw.digital_dig.emit_generic import emit_dig

    ir = rewrite_ir_pin_names(
        {
            "components": [
                {"id": "U1", "type": "74151"},
                {"id": "Y", "type": "Out", "label": "Y"},
            ],
            "connections": [{"from": "U1.Y", "to": "Y.IN"}],
            "constants": [
                {"pin": "U1.S", "value": "LOW"},
                {"pin": "U1.D0", "value": "LOW"},
                {"pin": "U1.D1", "value": "HIGH"},
                {"pin": "U1.D2", "value": "HIGH"},
                {"pin": "U1.D3", "value": "LOW"},
                {"pin": "U1.D4", "value": "HIGH"},
                {"pin": "U1.D5", "value": "LOW"},
                {"pin": "U1.D6", "value": "LOW"},
                {"pin": "U1.D7", "value": "HIGH"},
            ],
        }
    )
    tree, _warns = emit_dig(ir)
    root = tree.getroot()
    chip_x = out_x = None
    for ve in root.iter("visualElement"):
        name = ve.findtext("elementName") or ""
        pos = ve.find("pos")
        if pos is None:
            continue
        x = int(pos.get("x"))
        if "74151" in name:
            chip_x = x
        if name == "Out":
            out_x = x
    assert chip_x is not None and out_x is not None
    assert out_x < chip_x, f"Y Out should be left of chip, out_x={out_x} chip_x={chip_x}"

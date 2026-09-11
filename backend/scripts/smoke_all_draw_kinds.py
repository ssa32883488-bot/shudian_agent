# -*- coding: utf-8 -*-
"""全线画图冒烟：各 diagram_kind + MSI 多 method + xor。

用法（在 backend 目录）:
  set PYTHONPATH=.
  py -3 scripts/smoke_all_draw_kinds.py

产物写入 data/artifacts/smoke_draw_report/
"""
from __future__ import annotations

import json
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]  # backend
OUT = ROOT / "data" / "artifacts" / "smoke_draw_report"
OUT.mkdir(parents=True, exist_ok=True)


def _save_svg(name: str, svg: str | None) -> str | None:
    if not svg:
        return None
    path = OUT / f"{name}.svg"
    path.write_text(svg, encoding="utf-8")
    return str(path)


def _case(name: str, fn: Callable[[], Any]) -> dict[str, Any]:
    t0 = time.perf_counter()
    row: dict[str, Any] = {"name": name, "ok": False}
    try:
        res = fn()
        elapsed = round(time.perf_counter() - t0, 3)
        row["elapsed_s"] = elapsed
        ok = bool(getattr(res, "ok", False))
        row["ok"] = ok
        row["engine"] = getattr(res, "engine", None)
        row["error"] = getattr(res, "error", None)
        meta = getattr(res, "meta", None) or {}
        row["meta"] = {
            k: meta.get(k)
            for k in (
                "kind",
                "emitter",
                "cli_test",
                "draw_kind",
                "prefix",
                "warnings",
                "methodology",
            )
            if k in meta
        }
        url = getattr(res, "artifact_url", None)
        row["artifact_url"] = url
        svg = getattr(res, "artifact", None)
        row["svg_bytes"] = len(svg) if svg else 0
        row["svg_path"] = _save_svg(name.replace("/", "_"), svg if ok else None)
        if not ok and not row["error"]:
            row["error"] = "ok=False without error"
    except Exception as e:  # noqa: BLE001
        row["elapsed_s"] = round(time.perf_counter() - t0, 3)
        row["ok"] = False
        row["error"] = f"{type(e).__name__}: {e}"
        row["traceback"] = traceback.format_exc()[-800:]
    return row


def _wf(kind: str, ir: dict[str, Any], brief: str = ""):
    from app.tools.draw_workflow import draw_with_workflow

    return draw_with_workflow(
        diagram_kind=kind,
        brief=brief or kind,
        script=json.dumps(ir, ensure_ascii=False),
        max_retries=1,
    )


def build_cases() -> list[tuple[str, Callable[[], Any]]]:
    from app.tools.draw.digital_dig import draw_digital_msi, load_gold_mod7

    logic_ir = {
        "schema_version": "logic_ir_v1",
        "diagram_type": "logic",
        "inputs": ["A", "B", "Cin"],
        "outputs": ["S", "Cout"],
        "gates": [
            {"id": "x1", "type": "XOR", "inputs": ["A", "B"]},
            {"id": "x2", "type": "XOR", "inputs": ["x1", "Cin"]},
            {"id": "a1", "type": "AND", "inputs": ["A", "B"]},
            {"id": "a2", "type": "AND", "inputs": ["x1", "Cin"]},
            {"id": "o1", "type": "OR", "inputs": ["a1", "a2"]},
        ],
        "nets": {"S": "x2", "Cout": "o1"},
    }

    wave_ir = {
        "schema_version": "wave_ir_v1",
        "diagram_type": "waveform",
        "title": "CLK-Q 波形",
        "signals": [
            {"name": "CLK", "wave": "01010101"},
            {"name": "Q", "wave": "0.1.0.1."},
            {"name": "~Q", "wave": "1.0.1.0."},
        ],
    }

    state_ir = {
        "schema_version": "state_ir_v1",
        "diagram_type": "state",
        "title": "模4计数状态图",
        "states": ["00", "01", "10", "11"],
        "transitions": [
            {"from": "00", "to": "01", "label": "1"},
            {"from": "01", "to": "10", "label": "1"},
            {"from": "10", "to": "11", "label": "1"},
            {"from": "11", "to": "00", "label": "1"},
        ],
        "initial": "00",
    }

    truth_ir = {
        "inputs": ["A", "B"],
        "outputs": ["Y"],
        "rows": [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]],
        "title": "异或真值表",
    }

    kmap_ir = {
        "minterms": [1, 3, 5, 7],
        "var_count": 3,
        "dont_cares": [],
        "auto_group": True,
        "title": "Σm(1,3,5,7)",
    }

    # MSI: 74160 模6 置零（正确检态5）
    msi_mod6 = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "circuit_name": "mod6_74160",
        "logic_first": {
            "method": "sync_clear",
            "chip": "74160",
            "goal": "mod6",
            "modulus": 6,
            "detect_state": 5,
            "clear_expr": "NAND(Q2,Q0)",
            "carry_expr": "AND(Q2,Q0)",
        },
        "components": [
            {"id": "U1", "type": "74160"},
            {"id": "G1", "type": "NAND2"},
            {"id": "G2", "type": "AND2"},
            {"id": "CLK", "type": "Clock", "label": "CLK"},
            {"id": "CO", "type": "Out", "label": "CO"},
        ],
        "connections": [
            {"from": "CLK.OUT", "to": "U1.CLK"},
            {"from": "U1.Q0", "to": "G1.A"},
            {"from": "U1.Q2", "to": "G1.B"},
            {"from": "G1.OUT", "to": "U1.~R"},
            {"from": "U1.Q0", "to": "G2.A"},
            {"from": "U1.Q2", "to": "G2.B"},
            {"from": "G2.OUT", "to": "CO.IN"},
        ],
        "constants": [
            {"pin": "U1.EP", "value": "HIGH"},
            {"pin": "U1.ET", "value": "HIGH"},
            {"pin": "U1.~LD", "value": "HIGH"},
            {"pin": "U1.D0", "value": "LOW"},
            {"pin": "U1.D1", "value": "LOW"},
            {"pin": "U1.D2", "value": "LOW"},
            {"pin": "U1.D3", "value": "LOW"},
        ],
    }

    msi_555 = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "circuit_name": "ne555_astable",
        "logic_first": {
            "method": "timer_555",
            "chip": "NE555",
            "goal": "astable",
            "mode": "astable",
            "timing": "T=0.693*(Ra+2*Rb)*C",
        },
        "components": [
            {"id": "U1", "type": "NE555"},
            {"id": "Ra", "type": "Resistor"},
            {"id": "Rb", "type": "Resistor"},
            {"id": "C1", "type": "Capacitor"},
            {"id": "OUT", "type": "Out", "label": "vO"},
        ],
        "connections": [
            {"from": "U1.OUT", "to": "OUT.IN"},
            {"from": "Ra.B", "to": "U1.DISCH"},
            {"from": "Rb.A", "to": "U1.DISCH"},
            {"from": "Rb.B", "to": "U1.THRES"},
            {"from": "C1.A", "to": "U1.THRES"},
        ],
        "constants": [{"pin": "U1.RESET", "value": "HIGH"}],
    }

    msi_dac = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "circuit_name": "ad7520_stair",
        "logic_first": {
            "method": "dac_circuit",
            "chip": "AD7520+74161",
            "goal": "staircase",
            "bits": 4,
            "VREF": -10,
            "topology": "counter_high_nibble",
        },
        "components": [
            {"id": "U1", "type": "74161"},
            {"id": "U2", "type": "AD7520"},
            {"id": "A1", "type": "OPAMP"},
            {"id": "CLK", "type": "Clock", "label": "CLK"},
        ],
        "connections": [
            {"from": "CLK.OUT", "to": "U1.CLK"},
            {"from": "U1.Q0", "to": "U2.d6"},
            {"from": "U1.Q1", "to": "U2.d7"},
            {"from": "U1.Q2", "to": "U2.d8"},
            {"from": "U1.Q3", "to": "U2.d9"},
            {"from": "U2.OUT1", "to": "A1.IN-"},
        ],
        "constants": [],
    }

    msi_cmos = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "circuit_name": "cc4069_inv",
        "logic_first": {
            "method": "cmos_gate",
            "chip": "CC4069",
            "goal": "inverter",
            "topology": "single_inverter",
            "role": "inverter",
        },
        "components": [
            {"id": "U1", "type": "CC4069"},
            {"id": "IN", "type": "Clock", "label": "vi"},
            {"id": "OUT", "type": "Out", "label": "vo"},
        ],
        "connections": [
            {"from": "IN.OUT", "to": "U1.1A"},
            {"from": "U1.1Y", "to": "OUT.IN"},
        ],
        "constants": [],
    }

    msi_mux = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "circuit_name": "mux_151",
        "logic_first": {
            "method": "mux",
            "chip": "74151",
            "goal": "8to1",
            "select_vars": ["A", "B", "C"],
            "data_map": {"D0": "0", "D1": "1"},
        },
        "components": [
            {"id": "U1", "type": "74151"},
            {"id": "Y", "type": "Out", "label": "Y"},
        ],
        "connections": [{"from": "U1.Y", "to": "Y.IN"}],
        "constants": [{"pin": "U1.~G", "value": "LOW"}],
    }

    # 故意错误的模6（检态6）——应失败，用于回归门禁
    msi_bad_detect = {
        "schema_version": "digital_msi_v1",
        "diagram_type": "msi_design",
        "logic_first": {
            "method": "sync_clear",
            "chip": "74160",
            "goal": "mod6",
            "modulus": 6,
            "detect_state": 6,
            "clear_expr": "NAND(Q2,Q1)",
            "carry_expr": "AND(Q2,Q1)",
        },
        "components": [{"id": "U1", "type": "74160"}],
        "connections": [{"from": "U1.Q0", "to": "U1.~R"}],
    }

    cases: list[tuple[str, Callable[[], Any]]] = [
        ("01_logic_dag", lambda: _wf("logic_dag", logic_ir)),
        ("02_timing_wave", lambda: _wf("timing_wave", wave_ir)),
        ("03_state_machine", lambda: _wf("state_machine", state_ir)),
        ("04_truth_table", lambda: _wf("truth_table", truth_ir)),
        ("05_kmap", lambda: _wf("kmap", kmap_ir)),
        ("06_seven_seg", lambda: _wf("seven_seg", {"digit": 5, "title": "显示5"})),
        ("07_char_curve_ttl", lambda: _wf("char_curve", {"curve": "ttl_vtc", "title": "TTL VTC"})),
        ("08_char_curve_cmos", lambda: _wf("char_curve", {"curve": "cmos_vtc", "title": "CMOS VTC"})),
        ("09_msi_mod7_gold", lambda: draw_digital_msi(load_gold_mod7())),
        ("10_msi_mod6_74160", lambda: _wf("msi_design", msi_mod6)),
        ("11_msi_ne555", lambda: _wf("msi_design", msi_555)),
        ("12_msi_ad7520", lambda: _wf("msi_design", msi_dac)),
        ("13_msi_cc4069", lambda: _wf("msi_design", msi_cmos)),
        ("14_msi_74151_mux", lambda: _wf("msi_design", msi_mux)),
        # expect_fail
        ("15_msi_bad_detect_expect_fail", lambda: _wf("msi_design", msi_bad_detect)),
    ]
    return cases


def main() -> int:
    cases = build_cases()
    results: list[dict[str, Any]] = []
    expect_fail = {"15_msi_bad_detect_expect_fail"}

    print(f"OUT={OUT}")
    print(f"cases={len(cases)}")
    for name, fn in cases:
        print(f"\n=== {name} ===")
        row = _case(name, fn)
        # 期望失败的用例：ok 取反记为 pass
        if name in expect_fail:
            row["expect_fail"] = True
            row["pass"] = not row["ok"]
            if row["pass"]:
                row["note"] = "correctly rejected"
            else:
                row["note"] = "SHOULD have failed but succeeded"
        else:
            row["expect_fail"] = False
            row["pass"] = bool(row["ok"])
        results.append(row)
        status = "PASS" if row["pass"] else "FAIL"
        print(f"{status} ok={row['ok']} engine={row.get('engine')} err={row.get('error')}")
        if row.get("artifact_url"):
            print(f"  url={row['artifact_url']}")
        if row.get("svg_path"):
            print(f"  svg={row['svg_path']}")

    passed = sum(1 for r in results if r["pass"])
    failed = [r["name"] for r in results if not r["pass"]]
    summary = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "total": len(results),
        "passed": passed,
        "failed": len(failed),
        "failed_names": failed,
        "results": results,
    }
    report_path = OUT / "report.json"
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # markdown 摘要
    lines = [
        f"# 画图全线冒烟报告",
        f"",
        f"- 时间：{summary['time']}",
        f"- 合计：{passed}/{len(results)} 通过",
        f"",
        f"| 用例 | 结果 | 引擎 | 耗时s | 说明 |",
        f"|------|------|------|-------|------|",
    ]
    for r in results:
        mark = "OK" if r["pass"] else "FAIL"
        err = (r.get("error") or r.get("note") or "")[:80].replace("|", "/")
        lines.append(
            f"| {r['name']} | {mark} | {r.get('engine') or '-'} | {r.get('elapsed_s')} | {err} |"
        )
    md_path = OUT / "report.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n==== SUMMARY {passed}/{len(results)} ====")
    print(f"report: {report_path}")
    print(f"md: {md_path}")
    if failed:
        print("FAILED:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

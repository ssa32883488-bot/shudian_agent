# -*- coding: utf-8 -*-
"""各图类出图 runner。"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from app.tools.gateway import ToolResult, wrap_err, wrap_ok

logger = logging.getLogger(__name__)

def _candidate_roots() -> list[Path]:
    """向上收集可能的仓库 / 包根。"""
    here = Path(__file__).resolve()
    roots: list[Path] = []
    seen: set[Path] = set()
    for depth in range(2, 8):
        if depth >= len(here.parents):
            break
        root = here.parents[depth].resolve()
        if root in seen:
            continue
        seen.add(root)
        roots.append(root)
    return roots


def _find_workbench(name: str) -> Path:
    """定位 netlist/schematex workbench。

    顺序：`DRAW_RUNTIME_ROOT` → `…/runtime/{name}` → `/app/runtime` →
    同级正式名 → `_archive/{name}`（本机兼容）。
    """
    candidates: list[Path] = []
    env = (os.environ.get("DRAW_RUNTIME_ROOT") or os.environ.get("WORKBENCH_ROOT") or "").strip()
    if env:
        candidates.append(Path(env) / name)
    candidates.append(Path("/app/runtime") / name)
    for root in _candidate_roots():
        candidates.extend(
            (
                root / "runtime" / name,
                root / name,
                root / "_archive" / name,
            )
        )
    seen: set[Path] = set()
    for cand in candidates:
        try:
            resolved = cand.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_dir() and (resolved / "scripts").is_dir():
            return resolved
    # 回退路径仅用于报错信息
    if env:
        return Path(env) / name
    roots = _candidate_roots()
    return (roots[0] / "runtime" / name) if roots else Path("runtime") / name


_NETLIST = _find_workbench("netlist_workbench")
_SCHEMATEX = _find_workbench("schematex_workbench")
logger.info("draw runners netlist=%s schematex=%s", _NETLIST, _SCHEMATEX)


def _node_bin() -> str:
    return os.environ.get("NODE_BIN") or "node"


def _run_node_script(script: Path, ir: dict[str, Any], timeout: int = 60) -> ToolResult:
    if not script.is_file():
        return wrap_err(f"缺少渲染脚本：{script}", tier="W", engine="draw_workflow")
    with tempfile.TemporaryDirectory(prefix="draw_wf_") as td:
        ir_path = Path(td) / "ir.json"
        out_path = Path(td) / "out.svg"
        ir_path.write_text(json.dumps(ir, ensure_ascii=False), encoding="utf-8")
        try:
            proc = subprocess.run(
                [_node_bin(), str(script), str(ir_path), str(out_path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                cwd=str(script.parent.parent),
            )
        except FileNotFoundError:
            return wrap_err("未找到 node，无法渲染", tier="W", engine="draw_workflow")
        except subprocess.TimeoutExpired:
            return wrap_err("渲染超时", tier="W", engine="draw_workflow")
        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "render failed").strip()
            return wrap_err(err[:800], tier="W", engine="draw_workflow")
        if not out_path.is_file():
            return wrap_err("渲染未写出 SVG", tier="W", engine="draw_workflow")
        svg = out_path.read_text(encoding="utf-8")
        return wrap_ok(
            svg=svg,
            tier="W",
            engine=script.stem,
            prefix="wf",
            meta={"runner": script.stem},
        )


def run_logic_netlist(data: dict[str, Any]) -> ToolResult:
    script = _NETLIST / "scripts" / "render_ir.mjs"
    res = _run_node_script(script, data)
    if res.ok:
        res.meta["kind"] = "logic_dag"
        res.engine = "netlistsvg"
    return res


def run_wave(data: dict[str, Any]) -> ToolResult:
    script = _SCHEMATEX / "scripts" / "render_wave_ir.mjs"
    res = _run_node_script(script, data)
    if res.ok:
        res.meta["kind"] = "timing_wave"
        res.engine = "wave_ir_to_svg"
    return res


def run_state(data: dict[str, Any]) -> ToolResult:
    script = _SCHEMATEX / "scripts" / "render_state_ir.mjs"
    res = _run_node_script(script, data)
    if res.ok:
        res.meta["kind"] = "state_machine"
        res.engine = "state_ir_to_svg"
    return res


def run_tier_b(kind: str, data: dict[str, Any]) -> ToolResult:
    if kind == "truth_table":
        from app.tools.draw.truth_and_misc import draw_truth_table

        return draw_truth_table(
            inputs=list(data["inputs"]),
            outputs=list(data["outputs"]),
            rows=list(data["rows"]),
            title=str(data.get("title") or "真值表"),
        )
    if kind == "kmap":
        from app.tools.draw.kmap import draw_kmap

        return draw_kmap(
            minterms=list(data["minterms"]),
            var_count=int(data.get("var_count") or 4),
            dont_cares=list(data.get("dont_cares") or []),
            auto_group=bool(data.get("auto_group", True)),
            title=str(data.get("title") or "卡诺图化简"),
        )
    if kind == "seven_seg":
        from app.tools.draw.truth_and_misc import draw_seven_seg

        return draw_seven_seg(
            digit=int(data.get("digit", 8)),
            title=str(data.get("title") or "七段数码管"),
        )
    if kind == "char_curve":
        from app.tools.draw.char_curve_mpl import draw_char_curve

        return draw_char_curve(
            curve=str(data.get("curve") or "ttl_vtc"),
            title=str(data.get("title") or "特性曲线"),
        )
    return wrap_err(f"tier_b 不支持 kind={kind}", tier="B", engine="draw_workflow")


def run_digital_dig(data: dict[str, Any]) -> ToolResult:
    from app.tools.draw.digital_dig import draw_digital_msi

    brief = str(data.get("_brief") or data.get("brief") or "")
    return draw_digital_msi(data, brief=brief)


def dispatch_runner(kind: str, data: dict[str, Any]) -> ToolResult:
    from app.tools.draw_workflow.catalog import get_kind

    spec = get_kind(kind)
    if not spec:
        return wrap_err(f"未知 kind={kind}", tier="W", engine="draw_workflow")
    if spec.runner == "logic_netlist":
        return run_logic_netlist(data)
    if spec.runner == "wave":
        return run_wave(data)
    if spec.runner == "state":
        return run_state(data)
    if spec.runner == "tier_b":
        return run_tier_b(kind, data)
    if spec.runner == "digital_dig":
        return run_digital_dig(data)
    return wrap_err(f"无 runner：{spec.runner}", tier="W", engine="draw_workflow")

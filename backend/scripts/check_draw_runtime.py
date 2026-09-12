# -*- coding: utf-8 -*-
"""绘图运行时自检：本机 / 服务器 / 第三方部署前先跑。

用法：
  cd shudian_agent/backend
  python -m scripts.check_draw_runtime

退出码：0=宣称支持的图类依赖齐全；1=有缺失。
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

# 保证可直接 python -m scripts.check_draw_runtime
_BACKEND = Path(__file__).resolve().parents[1]
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))


def _ok(msg: str) -> None:
    print(f"  OK  {msg}")


def _fail(msg: str) -> None:
    print(f" FAIL {msg}")


def _find_workbench(name: str) -> Path | None:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    env = (os.environ.get("DRAW_RUNTIME_ROOT") or os.environ.get("WORKBENCH_ROOT") or "").strip()
    if env:
        candidates.append(Path(env) / name)
    candidates.append(Path("/app/runtime") / name)
    seen: set[Path] = set()
    for depth in range(2, 8):
        if depth >= len(here.parents):
            break
        root = here.parents[depth].resolve()
        if root in seen:
            continue
        seen.add(root)
        candidates.extend(
            (
                root / "runtime" / name,
                root / name,
                root / "_archive" / name,
            )
        )
    for cand in candidates:
        if cand.is_dir() and (cand / "scripts").is_dir():
            return cand
    return None


def _find_java() -> str | None:
    env = os.environ.get("JAVA_HOME")
    if env:
        for rel in ("bin/java.exe", "bin/java"):
            cand = Path(env) / rel
            if cand.is_file():
                return str(cand)
    return shutil.which("java")


def _find_digital_jar() -> Path | None:
    env = os.environ.get("DIGITAL_JAR") or os.environ.get("DIGITAL_HOME")
    if env:
        p = Path(env)
        if p.is_file() and p.suffix.lower() == ".jar":
            return p
        jar = p / "Digital.jar"
        if jar.is_file():
            return jar
    vendor = (
        _BACKEND
        / "app"
        / "tools"
        / "draw"
        / "digital_dig"
        / "vendor"
        / "Digital.jar"
    )
    if vendor.is_file():
        return vendor
    here = Path(__file__).resolve()
    for depth in range(3, 8):
        if depth >= len(here.parents):
            break
        root = here.parents[depth]
        for cand in (
            root / "digital-circuit-poc" / "digital" / "Digital.jar",
            root.parent / "digital-circuit-poc" / "digital" / "Digital.jar",
        ):
            if cand.is_file():
                return cand
    return None


def main() -> int:
    print("=== draw runtime check ===\n")
    missing: list[str] = []
    report: dict[str, object] = {"kinds": {}, "env": {}}

    # —— Tier-B（纯 Python）——
    print("[Tier-B] truth_table / kmap / seven_seg / char_curve")
    try:
        import matplotlib  # noqa: F401

        _ok(f"matplotlib {matplotlib.__version__}")
        report["kinds"]["tier_b"] = "ok"
    except Exception as e:  # noqa: BLE001
        _fail(f"matplotlib: {e}")
        missing.append("matplotlib")
        report["kinds"]["tier_b"] = "fail"

    # —— Node workbench ——
    print("\n[Node] logic_dag / timing_wave / state_machine")
    node = os.environ.get("NODE_BIN") or shutil.which("node")
    report["env"]["NODE_BIN"] = node
    if node:
        _ok(f"node → {node}")
    else:
        _fail("未找到 node（设 NODE_BIN 或装 Node.js）")
        missing.append("node")

    for name, kinds in (
        ("netlist_workbench", "logic_dag"),
        ("schematex_workbench", "timing_wave+state_machine"),
    ):
        wb = _find_workbench(name)
        if wb:
            # 必须有 npm 依赖，否则 logic_dag / wave 渲染会挂
            dep_ok = True
            if name == "netlist_workbench":
                dep = wb / "node_modules" / "netlistsvg" / "package.json"
                if not dep.is_file():
                    _fail(f"{name} 缺少 node_modules/netlistsvg（请在该目录执行 npm ci）")
                    missing.append(f"{name}:npm")
                    dep_ok = False
            elif name == "schematex_workbench":
                # schematex 至少应有 node_modules
                if not (wb / "node_modules").is_dir():
                    _fail(f"{name} 缺少 node_modules（请在该目录执行 npm ci）")
                    missing.append(f"{name}:npm")
                    dep_ok = False
            if dep_ok:
                _ok(f"{name} → {wb}  ({kinds})")
                report["kinds"][kinds] = str(wb)
            else:
                report["kinds"][kinds] = "missing_npm"
        else:
            _fail(f"未找到 {name}（runtime/ 或 DRAW_RUNTIME_ROOT 或 _archive/）")
            missing.append(name)
            report["kinds"][kinds] = "missing"

    # —— MSI Digital ——
    print("\n[MSI] msi_design")
    java = _find_java()
    report["env"]["java"] = java
    if java:
        _ok(f"java → {java}")
    else:
        _fail("未找到 Java 17+（设 JAVA_HOME 或 PATH）")
        missing.append("java")

    jar = _find_digital_jar()
    report["env"]["DIGITAL_JAR"] = str(jar) if jar else None
    if jar:
        _ok(f"Digital.jar → {jar}")
        report["kinds"]["msi_design"] = "ok"
    else:
        _fail(
            "未找到 Digital.jar（设 DIGITAL_JAR，或放到 "
            "app/tools/draw/digital_dig/vendor/Digital.jar）"
        )
        missing.append("Digital.jar")
        report["kinds"]["msi_design"] = "fail"

    # —— Agent 配额 ——
    print("\n[Agent caps]")
    for key, default in (
        ("AGENT_MAX_DRAW_CALLS", "3"),
        ("AGENT_MAX_ITERATIONS", "8"),
    ):
        val = os.environ.get(key, default)
        _ok(f"{key}={val}")
        report["env"][key] = val

    print("\n=== summary ===")
    if missing:
        print(f"MISSING ({len(missing)}): {', '.join(missing)}")
        print("详见 docs/定稿-绘图子系统.md §5")
        out = _BACKEND / "data" / "artifacts" / "draw_runtime_check.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"report → {out}")
        return 1

    print("All required draw runtimes present.")
    out = _BACKEND / "data" / "artifacts" / "draw_runtime_check.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"report → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""知识图谱 JSON → backend/data/knowledge_graph.json（供路径 API）。

用法:
  python data/ingest_graph.py
  python data/ingest_graph.py --input data/kg/path_graph.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "data" / "kg" / "path_graph.json"
FALLBACK_IN = ROOT / "data" / "sample" / "knowledge_graph.json"
DEFAULT_OUT = ROOT / "backend" / "data" / "knowledge_graph.json"


def _to_path_format(data: dict) -> dict:
    """完整 v0.2 图 → path 兼容格式。"""
    if "path_compat" in data and isinstance(data["path_compat"], dict):
        return data["path_compat"]
    nodes = data.get("nodes")
    edges = data.get("edges") or []
    if isinstance(nodes, dict) and nodes and isinstance(next(iter(nodes.values()), None), dict):
        if isinstance(edges, dict):
            edges = edges.get("PRE_REQUISITE_OF") or []
        return {"nodes": nodes, "edges": edges}
    return data


def ingest(input_path: Path, output_path: Path) -> None:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    payload = _to_path_format(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    n_nodes = len(payload.get("nodes") or {})
    n_edges = len(payload.get("edges") or [])
    print(f"图谱已写入 {output_path}（概念 {n_nodes}，前置边 {n_edges}）from {input_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="")
    parser.add_argument("--output", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    if args.input:
        src = Path(args.input)
    elif DEFAULT_IN.exists():
        src = DEFAULT_IN
    else:
        src = FALLBACK_IN
    if not src.exists():
        sample = {
            "nodes": {"逻辑代数": {"chapter": "第2章", "id": "de_0201"}},
            "edges": [],
        }
        src = FALLBACK_IN
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
    ingest(src, Path(args.output))


if __name__ == "__main__":
    main()

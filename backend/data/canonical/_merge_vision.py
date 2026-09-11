# -*- coding: utf-8 -*-
"""Merge partial vision description dicts into batch JSON files."""
import json
from pathlib import Path

base = Path(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical")

def write_batches(ch, ranges):
    jobs = json.loads((base / ch / "vision_jobs.json").read_text(encoding="utf-8"))
    partial_path = base / ch / "_vision_partial.json"
    data = json.loads(partial_path.read_text(encoding="utf-8")) if partial_path.exists() else {}
    for name, lo, hi in ranges:
        out = {}
        missing = []
        for i in range(lo, hi + 1):
            key = jobs[i]["key"]
            if key not in data:
                missing.append(i)
            else:
                out[key] = data[key]
        dest = base / ch / name
        dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{ch}/{name}: {len(out)} entries, missing={missing}")

if __name__ == "__main__":
    write_batches("ch07", [
        ("vision_batch_01.json", 0, 59),
        ("vision_batch_02.json", 60, 118),
    ])
    write_batches("ch08", [
        ("vision_batch_01.json", 0, 39),
        ("vision_batch_02.json", 40, 73),
    ])

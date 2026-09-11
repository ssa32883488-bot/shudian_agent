# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical")
for ch in ["ch07", "ch08"]:
    jobs = json.loads((base / ch / "vision_jobs.json").read_text(encoding="utf-8"))
    lines = [f"count={len(jobs)}"]
    for i, x in enumerate(jobs):
        lines.append(f"{i}\t{x['key']}\t{x['caption']}\t{x['path']}")
    out = base / ch / "_jobs_index.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(ch, len(jobs), "->", out)

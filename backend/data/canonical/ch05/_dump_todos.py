# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(__file__).parent
out = []
for f in sorted(base.glob("vision_todo_*.json")):
    jobs = json.loads(f.read_text(encoding="utf-8"))
    out.append(f"==== {f.name} ({len(jobs)})")
    for i, j in enumerate(jobs):
        exists = Path(j["path"]).exists()
        cap = j.get("caption") or "(empty)"
        out.append(f"{i:02d}\texists={exists}\t{j['figure_id']}\t{cap}\t{j['path']}")

(base / "_todo_dump.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out), "lines")

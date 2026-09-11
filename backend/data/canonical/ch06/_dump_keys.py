# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(__file__).resolve().parent
d = json.load(open(p / "_missing_now.json", encoding="utf-8"))
with open(p / "_keys_tmp.txt", "w", encoding="utf-8") as f:
    for i, x in enumerate(d):
        hash16 = x["key"].split("|")[1][:16]
        f.write(f"{i}\t{x['figure_id']}\t{hash16}\n")
print("missing", len(d))

t = json.load(open(p / "vision_todo_0120_0139.json", encoding="utf-8"))
with open(p / "_todo0120_tmp.txt", "w", encoding="utf-8") as f:
    for i, x in enumerate(t):
        name = Path(x["path"]).name[:24]
        f.write(f"{i}\t{x['figure_id']}\t{name}\n")
print("todo0120", len(t))

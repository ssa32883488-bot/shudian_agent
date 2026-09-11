# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(__file__).resolve().parent
d = json.load(open(base / "_uncovered.json", encoding="utf-8"))
lines = []
for i, x in enumerate(d):
    it = x["item"]
    lines.append(f"{i:02d}\t{x['todo']}\t{it['key']}\t{it.get('caption','')}\t{it.get('path','')}")
out = base / "_uncovered_list.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {len(lines)} lines to {out}")
# also dump keys only for batch grouping
by = {}
for x in d:
    by.setdefault(x["todo"], []).append(x["item"])
for t, items in by.items():
    print(t, len(items), "first", items[0]["key"], "last", items[-1]["key"])

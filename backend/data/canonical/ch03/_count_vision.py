# -*- coding: utf-8 -*-
import json
from pathlib import Path
p = Path(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical\ch03\vision_batch_02.json")
d = json.loads(p.read_text(encoding="utf-8"))
bad = []
for k, v in d.items():
    n = len(v)
    if not (40 <= n <= 90):
        bad.append((n, k.split("|")[0], v))
    print(f"{n:3d} {'OK' if 40<=n<=90 else 'BAD'} {k.split('|')[0]}")
print("count", len(d), "bad", len(bad))

# -*- coding: utf-8 -*-
import json
jobs = json.load(open(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical\ch04\vision_jobs.json", encoding="utf-8"))
out = []
for i, j in enumerate(jobs):
    out.append({"i": i, "key": j["key"], "figure_id": j["figure_id"], "caption": j["caption"], "path": j["path"]})
with open(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical\ch04\_jobs_meta.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("wrote", len(out))

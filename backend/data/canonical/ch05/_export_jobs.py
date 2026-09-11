# -*- coding: utf-8 -*-
import json
jobs = json.load(open(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical\ch05\vision_jobs.json", encoding="utf-8"))
out = r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical\ch05\_jobs_list.txt"
with open(out, "w", encoding="utf-8") as f:
    for i, j in enumerate(jobs):
        f.write(f"{i}\t{j['key']}\t{j['caption']}\t{j['path']}\n")
print("wrote", len(jobs))

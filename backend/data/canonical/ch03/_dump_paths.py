# -*- coding: utf-8 -*-
import json
jobs = json.load(open("vision_jobs.json", encoding="utf-8"))
with open("_paths50.txt", "w", encoding="utf-8") as f:
    for i, j in enumerate(jobs[0:50]):
        f.write(f"{i}\t{j['figure_id']}\t{j['caption']}\t{j['key']}\t{j['path']}\n")
print("ok", 50)

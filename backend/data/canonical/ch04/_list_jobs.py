import json
jobs = json.load(open(r"f:\code\揭榜挂帅-单学科教育智能体\shudian_agent\backend\data\canonical\ch04\vision_jobs.json", encoding="utf-8"))
print(len(jobs))
for i, j in enumerate(jobs):
    print(f"{i}\t{j['figure_id']}\t{j['caption']}\t{j['path']}")

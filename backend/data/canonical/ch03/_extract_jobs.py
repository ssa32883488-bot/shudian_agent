import json
from pathlib import Path

jobs_path = Path(__file__).with_name("vision_jobs.json")
jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
batch = jobs[100:150]
print(len(batch))
out = []
for i, j in enumerate(batch):
    row = {
        "index": 100 + i,
        "key": j["key"],
        "figure_id": j["figure_id"],
        "caption": j["caption"],
        "path": j["path"],
    }
    out.append(row)
    print(f"{row['index']}\t{row['figure_id']}\t{row['caption']}")
Path(__file__).with_name("_batch03_jobs.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)

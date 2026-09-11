#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "reports/qb_vision_fail_regression4.json").read_text(encoding="utf-8"))
fails = [x for x in d["results"] if not (x.get("verdict") or {}).get("pass")]
passes = [x for x in d["results"] if (x.get("verdict") or {}).get("pass")]
print("round4 pass", len(passes), "fail", len(fails))
print("NEW_PASS", [x.get("eid") for x in passes])
print("STILL_FAIL:")
for x in fails:
    iss = (x.get("verdict") or {}).get("issues") or []
    print("-", x.get("eid"), "|", (iss[0] if iss else "")[:100])
still = {x.get("eid") for x in fails}
recovered = set()
for p in [
    "qb_vision_fail_regression.json",
    "qb_vision_fail_regression2.json",
    "qb_vision_fail_regression3.json",
    "qb_vision_fail_regression4.json",
]:
    rr = json.loads((ROOT / "reports" / p).read_text(encoding="utf-8"))
    for x in rr["results"]:
        if (x.get("verdict") or {}).get("pass"):
            recovered.add(x.get("eid"))
recovered -= still
print("CUMULATIVE", len(recovered), "/72 =", round(len(recovered) / 72, 3), "still", len(still))
out = {
    "round4_pass": len(passes),
    "round4_fail": len(fails),
    "cumulative_recovered": len(recovered),
    "cumulative_still_fail": len(still),
    "still_fail_eids": sorted(still),
    "new_pass_eids": [x.get("eid") for x in passes],
}
(ROOT / "reports/qb_fail_regression4_summary.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)

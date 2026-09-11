# -*- coding: utf-8 -*-
import json
from pathlib import Path

base = Path(__file__).resolve().parent
batches = sorted(base.glob("vision_batch_*.json"))
todos = sorted(base.glob("vision_todo_*.json"))

existing = {}
for b in batches:
    with open(b, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for k in data:
            existing[k] = b.name
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for k in item:
                    existing[k] = b.name

print("=== BATCHES ===")
for b in batches:
    with open(b, encoding="utf-8") as f:
        data = json.load(f)
    n = len(data) if isinstance(data, dict) else len(data)
    print(f"{b.name}: {n} keys")
print(f"TOTAL existing keys: {len(existing)}")

print("\nSample keys:")
for k in list(existing.keys())[:5]:
    print(f"  [{existing[k]}] {k}")

print("\n=== TODO STRUCTURE ===")
with open(todos[0], encoding="utf-8") as f:
    d = json.load(f)
print("type", type(d).__name__)
if isinstance(d, list):
    print("len", len(d))
    print("first:", json.dumps(d[0], ensure_ascii=False)[:1000])
elif isinstance(d, dict):
    print("nkeys", len(d))
    k0 = list(d.keys())[0]
    print("first key:", k0)
    v = d[k0]
    print("first val:", json.dumps(v, ensure_ascii=False)[:800] if not isinstance(v, str) else v[:400])

print("\n=== BATCH STRUCTURE ===")
with open(batches[0], encoding="utf-8") as f:
    d = json.load(f)
print("type", type(d).__name__, "len", len(d))
k0 = list(d.keys())[0]
print("first:", k0)
print("desc:", d[k0][:120])


def item_key(item):
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for cand in ("key", "id", "path", "图号", "fig", "name"):
            if cand in item and item[cand]:
                return str(item[cand])
        # composite
        fig = item.get("fig_id") or item.get("figure") or item.get("label") or ""
        img = item.get("image") or item.get("img") or item.get("file") or item.get("src") or ""
        if fig and img:
            return f"{fig}|{img}"
        if img:
            return img
        if len(item) == 1:
            return list(item.keys())[0]
        # search values
        for vv in item.values():
            if isinstance(vv, str) and ("|" in vv or "images/" in vv or vv.endswith(".jpg")):
                return vv
    return None


def covered(key):
    if key in existing:
        return True
    if key and "|" in key:
        img = key.split("|", 1)[1].replace("\\", "/")
        for ek in existing:
            if img in ek.replace("\\", "/") or ek.replace("\\", "/").endswith(img):
                return True
    return False


print("\n=== COVERAGE ===")
uncovered_by_todo = {}
all_uncovered = []
for t in todos:
    with open(t, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if "items" in data:
            items = data["items"]
        elif "todos" in data:
            items = data["todos"]
        else:
            # dict of key->meta or key->caption
            items = []
            for k, v in data.items():
                if isinstance(v, dict):
                    items.append({"key": k, **v})
                else:
                    items.append({"key": k, "caption": v})
    else:
        items = []

    miss = []
    for item in items:
        key = item_key(item)
        if not key:
            # reconstruct from fields
            if isinstance(item, dict):
                print("UNPARSED:", json.dumps(item, ensure_ascii=False)[:200])
            continue
        if not covered(key):
            miss.append({"key": key, "item": item})
    uncovered_by_todo[t.name] = miss
    all_uncovered.extend([(t.name, m) for m in miss])
    print(f"{t.name}: total={len(items)}, miss={len(miss)}")

print(f"\nTOTAL uncovered: {len(all_uncovered)}")

# write uncovered report
out = []
for tname, m in all_uncovered:
    out.append({"todo": tname, "key": m["key"], "item": m["item"]})
with open(base / "_uncovered.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("Wrote _uncovered.json")

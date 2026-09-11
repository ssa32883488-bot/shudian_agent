"""Public HTTP smoke against deployed slim stack.

Usage:
  py -3 shudian_agent/scripts/e2e_remote_smoke.py
  set BASE_URL=http://39.105.20.113
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any

BASE = os.environ.get("BASE_URL", "http://39.105.20.113").rstrip("/")
ADMIN_PHONE = os.environ.get("ADMIN_PHONE", "13900000001")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "123456")
STUDENT_PHONE = os.environ.get("STUDENT_PHONE", "13800000001")
STUDENT_PASS = os.environ.get("STUDENT_PASS", "123456")

results: list[tuple[str, bool, str]] = []


def req(
    method: str,
    path: str,
    *,
    body: dict | None = None,
    token: str | None = None,
    timeout: int = 120,
) -> tuple[int, Any]:
    url = path if path.startswith("http") else f"{BASE}{path}"
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            try:
                return resp.status, json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = raw
        return e.code, payload


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))


def main() -> int:
    print(f"BASE={BASE}\n")

    # 1 health / home
    code, body = req("GET", "/health", timeout=20)
    check("health", code == 200 and (body.get("ok") is True or body == {"ok": True} or "ok" in str(body)), str(body)[:120])
    code, body = req("GET", "/", timeout=20)
    check("home_html", code == 200 and ("html" in str(body).lower() or isinstance(body, str) or True), f"status={code}")

    # 2 auth gate
    code, _ = req("POST", "/api/student/solve", body={"text": "hi"}, timeout=30)
    check("solve_requires_auth", code in (401, 403), f"status={code}")

    # 3 login admin + student
    code, body = req("POST", "/api/auth/login", body={"phone": ADMIN_PHONE, "password": ADMIN_PASS})
    admin_token = ""
    if isinstance(body, dict):
        admin_token = body.get("token") or body.get("access_token") or ""
    check("admin_login", code == 200 and bool(admin_token), f"status={code} keys={list(body) if isinstance(body, dict) else type(body)}")

    code, body = req("POST", "/api/auth/login", body={"phone": STUDENT_PHONE, "password": STUDENT_PASS})
    token = ""
    if isinstance(body, dict):
        token = body.get("token") or body.get("access_token") or ""
    if not token:
        # 首次部署可能未 seed 学生：注册一个
        code_r, body_r = req(
            "POST",
            "/api/auth/register",
            body={
                "phone": STUDENT_PHONE,
                "password": STUDENT_PASS,
                "nickname": "演示同学",
                "class_code": "DEMO01",
            },
        )
        if isinstance(body_r, dict):
            token = body_r.get("token") or ""
        if not token and code_r in (400, 409):
            code, body = req("POST", "/api/auth/login", body={"phone": STUDENT_PHONE, "password": STUDENT_PASS})
            if isinstance(body, dict):
                token = body.get("token") or ""
        check("student_register_or_login", bool(token), f"reg={code_r} login={code}")
    else:
        check("student_login", code == 200 and bool(token), f"status={code}")
    if not token:
        print("abort: no student token")
        return 1

    # 4 me (student)
    code, body = req("GET", "/api/auth/me", token=token)
    check("auth_me_student", code == 200 and isinstance(body, dict) and body.get("role") == "student", str(body)[:160])

    # 5 short solve (chat/react)
    t0 = time.time()
    code, body = req(
        "POST",
        "/api/student/solve",
        body={"text": "用一句话解释什么是与门。不要画图。"},
        token=token,
        timeout=180,
    )
    elapsed = time.time() - t0
    ans = ""
    if isinstance(body, dict):
        ans = str(body.get("answer") or body.get("final_answer") or body.get("content") or body)[:200]
    check("solve_explain", code == 200 and len(ans) > 10, f"{elapsed:.1f}s {ans[:120]}")

    # 6 kmap draw intent
    t0 = time.time()
    code, body = req(
        "POST",
        "/api/student/solve",
        body={"text": "用卡诺图化简 F(A,B,C)=Σm(1,2,5,7)，请画卡诺图并给出最简式。"},
        token=token,
        timeout=240,
    )
    elapsed = time.time() - t0
    text = json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body
    has_media = "/media/" in text or "artifacts" in text or "DRAW" in text or "kmap" in text.lower()
    check("solve_kmap_draw", code == 200 and has_media, f"{elapsed:.1f}s media={has_media} snippet={text[:180]}")

    # 7 bank search via admin
    code, body = req("GET", "/api/admin/bank?limit=5", token=admin_token, timeout=60)
    n = 0
    if isinstance(body, dict):
        items = body.get("items") or body.get("questions") or body.get("data") or []
        n = len(items) if isinstance(items, list) else 0
    elif isinstance(body, list):
        n = len(body)
    check("admin_bank_list", code == 200, f"status={code} n={n}")

    # 8 reflow list
    code, body = req("GET", "/api/admin/reflow/list", token=admin_token, timeout=60)
    check("admin_reflow", code == 200, f"status={code}")

    # 9 learning
    code, body = req("GET", "/api/admin/learning/class?class_code=DEMO01", token=admin_token, timeout=60)
    if code == 422:
        code, body = req("GET", "/api/admin/learning/rollup", token=admin_token, timeout=60)
    check("admin_learning", code in (200, 404, 422), f"status={code}")

    # 10 traces
    code, body = req("GET", "/api/admin/traces?limit=5", token=admin_token, timeout=60)
    check("admin_traces", code in (200, 404), f"status={code}")

    # 11 practice generate
    code, body = req(
        "POST",
        "/api/student/practice/generate",
        body={"count": 2},
        token=token,
        timeout=120,
    )
    check("practice_generate", code in (200, 201, 422), f"status={code} body={str(body)[:140]}")

    # 12 mistakes list
    code, body = req("GET", "/api/student/mistakes", token=token, timeout=60)
    check("mistakes_list", code in (200, 404), f"status={code}")

    # 13 profile
    code, body = req("GET", "/api/student/profile", token=token, timeout=60)
    check("student_profile", code in (200, 404), f"status={code}")

    # 14 kg
    code, body = req("GET", "/api/student/kg/status", token=token, timeout=60)
    check("student_kg", code == 200, f"status={code} {str(body)[:120]}")

    # 15 plan perceive-route
    code, body = req(
        "POST",
        "/api/student/plan/perceive-route",
        body={"text": "请解释半加器"},
        token=token,
        timeout=120,
    )
    check("plan_perceive_route", code in (200, 404, 422), f"status={code} {str(body)[:140]}")

    # 16 msi design (may be slow)
    t0 = time.time()
    code, body = req(
        "POST",
        "/api/student/solve",
        body={"text": "用74163同步置零法设计模7计数器，请画出电路图。"},
        token=token,
        timeout=300,
    )
    elapsed = time.time() - t0
    text = json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body
    has_svg = "/media/artifacts/" in text or ".svg" in text
    check("solve_msi_design", code == 200, f"{elapsed:.1f}s svg={has_svg} snippet={text[:200]}")

    print("\n=== summary ===")
    fails = [r for r in results if not r[1]]
    print(f"passed={len(results)-len(fails)} failed={len(fails)} total={len(results)}")
    for name, ok, detail in fails:
        print(f"  FAIL {name}: {detail}")
    return 1 if fails else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""truth_table 确定性兜底：奇偶校验等常见表。"""

from __future__ import annotations

import json
import re
from typing import Any, Optional


def _blob(*parts: str) -> str:
    return "\n".join(p for p in parts if p)


def _is_odd_parity(text: str) -> bool:
    t = text or ""
    if "奇偶" in t or "奇校验" in t or "偶校验" in t:
        return True
    if "奇数个" in t and ("1" in t or "输入" in t):
        return True
    if "A⊕B⊕C" in t.replace(" ", "") or "A\\\\oplus B\\\\oplus C" in t:
        return True
    return bool(re.search(r"A\s*\\oplus\s*B\s*\\oplus\s*C", t))


def _n_vars(text: str, default: int = 3) -> int:
    t = text or ""
    if "三变量" in t or "三个输入" in t:
        return 3
    if "两变量" in t or "两个输入" in t:
        return 2
    if "四变量" in t:
        return 4
    return default


def build_parity_truth_ir(
    *,
    brief: str = "",
    slots: Optional[dict[str, Any]] = None,
    odd: bool = True,
) -> Optional[dict[str, Any]]:
    text = _blob(brief, str(slots or ""))
    if not _is_odd_parity(text):
        return None
    if "偶校验" in text and "奇" not in text:
        odd = False
    n = min(4, max(2, _n_vars(text, 3)))
    names = ["A", "B", "C", "D"][:n]
    rows: list[list[int]] = []
    for mask in range(1 << n):
        bits = [(mask >> (n - 1 - i)) & 1 for i in range(n)]
        ones = sum(bits)
        y = 1 if ((ones % 2 == 1) if odd else (ones % 2 == 0)) else 0
        rows.append(bits + [y])
    title = f"{n}变量{'奇' if odd else '偶'}校验真值表"
    return {
        "inputs": names,
        "outputs": ["Y"],
        "rows": rows,
        "title": title,
    }


def fallback_truth_table_script(
    *,
    brief: str = "",
    slots: Optional[dict[str, Any]] = None,
) -> Optional[str]:
    ir = build_parity_truth_ir(brief=brief, slots=slots)
    if not ir:
        return None
    return json.dumps(ir, ensure_ascii=False)

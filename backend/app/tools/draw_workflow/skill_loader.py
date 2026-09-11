# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

_SKILLS_DIR = Path(__file__).resolve().parent / "skills"


def load_skill(filename: str) -> str:
    path = _SKILLS_DIR / filename
    if not path.is_file():
        return f"（缺少 skill 文件：{filename}）"
    return path.read_text(encoding="utf-8")

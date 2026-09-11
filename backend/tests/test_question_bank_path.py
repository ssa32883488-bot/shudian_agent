# -*- coding: utf-8 -*-
"""题库路径关键断言：阈值、瀑布校验、质检不放行、禁用同步、预检索直出。"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from app.graphs.solve_graph import node_bank_prefetch, route_after_bank
from app.services.question_bank import _near_exact, sync_question_to_chroma
from app.tools.retrieve import format_bank_hit_answer, tool_search_question_bank


def test_near_exact_only_for_originalish():
    stem = "试比较组合逻辑电路与时序逻辑电路的主要特点并举例说明"
    assert _near_exact(stem, stem)
    assert _near_exact(stem, stem + "。补充说明")
    assert not _near_exact("完全无关的一句话用来测试召回", stem)


def test_format_bank_hit_answer_minimal():
    text = format_bank_hit_answer(
        {"answer": "答：组合无存储，时序有状态。", "analysis": "见教材第5章"}
    )
    assert "题库原题解答" in text
    assert "组合无存储" in text
    assert "见教材第5章" in text


def test_tool_search_waterfall_skips_bad_first(monkeypatch: pytest.MonkeyPatch):
    rows = [
        {
            "question_id": 1,
            "content": "题A",
            "answer": "答A",
            "analysis": "",
            "knowledge_tags": None,
            "source": None,
            "score": 0.99,
        },
        {
            "question_id": 2,
            "content": "题B",
            "answer": "答B",
            "analysis": "",
            "knowledge_tags": {"tags": ["时序"]},
            "source": "课本",
            "score": 0.97,
        },
    ]
    monkeypatch.setattr(
        "app.tools.retrieve.search_question_bank", lambda *_a, **_k: rows
    )
    monkeypatch.setattr(
        "app.tools.retrieve.get_settings",
        lambda: SimpleNamespace(hit_score_threshold=0.95),
    )

    calls: list[str] = []

    async def fake_validate(q, content, answer, *, retrieval_score):
        calls.append(content)
        if content == "题A":
            return {"usable": False, "reason": "非同题", "score": 0.2}
        return {"usable": True, "reason": "同题", "score": 0.9}

    monkeypatch.setattr("app.tools.retrieve._validate_bank_hit", fake_validate)
    monkeypatch.setattr(
        "app.services.embedding.get_embedding_service",
        lambda: SimpleNamespace(mode="test"),
    )
    monkeypatch.setattr(
        "app.services.rerank.get_rerank_service",
        lambda: SimpleNamespace(mode="test"),
    )

    db = MagicMock()
    out = tool_search_question_bank(db, "用户题干", top_k=3)
    assert out["hit"] is True
    assert out["question_id"] == 2
    assert out["answer"] == "答B"
    assert calls == ["题A", "题B"]


def test_tool_search_rejects_below_threshold(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "app.tools.retrieve.search_question_bank",
        lambda *_a, **_k: [
            {
                "question_id": 9,
                "content": "x",
                "answer": "y",
                "analysis": "",
                "score": 0.61,
            }
        ],
    )
    monkeypatch.setattr(
        "app.tools.retrieve.get_settings",
        lambda: SimpleNamespace(hit_score_threshold=0.95),
    )
    monkeypatch.setattr(
        "app.services.embedding.get_embedding_service",
        lambda: SimpleNamespace(mode="test"),
    )
    monkeypatch.setattr(
        "app.services.rerank.get_rerank_service",
        lambda: SimpleNamespace(mode="test"),
    )
    out = tool_search_question_bank(MagicMock(), "随便问问", top_k=3)
    assert out["hit"] is False
    assert out["message"] == "无"
    assert "0.95" in (out.get("reason") or "")


def test_sync_disabled_deletes_chroma():
    row = SimpleNamespace(id=42, content="题干", source="t", status="disabled")
    store = MagicMock()
    with patch("app.services.question_bank.get_chroma_store", return_value=store):
        sync_question_to_chroma(row)  # type: ignore[arg-type]
    store.delete_question.assert_called_once_with(42)
    store.upsert_question.assert_not_called()


def test_sync_active_upserts_chroma():
    row = SimpleNamespace(id=7, content="题干", source="课本", status="active")
    store = MagicMock()
    with patch("app.services.question_bank.get_chroma_store", return_value=store):
        sync_question_to_chroma(row)  # type: ignore[arg-type]
    store.upsert_question.assert_called_once()
    kwargs = store.upsert_question.call_args.kwargs
    assert kwargs["question_id"] == 7
    assert kwargs["metadata"]["status"] == "active"


def test_bank_prefetch_hit_skips_react(monkeypatch: pytest.MonkeyPatch):
    hit: dict[str, Any] = {
        "hit": True,
        "question_id": 5,
        "score": 0.99,
        "answer": "权威答案正文",
        "analysis": "",
        "match_reason": "同题",
        "content": "原题",
    }
    monkeypatch.setattr(
        "app.tools.retrieve.tool_search_question_bank",
        lambda *_a, **_k: hit,
    )
    state = {
        "question_text": "一道数电题",
        "db": MagicMock(),
        "decision_plan": {"intent": "solve", "summary": "解题", "steps": []},
        "intent": "solve",
        "trace": [],
    }
    out = node_bank_prefetch(state)  # type: ignore[arg-type]
    assert out["hit"] is True
    assert out["trust_level"] == "authoritative"
    assert "权威答案正文" in (out.get("answer") or "")
    assert route_after_bank({**state, **out}) == "bank_done"  # type: ignore[arg-type]


def test_bank_prefetch_miss_goes_kg(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "app.tools.retrieve.tool_search_question_bank",
        lambda *_a, **_k: {"hit": False, "message": "无", "reason": "未达阈值"},
    )
    state = {
        "question_text": "新题",
        "db": MagicMock(),
        "decision_plan": {"intent": "solve", "summary": "解题", "steps": []},
        "intent": "solve",
        "trace": [],
    }
    out = node_bank_prefetch(state)  # type: ignore[arg-type]
    assert out["hit"] is False
    assert "不必再调 search_question_bank" in (out.get("bank_prefetch_note") or "")
    assert route_after_bank({**state, **out}) == "kg_ground"  # type: ignore[arg-type]


def test_bank_prefetch_skips_non_solve():
    state = {
        "question_text": "你好",
        "db": MagicMock(),
        "decision_plan": {"intent": "chat", "summary": "寒暄", "steps": []},
        "intent": "chat",
        "trace": [],
    }
    out = node_bank_prefetch(state)  # type: ignore[arg-type]
    assert out["hit"] is False
    assert "跳过题库预检索" in (out.get("trace") or [])[-1]

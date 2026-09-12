# -*- coding: utf-8 -*-
from app.services.provenance import build_solve_provenance


def test_provenance_bank_hit():
    p = build_solve_provenance(
        {
            "hit": True,
            "hit_question_id": 7,
            "hit_score": 0.99,
            "intent": "solve",
            "tool_trace": ["search_question_bank:hit:7"],
            "match_reason": "同题校验通过",
        }
    )
    assert p["origin"] == "question_bank"
    assert "题库" in p["summary"] or "原题" in p["summary"]
    assert p["bank"]["id"] == 7


def test_provenance_ai_with_textbook_and_kg():
    p = build_solve_provenance(
        {
            "hit": False,
            "intent": "solve",
            "tool_trace": [
                "search_question_bank:miss",
                "call:retrieve_multi_rerank args={}",
                "result:retrieve_multi_rerank",
            ],
            "kg_context": {
                "keywords": ["MUX"],
                "chapters": ["第3章"],
                "related_problems": [{"problem_id": "题3.1"}],
            },
            "textbook_hits": [{"chapter": "第3章"}],
        }
    )
    assert p["origin"] == "ai_solve"
    assert "教材" in p["summary"]
    assert "教材知识库检索" in p["tools"]
    assert p["textbook"]["chapters"] == ["第3章"]
    assert "MUX" in (p["knowledge_graph"] or {}).get("keywords") or []

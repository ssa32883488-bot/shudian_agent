"""将 knowledge_graph_v0.2.json 同步到 Neo4j。

用法（需先起 Neo4j，并在 .env 设 NEO4J_ENABLED=true）::

    cd shudian_agent/backend
    .\\.venv\\Scripts\\python.exe scripts\\sync_kg_to_neo4j.py

可选::

    python scripts/sync_kg_to_neo4j.py --reset
    python scripts/sync_kg_to_neo4j.py --path ../data/kg/knowledge_graph_v0.2.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from app.config import get_settings  # noqa: E402
from app.services.neo4j_client import close_neo4j, get_neo4j_driver, is_neo4j_ready  # noqa: E402

DEFAULT_KG = BACKEND.parent / "data" / "kg" / "knowledge_graph_v0.2.json"


def _constraints(session) -> None:
    stmts = [
        "CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT concept_name IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT chapter_id IF NOT EXISTS FOR (ch:Chapter) REQUIRE ch.id IS UNIQUE",
        "CREATE CONSTRAINT problem_id IF NOT EXISTS FOR (p:Problem) REQUIRE p.id IS UNIQUE",
    ]
    for q in stmts:
        try:
            session.run(q)
        except Exception as exc:  # noqa: BLE001
            print(f"  constraint skip: {exc}")


def _reset(session) -> None:
    session.run("MATCH (n) DETACH DELETE n")
    print("  cleared all nodes/relationships")


def sync(path: Path, *, reset: bool = False) -> int:
    settings = get_settings()
    if not settings.neo4j_enabled:
        print("ERROR: NEO4J_ENABLED=false。请在 .env 设为 true 后重试。")
        return 2
    if not path.exists():
        print(f"ERROR: KG 文件不存在: {path}")
        return 2

    close_neo4j()
    if not is_neo4j_ready():
        print(
            f"ERROR: 无法连接 Neo4j {settings.neo4j_uri}。"
            "请先: cd docker && docker compose up -d neo4j"
        )
        return 2

    raw = json.loads(path.read_text(encoding="utf-8"))
    nodes = raw.get("nodes") or {}
    edges = raw.get("edges") or {}
    chapters = nodes.get("Chapter") or []
    concepts = nodes.get("Concept") or []
    problems = nodes.get("Problem") or []

    driver = get_neo4j_driver()
    assert driver is not None

    with driver.session() as session:
        _constraints(session)
        if reset:
            _reset(session)

        # Chapters
        session.run(
            """
            UNWIND $rows AS row
            MERGE (ch:Chapter {id: row.id})
            SET ch.name = row.name,
                ch.num = coalesce(row.chapter_num, row.num)
            """,
            rows=[
                {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "chapter_num": c.get("chapter_num") or c.get("num"),
                }
                for c in chapters
                if c.get("id")
            ],
        )
        print(f"  chapters={len(chapters)}")

        # Concepts in batches
        batch: list[dict] = []
        for c in concepts:
            if not c.get("name"):
                continue
            batch.append(
                {
                    "id": c.get("id") or c["name"],
                    "name": c["name"],
                    "aliases": c.get("aliases") or [],
                    "chapter_ids": c.get("chapter_ids") or [],
                    "primary_chapter_num": c.get("primary_chapter_num"),
                    "confidence": c.get("confidence") or "",
                }
            )
            if len(batch) >= 200:
                session.run(
                    """
                    UNWIND $rows AS row
                    MERGE (n:Concept {name: row.name})
                    SET n.id = row.id,
                        n.aliases = row.aliases,
                        n.chapter_ids = row.chapter_ids,
                        n.primary_chapter_num = row.primary_chapter_num,
                        n.confidence = row.confidence
                    """,
                    rows=batch,
                )
                batch = []
        if batch:
            session.run(
                """
                UNWIND $rows AS row
                MERGE (n:Concept {name: row.name})
                SET n.id = row.id,
                    n.aliases = row.aliases,
                    n.chapter_ids = row.chapter_ids,
                    n.primary_chapter_num = row.primary_chapter_num,
                    n.confidence = row.confidence
                """,
                rows=batch,
            )
        print(f"  concepts={len(concepts)}")

        # Problems (limit stem size)
        batch = []
        for p in problems:
            pid = p.get("id")
            if not pid:
                continue
            stem = (p.get("stem_preview") or p.get("stem_full") or p.get("stem") or "")[:500]
            batch.append(
                {
                    "id": pid,
                    "kind": p.get("kind") or "",
                    "stem": stem,
                    "chapter_id": p.get("chapter_id") or "",
                    "name": p.get("name") or pid,
                }
            )
            if len(batch) >= 200:
                session.run(
                    """
                    UNWIND $rows AS row
                    MERGE (p:Problem {id: row.id})
                    SET p.kind = row.kind,
                        p.stem = row.stem,
                        p.chapter_id = row.chapter_id,
                        p.name = row.name
                    """,
                    rows=batch,
                )
                batch = []
        if batch:
            session.run(
                """
                UNWIND $rows AS row
                MERGE (p:Problem {id: row.id})
                SET p.kind = row.kind,
                    p.stem = row.stem,
                    p.chapter_id = row.chapter_id,
                    p.name = row.name
                """,
                rows=batch,
            )
        print(f"  problems={len(problems)}")

        def _rel(label: str, rows: list[dict], cypher: str) -> None:
            if not rows:
                print(f"  {label}=0")
                return
            for i in range(0, len(rows), 300):
                session.run(cypher, rows=rows[i : i + 300])
            print(f"  {label}={len(rows)}")

        _rel(
            "PRE_REQUISITE_OF",
            [
                {
                    "from": e.get("from"),
                    "to": e.get("to"),
                    "confidence": e.get("confidence") or "medium",
                    "evidence": e.get("evidence") or "",
                }
                for e in (edges.get("PRE_REQUISITE_OF") or [])
                if e.get("from") and e.get("to")
            ],
            """
            UNWIND $rows AS row
            MATCH (a:Concept {name: row.from})
            MATCH (b:Concept {name: row.to})
            MERGE (a)-[r:PRE_REQUISITE_OF]->(b)
            SET r.confidence = row.confidence, r.evidence = row.evidence
            """,
        )

        _rel(
            "BELONGS_TO",
            [
                {
                    "from": e.get("from"),
                    "to_id": e.get("to_id") or e.get("to"),
                }
                for e in (edges.get("BELONGS_TO") or [])
                if e.get("from") and (e.get("to_id") or e.get("to"))
            ],
            """
            UNWIND $rows AS row
            MATCH (c:Concept {name: row.from})
            MATCH (ch:Chapter {id: row.to_id})
            MERGE (c)-[:BELONGS_TO]->(ch)
            """,
        )

        # TESTS: Problem -> Concept (to may be name)
        _rel(
            "TESTS",
            [
                {
                    "from": e.get("from"),
                    "to": e.get("to"),
                    "confidence": e.get("confidence") or "",
                    "evidence": e.get("evidence") or "",
                }
                for e in (edges.get("TESTS") or [])
                if e.get("from") and e.get("to")
            ],
            """
            UNWIND $rows AS row
            MATCH (p:Problem {id: row.from})
            MATCH (c:Concept {name: row.to})
            MERGE (p)-[r:TESTS]->(c)
            SET r.confidence = row.confidence, r.evidence = row.evidence
            """,
        )

        # SIMILAR_TO can be huge; sync top by score or all in batches
        similar = edges.get("SIMILAR_TO") or []
        # Cap to keep sync reasonable
        similar_rows = [
            {
                "from": e.get("from"),
                "to": e.get("to"),
                "score": float(e.get("score") or 0),
                "shared": e.get("shared") or [],
            }
            for e in similar
            if e.get("from") and e.get("to")
        ]
        similar_rows.sort(key=lambda x: -x["score"])
        similar_rows = similar_rows[:1500]
        _rel(
            "SIMILAR_TO",
            similar_rows,
            """
            UNWIND $rows AS row
            MATCH (a:Problem {id: row.from})
            MATCH (b:Problem {id: row.to})
            MERGE (a)-[r:SIMILAR_TO]->(b)
            SET r.score = row.score, r.shared = row.shared
            """,
        )

        # Stats
        stats = session.run(
            """
            MATCH (c:Concept) WITH count(c) AS concepts
            MATCH (ch:Chapter) WITH concepts, count(ch) AS chapters
            MATCH (p:Problem) WITH concepts, chapters, count(p) AS problems
            MATCH ()-[r:PRE_REQUISITE_OF]->() WITH concepts, chapters, problems, count(r) AS prereq
            RETURN concepts, chapters, problems, prereq
            """
        ).single()
        print(
            "DONE neo4j sync:",
            dict(stats) if stats else {},
            f"from={path}",
        )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync KG JSON → Neo4j")
    ap.add_argument("--path", type=Path, default=DEFAULT_KG)
    ap.add_argument("--reset", action="store_true", help="清空后再导入")
    args = ap.parse_args()
    return sync(args.path, reset=args.reset)


if __name__ == "__main__":
    raise SystemExit(main())

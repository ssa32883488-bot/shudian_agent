"""灌入少量数电样例题到 question_bank，并同步 ChromaDB。

用法（在 backend/ 目录）:
  python -m scripts.seed_questions
"""

from __future__ import annotations

import sys
from pathlib import Path

# 保证可从 backend/ 直接运行
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import SessionLocal, init_db
from app.db.models import QuestionBank
from app.services.question_bank import sync_question_to_chroma

SAMPLES = [
    {
        "content": "请简述组合逻辑电路与时序逻辑电路的主要区别。",
        "answer": (
            "组合逻辑的输出仅由当前输入决定，无存储元件；"
            "时序逻辑的输出还取决于内部状态（历史输入），含触发器等存储元件。"
        ),
        "analysis": "抓住「是否有记忆」这一核心差异即可。",
        "knowledge_tags": {"tags": ["组合逻辑", "时序逻辑"]},
        "source": "教材·逻辑电路基础",
    },
    {
        "content": "什么是竞争冒险？如何消除？",
        "answer": (
            "竞争冒险指组合电路中因门延迟不同，输入变化时输出出现瞬时错误毛刺。"
            "消除方法包括增加冗余项、引入选通脉冲、增加惯性延迟等。"
        ),
        "analysis": "卡诺图中相邻项合并时注意覆盖过渡。",
        "knowledge_tags": {"tags": ["竞争冒险", "组合逻辑"]},
        "source": "教材·组合逻辑",
    },
    {
        "content": "用卡诺图化简函数 F(A,B,C)=Σm(0,2,4,5,6)。",
        "answer": "F = B'C' + AC' + AB'（具体分组以卡诺图圈选为准，常见结果为 C'+AB' 等等价式）。",
        "analysis": "将 1 填入卡诺图，圈成 2 的幂次方，写出最简与或式。",
        "knowledge_tags": {"tags": ["卡诺图", "逻辑化简"]},
        "source": "教材·逻辑代数",
    },
    {
        "content": "D 触发器的特性方程是什么？",
        "answer": "Q* = D（次态等于 D 端输入）。",
        "analysis": "边沿触发时，时钟有效沿采样 D。",
        "knowledge_tags": {"tags": ["触发器", "D触发器"]},
        "source": "教材·时序逻辑",
    },
    {
        "content": "简述同步时序电路与异步时序电路的区别。",
        "answer": (
            "同步时序中所有触发器共用同一时钟，状态在同一时刻翻转；"
            "异步时序中触发器时钟不同源或无统一时钟，状态改变不同步。"
        ),
        "analysis": "同步设计更易分析与避免竞争。",
        "knowledge_tags": {"tags": ["同步时序", "异步时序"]},
        "source": "教材·时序逻辑",
    },
]


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(QuestionBank).count()
        if existing > 0:
            print(f"题库已有 {existing} 道题，跳过重复灌入；仍同步向量…")
            for row in db.query(QuestionBank).filter(QuestionBank.status == "active"):
                sync_question_to_chroma(row)
            print("ChromaDB 同步完成")
            return

        for s in SAMPLES:
            row = QuestionBank(
                content=s["content"],
                answer=s["answer"],
                analysis=s["analysis"],
                knowledge_tags=s["knowledge_tags"],
                source=s["source"],
                status="active",
            )
            db.add(row)
            db.flush()
            sync_question_to_chroma(row)
            print(f"已入库 id={row.id}: {row.content[:40]}…")
        db.commit()
        print(f"完成，共灌入 {len(SAMPLES)} 道样例题")
    finally:
        db.close()


if __name__ == "__main__":
    main()

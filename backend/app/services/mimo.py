"""MiMo 云端 API 封装（LLM 生成 + OCR 识图）。

P1 支持 mock 模式：无 API Key 或 MIMO_MOCK=true 时返回占位结果，便于本地跑通闭环。
"""

from __future__ import annotations

import base64
import logging
import re
from typing import Any, Optional

import httpx

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


class MiMoClient:
    """小米 MiMo 云端客户端。接口可切换 mock / 真实。"""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self.settings = settings or get_settings()
        self.base = self.settings.mimo_api_base.rstrip("/")
        self.api_key = self.settings.mimo_api_key
        self.mock = self.settings.mimo_mock or not self.api_key

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if self.mock:
            return self._mock_chat(messages)

        payload = {
            "model": model or self.settings.mimo_model,
            "messages": messages,
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{self.base}/chat/completions",
                headers=self._headers(),
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            msg = data["choices"][0]["message"]
            content = (msg.get("content") or "").strip()
            # 部分推理模型偶发 content 为空，仅有 reasoning_content
            if not content:
                content = (msg.get("reasoning_content") or "").strip()
            return content

    async def ocr_extract_question(self, image_base64: str) -> str:
        """视模型识图：直接理解图片中的题目，返回题面文本。"""
        raw = self._strip_data_url(image_base64)
        if self.mock:
            return (
                "【Mock OCR】请简述组合逻辑与时序逻辑的区别，并各举一例。"
                f"（图像字节约 {len(base64.b64decode(raw))}）"
            )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "请识别图片中的数电题目。只输出题面文字（可含必要图注），不要解答。\n"
                            "若含触发器符号，须写明：器件类型（D/JK/SR/T）、时钟触发沿"
                            "（上升沿/下降沿，看时钟端有无小圆）、各输入接法或常数（如 J=K=1）、"
                            "图中给出了哪些输入波形（仅 CLK，或 CLK+D 等）、初始状态。"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{raw}"},
                    },
                ],
            }
        ]
        return await self.chat(messages, model=self.settings.mimo_ocr_model)

    async def solve_problem(
        self, question: str, *, kg_context: str | None = None
    ) -> dict[str, str]:
        """AI 解题：返回答案与解析。调用方须标注「仅供参考」。"""
        if self.mock:
            prefix = (kg_context or "")[:120]
            return {
                "answer": (
                    f"【Mock AI解答】针对题目「{question[:80]}…」的参考解法："
                    "先明确题型与考点，再分步推导。本答案为占位，接入真实 MiMo 后替换。"
                ),
                "analysis": (
                    f"（Mock）解题步骤：1) 审题 2) 定位知识点 3) 推导 4) 校验。"
                    + (f"\n图谱提示：{prefix}" if prefix else "")
                ),
            }

        kg_block = f"\n\n{kg_context}\n请以上述知识图谱为依据组织解题逻辑，先点明考点再分步推导。" if kg_context else ""
        prompt = (
            "你是数字电子技术助学导师。请分步解答下列题目，"
            "输出 JSON：{\"answer\": \"...\", \"analysis\": \"...\"}。\n\n"
            f"题目：{question}{kg_block}"
        )
        content = await self.chat(
            [
                {"role": "system", "content": "你是严谨的数电助教，不编造无依据结论。优先依据给定知识图谱考点与逻辑链作答。"},
                {"role": "user", "content": prompt},
            ]
        )
        return self._parse_answer_json(content, fallback=content)

    async def judge_question_match(
        self, user_question: str, bank_content: str, *, retrieval_score: float = 0.0
    ) -> dict[str, Any]:
        """判断题库题面与用户题是否为同一道题（条件/数值须实质一致）。

        返回 matched / score / reason。向量分高只作参考，不能替代本判断。
        """
        th = float(self.settings.match_accept_threshold)
        uq = (user_question or "").strip()
        bc = (bank_content or "").strip()
        if not uq or not bc:
            return {
                "matched": False,
                "score": 0.0,
                "reason": "题面为空，无法匹配",
            }

        if self.mock:
            # Mock：字符重合粗判，便于本地联调
            a = set(re.sub(r"\s+", "", uq)[:120])
            b = set(re.sub(r"\s+", "", bc)[:120])
            jacc = (len(a & b) / max(1, len(a | b))) if a or b else 0.0
            contained = uq[:40] in bc or bc[:40] in uq
            score = max(jacc, float(retrieval_score) * 0.55)
            if contained:
                score = max(score, 0.88)
            matched = score >= th or (
                contained and retrieval_score >= 0.8
            ) or (jacc >= 0.55 and retrieval_score >= 0.9)
            return {
                "matched": bool(matched),
                "score": round(min(1.0, score), 3),
                "reason": f"Mock 重合度≈{jacc:.2f}，检索分={retrieval_score:.3f}",
            }

        prompt = (
            "你是数电题库质检员。判断【用户题】与【题库题】是否为同一道考题。\n"
            "必须逐项核对，任一关键项不一致 → matched=false：\n"
            "1) 器件类型（D/JK/SR/T/门电路等）\n"
            "2) 触发沿（上升/下降/电平）\n"
            "3) 输入端集合与常数（如仅有 CLK 且 J=K=1，≠ 另给 D 波形）\n"
            "4) 待求量与初值\n"
            "仅考点相近、题号不同、条件数字不同、问法不同 → 一律不算同一道。\n"
            "只输出 JSON："
            '{"matched": true/false, "score": 0.0~1.0, "reason": "一句中文理由"}。\n'
            f"检索相似度仅供参考（不能单独作为同一题依据）：{retrieval_score:.3f}\n\n"
            f"【用户题】\n{uq[:2500]}\n\n"
            f"【题库题】\n{bc[:2500]}"
        )
        content = await self.chat(
            [
                {
                    "role": "system",
                    "content": "严格比对题面同一性，宁可判不匹配也不误收。只输出 JSON。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        parsed = self._parse_match_json(content)
        matched = bool(parsed["matched"]) and float(parsed["score"]) >= th
        return {
            "matched": matched,
            "score": float(parsed["score"]),
            "reason": str(parsed.get("reason") or ""),
        }

    async def validate_authority(self, question: str, answer: str) -> dict[str, Any]:
        """自主解题后的评审：严谨性、步骤完整性、是否可回流题库。"""
        if self.mock:
            score = 0.75 if len(answer) > 40 else 0.45
            try:
                from app.services.runtime_config import get_runtime_config

                thr = float(
                    get_runtime_config().get("authority_validate_threshold")
                    or self.settings.authority_validate_threshold
                )
            except Exception:
                thr = self.settings.authority_validate_threshold
            return {
                "passed": score >= thr,
                "score": score,
                "reason": "Mock 启发式校验",
            }

        prompt = (
            "你是数字电子技术命题评审。评估下列 AI 解答是否严谨、步骤完整、"
            "无明显科学性错误，以及是否适合作为题库候选回流。\n"
            "只输出 JSON："
            '{"score": 0.0~1.0, "reason": "评审要点", "issues": ["可选问题列表"]}。\n\n'
            f"【题目】\n{question[:2000]}\n\n【解答】\n{answer[:4000]}"
        )
        content = await self.chat(
            [
                {
                    "role": "system",
                    "content": "做严格评审：步骤跳跃、公式错误、答非所问应压低 score。只输出 JSON。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        parsed = self._parse_validate_json(content)
        try:
            from app.services.runtime_config import get_runtime_config

            thr = float(get_runtime_config().get("authority_validate_threshold") or self.settings.authority_validate_threshold)
        except Exception:
            thr = self.settings.authority_validate_threshold
        passed = parsed["score"] >= thr
        return {"passed": passed, "score": parsed["score"], "reason": parsed["reason"]}

    async def grade_student_answer(
        self,
        *,
        question: str,
        reference_answer: str,
        student_text: str = "",
        image_data_urls: list[str] | None = None,
    ) -> dict[str, Any]:
        """加练逐题阅卷：结合题干、参考答案、学生文字与图片。

        返回 correct / score(0~1) / comment。
        """
        text = (student_text or "").strip()
        images = [u for u in (image_data_urls or []) if u and str(u).strip()]
        if not text and not images:
            return {
                "correct": False,
                "score": 0.0,
                "comment": "未作答",
            }

        if self.mock:
            ref = (reference_answer or "").strip()
            norm_t = re.sub(r"\s+", "", text.lower())
            norm_r = re.sub(r"\s+", "", ref.lower())
            if norm_t and norm_r and norm_t == norm_r:
                return {
                    "correct": True,
                    "score": 1.0,
                    "comment": "Mock：与参考答案一致",
                }
            if images and not text:
                return {
                    "correct": True,
                    "score": 0.72,
                    "comment": f"Mock：已收到 {len(images)} 张作答图，按通过计（接入真实模型后细判）",
                }
            if text and ref and (norm_t in norm_r or norm_r in norm_t or len(text) > 20):
                return {
                    "correct": True,
                    "score": 0.8,
                    "comment": "Mock：文字作答较完整，判为基本正确",
                }
            return {
                "correct": False,
                "score": 0.35,
                "comment": "Mock：与参考答案差异较大或作答过短",
            }

        parts: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": (
                    "你是数字电子技术助教，正在批改学生加练作答。\n"
                    "请综合【题目】【参考答案】【学生文字】以及下方所有作答图片（手写/推导/电路图等）判分。\n"
                    "等价写法、合理推导过程应判正确；关键步骤错误、答非所问判错误。\n"
                    "只输出 JSON："
                    '{"correct": true/false, "score": 0.0~1.0, "comment": "一句中文评语"}。\n\n'
                    f"【题目】\n{(question or '')[:2500]}\n\n"
                    f"【参考答案】\n{(reference_answer or '')[:2500]}\n\n"
                    f"【学生文字】\n{(text or '（无文字，仅有图片）')[:2500]}"
                ),
            }
        ]
        for url in images[:4]:
            raw = self._strip_data_url(url)
            if not raw:
                continue
            if not str(url).startswith("data:"):
                url = f"data:image/jpeg;base64,{raw}"
            parts.append(
                {
                    "type": "image_url",
                    "image_url": {"url": url},
                }
            )

        content = await self.chat(
            [
                {
                    "role": "system",
                    "content": "严格对照题目与参考答案批改学生作答；只输出 JSON。",
                },
                {"role": "user", "content": parts},
            ],
            model=self.settings.mimo_ocr_model if images else None,
            temperature=0.0,
        )
        return self._parse_grade_json(content)

    @staticmethod
    def _parse_grade_json(content: str) -> dict[str, Any]:
        import json

        try:
            m = re.search(r"\{[\s\S]*\}", content)
            if m:
                obj = json.loads(m.group(0))
                correct = obj.get("correct")
                if isinstance(correct, str):
                    correct = correct.strip().lower() in {"1", "true", "yes", "是", "正确"}
                score = float(obj.get("score", 0.5 if correct else 0.3))
                if correct is None:
                    correct = score >= 0.6
                return {
                    "correct": bool(correct),
                    "score": max(0.0, min(1.0, score)),
                    "comment": str(obj.get("comment") or obj.get("reason") or "")[:500],
                }
        except Exception:
            logger.warning("解析加练判卷 JSON 失败")
        return {
            "correct": False,
            "score": 0.4,
            "comment": (content or "")[:200] or "判卷解析失败",
        }

    @staticmethod
    def _strip_data_url(image_base64: str) -> str:
        if "," in image_base64 and image_base64.startswith("data:"):
            return image_base64.split(",", 1)[1]
        return image_base64

    @staticmethod
    def _mock_chat(messages: list[dict[str, Any]]) -> str:
        last = messages[-1].get("content", "") if messages else ""
        if isinstance(last, list):
            return "【Mock MiMo】已收到多模态消息。"
        return f"【Mock MiMo】已收到：{str(last)[:120]}"

    @staticmethod
    def _parse_answer_json(content: str, fallback: str) -> dict[str, str]:
        import json

        try:
            m = re.search(r"\{[\s\S]*\}", content)
            if m:
                obj = json.loads(m.group(0))
                return {
                    "answer": str(obj.get("answer", fallback)),
                    "analysis": str(obj.get("analysis", "")),
                }
        except Exception:
            logger.warning("解析 MiMo 解题 JSON 失败，使用原文")
        return {"answer": content, "analysis": ""}

    @staticmethod
    def _parse_validate_json(content: str) -> dict[str, Any]:
        import json

        try:
            m = re.search(r"\{[\s\S]*\}", content)
            if m:
                obj = json.loads(m.group(0))
                issues = obj.get("issues")
                reason = str(obj.get("reason", ""))
                if isinstance(issues, list) and issues:
                    reason = (reason + "；问题：" + "；".join(str(x) for x in issues[:4])).strip("；")
                return {
                    "score": float(obj.get("score", 0.5)),
                    "reason": reason,
                }
        except Exception:
            logger.warning("解析校验 JSON 失败")
        return {"score": 0.5, "reason": content[:200]}

    @staticmethod
    def _parse_match_json(content: str) -> dict[str, Any]:
        import json

        try:
            m = re.search(r"\{[\s\S]*\}", content)
            if m:
                obj = json.loads(m.group(0))
                matched = obj.get("matched")
                if isinstance(matched, str):
                    matched = matched.strip().lower() in {"1", "true", "yes", "是"}
                return {
                    "matched": bool(matched),
                    "score": float(obj.get("score", 0.0)),
                    "reason": str(obj.get("reason", "")),
                }
        except Exception:
            logger.warning("解析匹配 JSON 失败")
        return {"matched": False, "score": 0.0, "reason": content[:200]}


_mimo: Optional[MiMoClient] = None


def get_mimo() -> MiMoClient:
    global _mimo
    if _mimo is None:
        _mimo = MiMoClient()
    return _mimo

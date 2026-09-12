"""助学导师：短任务 / Plan 子任务一律走 ReAct 工具链（不再默认无工具直出）。"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from typing import Any, AsyncIterator, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
from sqlalchemy.orm import Session

from app.agents.guardrails import CircuitBreaker
from app.agents.mock_llm import build_chat_model
from app.config import get_settings
from app.services.draw_blocks import (
    DRAW_SYSTEM_RULES,
    artifacts_from_pairs,
    has_draw_markers,
    replace_draw_markers,
    strip_unfilled_draw_markers,
    unused_as_pairs,
    wants_drawing_tools,  # re-export for decision_maker
)
from app.tools import build_tutor_tools, set_tool_db

logger = logging.getLogger(__name__)

SYSTEM = f"""你是「数电助学」导师：面向高校《数字电子技术》课程的学习伙伴，教材主线对齐阎石《数字电子技术基础》。
你像一位耐心、清醒的任课助教——能把抽象概念讲透，也能陪着拆题、纠错、补漏；语气自然、克制，不卖关子，不堆术语吓人，也不夸大自己做不到的事。
擅长门电路与逻辑代数、卡诺图化简、组合/时序电路、触发器与计数器、555、存储器与 DAC/ADC 等；可讲解、解题、规划练习，并在需要时查阅教材、知识图谱、题库或绘制逻辑图/波形/真值表等。记住学生的易错点与进度，下次接着帮。

【场景边界 · 一律在本对话内处理，无旁路】
1. 寒暄与自我介绍：按上述人设与能力自然回答即可，勿调工具。
2. 与数电学习无关的闲聊：礼貌说明本助手专注数电助学，可请对方换相关问题。
3. 敏感/违法/危险请求：明确拒绝，不提供任何操作建议；可请对方回到数电学习问题。
4. 知识点讲解、刷题计划、解题：均在本 ReAct 流程内用工具协助完成。

【题面】
1. 用户消息里的题面**已是识图/OCR 得到的文字**或用户直接输入；禁止说「无法查看图片」。
2. 题面不完整则据已有文字作答并点明缺什么；禁止循环重复同一段落。
3. 多道小题只解系统给出的范围内题目。
4. 最终输出一份完整中文分步解答（讲解/寒暄类可更短）。

【解题策略 · 题库】
解题主链路会在进入本对话前预检索题库：
- 若用户消息含「题库预检索：无命中…」：已确认非原题，直接解题，勿再调 search_question_bank。
- 其它入口（非预检索链路）若明显是完整题干：可先调一次 search_question_bank；hit=true 采用其答案；message=无 则自主解答。
按需再用教材检索、图谱、绘图等工具。

【可用工具 · 按需调用】
- search_question_bank：题干 → 原题检索（高阈值+同题校验）；未通过返回「无」（预检索已做过则勿重复）
- retrieve_multi_rerank：教材摘录与插图占位
- graph_query：知识图谱路径/逻辑链
- draw_with_workflow：唯一绘图工具（八种 diagram_kind，见工具说明）
- memory_search / memory_upsert / memory_forget：学生长期记忆
- read_profile：学情聚合画像

{DRAW_SYSTEM_RULES}

教材插图：retrieve 返回的 <<<FIGURE id="..." path="..." desc="...">>> 需要时原样保留。
排版：标准 Markdown；公式用 $...$；段落之间空一行。
"""

def _collapse_repetitive_text(text: str) -> str:
    """去掉模型卡死时的段落/句子级重复。"""
    if not text or len(text) < 60:
        return text

    paras = re.split(r"\n\s*\n+", text.strip())
    kept: list[str] = []
    seen_norm: set[str] = set()
    for p in paras:
        raw = p.strip()
        if not raw:
            continue
        norm = re.sub(r"\s+", "", raw)
        if len(norm) >= 20 and norm in seen_norm:
            continue
        if len(norm) >= 20:
            seen_norm.add(norm)
        kept.append(raw)
    collapsed = "\n\n".join(kept)

    sentences = re.split(r"(?<=[。！？])", collapsed)
    out: list[str] = []
    sent_seen: set[str] = set()
    for s in sentences:
        key = re.sub(r"\s+", "", s.strip())
        if len(key) >= 24:
            if key in sent_seen:
                continue
            sent_seen.add(key)
        out.append(s)
    collapsed = "".join(out).strip()

    n = len(collapsed)
    if n >= 200:
        half = n // 2
        a, b = collapsed[:half], collapsed[half : half * 2]
        a_n, b_n = re.sub(r"\s+", "", a), re.sub(r"\s+", "", b)
        if a_n and b_n and (a_n in b_n or b_n in a_n or a_n[:80] == b_n[:80]):
            collapsed = a.rstrip()

    return collapsed


def _looks_like_generation_loop(text: str) -> bool:
    if len(text) < 120:
        return False
    markers = (
        "由于我无法直接查看图片",
        "无法直接查看图片",
        "让我根据教材知识来分析",
        "根据阎石《数字电子技术基础》",
        "让我重新",
        "再次整理",
    )
    if sum(text.count(m) for m in markers) >= 3:
        return True
    window = re.sub(r"\s+", "", text[-500:])
    if len(window) >= 80:
        frag = window[:36]
        if frag and window.count(frag) >= 3:
            return True
    # 同一最小项编号反复刷屏（正常卡诺展开会有多个不同 m，不算循环）
    m_ids = re.findall(r"m[_\\{]*(\d+)", text, flags=re.I)
    if len(m_ids) >= 36:
        from collections import Counter

        cnt = Counter(m_ids)
        # 至少 36 次引用且某一编号 ≥8 次，才判为刷屏
        if any(v >= 8 for v in cnt.values()):
            return True
    return False


def _chunk_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text") or ""))
            elif hasattr(block, "text"):
                parts.append(str(getattr(block, "text") or ""))
        return "".join(parts)
    return str(content)


def _wants_timing_wave(question: str) -> bool:
    q = question or ""
    if not any(k in q for k in ("波形", "时序图", "电压波形")):
        return False
    return any(k in q for k in ("画", "绘制", "作出", "画出", "作出")) or "波形" in q


def _answer_has_wave_image(answer: str) -> bool:
    return bool(
        re.search(
            r"!\[[^\]]*\]\([^)]*(?:timing|wave|波形)[^)]*\)",
            answer or "",
            flags=re.I,
        )
    )


def _ensure_timing_wave_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    """题面要波形但模型未出图时，强制走 timing_wave 补图。"""
    if _answer_has_wave_image(answer):
        return answer, None
    try:
        from app.tools.draw_workflow import draw_with_workflow

        brief = (
            "根据下列数电题目画出电压波形图（含 CLK 及题中要求的 Q、Q' 等输出；"
            "注明触发沿）。只画波形，不要门电路。\n\n"
            f"【题面】\n{(question or '')[:1600]}\n\n"
            f"【解答要点摘要】\n{(answer or '')[:900]}"
        )
        res = draw_with_workflow(
            diagram_kind="timing_wave",
            brief=brief,
            max_retries=2,
        )
        url = getattr(res, "artifact_url", None) or (res.meta or {}).get("url")
        if not url and isinstance(getattr(res, "meta", None), dict):
            url = res.meta.get("artifact_url")
        if not url:
            logger.warning(
                "强制 timing_wave 未出图 ok=%s err=%s",
                getattr(res, "ok", None),
                getattr(res, "error", None),
            )
            return answer, None
        return _place_markdown_image(answer, "本题波形图", url), url
    except Exception as exc:
        logger.warning("强制 timing_wave 失败: %s", exc)
        return answer, None


def _wants_kmap(question: str) -> bool:
    q = question or ""
    if any(k in q for k in ("卡诺", "卡诺图")):
        return True
    ql = q.lower()
    return any(k in ql for k in ("karnaugh", "kmap"))


def _answer_has_kmap_image(answer: str) -> bool:
    return bool(
        re.search(
            r"!\[[^\]]*\]\([^)]*kmap[^)]*\)",
            answer or "",
            flags=re.I,
        )
        or re.search(r"!\[本题卡诺图\]\([^)]+\)", answer or "")
    )


def _parse_kmap_var_count(question: str, answer: str, fallback: int) -> int:
    blob = f"{question or ''}\n{answer or ''}"
    m = re.search(r"F\s*\(\s*([A-Za-z](?:\s*,\s*[A-Za-z]){1,3})\s*\)", blob)
    if m:
        n = len([p.strip() for p in m.group(1).split(",") if p.strip()])
        if n in (2, 3, 4):
            return n
    return fallback if fallback in (2, 3, 4) else 4


def _strip_markdown_image_url(answer: str, url: str) -> str:
    """去掉正文中已有的同一 url 配图，便于改插到正确位置。"""
    if not url or not answer:
        return answer or ""
    text = re.sub(
        rf"\n*\s*!\[[^\]]*\]\({re.escape(url)}\)\s*\n*",
        "\n\n",
        answer,
    )
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _image_placement_kind(alt: str, url: str = "") -> str:
    blob = f"{alt or ''} {url or ''}".lower()
    if "kmap" in blob or "卡诺" in (alt or ""):
        return "kmap"
    if any(k in blob for k in ("timing", "wave", "波形", "时序")):
        return "wave"
    if any(k in blob for k in ("truth", "真值表")):
        return "truth"
    if any(k in blob for k in ("state", "状态图")):
        return "state"
    if any(k in blob for k in ("xor", "异或", "gate", "logic", "门", "电路")):
        return "circuit"
    return "generic"


# 配图应插在「绘图步骤」之后、「后续分析」之前
_IMAGE_ANCHORS: dict[str, dict[str, tuple[str, ...]]] = {
    "kmap": {
        "after": (
            # 优先匹配「画卡诺」步骤标题；不要用裸「卡诺图」（会误中总标题）
            r"(?m)^#{1,4}\s*[^\n]{0,48}(?:画.?卡诺图|画.?卡诺|第二步)[^\n]*$",
            r"(?m)^[^\n]{0,48}(?:画出卡诺图|画卡诺图|绘制卡诺图)[^\n]*$",
        ),
        "before": (
            # 不要用裸「圈组」（会误中「画卡诺图并圈组」）
            r"(?m)^#{1,4}\s*[^\n]{0,48}(?:圈组分析|第三步|化简结果|进一步化简|写出化简|第四步)[^\n]*$",
            r"(?m)^[^\n]{0,48}圈组分析[^\n]*$",
        ),
    },
    "wave": {
        "after": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}(?:波形|时序)[^\n]*$",
            r"(?m)^[^\n]*(?:画出?波形|波形图如下)[^\n]*$",
        ),
        "before": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}(?:分析|结论|说明|总结)[^\n]*$",
        ),
    },
    "truth": {
        "after": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}真值表[^\n]*$",
            r"(?m)^[^\n]*(?:列出真值表|真值表如下)[^\n]*$",
        ),
        "before": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}(?:分析|化简|结论)[^\n]*$",
        ),
    },
    "state": {
        "after": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}状态图[^\n]*$",
            r"(?m)^[^\n]*(?:画出?状态图|状态图如下)[^\n]*$",
        ),
        "before": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}(?:分析|说明|结论)[^\n]*$",
        ),
    },
    "circuit": {
        "after": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}(?:电路|逻辑图|门)[^\n]*$",
            r"(?m)^[^\n]*(?:电路图如下|逻辑图如下)[^\n]*$",
        ),
        "before": (
            r"(?m)^#{1,4}\s*[^\n]{0,40}(?:分析|说明|结论|验证)[^\n]*$",
        ),
    },
}


def _find_image_insert_pos(answer: str, kind: str) -> Optional[int]:
    """返回应插入配图的字符下标；找不到则 None（调用方改文末追加）。"""
    text = answer or ""
    if not text:
        return None
    cfg = _IMAGE_ANCHORS.get(kind) or {}

    # 1) 优先：落在「绘图步骤」标题之后、下一节标题之前
    after_end: Optional[int] = None
    for pat in cfg.get("after") or ():
        m = re.search(pat, text)
        if not m:
            continue
        # 标题/提示行结束后，再吃掉紧随的一两段说明，再插图
        after_end = m.end()
        rest = text[after_end:]
        # 跳过空行与最多 2 段非标题正文
        pos = 0
        paras = 0
        while pos < len(rest) and paras < 2:
            if rest[pos] == "\n":
                pos += 1
                continue
            line_end = rest.find("\n", pos)
            if line_end < 0:
                line_end = len(rest)
            line = rest[pos:line_end]
            if re.match(r"^#{1,4}\s+", line):
                break
            if line.strip().startswith("!"):
                break
            pos = line_end
            paras += 1
        after_end = after_end + pos
        break

    before_start: Optional[int] = None
    for pat in cfg.get("before") or ():
        m = re.search(pat, text)
        if m:
            before_start = m.start()
            break
    # 若没匹配到「圈组/第三步」，则取绘图段落后的下一个 Markdown 标题
    if before_start is None and after_end is not None:
        m = re.search(r"(?m)^#{1,4}\s+", text[after_end:])
        if m:
            before_start = after_end + m.start()

    if after_end is not None and before_start is not None and before_start >= after_end:
        return before_start
    if before_start is not None:
        return before_start
    if after_end is not None:
        return after_end
    return None


def _place_markdown_image(answer: str, alt: str, url: str) -> str:
    """把配图嵌进答复正文的合适步骤位置（可改插已有同 url 图）。"""
    if not url:
        return answer or ""
    kind = _image_placement_kind(alt, url)
    text = _strip_markdown_image_url(answer or "", url)
    block = f"\n\n![{alt or '本题配图'}]({url})\n\n"
    pos = _find_image_insert_pos(text, kind)
    if pos is None:
        return text.rstrip() + block
    # 保证前后空行，避免粘进标题
    left = text[:pos].rstrip()
    right = text[pos:].lstrip()
    return f"{left}{block}{right}"


def _insert_image_near_hint(answer: str, block: str, hints: tuple[str, ...]) -> str:
    """兼容旧调用：从 block 解析 alt/url 后走智能定位。"""
    m = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", block or "")
    if m:
        return _place_markdown_image(answer, m.group(1), m.group(2))
    ans = (answer or "").rstrip()
    for hint in hints:
        hm = re.search(rf"({re.escape(hint)}[^\n]*\n)", ans)
        if hm:
            return ans[: hm.end()] + block + ans[hm.end() :]
    return ans + block


def _ensure_kmap_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    """题面要卡诺图但答案未嵌入时，强制 draw_with_workflow(kmap)；优先填满已有 DRAW 占位。"""
    from app.services.draw_blocks import list_draw_markers, make_draw_marker

    if _answer_has_kmap_image(answer):
        m = re.search(r"!\[([^\]]*)\]\(([^)]*kmap[^)]*)\)", answer or "", flags=re.I)
        if not m:
            m = re.search(r"!\[(本题卡诺图)\]\(([^)]+)\)", answer or "")
        if m:
            return _place_markdown_image(answer, m.group(1) or "本题卡诺图", m.group(2)), None
        return answer, None
    try:
        from app.tools.draw.kmap import parse_sum_of_minterms
        from app.tools.draw_workflow import draw_with_workflow

        blob = f"{question or ''}\n{answer or ''}"
        vc_parsed, minterms = parse_sum_of_minterms(blob)
        if not minterms:
            logger.warning("强制 kmap：未能从题面解析最小项")
            return answer, None
        var_count = _parse_kmap_var_count(question, answer, vc_parsed)
        script = json.dumps(
            {
                "minterms": minterms,
                "var_count": var_count,
                "auto_group": True,
                "title": "卡诺图化简",
            },
            ensure_ascii=False,
        )
        res = draw_with_workflow(
            diagram_kind="kmap",
            brief=f"画出卡诺图并化简：Σm({','.join(str(m) for m in minterms)})",
            script=script,
            max_retries=2,
        )
        url = getattr(res, "artifact_url", None)
        if not url and isinstance(getattr(res, "meta", None), dict):
            url = res.meta.get("artifact_url") or res.meta.get("url")
        if not url:
            logger.warning(
                "强制 kmap 未出图 ok=%s err=%s",
                getattr(res, "ok", None),
                getattr(res, "error", None),
            )
            return answer, None

        ans = answer or ""
        has_kmap_slot = any(m.get("kind") == "kmap" for m in list_draw_markers(ans))
        # 模型未写占位时，先在正确步骤插入 DRAW，再回填——与「先定位再嵌入」一致
        if not has_kmap_slot:
            marker = make_draw_marker("kmap", "本题卡诺图")
            pos = _find_image_insert_pos(ans, "kmap")
            if pos is None:
                ans = ans.rstrip() + f"\n\n{marker}\n"
            else:
                left, right = ans[:pos].rstrip(), ans[pos:].lstrip()
                ans = f"{left}\n\n{marker}\n\n{right}"
        ans = _bind_draw_images(ans, [("本题卡诺图", url)])
        return ans, url
    except Exception as exc:
        logger.warning("强制 kmap 失败: %s", exc)
        return answer, None


def _answer_has_kind_image(answer: str, kind: str) -> bool:
    from app.services.draw_blocks import answer_has_tool_drawing

    if not answer_has_tool_drawing(answer or ""):
        return False
    blob = (answer or "").lower()
    keys = {
        "seven": ("7seg", "seven", "数码管"),
        "truth": ("truth", "真值表"),
        "state": ("state", "状态"),
        "curve": ("char_curve", "curve", "vtc", "特性"),
        "logic": ("logic", "gate", "xor", "wf_"),
        "gate": ("logic", "gate", "xor", "wf_"),
    }.get(kind, (kind,))
    # 有工具图且 URL/alt 命中该种，或至少已有任意工具图且题面专指该种时由 ensure 负责
    return any(k.lower() in blob for k in keys)


def _insert_draw_slot_then_bind(
    answer: str, *, kind: str, alt: str, url: str
) -> str:
    from app.services.draw_blocks import list_draw_markers, make_draw_marker

    ans = answer or ""
    has_slot = any(m.get("kind") == kind for m in list_draw_markers(ans))
    if not has_slot:
        marker = make_draw_marker(kind, alt)
        place_kind = kind if kind in _IMAGE_ANCHORS else {
            "seven": "truth",
            "curve": "truth",
        }.get(kind, "truth")
        pos = _find_image_insert_pos(ans, place_kind)
        if kind == "seven":
            m = re.search(
                r"(?m)^#{1,4}\s*[^\n]{0,48}(?:七段|数码管|显示)[^\n]*$",
                ans,
            )
            if m:
                rest = ans[m.end() :]
                nxt = re.search(r"(?m)^#{1,4}\s+", rest)
                pos = m.end() + (nxt.start() if nxt else min(len(rest), 1))
        if kind == "curve":
            m = re.search(
                r"(?m)^#{1,4}\s*[^\n]{0,48}(?:特性曲线|传输特性|VTC)[^\n]*$",
                ans,
            )
            if m:
                rest = ans[m.end() :]
                nxt = re.search(r"(?m)^#{1,4}\s+", rest)
                pos = m.end() + (nxt.start() if nxt else min(len(rest), 1))
        if pos is None:
            ans = ans.rstrip() + f"\n\n{marker}\n"
        else:
            left, right = ans[:pos].rstrip(), ans[pos:].lstrip()
            ans = f"{left}\n\n{marker}\n\n{right}"
    return _bind_draw_images(ans, [(alt, url)])


def _wants_seven_seg(question: str) -> bool:
    q = question or ""
    return any(k in q for k in ("七段", "数码管", "段码"))


def _ensure_seven_seg_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    if _answer_has_kind_image(answer, "seven"):
        return answer, None
    try:
        from app.tools.draw_workflow import draw_with_workflow

        blob = f"{question or ''}\n{answer or ''}"
        m = re.search(r"(?:显示|数字|为)\s*([0-9])|([0-9])\s*(?:的点亮|点亮)", blob)
        digit = 8
        if m:
            digit = int(next(g for g in m.groups() if g is not None))
        else:
            m2 = re.search(r"(?<![0-9])([0-9])(?![0-9])", blob)
            if m2:
                digit = int(m2.group(1))
        script = json.dumps(
            {"digit": digit, "title": f"七段数码管显示{digit}"},
            ensure_ascii=False,
        )
        res = draw_with_workflow(
            diagram_kind="seven_seg",
            brief=f"画出共阴七段数码管点亮数字 {digit}",
            script=script,
            max_retries=2,
        )
        url = getattr(res, "artifact_url", None)
        if not url and isinstance(getattr(res, "meta", None), dict):
            url = res.meta.get("artifact_url") or res.meta.get("url")
        if not url:
            return answer, None
        return _insert_draw_slot_then_bind(
            answer, kind="seven", alt=f"七段数码管显示{digit}", url=url
        ), url
    except Exception as exc:
        logger.warning("强制 seven_seg 失败: %s", exc)
        return answer, None


def _wants_truth_table(question: str) -> bool:
    return "真值表" in (question or "") or "功能表" in (question or "")


def _ensure_truth_table_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    if _answer_has_kind_image(answer, "truth"):
        return answer, None
    try:
        from app.tools.draw_workflow import draw_with_workflow

        brief = (
            "根据题面画出真值表（含全部输入组合与输出）。\n\n"
            f"【题面】\n{(question or '')[:1200]}\n\n"
            f"【解答摘要】\n{(answer or '')[:800]}"
        )
        res = draw_with_workflow(
            diagram_kind="truth_table", brief=brief, max_retries=2
        )
        url = getattr(res, "artifact_url", None) or (res.meta or {}).get("url")
        if not url:
            return answer, None
        return _insert_draw_slot_then_bind(
            answer, kind="truth", alt="本题真值表", url=url
        ), url
    except Exception as exc:
        logger.warning("强制 truth_table 失败: %s", exc)
        return answer, None


def _wants_state_diagram(question: str) -> bool:
    q = question or ""
    return any(k in q for k in ("状态图", "状态转换", "状态机", "FSM"))


def _ensure_state_diagram_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    if _answer_has_kind_image(answer, "state"):
        return answer, None
    try:
        from app.tools.draw_workflow import draw_with_workflow

        brief = (
            "根据题面画出状态转换图（圆状态+转移边）。\n\n"
            f"【题面】\n{(question or '')[:1200]}\n\n"
            f"【解答摘要】\n{(answer or '')[:800]}"
        )
        res = draw_with_workflow(
            diagram_kind="state_machine", brief=brief, max_retries=2
        )
        url = getattr(res, "artifact_url", None) or (res.meta or {}).get("url")
        if not url:
            return answer, None
        return _insert_draw_slot_then_bind(
            answer, kind="state", alt="本题状态图", url=url
        ), url
    except Exception as exc:
        logger.warning("强制 state_machine 失败: %s", exc)
        return answer, None


def _wants_char_curve(question: str) -> bool:
    q = question or ""
    return any(k in q for k in ("特性曲线", "传输特性", "VTC", "电压传输"))


def _ensure_char_curve_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    if _answer_has_kind_image(answer, "curve"):
        return answer, None
    try:
        from app.tools.draw_workflow import draw_with_workflow

        blob = f"{question or ''}{answer or ''}".upper()
        curve = "cmos_vtc" if "CMOS" in blob else "ttl_vtc"
        script = json.dumps(
            {"curve": curve, "title": "本题特性曲线"},
            ensure_ascii=False,
        )
        res = draw_with_workflow(
            diagram_kind="char_curve",
            brief=f"画出 {curve} 电压传输特性曲线",
            script=script,
            max_retries=2,
        )
        url = getattr(res, "artifact_url", None)
        if not url and isinstance(getattr(res, "meta", None), dict):
            url = res.meta.get("artifact_url") or res.meta.get("url")
        if not url:
            return answer, None
        return _insert_draw_slot_then_bind(
            answer, kind="curve", alt="本题特性曲线", url=url
        ), url
    except Exception as exc:
        logger.warning("强制 char_curve 失败: %s", exc)
        return answer, None


def _wants_logic_dag(question: str, answer: str = "") -> bool:
    blob = f"{question or ''}\n{answer or ''}"
    keys = (
        "逻辑图",
        "逻辑符号",
        "符号图",
        "门电路",
        "门符号",
        "与门",
        "或门",
        "与非",
        "或非",
        "异或门",
        "非门",
        "logic_dag",
        'kind="logic',
        "DRAW kind=\"logic",
        "<<<DRAW",
    )
    # 「逻辑符号图」不含连续「逻辑图」子串，需单独覆盖
    return any(k in blob for k in keys)


def _ensure_logic_dag_image(answer: str, question: str) -> tuple[str, Optional[str]]:
    """题面/解答需要门级逻辑图但未嵌入时，强制 draw_with_workflow(logic_dag)。"""
    if _answer_has_kind_image(answer, "logic") or _answer_has_kind_image(answer, "gate"):
        return answer, None
    try:
        from app.tools.draw_workflow import draw_with_workflow

        brief = (
            "根据题面与解答画出教材风格门级逻辑符号图（logic_ir_v1）。\n"
            "优先识别文中『A、B经与门得Y1…』类步骤，生成对应门网表。\n\n"
            f"【题面】\n{(question or '')[:1200]}\n\n"
            f"【解答摘要】\n{(answer or '')[:1200]}"
        )
        res = draw_with_workflow(
            diagram_kind="logic_dag",
            brief=brief,
            max_retries=3,
        )
        url = getattr(res, "artifact_url", None)
        if not url and isinstance(getattr(res, "meta", None), dict):
            url = res.meta.get("artifact_url") or res.meta.get("url")
        if not url:
            logger.warning(
                "强制 logic_dag 未出图 ok=%s err=%s",
                getattr(res, "ok", None),
                getattr(res, "error", None),
            )
            return answer, None
        return _insert_draw_slot_then_bind(
            answer, kind="logic", alt="本题逻辑电路图", url=url
        ), url
    except Exception as exc:
        logger.warning("强制 logic_dag 失败: %s", exc)
        return answer, None


_MARKER_KIND_TO_WORKFLOW: dict[str, str] = {
    "logic": "logic_dag",
    "gate": "logic_dag",
    "circuit": "msi_design",
    "kmap": "kmap",
    "timing": "timing_wave",
    "truth": "truth_table",
    "state": "state_machine",
    "seven": "seven_seg",
    "curve": "char_curve",
}


def _fill_unfilled_draw_markers(
    answer: str,
    question: str,
    generated: list[tuple[str, str]],
    tool_trace: list[str],
) -> tuple[str, list[tuple[str, str]], list[str]]:
    """对仍未回填的 <<<DRAW>>> 按 kind 强制调工作流出图，再回填。

    解决：模型写了占位却未成功调工具 / 工具失败后留下『配图未生成』。
    """
    from app.services.draw_blocks import list_draw_markers
    from app.tools.draw_workflow import draw_with_workflow

    text = answer or ""
    gen = list(generated)
    trace = list(tool_trace)
    markers = list_draw_markers(text)
    if not markers:
        return text, gen, trace

    for m in markers:
        kind = m.get("kind") or "auto"
        desc = (m.get("desc") or "本题配图").strip() or "本题配图"
        raw = m.get("raw") or ""
        if not raw or raw not in text:
            continue
        diagram_kind = _MARKER_KIND_TO_WORKFLOW.get(kind)
        if not diagram_kind and kind == "auto":
            # 从 desc 猜
            dlow = desc.lower()
            if any(x in desc for x in ("逻辑", "与门", "或门", "门电路", "符号图")):
                diagram_kind = "logic_dag"
            elif "卡诺" in desc or "kmap" in dlow:
                diagram_kind = "kmap"
            elif "波形" in desc or "时序" in desc:
                diagram_kind = "timing_wave"
            elif "真值" in desc:
                diagram_kind = "truth_table"
            elif "状态" in desc:
                diagram_kind = "state_machine"
            elif "七段" in desc:
                diagram_kind = "seven_seg"
            elif "特性" in desc or "VTC" in desc:
                diagram_kind = "char_curve"
            else:
                diagram_kind = "logic_dag"
        if not diagram_kind:
            continue
        try:
            brief = (
                f"{desc}\n\n【题面】\n{(question or '')[:800]}\n\n"
                f"【上下文】\n{text[:900]}"
            )
            res = draw_with_workflow(
                diagram_kind=diagram_kind,
                brief=brief,
                max_retries=3,
            )
            url = getattr(res, "artifact_url", None)
            if not url and isinstance(getattr(res, "meta", None), dict):
                url = res.meta.get("artifact_url") or res.meta.get("url")
            if not url:
                logger.warning(
                    "占位回填失败 kind=%s ok=%s err=%s",
                    diagram_kind,
                    getattr(res, "ok", None),
                    getattr(res, "error", None),
                )
                continue
            md = f"![{desc}]({url})"
            text = text.replace(raw, md, 1)
            gen.append((desc, url))
            trace.append(f"force_fill:{diagram_kind}")
        except Exception as exc:  # noqa: BLE001
            logger.warning("占位回填异常 kind=%s: %s", diagram_kind, exc)
    return text, gen, trace


def _force_missing_drawings(
    answer: str, question: str, generated: list[tuple[str, str]], tool_trace: list[str]
) -> tuple[str, list[tuple[str, str]], list[str]]:
    """题面要图但尚无对应产物时，按图种强制补画并嵌入。"""
    text = answer or ""
    gen = list(generated)
    trace = list(tool_trace)
    # 只看真实图片 URL，勿把正文/失败备注里的「真值表」「波形」「truth」当成已出图
    url_blob = " ".join(u for _, u in gen).lower()
    url_blob += " " + " ".join(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)).lower()

    def _has_img(*keys: str) -> bool:
        return any(k.lower() in url_blob for k in keys)

    checks = (
        (_wants_kmap, _has_img("kmap"), _ensure_kmap_image, "本题卡诺图", "force:kmap"),
        (
            _wants_timing_wave,
            _has_img("timing", "wave", "wf_"),
            _ensure_timing_wave_image,
            "本题波形图",
            "force:timing_wave",
        ),
        (
            _wants_seven_seg,
            _has_img("7seg", "seven"),
            _ensure_seven_seg_image,
            "本题七段显示",
            "force:seven_seg",
        ),
        (
            _wants_truth_table,
            _has_img("truth"),
            _ensure_truth_table_image,
            "本题真值表",
            "force:truth_table",
        ),
        (
            _wants_state_diagram,
            _has_img("state"),
            _ensure_state_diagram_image,
            "本题状态图",
            "force:state_machine",
        ),
        (
            _wants_char_curve,
            _has_img("char_curve", "curve", "vtc"),
            _ensure_char_curve_image,
            "本题特性曲线",
            "force:char_curve",
        ),
        (
            lambda q: _wants_logic_dag(q, text),
            _has_img("logic", "gate", "wf_", "xor"),
            _ensure_logic_dag_image,
            "本题逻辑电路图",
            "force:logic_dag",
        ),
    )
    for want_fn, already, ensure_fn, alt, tag in checks:
        if not want_fn(question) or already:
            continue
        text, url = ensure_fn(text, question)
        if url:
            gen.append((alt, url))
            trace.append(tag)
            url_blob += " " + url.lower()
            # 清掉同种失败备注
            text = re.sub(
                r"\n*>\s*\*\*【配图未生成：[^\n]*\n*",
                "\n",
                text,
            )
    return text, gen, trace


def _reinject_markdown_images(text: str, source: str) -> str:
    """流式合并后，把 source 里已有、text 里丢失的 markdown 图按步骤位置补回。"""
    imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", source or "")
    return _inject_generated_images(text or "", [(a, u) for a, u in imgs])


async def _fake_stream_text(answer: str, *, step: int = 28) -> AsyncIterator[dict[str, Any]]:
    """整篇答案（含已嵌入图片）就绪后再假流式输出。"""
    ans = answer or ""
    yield {"type": "status", "message": "正在组织回答…"}
    yield {"type": "delta_reset"}
    for i in range(0, len(ans), step):
        yield {"type": "delta", "text": ans[i : i + step]}
        await asyncio.sleep(0.012)


_DRAW_ALT_BY_HINT = (
    ("kmap", "本题卡诺图"),
    ("truth", "本题真值表"),
    ("timing", "本题波形图"),
    ("wave", "本题波形图"),
    ("state", "本题状态图"),
    ("seven", "本题七段显示"),
    ("xor", "本题逻辑电路图"),
    ("gate", "本题门电路图"),
    ("logic", "本题逻辑电路图"),
    ("char_curve", "本题特性曲线"),
)


def _artifact_alt(tool_name: str, data: dict[str, Any]) -> str:
    blob = f"{tool_name} {data.get('artifact_url') or ''} {data.get('title') or ''}".lower()
    for hint, alt in _DRAW_ALT_BY_HINT:
        if hint in blob:
            return alt
    return "本题配图"


def _inject_generated_images(answer: str, generated: list[tuple[str, str]]) -> str:
    """按题型把工具配图嵌进对应步骤，而不是一律扔到文末。"""
    text = answer or ""
    for alt, url in generated:
        if not url:
            continue
        text = _place_markdown_image(text, alt, url)
    return text


def _relocate_inline_draw_images(answer: str) -> str:
    """把已在文末/错位的工具配图改插到答复对应步骤。"""
    text = answer or ""
    imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)
    for alt, url in imgs:
        kind = _image_placement_kind(alt, url)
        if kind == "generic":
            continue
        # 仅改插工具产物（artifact / kmap / timing 等）
        if not re.search(
            r"(?:/media/artifacts/|kmap_|timing_|wave_|truth_|xor_|gate_|state_)",
            url or "",
            flags=re.I,
        ):
            continue
        text = _place_markdown_image(text, alt, url)
    return text


def _bind_draw_images(
    answer: str,
    generated: list[tuple[str, str]],
) -> str:
    """优先按模型写的 <<<DRAW>>> 占位回填；剩余产物再启发式嵌入步骤中。"""
    text = answer or ""
    if not generated and not has_draw_markers(text):
        return text
    arts = artifacts_from_pairs(generated)
    text, unused, _filled = replace_draw_markers(text, arts)
    if unused:
        text = _inject_generated_images(text, unused_as_pairs(unused))
    return text


def _finalize_from_messages(
    messages: list[Any],
    *,
    use_mock: bool,
    question: str = "",
) -> dict[str, Any]:
    from app.services.figure_blocks import (
        collect_marker_paths,
        replace_figure_markers,
    )

    generated: list[tuple[str, str]] = []
    related: list[str] = []
    tool_trace: list[str] = []
    textbook_hits: list[dict[str, Any]] = []
    seen_gen: set[str] = set()
    seen_rel: set[str] = set()

    def _add_related(url: str) -> None:
        if url and url not in seen_rel:
            seen_rel.add(url)
            related.append(url)

    for m in messages:
        if isinstance(m, AIMessage) and getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                tool_trace.append(f"call:{tc.get('name')} args={tc.get('args')}")
        if isinstance(m, ToolMessage):
            tname = m.name or "tool"
            tool_trace.append(f"result:{tname}")
            try:
                data = json.loads(m.content)
                url = data.get("artifact_url")
                if url and url not in seen_gen:
                    seen_gen.add(url)
                    generated.append((_artifact_alt(tname, data), url))
                for fig in data.get("figures") or []:
                    p = fig.get("path") if isinstance(fig, dict) else None
                    if p:
                        _add_related(p)
                for u in data.get("hits") or []:
                    if not isinstance(u, dict):
                        continue
                    for mu in u.get("media_urls") or []:
                        if mu:
                            _add_related(mu)
                    if tname == "retrieve_multi_rerank" or u.get("chapter"):
                        textbook_hits.append(
                            {
                                "chapter": u.get("chapter"),
                                "score": u.get("score"),
                                "source": u.get("source"),
                                "preview": str(u.get("text") or "")[:120],
                            }
                        )
            except Exception:
                pass

    final_text = ""
    ai_parts: list[str] = []
    for m in messages:
        if not isinstance(m, AIMessage):
            continue
        body = str(m.content or "").strip()
        if not body:
            continue
        ai_parts.append(body)
    if not ai_parts:
        final_text = ""
    elif len(ai_parts) == 1:
        final_text = ai_parts[0]
    else:
        last = ai_parts[-1]
        earlier = "\n\n".join(ai_parts[:-1])
        # 工具调用后模型常只续写「第N步」，须与工具前正文合并；完整重写则用末条
        looks_like_continuation = bool(
            re.match(r"^第[二三四五六七八九十百\d]+步", last)
            or (
                re.search(r"第[二三四五六七八九十百\d]+步", last)
                and not re.search(r"第\s*一\s*步", last)
            )
        )
        if looks_like_continuation:
            final_text = f"{earlier}\n\n{last}".strip()
        elif len(last) >= max(400, int(len(earlier) * 0.55)):
            final_text = last
        else:
            final_text = f"{earlier}\n\n{last}".strip()

    final_text = replace_figure_markers(final_text)
    final_text = _collapse_repetitive_text(final_text)
    for u in collect_marker_paths(final_text):
        _add_related(u)

    # 1) 先按模型指定的 <<<DRAW>>> 位置回填；无占位时再启发式插入
    final_text = _bind_draw_images(final_text, generated)

    # 2) 题面要图但模型未调工具时，按图种强制补画
    final_text, generated, tool_trace = _force_missing_drawings(
        final_text, question, generated, tool_trace
    )

    # 3) 仍有未填 DRAW 占位：按 kind 强制出图回填（彻底消灭「配图未生成」空壳）
    final_text, generated, tool_trace = _fill_unfilled_draw_markers(
        final_text, question, generated, tool_trace
    )

    # 4) 再次绑定；仍失败才改为缺图提示；改插错位 markdown
    final_text = _bind_draw_images(final_text, generated)
    final_text = strip_unfilled_draw_markers(final_text)
    final_text = _relocate_inline_draw_images(final_text)

    for _alt, u in generated:
        if u:
            seen_gen.add(u)

    inline_urls = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", final_text))
    gallery = [u for u in related if u not in inline_urls and u not in seen_gen]


    mode = "mock" if use_mock else "mimo"
    analysis = ""
    if tool_trace:
        analysis = (
            f"**本轮工具**（ReAct · {mode}）\n\n"
            + "\n".join(f"- `{t}`" for t in tool_trace[:12])
        )

    return {
        "answer": final_text or "（Agent 未产生文本回答）",
        "analysis": analysis,
        "images": gallery,
        "tool_trace": tool_trace,
        "textbook_hits": textbook_hits[:8],
        "mode": mode,
    }


def _build_agent(*, db: Optional[Session], user_id: Optional[int] = None):
    settings = get_settings()
    set_tool_db(db, user_id=user_id)
    tools = build_tutor_tools()
    use_mock = bool(settings.deepseek_mock or not settings.deepseek_key)
    llm = build_chat_model(
        mock=use_mock,
        api_key=settings.deepseek_key or "mock",
        base_url=settings.deepseek_api_base,
        model=settings.deepseek_model,
    )
    if hasattr(llm, "bind_tools") and use_mock:
        llm = llm.bind_tools(tools)
    agent = create_react_agent(llm, tools)
    return agent, use_mock, settings


async def run_tutor_react(
    question: str,
    *,
    db: Optional[Session] = None,
    kg_context: Optional[str] = None,
    force_tools: Optional[bool] = None,
    memory_brief: Optional[str] = None,
    user_id: Optional[int] = None,
    bank_prefetch_note: str = "",
) -> dict[str, Any]:
    """短任务 / Plan 子任务统一走 ReAct。force_tools 保留兼容，已忽略。"""
    _ = force_tools
    final: dict[str, Any] | None = None
    async for ev in stream_tutor_react(
        question,
        db=db,
        kg_context=kg_context,
        memory_brief=memory_brief,
        user_id=user_id,
        bank_prefetch_note=bank_prefetch_note,
    ):
        if ev.get("type") == "react_done":
            final = ev.get("result")
    return final or {
        "answer": "（Agent 未产生文本回答）",
        "analysis": "",
        "images": [],
        "tool_trace": [],
        "mode": "mimo",
    }


async def stream_tutor_react(
    question: str,
    *,
    db: Optional[Session] = None,
    kg_context: Optional[str] = None,
    force_tools: Optional[bool] = None,
    memory_brief: Optional[str] = None,
    user_id: Optional[int] = None,
    bank_prefetch_note: str = "",
) -> AsyncIterator[dict[str, Any]]:
    """
    解题 ReAct 入口（短任务与 Plan 子任务共用）。
    意图路由已在上游完成：短任务直达本函数；长任务拆子任务后逐个进入本函数。
    不再按「是否画图」降级为无工具直出。force_tools 保留兼容，已忽略。
    """
    _ = force_tools
    agent, use_mock, settings = _build_agent(db=db, user_id=user_id)
    wall = float(settings.agent_wall_timeout_sec)
    idle = float(settings.agent_idle_timeout_sec)
    max_chars = int(settings.agent_max_output_chars)
    recursion_limit = max(4, int(settings.agent_max_iterations))
    breaker = CircuitBreaker()

    user_block = (
        "【题面文字】（已由系统识图/用户输入得到，请直接据此解题，"
        "不要声称无法看图，不要重复开场白）\n\n"
        f"{question.strip()}"
    )
    if (bank_prefetch_note or "").strip():
        user_block += f"\n\n【{bank_prefetch_note.strip()}】"
    if memory_brief:
        user_block += f"\n\n【学生记忆摘要】\n{memory_brief[:900]}"
    if kg_context:
        user_block += f"\n\n【知识图谱提示】\n{kg_context[:800]}"

    logger.info(
        "tutor_react stream start mock=%s model=%s recursion_limit=%s",
        use_mock,
        settings.deepseek_model,
        recursion_limit,
    )
    yield {"type": "status", "message": "正在分析题目（ReAct）…"}

    inputs = {
        "messages": [
            SystemMessage(content=SYSTEM),
            HumanMessage(content=user_block),
        ]
    }
    config = {"recursion_limit": recursion_limit}

    streamed_any = False
    final_messages: list[Any] = []
    stream_buf = ""
    loop_stopped = False
    in_tool = False
    deadline = time.monotonic() + wall
    last_event_at = time.monotonic()

    try:
        # 后台跑完工具+全文，仅推送 status/tool；配图嵌入后再假流式
        async for event in agent.astream_events(inputs, config=config, version="v2"):
            now = time.monotonic()
            # 工具内部可能连续 LLM 重试且长时间无 astream 事件；idle 只约束工具外空转
            idle_exceeded = (not in_tool) and (now - last_event_at > idle)
            if now > deadline or idle_exceeded:
                logger.warning(
                    "ReAct 超时 wall=%.0fs idle=%.0fs in_tool=%s，截断返回",
                    wall,
                    idle,
                    in_tool,
                )
                loop_stopped = True
                breaker.stop_reason = breaker.stop_reason or "wall_or_idle_timeout"
                if stream_buf:
                    stream_buf = _collapse_repetitive_text(stream_buf)
                break
            last_event_at = now

            kind = event.get("event")
            if kind == "on_chat_model_stream":
                chunk = (event.get("data") or {}).get("chunk")
                if chunk is None:
                    continue
                tcc = getattr(chunk, "tool_call_chunks", None) or []
                if tcc:
                    yield {"type": "status", "message": "准备调用绘图/检索工具…"}
                    continue
                text = _chunk_text(getattr(chunk, "content", None))
                if not text:
                    continue
                stream_buf += text
                streamed_any = True
                if (
                    len(stream_buf) >= max_chars
                    or _looks_like_generation_loop(stream_buf)
                ):
                    logger.warning("检测到过长/循环输出，截断")
                    stream_buf = _collapse_repetitive_text(stream_buf[:max_chars])
                    loop_stopped = True
                    breaker.stop_reason = breaker.stop_reason or "generation_loop"
                    break
            elif kind == "on_tool_start":
                in_tool = True
                name = event.get("name") or "tool"
                raw_input = (event.get("data") or {}).get("input")
                trip = breaker.record_tool(name, raw_input)
                yield {
                    "type": "tool_start",
                    "name": name,
                    "input": raw_input
                    if isinstance(raw_input, (dict, str))
                    else str(raw_input)[:300],
                }
                yield {"type": "status", "message": f"正在调用工具：{name}"}
                if trip:
                    logger.warning("circuit breaker trip: %s", trip)
                    loop_stopped = True
                    in_tool = False
                    notice = (
                        f"\n\n> **系统熔断**：{trip}。已停止继续调用工具，"
                        "请根据已有信息理解；建议一次只上传一道题。\n"
                    )
                    stream_buf = (
                        _collapse_repetitive_text(stream_buf) + notice
                        if stream_buf
                        else notice.strip()
                    )
                    break
            elif kind == "on_tool_end":
                in_tool = False
                last_event_at = time.monotonic()
                name = event.get("name") or "tool"
                output = (event.get("data") or {}).get("output")
                content = getattr(output, "content", output)
                preview = content if isinstance(content, str) else str(content)
                yield {
                    "type": "tool_end",
                    "name": name,
                    "preview": preview[:400],
                }
                yield {"type": "status", "message": f"工具完成：{name}"}
                if stream_buf and not stream_buf.endswith("\n"):
                    stream_buf += "\n"
                yield {"type": "status", "message": "继续组织解答…"}
            elif kind == "on_chain_end":
                data = event.get("data") or {}
                output = data.get("output")
                if isinstance(output, dict) and "messages" in output:
                    final_messages = list(output["messages"])
    except Exception as exc:
        logger.exception("tutor_react stream failed")
        yield {"type": "error", "message": f"ReAct 失败: {exc}"}
        return

    yield {"type": "status", "message": "正在嵌入配图…"}
    result = _finalize_from_messages(
        final_messages, use_mock=use_mock, question=question
    )
    finalized_before_merge = str(result.get("answer") or "").strip()
    # 流式过程中已累计的正文优先与 finalize 合并，避免只剩工具后半段
    if stream_buf.strip():
        finalized = finalized_before_merge
        pre = _collapse_repetitive_text(stream_buf.strip())
        if finalized and finalized not in pre and pre not in finalized:
            if re.match(r"^第[二三四五六七八九十百\d]+步", finalized) or (
                "第一步" not in finalized and "第一步" in pre
            ):
                result["answer"] = f"{pre}\n\n{finalized}".strip()
            elif len(pre) > len(finalized):
                result["answer"] = pre
        elif pre and not finalized:
            result["answer"] = pre
        elif pre and finalized and len(pre) > len(finalized) * 1.2:
            result["answer"] = pre
        # 合并可能冲掉 finalize 已注入的 markdown 图，必须补回
        result["answer"] = _reinject_markdown_images(
            str(result.get("answer") or ""), finalized_before_merge
        )
    if loop_stopped and stream_buf:
        result["answer"] = _collapse_repetitive_text(str(result.get("answer") or stream_buf))
        result["answer"] = _reinject_markdown_images(
            str(result.get("answer") or ""), finalized_before_merge
        )
        result["tool_trace"] = list(result.get("tool_trace") or []) + [
            f"guard:{breaker.stop_reason or 'timeout_or_loop_stop'}"
        ]
    if breaker.tool_history:
        result["tool_trace"] = list(result.get("tool_trace") or []) + [
            f"breaker:{json.dumps(breaker.snapshot(), ensure_ascii=False)}"
        ]

    # 流式合并后再次强制补齐缺图，并定稿
    yield {"type": "status", "message": "正在核对配图…"}
    ans0 = str(result.get("answer") or "")
    gen_pairs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", ans0)
    ans0, gen_pairs, tr = _force_missing_drawings(
        ans0, question, [(a, u) for a, u in gen_pairs], list(result.get("tool_trace") or [])
    )
    ans0, gen_pairs, tr = _fill_unfilled_draw_markers(
        ans0, question, gen_pairs, tr
    )
    result["tool_trace"] = tr
    ans = _collapse_repetitive_text(ans0)
    ans = _bind_draw_images(ans, gen_pairs)
    ans = strip_unfilled_draw_markers(_relocate_inline_draw_images(ans))
    result["answer"] = ans
    if ans:
        # 全文（含已嵌入配图）就绪后再假流式给用户
        async for ev in _fake_stream_text(ans):
            yield ev
    elif streamed_any:
        pass

    for url in result.get("images") or []:
        yield {"type": "image", "url": url}

    yield {"type": "react_done", "result": result}

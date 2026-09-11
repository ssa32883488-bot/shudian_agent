# -*- coding: utf-8 -*-
"""课本插图块：从 chunk 中的「图x.x.x / 图x-x-x」捞图，供 LLM 的文字占位与回填。

约定（发给大模型）：
  <<<FIGURE id="图2.2.1(a)" path="/media/chapters/xxx.jpg" desc="……">>>

- 不向模型传二进制图片，只传上述文字块
- 模型可整块删除不需要的 FIGURE；保留的块禁止改格式/字段
- 对用户展示前：replace_figure_markers → Markdown 图片
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Optional
from urllib.parse import unquote, urlparse

# 图 2.2.1 / 图2-2-1 / 图P4.1 / 图 2.2.1(a)
FIG_ID_RE = re.compile(
    r"图\s*(?P<body>(?:P?\d+)(?:[\.\-．]\d+)*(?:\([a-z]\))?)",
    re.IGNORECASE,
)

FIGURE_MARKER_RE = re.compile(
    r'<<<FIGURE\s+id="(?P<id>[^"]*)"\s+path="(?P<path>[^"]*)"\s+desc="(?P<desc>[^"]*)"\s*>>>',
    re.DOTALL,
)

FIGURE_MARKER_TMPL = '<<<FIGURE id="{id}" path="{path}" desc="{desc}">>>'


@dataclass
class FigureBlock:
    fig_id: str
    path: str
    desc: str
    chunk_id: str = ""

    def marker(self) -> str:
        return FIGURE_MARKER_TMPL.format(
            id=_esc(self.fig_id),
            path=_esc(self.path),
            desc=_esc(self.desc),
        )

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["marker"] = self.marker()
        return d


def _esc(s: str) -> str:
    return (s or "").replace('"', "'").replace("\n", " ").strip()


def normalize_fig_id(raw: str) -> str:
    """统一为「图2.2.1(a)」形态（点分、去空格）。"""
    s = (raw or "").strip()
    if not s:
        return ""
    if not s.startswith("图"):
        s = "图" + s
    s = s.replace(" ", "").replace("．", ".").replace("-", ".")
    # 图P4.1 保留 P
    return s


def find_fig_ids_in_text(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for m in FIG_ID_RE.finditer(text or ""):
        fid = normalize_fig_id("图" + m.group("body"))
        if fid and fid not in seen:
            # 过滤过短噪声：图3 / 图5（无小节号）——仍保留若正文仅此
            body = m.group("body")
            if re.fullmatch(r"\d+", body or ""):
                continue
            seen.add(fid)
            found.append(fid)
    return found


def _desc_near_fig(text: str, fig_id: str, window: int = 120) -> str:
    """取图号附近一句作为文字描述（给模型，非图片本身）。"""
    t = text or ""
    # 宽松定位
    key = fig_id.replace("图", "图\\s*")
    key = key.replace(".", r"[\.\-．]")
    m = re.search(key, t)
    if not m:
        # 试父图号 图2.2.1(a) → 图2.2.1
        parent = re.sub(r"\([a-z]\)$", "", fig_id)
        if parent != fig_id:
            return _desc_near_fig(t, parent, window)
        return f"{fig_id}（教材插图）"
    start = max(0, m.start() - 20)
    end = min(len(t), m.end() + window)
    snip = re.sub(r"\s+", " ", t[start:end]).strip()
    if len(snip) > 160:
        snip = snip[:157] + "…"
    return snip or f"{fig_id}（教材插图）"


def _to_public_path(url_or_path: str, media_base: str = "") -> str:
    """本地绝对路径 / 已是 http → 尽量变成 /media/... 或原 http。"""
    u = (url_or_path or "").strip()
    if not u:
        return ""
    if u.startswith("http://") or u.startswith("https://"):
        return u
    # file path → basename under chapters/guide
    name = u.replace("\\", "/").split("/")[-1]
    if not name:
        return u
    kind = "guide" if "/guide/" in u.replace("\\", "/").lower() or "学习辅导" in u else "chapters"
    if media_base:
        return f"{media_base.rstrip('/')}/{kind}/{name}"
    return f"/media/{kind}/{name}"


def extract_figures_from_chunk(
    *,
    text: str,
    figure_ids: list[str] | str | None = None,
    media_urls: list[str] | str | None = None,
    chunk_id: str = "",
    media_base: str = "",
) -> list[FigureBlock]:
    """chunk 内只要出现「图x…」或已有 figure_ids/media，则按图号捞齐对应图片路径。

    配对策略：
    1) figure_ids 与 media_urls 等长 → 按下标 zip（主路径，约 95% 数据）
    2) 否则：正文图号 ∪ figure_ids，按顺序对齐 media；多余 media 用「图(附N)」补齐
    """
    if isinstance(figure_ids, str):
        figure_ids = [x.strip() for x in figure_ids.split(",") if x.strip()]
    if isinstance(media_urls, str):
        media_urls = [x.strip() for x in media_urls.split(",") if x.strip()]
    figure_ids = list(figure_ids or [])
    media_urls = list(media_urls or [])

    text_figs = find_fig_ids_in_text(text or "")
    # 触发条件：正文有图号，或元数据有 figure_ids/media
    if not text_figs and not figure_ids and not media_urls:
        return []

    meta_figs = [normalize_fig_id(f) for f in figure_ids if f]
    paths = [_to_public_path(u, media_base) for u in media_urls]
    paths = [p for p in paths if p]

    blocks: list[FigureBlock] = []
    if meta_figs and paths and len(meta_figs) == len(paths):
        for fid, path in zip(meta_figs, paths):
            blocks.append(
                FigureBlock(
                    fig_id=fid,
                    path=path,
                    desc=_desc_near_fig(text, fid),
                    chunk_id=chunk_id,
                )
            )
        return blocks

    # 合并图号：正文优先顺序，再补 meta
    ordered: list[str] = []
    seen: set[str] = set()
    for fid in text_figs + meta_figs:
        if fid and fid not in seen:
            seen.add(fid)
            ordered.append(fid)

    if not ordered and paths:
        # 仅有图无可靠图号：仍全部捞出
        for i, path in enumerate(paths, 1):
            fid = f"图(附{i})"
            blocks.append(
                FigureBlock(
                    fig_id=fid,
                    path=path,
                    desc=f"教材插图（chunk={chunk_id or '?'} 附带图{i}）",
                    chunk_id=chunk_id,
                )
            )
        return blocks

    for i, fid in enumerate(ordered):
        path = paths[i] if i < len(paths) else ""
        if not path:
            # 无路径则跳过（测「找全」时计为缺失）
            continue
        blocks.append(
            FigureBlock(
                fig_id=fid,
                path=path,
                desc=_desc_near_fig(text, fid),
                chunk_id=chunk_id,
            )
        )
    # 多余图片仍全部带上
    if len(paths) > len(ordered):
        for j, path in enumerate(paths[len(ordered) :], 1):
            blocks.append(
                FigureBlock(
                    fig_id=f"图(附{j})",
                    path=path,
                    desc=f"教材插图（同切片附加图{j}）",
                    chunk_id=chunk_id,
                )
            )
    return blocks


def figures_to_llm_appendix(figures: list[FigureBlock], *, chunk_text: str = "") -> str:
    """拼进工具结果/上下文：正文摘录 + FIGURE 文字块（无图片二进制）。"""
    parts: list[str] = []
    if chunk_text:
        parts.append(chunk_text.strip())
    if figures:
        parts.append("【教材插图占位——保留原格式，勿改字段；不需要的整块删除】")
        for f in figures:
            parts.append(f.marker())
    return "\n".join(parts)


def replace_figure_markers(text: str) -> str:
    """把保留下来的 FIGURE 标记替换为 Markdown 图片，给用户看。"""

    def _sub(m: re.Match[str]) -> str:
        fid = m.group("id") or "教材插图"
        path = m.group("path") or ""
        desc = m.group("desc") or fid
        if not path:
            return f"（缺图：{fid}）"
        alt = desc[:60] if desc else fid
        return f"![{alt}]({path})"

    return FIGURE_MARKER_RE.sub(_sub, text or "")


def collect_marker_paths(text: str) -> list[str]:
    return [m.group("path") for m in FIGURE_MARKER_RE.finditer(text or "") if m.group("path")]


# 系统提示中复用的规则说明
FIGURE_SYSTEM_RULES = """
教材插图规则（必须遵守）：
1. 检索工具返回的插图以特殊文字块给出，格式固定为单行：
   <<<FIGURE id="图号" path="图片URL或路径" desc="文字描述">>>
2. 禁止改动上述块的格式与字段名；禁止把 path 改成别的地址；禁止编造未给出的 FIGURE 块。
3. 可按讲解需要整块删除不需要的 <<<FIGURE ...>>>；需要保留的块必须原样输出。
4. 不要输出真实图片二进制或 HTML <img>；也不要自行把 FIGURE 改成 ![ ](url)——系统会在返回用户前自动替换。
5. 解答中引用插图时，直接保留对应 FIGURE 块即可。
""".strip()

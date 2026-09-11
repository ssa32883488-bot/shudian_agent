/**
 * Markdown + KaTeX 渲染器（全站公式统一入口）
 * 支持：$...$ / $$...$$ / \(...\) / \[...\] ，以及 GFM 基础语法
 * 另：教材答案中偶发的 <table> HTML 会安全保留并渲染
 */

import katex from 'katex'
import MarkdownIt from 'markdown-it'
import multimdTable from 'markdown-it-multimd-table'

import 'katex/dist/katex.min.css'

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
})

// markdown-it@15 移除了 utils.assign；旧版 table 插件仍依赖它
const mdUtils = md.utils as unknown as { assign?: typeof Object.assign }
if (typeof mdUtils.assign !== 'function') {
  mdUtils.assign = Object.assign
}

md.use(multimdTable, {
  multiline: false,
  rowspan: false,
  headerless: true,
})

/** 不含 markdown 特殊字符的占位符，避免被强调/代码规则拆坏 */
function mathToken(i: number): string {
  return `§§MATH${i}§§`
}

function htmlBlockToken(i: number): string {
  return `§§HTML${i}§§`
}

interface MathSlot {
  token: string
  html: string
}

function renderKatex(tex: string, displayMode: boolean): string {
  try {
    return katex.renderToString(normalizeTex(tex), {
      displayMode,
      throwOnError: false,
      strict: 'ignore',
      trust: false,
      errorColor: '#64748b',
    })
  } catch {
    return `<code class="math-fallback">${escapeHtml(tex)}</code>`
  }
}

/** 常见 LLM / 教材噪声归一 */
function normalizeTex(tex: string): string {
  return tex
    .trim()
    .replace(/\u00a0/g, ' ')
    .replace(/＄/g, '\\$')
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** 表格单元格内常见 $...$ / \\(...\\) → KaTeX（html:false 时表格整块旁路 markdown-it） */
function renderMathInHtmlFragment(html: string): string {
  let s = html
  s = s.replace(/\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]/g, (_m, a: string, b: string) =>
    renderKatex(a ?? b ?? '', true),
  )
  s = s.replace(/\$((?:\\.|[^$\\])+)\$|\\\(([\s\S]+?)\\\)/g, (m, a: string, b: string) => {
    const tex = (a ?? b ?? '').trim()
    if (!tex) return m
    return renderKatex(tex, false)
  })
  return s
}

/** 仅允许表格相关标签，去掉事件属性 */
function sanitizeTableHtml(raw: string): string {
  let s = raw
  s = s.replace(/<\/?(?:script|style|iframe|object|embed)[^>]*>/gi, '')
  s = s.replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, '')
  s = s.replace(/\s(href|src)\s*=\s*("|')\s*javascript:[^"']*\2/gi, '')
  const allowed = /^<\/?(?:table|thead|tbody|tfoot|tr|th|td|caption)(\s[^>]*)?>$/i
  s = s.replace(/<\/?[a-zA-Z][^>]*>/g, (tag) => {
    const compact = tag.replace(/\s+/g, ' ').trim()
    if (allowed.test(tag) || allowed.test(compact)) {
      return tag.replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, '')
    }
    return escapeHtml(tag)
  })
  s = renderMathInHtmlFragment(s)
  return `<div class="md-html-table">${s}</div>`
}

/**
 * 抽取教材 HTML 表格，避免被 markdown-it（html:false）转义成可见源码
 */
function extractHtmlTables(source: string): { text: string; slots: MathSlot[] } {
  const slots: MathSlot[] = []
  let i = 0
  const text = source.replace(/<table\b[\s\S]*?<\/table>/gi, (m) => {
    const token = htmlBlockToken(i++)
    slots.push({ token, html: sanitizeTableHtml(m) })
    return `\n\n${token}\n\n`
  })
  return { text, slots }
}

/**
 * 抽取并渲染公式；代码围栏内不处理。
 */
function extractMath(source: string): { text: string; slots: MathSlot[] } {
  const slots: MathSlot[] = []
  let i = 0
  const codeStore: string[] = []

  // 1) 保护 fenced / inline code
  let text = source.replace(/```[\s\S]*?```/g, (m) => {
    const idx = codeStore.length
    codeStore.push(m)
    return `§§CODE${idx}§§`
  })
  text = text.replace(/`[^`\n]+`/g, (m) => {
    const idx = codeStore.length
    codeStore.push(m)
    return `§§CODE${idx}§§`
  })

  // 2) 块级公式
  text = text.replace(/\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]/g, (_m, a: string, b: string) => {
    const token = mathToken(i++)
    slots.push({ token, html: renderKatex(a ?? b ?? '', true) })
    return token
  })

  // 3) 行内公式
  text = text.replace(/\$((?:\\.|[^$\\])+)\$|\\\(([\s\S]+?)\\\)/g, (m, a: string, b: string) => {
    const tex = (a ?? b ?? '').trim()
    if (!tex) return m
    const token = mathToken(i++)
    slots.push({ token, html: renderKatex(tex, false) })
    return token
  })

  // 4) 还原代码占位（仍为 markdown 源码）
  text = text.replace(/§§CODE(\d+)§§/g, (_m, n: string) => codeStore[Number(n)] ?? '')

  return { text, slots }
}

function restoreSlots(html: string, slots: MathSlot[]): string {
  let out = html
  for (const slot of slots) {
    if (out.includes(slot.token)) {
      out = out.split(slot.token).join(slot.html)
    }
    const escaped = escapeHtml(slot.token)
    if (out.includes(escaped)) {
      out = out.split(escaped).join(slot.html)
    }
  }
  return out
}

/**
 * 去掉灌库/识图残留的图注垃圾行（真图用 Markdown ![]() 展示即可）。
 * 例：单独的「图5.5.16 …」、[图5.5.16]、[图5.5.16描述]…、**配图** 标题行。
 */
export function stripVisionCaptionNoise(source: string): string {
  if (!source) return ''
  let s = source
  // JS 用 m 标志，不支持 Python 的 (?m)
  s = s.replace(/^[ \t]*\*\*配图\*\*[ \t]*\n*/gm, '')
  s = s.replace(/^[ \t]*\[图[^\]]*描述\][^\n]*\n?/gm, '')
  s = s.replace(/^[ \t]*\[图[^\]]+\][^\n]*\n?/gm, '')
  // 「图x.y.z 例… / 题…」说明行（非句中引用）
  s = s.replace(
    /^[ \t]*图[ \t]*[PA]?\d+(?:[.\uFF0E]\d+)*(?:\([a-z]\))?[ \t]+(?:例|题|习题)[^\n]*\n?/gm,
    '',
  )
  s = s.replace(/\n{3,}/g, '\n\n')
  return s
}

/**
 * 将 Markdown（可含公式）渲染为安全 HTML。
 */
export function renderMarkdown(source: string): string {
  if (!source) return ''

  // 兼容后端偶发把换行写成字面 \\n
  // 题库配图常写成 http://127.0.0.1:8000/media/...，开发态后端多在 8001，
  // 统一改写为同源 /media/...，走 Vite 代理。
  const normalized = stripVisionCaptionNoise(
    source
      .replace(/\\n/g, '\n')
      .replace(/https?:\/\/(?:127\.0\.0\.1|localhost):\d+\/media\//gi, '/media/'),
  )

  const tables = extractHtmlTables(normalized)
  const { text, slots } = extractMath(tables.text)
  let html = md.render(text)
  html = restoreSlots(html, [...tables.slots, ...slots])

  return html
}

/** 粗判一段文本是否可能含公式 */
export function looksLikeFormula(text: string): boolean {
  if (!text) return false
  return /\$\$|\$[^$]+\$|\\\(|\\\[|\\begin\{|[_^]\{/.test(text)
}

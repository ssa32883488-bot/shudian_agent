/**
 * 解题 API 适配层。
 *
 * 背景：任务约定与后端并行开发中的 Schema 可能不完全一致。
 * - 任务约定请求：{ text, image, student_id }
 * - 当前后端 Schema：{ text, image_base64, student_id }
 * - 任务约定响应：{ source: answer_bank|ai_solve, answer, images, note }
 * - 当前后端响应：{ trust_level: authoritative|ai_reference, trust_label, answer, analysis, hit, ... }
 *
 * 本文件把「发请求 / 收响应」都归一到前端类型，后端字段变更时优先改这里。
 */

import type {
  NormalizedSolveResult,
  SolveRequestPayload,
  TrustSource,
} from '@/types/solve'

/** 宪法规定的默认角标文案 */
export const TRUST_LABELS: Record<TrustSource, string> = {
  answer_bank: '已收录权威答案',
  ai_solve: 'AI解答，仅供参考·不一定准确',
}

/** 将前端规范化请求转为后端可接受的 body（兼容双字段名） */
export function toBackendSolveBody(payload: SolveRequestPayload): Record<string, unknown> {
  const body: Record<string, unknown> = {
    // 两边都认 text
    text: payload.text || null,
    // student_id：后端当前为 Optional[int]，能转数字就转，否则原样字符串
    student_id: coerceStudentId(payload.student_id),
  }

  if (payload.image) {
    // 任务约定字段
    body.image = payload.image
    // 当前后端字段
    body.image_base64 = payload.image
  }
  if (payload.thread_id) {
    body.thread_id = payload.thread_id
  }
  if (payload.client_message_id) {
    body.client_message_id = payload.client_message_id
  }
  if (payload.reflow_stem) {
    body.reflow_stem = payload.reflow_stem
  }
  if (payload.reflow_image_path) {
    body.reflow_image_path = payload.reflow_image_path
  }

  return body
}

function coerceStudentId(id: string): string | number {
  const n = Number(id)
  if (id !== '' && Number.isFinite(n) && String(n) === id.trim()) {
    return n
  }
  return id
}

/**
 * 将任意后端响应归一为 NormalizedSolveResult。
 * 优先识别任务约定字段，其次兼容当前后端 trust_level 字段。
 */
export function normalizeSolveResponse(raw: unknown): NormalizedSolveResult {
  const data = (raw && typeof raw === 'object' ? raw : {}) as Record<string, unknown>

  const source = resolveTrustSource(data)
  const images = Array.isArray(data.images)
    ? (data.images as unknown[]).filter((x): x is string => typeof x === 'string')
    : []

  const note =
    (typeof data.note === 'string' && data.note) ||
    (typeof data.trust_label === 'string' && data.trust_label) ||
    TRUST_LABELS[source]

  const trustLabel =
    (typeof data.trust_label === 'string' && data.trust_label) || TRUST_LABELS[source]

  const hit =
    typeof data.hit === 'boolean'
      ? data.hit
      : source === 'answer_bank'

  const kgRaw = data.kg_context
  const kgContext =
    kgRaw && typeof kgRaw === 'object'
      ? (kgRaw as NormalizedSolveResult['kgContext'])
      : null

  return {
    source,
    answer: appendProvenanceMarkdown(buildAnswerMarkdown(data, source), {
      source,
      hit,
      kg: kgContext,
      hitQuestionId: data.hit_question_id,
    }),
    images,
    note,
    trustLabel,
    hit,
    kgContext,
    raw,
  }
}

function resolveTrustSource(data: Record<string, unknown>): TrustSource {
  // 1) 任务约定：source = answer_bank | ai_solve
  if (data.source === 'answer_bank' || data.source === 'ai_solve') {
    return data.source
  }

  // 2) 当前后端：trust_level = authoritative | ai_reference
  if (data.trust_level === 'authoritative') return 'answer_bank'
  if (data.trust_level === 'ai_reference') return 'ai_solve'

  // 3) 兜底：有 hit 字段
  if (data.hit === true) return 'answer_bank'
  if (data.hit === false) return 'ai_solve'

  // 默认按 AI 现解处理（更安全：宁可多标「仅供参考」）
  return 'ai_solve'
}

/**
 * 气泡正文：只保留答案；题库命中时可附「解析」。
 * 不展示 ReAct 工具轨迹 / 考点逻辑链等思考链路。
 */
function buildAnswerMarkdown(
  data: Record<string, unknown>,
  source: TrustSource,
): string {
  const parts: string[] = []

  if (typeof data.answer === 'string' && data.answer.trim()) {
    parts.push(tidyAssistantMarkdown(data.answer.trim()))
  }

  // 仅权威题库的讲解性 analysis 可展示；工具轨迹一律丢弃
  if (
    source === 'answer_bank' &&
    typeof data.analysis === 'string' &&
    isPedagogicalAnalysis(data.analysis)
  ) {
    parts.push('### 解析\n\n' + data.analysis.trim())
  }

  if (!parts.length && typeof data.content === 'string') {
    parts.push(tidyAssistantMarkdown(data.content))
  }
  if (!parts.length && typeof data.markdown === 'string') {
    parts.push(tidyAssistantMarkdown(data.markdown))
  }

  return parts.join('\n\n') || '_（未返回答案内容）_'
}

/** 题库讲解：排除 ReAct / 工具 / 考点链噪音 */
function isPedagogicalAnalysis(raw: string): boolean {
  const t = raw.trim()
  if (!t || t.length < 8) return false
  if (/本轮工具|本轮未调用工具|ReAct|call:|result:/.test(t)) return false
  if (/^\*\*考点\*\*/m.test(t) || /^\*\*逻辑链\*\*/m.test(t)) return false
  return true
}

/**
 * 轻度整理模型输出：去掉易碎伪表格表头，保证列表可读。
 */
function tidyAssistantMarkdown(src: string): string {
  let s = src.replace(/\r\n/g, '\n').trim()
  // 去掉单独一行的「功能 … 说明」伪表头
  s = s.replace(/^[ \t]*功能[ \t]+说明[ \t]*$/gm, '')
  // 压缩多余空行
  s = s.replace(/\n{3,}/g, '\n\n')
  return s.trim()
}

type ProvenanceInput = {
  source: TrustSource
  hit: boolean
  kg: NormalizedSolveResult['kgContext'] | null | undefined
  hitQuestionId?: unknown
}

/**
 * 气泡底部只挂「溯源」，不展示学习/思考逻辑链。
 */
function appendProvenanceMarkdown(answer: string, info: ProvenanceInput): string {
  // 寒暄/能力介绍不挂溯源
  const head = answer.trim().slice(0, 80)
  if (/^你好/.test(head) || /我是.+助学导师|我能帮你做什么/.test(answer.slice(0, 400))) {
    return answer
  }

  const lines: string[] = ['### 溯源']
  if (info.source === 'answer_bank' || info.hit) {
    const qid =
      typeof info.hitQuestionId === 'number' || typeof info.hitQuestionId === 'string'
        ? `（题库 #${info.hitQuestionId}）`
        : ''
    lines.push(`- **来源**：正式题库${qid}`)
  } else {
    lines.push('- **来源**：AI 现解（仅供参考）')
  }

  const kg = info.kg
  const keywords = kg?.keywords || []
  const problems = (kg?.related_problems || [])
    .map((p) => p.problem_id)
    .filter(Boolean)

  if (keywords.length) {
    lines.push(`- **知识点**：${keywords.slice(0, 8).join('、')}`)
  }
  if (problems.length) {
    lines.push(`- **相关题**：${problems.slice(0, 8).join('、')}`)
  }

  // 只有「来源」且无其它线索时，寒暄类已 return；解题类仍展示来源
  if (lines.length <= 2 && !keywords.length && !problems.length && info.source === 'ai_solve') {
    // AI 现解且无图谱线索：仍保留一行来源溯源
  }

  return `${answer}\n\n${lines.join('\n')}`
}

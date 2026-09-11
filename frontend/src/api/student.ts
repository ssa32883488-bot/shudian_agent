import http from '@/api/http'
import {
  normalizeSolveResponse,
  toBackendSolveBody,
} from '@/api/adapters/solve'
import type { NormalizedSolveResult, SolveRequestPayload } from '@/types/solve'

/** POST /api/student/solve —— 学生解题（文字 / 图片，非流式） */
export async function solveQuestion(
  payload: SolveRequestPayload,
): Promise<NormalizedSolveResult> {
  const body = toBackendSolveBody(payload)
  const { data } = await http.post('/api/student/solve', body)
  return normalizeSolveResponse(data)
}

export type SolveStreamHandlers = {
  onStatus?: (message: string) => void
  onDelta?: (text: string) => void
  onDeltaReset?: () => void
  onAnswerReplace?: (text: string) => void
  onImage?: (url: string) => void
  onToolStart?: (name: string) => void
  onToolEnd?: (name: string) => void
  onFinal?: (result: NormalizedSolveResult) => void
  onError?: (message: string) => void
}

/**
 * POST /api/student/solve/stream —— SSE 流式解题。
 * 使用 fetch（axios 不适合 SSE）；鉴权头与 http 拦截器一致。
 */
export async function solveQuestionStream(
  payload: SolveRequestPayload,
  handlers: SolveStreamHandlers,
  signal?: AbortSignal,
): Promise<NormalizedSolveResult> {
  const body = toBackendSolveBody(payload)
  const base = import.meta.env.VITE_API_BASE_URL || ''
  const token = localStorage.getItem('shudian_auth_token')

  const res = await fetch(`${base}/api/student/solve/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
    signal,
  })

  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    try {
      const j = await res.json()
      if (typeof j?.detail === 'string') detail = j.detail
    } catch {
      /* ignore */
    }
    handlers.onError?.(detail)
    throw new Error(detail)
  }

  if (!res.body) {
    const msg = '浏览器未拿到响应流'
    handlers.onError?.(msg)
    throw new Error(msg)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''
  let finalResult: NormalizedSolveResult | null = null

  const handleEvent = (raw: string) => {
    const dataLine = raw
      .split('\n')
      .filter((l) => l.startsWith('data:'))
      .map((l) => l.slice(5).trimStart())
      .join('\n')
    if (!dataLine || dataLine === '[DONE]') return
    let ev: Record<string, unknown>
    try {
      ev = JSON.parse(dataLine) as Record<string, unknown>
    } catch {
      return
    }
    const type = String(ev.type || '')
    switch (type) {
      case 'status':
        if (typeof ev.message === 'string') handlers.onStatus?.(ev.message)
        break
      case 'delta':
        if (typeof ev.text === 'string') handlers.onDelta?.(ev.text)
        break
      case 'delta_reset':
        handlers.onDeltaReset?.()
        break
      case 'answer_replace':
        if (typeof ev.text === 'string') handlers.onAnswerReplace?.(ev.text)
        break
      case 'image':
        if (typeof ev.url === 'string') handlers.onImage?.(ev.url)
        break
      case 'tool_start':
        if (typeof ev.name === 'string') handlers.onToolStart?.(ev.name)
        break
      case 'tool_end':
        if (typeof ev.name === 'string') handlers.onToolEnd?.(ev.name)
        break
      case 'final': {
        const result = normalizeSolveResponse(ev.result)
        finalResult = result
        handlers.onFinal?.(result)
        break
      }
      case 'error': {
        const msg = typeof ev.message === 'string' ? ev.message : '流式解题失败'
        handlers.onError?.(msg)
        throw new Error(msg)
      }
      default:
        break
    }
  }

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    // SSE 事件以空行分隔
    let idx: number
    while ((idx = buffer.indexOf('\n\n')) >= 0) {
      const chunk = buffer.slice(0, idx)
      buffer = buffer.slice(idx + 2)
      if (chunk.trim()) handleEvent(chunk)
    }
  }
  if (buffer.trim()) handleEvent(buffer)

  if (!finalResult) {
    const msg = '流式结束但未收到 final 事件'
    handlers.onError?.(msg)
    throw new Error(msg)
  }
  return finalResult
}

/** POST /api/student/parse-file —— MinerU 解析 Word/PDF/PPT 等 */
export async function parseUploadFile(file: File): Promise<{
  ok: boolean
  filename: string
  kind: string
  engine?: string
  chars: number
  text: string
}> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await http.post('/api/student/parse-file', form, {
    timeout: 600_000,
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

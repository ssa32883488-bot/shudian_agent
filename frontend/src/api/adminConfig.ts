import http from '@/api/http'

export type TraceStatus =
  | 'ok'
  | 'bank_hit'
  | 'validate_fail'
  | 'error'
  | 'ai_reference'
  | string

export interface AgentTraceItem {
  id: number
  student_id?: number | null
  nickname?: string | null
  thread_id?: string | null
  question_preview: string
  answer_preview?: string | null
  steps: string[]
  hit: boolean
  status: TraceStatus
  intent?: string | null
  validate_passed?: boolean | null
  validate_score?: number | null
  trust_label?: string | null
  tool_trace?: string[]
  error?: string | null
  detail?: Record<string, unknown>
  created_at?: string | null
}

export async function listAgentTraces(params?: {
  limit?: number
  student_id?: number
  status?: string
  q?: string
}): Promise<{ items: AgentTraceItem[]; privacy_note?: string }> {
  const { data } = await http.get<{
    ok: boolean
    items: AgentTraceItem[]
    privacy_note?: string
  }>('/api/admin/traces', { params })
  return { items: data.items || [], privacy_note: data.privacy_note }
}

export async function getAgentTrace(id: number): Promise<AgentTraceItem> {
  const { data } = await http.get<{ ok: boolean; item: AgentTraceItem }>(
    `/api/admin/traces/${id}`,
  )
  return data.item
}

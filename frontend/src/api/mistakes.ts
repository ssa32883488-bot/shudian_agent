import http from '@/api/http'

export interface MistakeItem {
  id: number
  question_snapshot: string
  answer_snapshot?: string | null
  reason?: string | null
  add_source?: string | null
  knowledge_tags?: Record<string, unknown> | null
  added_at?: string | null
}

export interface MistakeCreatePayload {
  question_snapshot: string
  answer_snapshot?: string
  reason?: string
  question_id?: number
  knowledge_tags?: Record<string, unknown>
  add_source?: string
}

export interface MistakeUpdatePayload {
  reason?: string
  answer_snapshot?: string
}

export async function listMistakes(): Promise<MistakeItem[]> {
  const { data } = await http.get<{ ok: boolean; items: MistakeItem[] }>(
    '/api/student/mistakes',
  )
  return data.items
}

export async function createMistake(payload: MistakeCreatePayload): Promise<number> {
  const { data } = await http.post<{ ok: boolean; id: number }>(
    '/api/student/mistakes',
    payload,
  )
  return data.id
}

export async function updateMistake(
  id: number,
  payload: MistakeUpdatePayload,
): Promise<void> {
  await http.put(`/api/student/mistakes/${id}`, payload)
}

export async function deleteMistake(id: number): Promise<void> {
  await http.delete(`/api/student/mistakes/${id}`)
}

export async function importMistakes(
  items: Array<{
    question: string
    answer?: string
    reason?: string
    question_id?: number
    knowledge_tags?: Record<string, unknown>
  }>,
): Promise<number> {
  const { data } = await http.post<{ ok: boolean; count: number }>(
    '/api/student/mistakes/import',
    { items },
  )
  return data.count
}

export async function exportMistakesWord(): Promise<Blob> {
  const { data } = await http.get<Blob>('/api/student/mistakes/export-word', {
    responseType: 'blob',
  })
  return data
}

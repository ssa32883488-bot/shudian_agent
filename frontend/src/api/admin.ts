import http from '@/api/http'

export interface BankItem {
  id: number
  content: string
  answer: string
  analysis?: string | null
  knowledge_tags?: Record<string, unknown> | null
  source?: string | null
  status: string
  score?: number
  match_via?: string
  needs_kg_review?: boolean
}

export interface BankSearchResult {
  ok: boolean
  mode: 'latest' | 'search' | 'concept' | string
  query: string
  concept?: string | null
  matched_concepts: string[]
  limit: number
  items: BankItem[]
}

export interface NearDupItem {
  question_id: number
  content: string
  answer?: string
  source?: string | null
  score: number
}

export interface ReflowItem {
  id: number
  question: string
  ai_answer: string
  validate_score?: number | string | null
  source?: string | null
  image_path?: string | null
  knowledge_tags?: Record<string, unknown> | null
  created_at?: string | null
  from_memory?: boolean
  has_near_dup?: boolean
  near_dups?: NearDupItem[]
}

export async function searchBank(params?: {
  q?: string
  concept?: string
  limit?: number
  status?: 'active' | 'disabled' | 'all'
}): Promise<BankSearchResult> {
  const { data } = await http.get<BankSearchResult>('/api/admin/bank', {
    params: {
      q: params?.q || undefined,
      concept: params?.concept || undefined,
      limit: params?.limit ?? 20,
      status: params?.status ?? 'active',
    },
  })
  return data
}

/** @deprecated 用 searchBank；保留兼容 */
export async function listBank(): Promise<BankItem[]> {
  const data = await searchBank({ limit: 20 })
  return data.items
}

export async function suggestConcepts(q: string, limit = 12): Promise<string[]> {
  const { data } = await http.get<{ ok: boolean; items: string[] }>(
    '/api/admin/bank/concepts',
    { params: { q: q || '', limit } },
  )
  return data.items || []
}

export async function createBankItem(payload: {
  content: string
  answer: string
  analysis?: string
  knowledge_tags?: Record<string, unknown>
  source?: string
}): Promise<number> {
  const { data } = await http.post<{ ok: boolean; id: number }>('/api/admin/bank', payload)
  return data.id
}

export async function updateBankItem(
  id: number,
  payload: {
    content: string
    answer: string
    analysis?: string
    knowledge_tags?: Record<string, unknown>
    source?: string
    status?: string
  },
): Promise<void> {
  await http.put(`/api/admin/bank/${id}`, payload)
}

export async function deleteBankItem(id: number): Promise<void> {
  await http.delete(`/api/admin/bank/${id}`)
}

export async function listReflow(params?: {
  source?: string
  with_near_dup?: boolean
}): Promise<ReflowItem[]> {
  const { data } = await http.get<{ ok: boolean; items: ReflowItem[] }>(
    '/api/admin/reflow/list',
    { params },
  )
  return data.items
}

export async function approveReflow(
  id: number,
  opts?: { force?: boolean },
): Promise<{
  ok: boolean
  question_id?: number
  needs_confirm?: boolean
  near_dups?: NearDupItem[]
  message?: string
}> {
  const { data } = await http.post<{
    ok: boolean
    question_id?: number
    needs_confirm?: boolean
    near_dups?: NearDupItem[]
    message?: string
  }>(`/api/admin/reflow/${id}/approve`, { force: Boolean(opts?.force) })
  return data
}

export async function rejectReflow(id: number): Promise<void> {
  await http.post(`/api/admin/reflow/${id}/reject`)
}

import http from '@/api/http'

export interface PracticeItem {
  question_id: number
  order_no: number
  content: string
  knowledge_tags?: Record<string, unknown> | null
}

export interface PracticeSession {
  ok: boolean
  session_id: number
  title: string
  mode?: string
  weak_points: string[]
  source: string
  count: number
  items: PracticeItem[]
}

export interface PracticeResultItem {
  id?: number
  question_id: number
  order_no?: number
  content?: string
  question_snapshot?: string
  knowledge_tags?: Record<string, unknown> | null
  answer_text?: string
  answer_images?: string[]
  correct: boolean | null
  ai_score?: number | null
  ai_comment?: string | null
  reference_answer?: string
  analysis?: string | null
  grade_method?: string
  error?: string
}

export interface PracticeSubmitResult {
  ok: boolean
  session_id: number
  total: number
  correct: number
  accuracy: number
  report_notes?: string[]
  results: PracticeResultItem[]
  last_session?: {
    session_id?: number
    correct?: number
    total?: number
    tags?: string[]
    missed_tags?: string[]
    at?: string
  }
  session?: PracticeSessionRecord
}

export type PracticeMode = 'auto' | 'probe' | 'focus' | 'review'

export interface PracticeSessionRecord {
  id: number
  title: string
  mode: string
  source: string
  weak_points: string[]
  status: string
  item_count: number
  correct_count?: number | null
  accuracy?: number | null
  report_notes?: string[]
  created_at?: string | null
  submitted_at?: string | null
}

export interface PracticeSessionDetail {
  ok: boolean
  session: PracticeSessionRecord
  items: PracticeResultItem[]
  results: PracticeResultItem[]
  total?: number | null
  correct?: number | null
  accuracy?: number | null
  report_notes?: string[]
}

export async function generatePractice(
  count = 5,
  opts?: { mode?: PracticeMode | string; tags?: string[] },
): Promise<PracticeSession> {
  const { data } = await http.post<PracticeSession>('/api/student/practice/generate', {
    count,
    mode: opts?.mode || 'auto',
    tags: opts?.tags || [],
  })
  return data
}

export async function submitPractice(
  sessionId: number,
  answers: Array<{ question_id: number; answer_text?: string; images?: string[] }>,
  writeMistakes = true,
): Promise<PracticeSubmitResult> {
  const { data } = await http.post<PracticeSubmitResult>('/api/student/practice/submit', {
    session_id: sessionId,
    answers,
    write_mistakes: writeMistakes,
  })
  return data
}

export async function listPracticeSessions(limit = 30): Promise<PracticeSessionRecord[]> {
  const { data } = await http.get<{ ok: boolean; items: PracticeSessionRecord[] }>(
    '/api/student/practice/sessions',
    { params: { limit } },
  )
  return data.items || []
}

export async function getPracticeSession(sessionId: number): Promise<PracticeSessionDetail> {
  const { data } = await http.get<PracticeSessionDetail>(
    `/api/student/practice/sessions/${sessionId}`,
  )
  return data
}

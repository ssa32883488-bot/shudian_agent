import http from '@/api/http'

export interface StudentProfileData {
  ok: boolean
  student_id: number
  nickname: string
  class_code?: string | null
  basics?: Record<string, unknown>
  mastery: Record<string, number>
  practice_stats: {
    total_solves?: number
    weekly_minutes?: number[]
    weekly_solves?: number[]
    accuracy?: number
    last_session?: {
      correct?: number
      total?: number
      accuracy?: number
      tags?: string[]
      missed_tags?: string[]
      at?: string
    }
    mistake_stats?: {
      count?: number
      top_tags?: Array<{ name: string; count: number }>
    }
    knowledge_radar?: Array<{ name: string; value: number }>
    [key: string]: unknown
  }
  weak_points: string[]
  chapter_progress?: Record<string, unknown>
  mistake_stats?: {
    count?: number
    top_tags?: Array<{ name: string; count: number }>
  }
  recommendations?: Array<{ type: string; label: string; payload?: Record<string, unknown> }>
  recent_topics?: string[]
  topic_freq?: Record<string, number>
  last_summary_at?: string | null
  last_rebuild_at?: string | null
  rebuild_status?: string
  updated_at?: string | null
  privacy_note?: string
}

export interface MemoryConfig {
  ok: boolean
  summary_every_n: number
  keep_recent_k: number
  auth_disabled: boolean
}

export interface SummarizeTurn {
  role: string
  content: string
}

export async function getStudentProfile(): Promise<StudentProfileData> {
  const { data } = await http.get<StudentProfileData>('/api/student/profile')
  return data
}

export async function rebuildStudentProfile(): Promise<StudentProfileData> {
  const { data } = await http.post<StudentProfileData>('/api/student/profile/rebuild')
  return data
}

export async function exportProfileWord(): Promise<Blob> {
  const { data } = await http.get<Blob>('/api/student/profile/export-word', {
    responseType: 'blob',
  })
  return data
}

export async function getMemoryConfig(): Promise<MemoryConfig> {
  const { data } = await http.get<MemoryConfig>('/api/memory/config')
  return data
}

export async function summarizeSession(payload: {
  session_id_client: string
  agent?: string
  turns: SummarizeTurn[]
  turn_from?: number
  turn_to?: number
}): Promise<{
  ok: boolean
  summary_id: number
  summary_text: string
  topics: string[]
  keep_recent_k: number
  profile: StudentProfileData
}> {
  const { data } = await http.post('/api/memory/summarize', payload)
  return data
}

export async function listMySummaries(): Promise<
  Array<{
    id: number
    agent: string
    summary_text: string
    topics: string[]
    created_at?: string | null
  }>
> {
  const { data } = await http.get<{ items: Array<any> }>('/api/memory/summaries/me')
  return data.items || []
}

/** 学生短期会话：服务端权威 + 本地缓存同步 */
import http from '@/api/http'

export type ServerThread = {
  id: string
  title: string
  agent?: string
  archived?: boolean
  summarized_until?: number
  created_at?: string | null
  updated_at?: string | null
  updated_at_ms?: number
}

export type ServerMessage = {
  id: number
  thread_id: string
  role: string
  content: string
  content_format?: string
  attachments?: Array<{ type?: string; url?: string; ref?: string }>
  trust_label?: string | null
  client_message_id?: string | null
  created_at?: string | null
  created_at_ms?: number
}

export async function listThreads(includeArchived = false) {
  const { data } = await http.get<{ ok: boolean; items: ServerThread[] }>(
    '/api/student/threads',
    { params: { include_archived: includeArchived } },
  )
  return data.items || []
}

export async function createThread(payload: { id?: string; title?: string }) {
  const { data } = await http.post<{ ok: boolean; thread: ServerThread }>(
    '/api/student/threads',
    payload,
  )
  return data.thread
}

export async function patchThread(
  threadId: string,
  payload: { title?: string; archived?: boolean; summarized_until?: number },
) {
  const { data } = await http.patch<{ ok: boolean; thread: ServerThread }>(
    `/api/student/threads/${encodeURIComponent(threadId)}`,
    payload,
  )
  return data.thread
}

export async function deleteThread(threadId: string, hard = false) {
  await http.delete(`/api/student/threads/${encodeURIComponent(threadId)}`, {
    params: { hard },
  })
}

export async function fetchMessages(threadId: string) {
  const { data } = await http.get<{ ok: boolean; items: ServerMessage[] }>(
    `/api/student/threads/${encodeURIComponent(threadId)}/messages`,
  )
  return data.items || []
}

export async function postMessage(
  threadId: string,
  payload: {
    role: string
    content: string
    trust_label?: string
    client_message_id?: string
    attachments?: unknown[]
  },
) {
  const { data } = await http.post(
    `/api/student/threads/${encodeURIComponent(threadId)}/messages`,
    payload,
  )
  return data
}

export async function syncThread(payload: {
  thread_id: string
  title?: string
  summarized_until?: number
  messages: Array<{
    role: string
    content: string
    client_message_id?: string
    trust_label?: string
    attachments?: unknown[]
  }>
}) {
  const { data } = await http.post('/api/student/threads/sync', payload)
  return data
}

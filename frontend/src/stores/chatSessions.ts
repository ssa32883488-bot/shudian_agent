/**
 * 助学答疑会话：服务端权威 + 按用户隔离的浏览器 IndexedDB 缓存。
 * 登录后与服务器同步；冲突以服务器 updated_at 为准。
 */
import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { getMemoryConfig, summarizeSession } from '@/api/profile'
import {
  createThread,
  deleteThread,
  fetchMessages,
  listThreads,
  patchThread,
  syncThread,
  type ServerMessage,
} from '@/api/threads'
import type { ChatMessage } from '@/types/solve'
import { useUserStore } from '@/stores/user'

export interface ChatSession {
  id: string
  title: string
  updatedAt: number
  messages: ChatMessage[]
  /** 已摘要到的消息下标（不含该下标之后的未摘要部分） */
  summarizedUntil: number
  /** 是否已从服务端拉取过消息正文 */
  hydrated?: boolean
}

const STORE = 'chat_sessions'
/** 旧版未按用户隔离的库（不再迁入新账号，避免串号） */
const LEGACY_SHARED_DB = 'shudian_memory_v2'
const LEGACY_DB = 'shudian_memory_v1'
const LEGACY_KEY = 'shudian_chat_sessions_v1'
const ACTIVE_KEY_PREFIX = 'shudian_chat_active_id'
const LEGACY_ACTIVE_KEY = 'shudian_chat_active_id'

function uid(prefix = 's'): string {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`
}

function dbNameFor(userId: string): string {
  return `shudian_memory_v2_u${userId}`
}

function activeKeyFor(userId: string): string {
  return `${ACTIVE_KEY_PREFIX}_u${userId}`
}

function openDb(name: string): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(name, 1)
    req.onupgradeneeded = () => {
      const db = req.result
      if (!db.objectStoreNames.contains(STORE)) {
        db.createObjectStore(STORE, { keyPath: 'id' })
      }
    }
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
  })
}

async function idbLoadAll(userId: string): Promise<ChatSession[]> {
  try {
    const db = await openDb(dbNameFor(userId))
    return await new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readonly')
      const req = tx.objectStore(STORE).getAll()
      req.onsuccess = () => resolve((req.result as ChatSession[]) || [])
      req.onerror = () => reject(req.error)
    })
  } catch {
    return []
  }
}

async function idbPut(userId: string, session: ChatSession): Promise<void> {
  const db = await openDb(dbNameFor(userId))
  await new Promise<void>((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite')
    tx.objectStore(STORE).put(session)
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

async function idbDelete(userId: string, id: string): Promise<void> {
  const db = await openDb(dbNameFor(userId))
  await new Promise<void>((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite')
    tx.objectStore(STORE).delete(id)
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

async function idbClear(userId: string): Promise<void> {
  try {
    const db = await openDb(dbNameFor(userId))
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite')
      tx.objectStore(STORE).clear()
      tx.oncomplete = () => resolve()
      tx.onerror = () => reject(tx.error)
    })
  } catch {
    /* ignore */
  }
}

/** 入库前去掉 dataURL/blob 预览，避免配额爆掉 */
function slimSession(session: ChatSession): ChatSession {
  return {
    ...session,
    messages: (session.messages || []).map((m) => {
      const preview = m.imagePreview
      const keepPreview =
        Boolean(preview) &&
        !preview!.startsWith('data:') &&
        !preview!.startsWith('blob:')
      return {
        ...m,
        imagePreview: keepPreview ? preview : undefined,
      }
    }),
  }
}

function titleFromMessages(messages: ChatMessage[]): string {
  const firstUser = messages.find((m) => m.role === 'user' && (m.content || m.imagePreview))
  if (!firstUser) return '新会话'
  const text = (firstUser.content || '').trim()
  if (text) return text.slice(0, 28) + (text.length > 28 ? '…' : '')
  if (firstUser.imagePreview) return '图片提问'
  return '新会话'
}

function serverMsgToLocal(m: ServerMessage): ChatMessage {
  const images =
    (m.attachments || [])
      .filter((a) => a?.type === 'image' && a.url)
      .map((a) => String(a.url)) || []
  return {
    id: m.client_message_id || `srv_${m.id}`,
    role: (m.role as ChatMessage['role']) || 'assistant',
    content: m.content || '',
    trustLabel: m.trust_label || undefined,
    images: images.length ? images : undefined,
    createdAt: m.created_at_ms || Date.now(),
  }
}

export const useChatSessionsStore = defineStore('chatSessions', () => {
  const sessions = ref<ChatSession[]>([])
  const activeId = ref<string>('')
  const ready = ref(false)
  const syncing = ref(false)
  const summaryEveryN = ref(20)
  const keepRecentK = ref(0)
  const summarizing = ref(false)
  /** 当前内存/IDB 绑定的用户；换号必须重置 */
  const boundUserId = ref('')

  const activeSession = computed(
    () => sessions.value.find((s) => s.id === activeId.value) || null,
  )

  const sortedSessions = computed(() =>
    [...sessions.value].sort((a, b) => b.updatedAt - a.updatedAt),
  )

  function currentUserId(): string {
    return useUserStore().studentId || ''
  }

  async function persistSession(session: ChatSession) {
    const userId = boundUserId.value || currentUserId()
    if (!userId) return
    const payload = slimSession(session)
    try {
      await idbPut(userId, payload)
    } catch (err) {
      console.warn('[chatSessions] IndexedDB 写入失败，尝试精简重试', err)
      try {
        await idbPut(userId, {
          ...payload,
          messages: payload.messages.map((m) => ({
            ...m,
            imagePreview: undefined,
            images: (m.images || []).slice(0, 8),
          })),
        })
      } catch (err2) {
        console.error('[chatSessions] IndexedDB 写入仍失败', err2)
      }
    }
  }

  function rememberActiveId(id: string) {
    activeId.value = id
    const userId = boundUserId.value || currentUserId()
    try {
      if (!userId) return
      const key = activeKeyFor(userId)
      if (id) localStorage.setItem(key, id)
      else localStorage.removeItem(key)
    } catch {
      /* ignore */
    }
  }

  /** 登出 / 换号：清空内存态，不读写他人缓存 */
  function reset() {
    try {
      if (boundUserId.value) {
        localStorage.removeItem(activeKeyFor(boundUserId.value))
      }
      localStorage.removeItem(LEGACY_ACTIVE_KEY)
    } catch {
      /* ignore */
    }
    sessions.value = []
    activeId.value = ''
    ready.value = false
    boundUserId.value = ''
    syncing.value = false
    summarizing.value = false
  }

  async function pushSessionToServer(session: ChatSession) {
    try {
      await syncThread({
        thread_id: session.id,
        title: session.title,
        summarized_until: session.summarizedUntil,
        messages: session.messages
          .filter((m) => m.role === 'user' || m.role === 'assistant')
          .filter((m) => !(m.loading || m.error))
          .map((m) => ({
            role: m.role,
            content: m.content || '',
            client_message_id: m.id,
            trust_label: m.trustLabel,
            attachments: (m.images || []).map((url) => ({ type: 'image', url })),
          })),
      })
    } catch (err) {
      console.warn('[chatSessions] sync failed', err)
    }
  }

  async function pullFromServer() {
    syncing.value = true
    try {
      const remote = await listThreads(false)
      const byId = new Map(sessions.value.map((s) => [s.id, s]))
      const merged: ChatSession[] = []
      const seen = new Set<string>()

      for (const t of remote) {
        seen.add(t.id)
        const local = byId.get(t.id)
        const remoteMs = t.updated_at_ms || 0
        if (!local) {
          merged.push({
            id: t.id,
            title: t.title || '新会话',
            updatedAt: remoteMs || Date.now(),
            messages: [],
            summarizedUntil: t.summarized_until || 0,
            hydrated: false,
          })
          continue
        }
        // 服务端较新：保留本地消息若更完整，否则标未 hydrate
        const preferRemoteMeta = remoteMs >= (local.updatedAt || 0)
        merged.push({
          ...local,
          title: preferRemoteMeta ? t.title || local.title : local.title,
          updatedAt: Math.max(local.updatedAt || 0, remoteMs),
          summarizedUntil: Math.max(
            local.summarizedUntil || 0,
            t.summarized_until || 0,
          ),
          hydrated: local.messages?.length ? true : false,
        })
      }

      // 仅本地有的：视为当前用户离线新建，上传到服务器
      // （库已按 userId 隔离，不会再把他人会话灌进来）
      for (const local of sessions.value) {
        if (seen.has(local.id)) continue
        merged.push(local)
        void pushSessionToServer(local)
      }

      sessions.value = merged
      for (const s of merged) void persistSession(s)
    } catch (err) {
      console.warn('[chatSessions] pullFromServer failed，继续用本地缓存', err)
    } finally {
      syncing.value = false
    }
  }

  async function hydrateSession(id: string) {
    const session = sessions.value.find((s) => s.id === id)
    if (!session) return
    if (session.hydrated && session.messages.length) return
    try {
      const items = await fetchMessages(id)
      if (!items.length) {
        session.hydrated = true
        void persistSession(session)
        return
      }
      // 若本地已有更多消息，合并去重
      const byClient = new Map<string, ChatMessage>()
      for (const m of session.messages) byClient.set(m.id, m)
      for (const sm of items) {
        const local = serverMsgToLocal(sm)
        if (!byClient.has(local.id)) byClient.set(local.id, local)
      }
      session.messages = [...byClient.values()].sort(
        (a, b) => (a.createdAt || 0) - (b.createdAt || 0),
      )
      session.hydrated = true
      session.title = titleFromMessages(session.messages) || session.title
      void persistSession(session)
    } catch (err) {
      console.warn('[chatSessions] hydrate failed', err)
    }
  }

  async function boot() {
    const userId = currentUserId()
    if (!userId) {
      reset()
      return
    }
    // 已为同一用户 boot 过则跳过；换号强制重载
    if (ready.value && boundUserId.value === userId) return
    if (boundUserId.value && boundUserId.value !== userId) {
      sessions.value = []
      activeId.value = ''
      ready.value = false
    }
    boundUserId.value = userId

    // 只读当前用户命名空间；不再从共享 LEGACY_SHARED_DB / localStorage 迁入（会串号）
    const loaded = await idbLoadAll(userId)
    sessions.value = loaded.map((s) => ({
      ...s,
      summarizedUntil: s.summarizedUntil ?? 0,
      messages: Array.isArray(s.messages) ? s.messages : [],
      hydrated: Boolean(s.messages?.length),
    }))
    try {
      const cfg = await getMemoryConfig()
      summaryEveryN.value = Math.max(10, cfg.summary_every_n || 20)
      keepRecentK.value = 0
    } catch {
      /* 后端未起时用默认 */
    }
    await pullFromServer()
    try {
      const saved = localStorage.getItem(activeKeyFor(userId)) || ''
      if (saved && sessions.value.some((s) => s.id === saved)) {
        activeId.value = saved
      }
    } catch {
      /* ignore */
    }
    ready.value = true
    ensureActive()
    if (activeId.value) void hydrateSession(activeId.value)

    // 清理旧共享库残留（一次性尽力，失败忽略）
    void indexedDB.deleteDatabase(LEGACY_SHARED_DB)
    void indexedDB.deleteDatabase(LEGACY_DB)
    try {
      localStorage.removeItem(LEGACY_KEY)
      localStorage.removeItem(LEGACY_ACTIVE_KEY)
    } catch {
      /* ignore */
    }
  }

  function ensureActive() {
    if (!ready.value) return
    if (activeId.value && sessions.value.some((s) => s.id === activeId.value)) {
      rememberActiveId(activeId.value)
      return
    }
    if (sessions.value.length) {
      rememberActiveId(sortedSessions.value[0].id)
      return
    }
    createSession()
  }

  function createSession() {
    const session: ChatSession = {
      id: uid('chat'),
      title: '新会话',
      updatedAt: Date.now(),
      messages: [],
      summarizedUntil: 0,
      hydrated: true,
    }
    sessions.value.unshift(session)
    rememberActiveId(session.id)
    void persistSession(session)
    void createThread({ id: session.id, title: session.title }).catch((err) => {
      console.warn('[chatSessions] createThread failed', err)
    })
    return session
  }

  function selectSession(id: string) {
    if (!sessions.value.some((s) => s.id === id)) return
    rememberActiveId(id)
    void hydrateSession(id)
  }

  async function deleteSession(id: string) {
    const userId = boundUserId.value || currentUserId()
    sessions.value = sessions.value.filter((s) => s.id !== id)
    if (userId) await idbDelete(userId, id)
    void deleteThread(id, false).catch(() => undefined)
    if (activeId.value === id) {
      rememberActiveId('')
      ensureActive()
    }
  }

  function touchActive() {
    const session = activeSession.value
    if (!session) return
    session.updatedAt = Date.now()
    session.title = titleFromMessages(session.messages)
    void persistSession(session)
  }

  function flushActive() {
    const session = activeSession.value
    if (!session) return
    session.updatedAt = Date.now()
    void persistSession(session)
    void pushSessionToServer(session)
  }

  function setMessages(messages: ChatMessage[]) {
    const session = activeSession.value
    if (!session) return
    session.messages = messages
    touchActive()
  }

  function patchMessage(
    id: string,
    patch: Partial<ChatMessage>,
    opts?: { persist?: boolean },
  ) {
    const session = activeSession.value
    if (!session) return
    const idx = session.messages.findIndex((m) => m.id === id)
    if (idx < 0) return
    session.messages[idx] = { ...session.messages[idx], ...patch }
    session.updatedAt = Date.now()
    if (opts?.persist !== false) void persistSession(session)
  }

  function appendMessage(message: ChatMessage) {
    const session = activeSession.value
    if (!session) return
    session.messages.push(message)
    touchActive()
  }

  /** 对话积累满 N 轮后上传摘要沉淀画像；本地历史全量保留 */
  async function maybeSummarizeActive() {
    const session = activeSession.value
    if (!session || summarizing.value) return
    const pending = session.messages.slice(session.summarizedUntil)
    if (pending.length < summaryEveryN.value) return

    const chunk = pending.slice(0, summaryEveryN.value)
    const turns = chunk
      .filter((m) => m.role === 'user' || m.role === 'assistant')
      .map((m) => ({
        role: m.role,
        content: (m.content || '').slice(0, 1200),
      }))
      .filter((t) => t.content.trim())

    if (turns.length < 2) {
      session.summarizedUntil += chunk.length
      void persistSession(session)
      return
    }

    summarizing.value = true
    try {
      const turnFrom = session.summarizedUntil
      const turnTo = session.summarizedUntil + chunk.length - 1
      const res = await summarizeSession({
        session_id_client: session.id,
        agent: 'student',
        turns,
        turn_from: turnFrom,
        turn_to: turnTo,
      })
      session.summarizedUntil += chunk.length
      void persistSession(session)
      void patchThread(session.id, {
        summarized_until: session.summarizedUntil,
      }).catch(() => undefined)
      void pushSessionToServer(session)
      return res
    } finally {
      summarizing.value = false
    }
  }

  if (typeof window !== 'undefined') {
    const onHide = () => flushActive()
    window.addEventListener('pagehide', onHide)
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') onHide()
    })
  }

  return {
    sessions,
    activeId,
    activeSession,
    sortedSessions,
    ready,
    syncing,
    summarizing,
    summaryEveryN,
    keepRecentK,
    boundUserId,
    ensureActive,
    createSession,
    selectSession,
    deleteSession,
    setMessages,
    patchMessage,
    appendMessage,
    maybeSummarizeActive,
    flushActive,
    hydrateSession,
    pullFromServer,
    boot,
    reset,
    clearLocalCache: idbClear,
  }
})

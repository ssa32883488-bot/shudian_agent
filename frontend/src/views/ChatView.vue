<script setup lang="ts">
/**
 * 助学答疑：感知优先 → 短 ReAct / Plan 模式（气泡内确认，无弹窗）
 */
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

import StudentLayout from '@/layouts/StudentLayout.vue'
import MessageList from '@/components/chat/MessageList.vue'
import ChatInput, { type ChatSendPayload } from '@/components/chat/ChatInput.vue'
import { solveQuestionStream } from '@/api/student'
import {
  cancelStudentPlan,
  classifyPlanIntent,
  confirmStudentPlan,
  fetchNextPlanItem,
  markPlanDone,
  perceiveAndRoute,
  type PlanTaskItem,
  type RoutePayload,
} from '@/api/studentPlan'
import { useUserStore } from '@/stores/user'
import { useChatSessionsStore } from '@/stores/chatSessions'
import type { ChatMessage } from '@/types/solve'
import { friendlySolveStatus, statusForTool } from '@/utils/solveStatus'
import ByokSettings from '@/components/chat/ByokSettings.vue'
import { createMistake } from '@/api/mistakes'

const user = useUserStore()
const sessions = useChatSessionsStore()
const route = useRoute()

const chatSeed = computed(() => {
  const q = route.query.q
  return typeof q === 'string' ? q : Array.isArray(q) ? String(q[0] || '') : ''
})

const sending = ref(false)
const historyOpen = ref(typeof window === 'undefined' ? true : window.innerWidth > 900)
const busyPlan = ref(false)

/** 当前会话活跃的 Plan */
const activePlanId = ref<string | null>(null)
const activeRoute = ref<RoutePayload | null>(null)
const planAwaitingConfirm = ref(false)
const planCardMessageId = ref<string | null>(null)
const perceivedTextCache = ref('')

const PLAN_STATE_KEY = 'shudian_active_plan_v1'

function persistPlanState() {
  try {
    if (!activePlanId.value) {
      sessionStorage.removeItem(PLAN_STATE_KEY)
      return
    }
    sessionStorage.setItem(
      PLAN_STATE_KEY,
      JSON.stringify({
        planId: activePlanId.value,
        awaiting: planAwaitingConfirm.value,
        route: activeRoute.value,
        perceived: perceivedTextCache.value,
        cardMsgId: planCardMessageId.value,
      }),
    )
  } catch {
    /* ignore */
  }
}

function restorePlanState() {
  try {
    const raw = sessionStorage.getItem(PLAN_STATE_KEY)
    if (!raw) return
    const data = JSON.parse(raw) as {
      planId?: string
      awaiting?: boolean
      route?: RoutePayload | null
      perceived?: string
      cardMsgId?: string | null
    }
    if (!data.planId) return
    activePlanId.value = data.planId
    planAwaitingConfirm.value = Boolean(data.awaiting)
    activeRoute.value = data.route || null
    perceivedTextCache.value = data.perceived || ''
    planCardMessageId.value = data.cardMsgId || null
  } catch {
    /* ignore */
  }
}

watch(
  [activePlanId, planAwaitingConfirm, activeRoute, perceivedTextCache, planCardMessageId],
  () => persistPlanState(),
  { deep: true },
)
onMounted(() => {
  restorePlanState()
  void sessions.boot()
})

if (typeof window !== 'undefined') {
  window.addEventListener('pagehide', () => sessions.flushActive())
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') sessions.flushActive()
  })
}
const messages = computed(() => sessions.activeSession?.messages || [])
const planModeOn = computed(
  () => Boolean(activePlanId.value) && !planAwaitingConfirm.value,
)

function uid(prefix: string) {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 7)}`
}

function friendlyError(err: unknown): string {
  const ax = err as {
    response?: { status?: number; data?: { detail?: unknown } }
    message?: string
    code?: string
    name?: string
  }
  if (ax?.name === 'AbortError') return '已取消'
  if (ax?.code === 'ECONNABORTED') return '解题超时，请稍后重试'
  if (typeof ax?.message === 'string' && ax.message && !ax.response) {
    if (ax.message.includes('Failed to fetch') || ax.message.includes('NetworkError')) {
      return '无法连接后端，请确认服务已启动'
    }
    return ax.message
  }
  if (!ax?.response) return '无法连接后端，请确认服务已启动'
  const detail = ax.response.data?.detail
  if (typeof detail === 'string') return detail
  return ax.message || '解题失败'
}

function formatTime(ts: number) {
  const d = new Date(ts)
  const now = new Date()
  const sameDay =
    d.getFullYear() === now.getFullYear() &&
    d.getMonth() === now.getMonth() &&
    d.getDate() === now.getDate()
  if (sameDay) {
    return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }
  return `${d.getMonth() + 1}/${d.getDate()}`
}

function newSession() {
  activePlanId.value = null
  activeRoute.value = null
  planAwaitingConfirm.value = false
  planCardMessageId.value = null
  perceivedTextCache.value = ''
  sessions.createSession()
}

function selectSession(id: string) {
  sessions.selectSession(id)
}

function removeSession(id: string, ev: Event) {
  ev.stopPropagation()
  sessions.deleteSession(id)
}

async function onAddMistake(msg: ChatMessage) {
  const list = sessions.activeSession?.messages || []
  const idx = list.findIndex((m) => m.id === msg.id)
  let question = ''
  if (idx > 0) {
    for (let i = idx - 1; i >= 0; i -= 1) {
      if (list[i].role === 'user' && list[i].content?.trim()) {
        question = list[i].content.trim()
        break
      }
    }
  }
  if (!question) question = '（答疑会话题干未找到，见下方 AI 解答）'
  const answer = (msg.content || '').trim().slice(0, 4000)
  if (!answer) {
    ElMessage.warning('暂无可保存的解答内容')
    return
  }
  try {
    await createMistake({
      question_snapshot: question.slice(0, 2000),
      answer_snapshot: answer,
      reason: '答疑页手动加入',
      add_source: 'solve',
      knowledge_tags: msg.trustSource ? { source: msg.trustSource } : undefined,
    })
    ElMessage.success('已加入错题本')
  } catch {
    ElMessage.error('加入错题本失败')
  }
}

function turnItems(route: RoutePayload | null | undefined): PlanTaskItem[] {
  if (!route) return []
  const allow = new Set(route.this_turn_ids || [])
  const listed = (route.items || []).filter((i) => allow.has(i.id))
  return listed.length ? listed : (route.items || []).slice(0, 5)
}

async function runSolveStream(
  userText: string,
  payload: ChatSendPayload,
  assistantId: string,
  opts?: {
    skipImage?: boolean
    reflowStem?: string
    reflowImagePath?: string
    userMessageId?: string
  },
) {
  sending.value = true
  const abortCtrl = new AbortController()
  // 后台先凑齐正文+配图再假流式；后端墙钟 180s，前端略放宽留出收尾余量
  const hardTimeout = window.setTimeout(() => {
    if (!abortCtrl.signal.aborted) abortCtrl.abort()
  }, 210_000)
  const liveImages: string[] = []
  let draft = ''
  let gotFinal = false
  let lastStatus = '正在理解题意…'
  const skipImage = Boolean(opts?.skipImage)

  const patchLive = (p: Partial<ChatMessage>) => {
    sessions.patchMessage(assistantId, p, { persist: false })
  }

  const setStatus = (raw: string) => {
    lastStatus = friendlySolveStatus(raw)
    if (!draft) patchLive({ statusText: lastStatus, loading: true })
  }

  try {
    await solveQuestionStream(
      {
        text: userText || undefined,
        image: skipImage ? undefined : payload.imageDataUrl || undefined,
        student_id: user.studentId,
        thread_id: sessions.activeId || undefined,
        client_message_id: opts?.userMessageId,
        reflow_stem: opts?.reflowStem,
        reflow_image_path: opts?.reflowImagePath,
      },
      {
        onStatus: (message) => setStatus(message),
        onDelta: (text) => {
          draft += text
          patchLive({ content: draft, loading: true, statusText: undefined })
        },
        onDeltaReset: () => {
          draft = ''
          patchLive({
            content: '',
            loading: true,
            statusText: lastStatus || '正在调用工具…',
          })
        },
        onAnswerReplace: (text) => {
          draft = text
          patchLive({ content: draft, loading: true, statusText: undefined })
        },
        onImage: (url) => {
          if (!liveImages.includes(url)) liveImages.push(url)
          patchLive({ images: [...liveImages] })
        },
        onToolStart: (name) => setStatus(statusForTool(name, 'start')),
        onToolEnd: (name) => setStatus(statusForTool(name, 'end')),
        onFinal: (res) => {
          gotFinal = true
          const answer = res.answer || draft
          const gallery = Array.isArray(res.images) ? res.images : liveImages
          const inline = new Set(
            [...answer.matchAll(/!\[[^\]]*\]\(([^)]+)\)/g)].map((m) => m[1]),
          )
          sessions.patchMessage(assistantId, {
            loading: false,
            statusText: undefined,
            content: answer,
            trustSource: res.source,
            trustLabel: res.trustLabel,
            images: gallery.filter((u) => u && !inline.has(u)),
            note: res.note,
          })
          sessions.flushActive()
        },
        onError: (message) => {
          if (gotFinal) return
          sessions.patchMessage(assistantId, {
            loading: false,
            statusText: undefined,
            error: message,
            content: draft || '',
          })
        },
      },
      abortCtrl.signal,
    )
  } catch (err) {
    if (!gotFinal) {
      const msg =
        (err as { name?: string })?.name === 'AbortError'
          ? '生成超时已中断，请重试或换题'
          : friendlyError(err)
      sessions.patchMessage(assistantId, {
        loading: false,
        statusText: undefined,
        error: msg,
        content: draft || '',
      })
      if (msg !== '已取消') ElMessage.error(msg)
    }
  } finally {
    window.clearTimeout(hardTimeout)
    sending.value = false
    void sessions.maybeSummarizeActive().then((res) => {
      if (res?.summary_text) ElMessage.success('本轮对话已总结并写入学情画像')
    })
  }
}

function patchPlanCard(
  messageId: string,
  route: RoutePayload,
  planId: string,
  opts: { awaitingConfirm?: boolean; active?: boolean; content?: string },
) {
  const items = turnItems(route).map((it) => ({
    id: it.id,
    title: it.title,
    kind: it.kind,
    allow_draw: it.allow_draw,
    status: it.status,
  }))
  sessions.patchMessage(messageId, {
    loading: false,
    statusText: undefined,
    content: opts.content,
    planCard: {
      planId,
      summary: route.plan_summary,
      mode: route.task_mode,
      totalDetected: route.total_detected || route.estimated_items || items.length,
      answerThisRound: route.answer_this_round || items.length,
      items,
      awaitingConfirm: opts.awaitingConfirm,
      active: opts.active,
    },
  })
}

async function executeNextSubtask(planId: string) {
  if (busyPlan.value || sending.value) return
  busyPlan.value = true
  try {
    const nxt = await fetchNextPlanItem(planId)
    if (!nxt.has_more || !nxt.next_item) {
      activePlanId.value = null
      activeRoute.value = null
      planAwaitingConfirm.value = false
      if (planCardMessageId.value) {
        sessions.patchMessage(planCardMessageId.value, {
          planCard: undefined,
          content:
            (sessions.activeSession?.messages.find((m) => m.id === planCardMessageId.value)
              ?.content || '') + `\n\n---\n${nxt.message || 'Plan 模式已结束。'}`,
        })
      }
      ElMessage.success(nxt.message || '全部子任务完成')
      return
    }
    const item = nxt.next_item
    const assistantId = uid('a')
    sessions.appendMessage({
      id: assistantId,
      role: 'assistant',
      content: '',
      loading: true,
      statusText: `Plan 模式 · 正在解答（剩余 ${nxt.remaining_count}）：${item.title}`,
      images: [],
      createdAt: Date.now(),
    })
    // 执行时附带完整识读文本，避免子任务 text 缺表达式时模型瞎问用户
    const perceived = (nxt.perceived_text || perceivedTextCache.value || '').trim()
    const solveText = perceived
      ? `【当前子任务】\n${item.text}\n\n【完整识读文本（已含题干与各小题，禁止再向用户索要表达式）】\n${perceived}`
      : item.text
    const reflowStem = [item.title, item.text].filter(Boolean).join('\n').trim() || item.text
    await runSolveStream(solveText, { text: solveText }, assistantId, {
      skipImage: true,
      reflowStem,
      reflowImagePath: nxt.stem_image_path || undefined,
    })
    const done = await markPlanDone(planId, [item.id])
    const followId = uid('a')
    if (done.has_more) {
      const route = activeRoute.value
      const remainSet = new Set(done.remaining_ids || [])
      const remainItems = turnItems(route)
        .filter((it) => remainSet.has(it.id))
        .map((it) => ({
          id: it.id,
          title: it.title,
          kind: it.kind,
          allow_draw: it.allow_draw,
          status: 'pending' as const,
        }))
      // 即使 activeRoute 丢失，也要用 remaining_ids 撑起可点的任务卡
      const cardItems =
        remainItems.length > 0
          ? remainItems
          : (done.remaining_ids || []).map((id) => ({
              id,
              title: id,
              kind: 'big',
              allow_draw: false,
              status: 'pending' as const,
            }))
      sessions.appendMessage({
        id: followId,
        role: 'assistant',
        content:
          `**Plan 模式进行中**\n\n本子任务已交付。剩余 **${done.remaining_ids.length}** 题。\n\n` +
          `请点击下方 **继续下一题** / **取消任务**，或直接回复「继续」「取消」。`,
        loading: false,
        createdAt: Date.now(),
        planCard: {
          planId,
          summary: route?.plan_summary || 'Plan 进行中',
          mode: 'plan_execute',
          totalDetected: route?.total_detected || route?.estimated_items || cardItems.length,
          answerThisRound: cardItems.length,
          items: cardItems,
          awaitingConfirm: false,
          active: true,
        },
      })
      planCardMessageId.value = followId
      // 保证底部栏一定还能点
      activePlanId.value = planId
      planAwaitingConfirm.value = false
    } else {
      activePlanId.value = null
      activeRoute.value = null
      sessions.appendMessage({
        id: followId,
        role: 'assistant',
        content: `**Plan 模式已结束**\n\n${done.message || '全部子任务已完成。'}`,
        loading: false,
        createdAt: Date.now(),
      })
    }
  } catch (err) {
    ElMessage.error(friendlyError(err))
  } finally {
    busyPlan.value = false
  }
}

async function onConfirmPlan(planId: string) {
  if (busyPlan.value) return
  busyPlan.value = true
  try {
    const route = activeRoute.value
    const ids = route?.this_turn_ids || turnItems(route).map((i) => i.id)
    const res = await confirmStudentPlan({
      plan_id: planId,
      selected_ids: ids,
      cancel: false,
    })
    if (res.cancelled) return
    planAwaitingConfirm.value = false
    activePlanId.value = planId
    if (planCardMessageId.value && route) {
      patchPlanCard(planCardMessageId.value, route, planId, {
        awaitingConfirm: false,
        active: true,
        content:
          (sessions.activeSession?.messages.find((m) => m.id === planCardMessageId.value)
            ?.content || '') +
          `\n\n---\n${res.message || '已确认，开始按 ReAct 逐题解答。'}`,
      })
    }
    busyPlan.value = false
    await executeNextSubtask(planId)
  } catch (err) {
    ElMessage.error(friendlyError(err))
    busyPlan.value = false
  }
}

async function onCancelPlan(planId: string) {
  try {
    const res = await cancelStudentPlan(planId)
    activePlanId.value = null
    activeRoute.value = null
    planAwaitingConfirm.value = false
    sessions.appendMessage({
      id: uid('a'),
      role: 'assistant',
      content: res.message || '已取消 Plan 模式。',
      loading: false,
      createdAt: Date.now(),
    })
  } catch (err) {
    ElMessage.error(friendlyError(err))
  }
}

async function onContinuePlan(planId: string) {
  await executeNextSubtask(planId)
}

async function onSend(payload: ChatSendPayload) {
  if (sending.value || busyPlan.value) return
  if (!sessions.ready) {
    await sessions.boot()
  }
  sessions.ensureActive()

  if (payload.fileKind && payload.fileKind !== 'txt' && !payload.fileText) {
    ElMessage.warning('附件尚未解析出正文，请重新上传文件')
    return
  }

  const parts: string[] = []
  if (payload.text) parts.push(payload.text)
  if (payload.fileName) {
    parts.push(`【附件：${payload.fileName}】`)
    if (payload.fileText) parts.push(payload.fileText)
  }
  const userText = parts.join('\n\n').trim()
  if (!userText && !payload.imageDataUrl) {
    ElMessage.warning('请输入题目文字，或上传图片 / 文件')
    return
  }

  // Plan 进行中：解析确认/继续/取消/旁路答疑
  if (activePlanId.value || planAwaitingConfirm.value) {
    const intentRes = await classifyPlanIntent({
      plan_id: activePlanId.value,
      thread_id: sessions.activeId || undefined,
      text: userText || '（图片）',
    })
    const sideUserId = uid('u')
    sessions.appendMessage({
      id: sideUserId,
      role: 'user',
      content: userText || (payload.imagePreview ? '（图片提问）' : ''),
      imagePreview: payload.imagePreview,
      createdAt: Date.now(),
    })

    if (intentRes.intent === 'cancel' && intentRes.plan_id) {
      await onCancelPlan(intentRes.plan_id)
      return
    }
    if (intentRes.intent === 'confirm' && intentRes.plan_id && planAwaitingConfirm.value) {
      await onConfirmPlan(intentRes.plan_id)
      return
    }
    if (intentRes.intent === 'continue' && intentRes.plan_id && !planAwaitingConfirm.value) {
      await onContinuePlan(intentRes.plan_id)
      return
    }
    // 旁路答疑：不关闭 Plan
    const sideId = uid('a')
    sessions.appendMessage({
      id: sideId,
      role: 'assistant',
      content: '',
      loading: true,
      statusText: 'Plan 模式保持中 · 先回答你的旁路问题…',
      images: [],
      createdAt: Date.now(),
    })
    await runSolveStream(userText, payload, sideId, { userMessageId: sideUserId })
    const pid = activePlanId.value || intentRes.plan_id
    const route = activeRoute.value
    sessions.appendMessage({
      id: uid('a'),
      role: 'assistant',
      content:
        '**提示**：Plan 模式未中断。请点击 **继续下一题**，或回复「继续」/「取消任务」。',
      loading: false,
      createdAt: Date.now(),
      planCard: pid
        ? {
            planId: pid,
            summary: route?.plan_summary || 'Plan 进行中',
            mode: 'plan_execute',
            totalDetected: route?.total_detected || route?.estimated_items || 0,
            answerThisRound: turnItems(route).length,
            items: turnItems(route).map((it) => ({
              id: it.id,
              title: it.title,
              kind: it.kind,
              allow_draw: it.allow_draw,
              status: it.status || 'pending',
            })),
            awaitingConfirm: false,
            active: true,
          }
        : undefined,
    })
    return
  }

  const userMsgId = uid('u')
  sessions.appendMessage({
    id: userMsgId,
    role: 'user',
    content: userText || (payload.imagePreview ? '（图片提问）' : ''),
    imagePreview: payload.imagePreview,
    createdAt: Date.now(),
  })

  const assistantId = uid('a')
  sessions.appendMessage({
    id: assistantId,
    role: 'assistant',
    content: '',
    loading: true,
    statusText: '正在读取你上传的内容…',
    images: [],
    createdAt: Date.now(),
  })

  try {
    const routed = await perceiveAndRoute({
      text: userText,
      image_base64: payload.imageDataUrl || null,
      has_file: Boolean(
        payload.fileName && payload.fileKind && payload.fileKind !== 'txt',
      ),
      file_kind:
        payload.fileKind && payload.fileKind !== 'txt' ? payload.fileKind : null,
      file_text: payload.fileText || null,
      thread_id: sessions.activeId || undefined,
    })

    perceivedTextCache.value = routed.perceived_text || ''

    if (routed.blocked) {
      sessions.patchMessage(assistantId, {
        loading: false,
        statusText: undefined,
        content:
          routed.bubble_markdown ||
          routed.route?.block_message ||
          '该内容不适合在本助学场景处理。请换一道数电相关的学习问题。',
      })
      return
    }

    if (routed.needs_confirm && routed.plan_id) {
      activePlanId.value = routed.plan_id
      activeRoute.value = routed.route
      planAwaitingConfirm.value = true
      planCardMessageId.value = assistantId
      patchPlanCard(assistantId, routed.route, routed.plan_id, {
        awaitingConfirm: true,
        active: false,
        content: '',
      })
      return
    }

    // 短任务：气泡内只滚动简短状态，不展示感知/路由明细框
    sessions.patchMessage(assistantId, {
      loading: true,
      statusText: '正在分析题目…',
      content: '',
    })
    await runSolveStream(
      routed.perceived_text || userText,
      payload,
      assistantId,
      { skipImage: Boolean(routed.perceived_text), userMessageId: userMsgId },
    )
  } catch (err) {
    sessions.patchMessage(assistantId, {
      loading: false,
      content: friendlyError(err),
    })
  }
}
</script>

<template>
  <StudentLayout active-nav="chat" flush>
    <div class="chat-page" :class="{ 'history-collapsed': !historyOpen }">
      <aside class="history-rail" aria-label="会话历史">
        <div class="history-rail__head">
          <p>历史记录</p>
          <button class="new-btn" type="button" @click="newSession">
            <iconify-icon icon="solar:add-circle-bold" />
            新会话
          </button>
        </div>

        <div class="history-rail__list">
          <button
            v-for="s in sessions.sortedSessions"
            :key="s.id"
            class="history-item"
            :class="{ 'is-active': s.id === sessions.activeId }"
            type="button"
            @click="selectSession(s.id)"
          >
            <span class="history-item__title">{{ s.title }}</span>
            <span class="history-item__meta">
              <time>{{ formatTime(s.updatedAt) }}</time>
              <button
                class="del-btn"
                type="button"
                title="删除会话"
                @click="removeSession(s.id, $event)"
              >
                <iconify-icon icon="solar:trash-bin-minimalistic-linear" />
              </button>
            </span>
          </button>
          <p v-if="!sessions.sortedSessions.length" class="history-empty">暂无历史会话</p>
        </div>
      </aside>

      <section class="chat-pane">
        <header class="chat-pane__bar">
          <button
            class="toggle-history"
            type="button"
            :title="historyOpen ? '收起历史' : '展开历史'"
            @click="historyOpen = !historyOpen"
          >
            <iconify-icon
              :icon="historyOpen ? 'solar:sidebar-minimalistic-linear' : 'solar:hamburger-menu-linear'"
            />
          </button>
          <div class="chat-pane__title">
            <b>{{ sessions.activeSession?.title || 'AI答疑' }}</b>
            <span class="ai-badge">AI 生成内容</span>
            <span v-if="planModeOn || planAwaitingConfirm" class="plan-badge">Plan 模式</span>
          </div>
          <ByokSettings />
        </header>

        <MessageList
          :messages="messages"
          @confirm-plan="onConfirmPlan"
          @cancel-plan="onCancelPlan"
          @continue-plan="onContinuePlan"
          @add-mistake="onAddMistake"
        />

        <div v-if="planAwaitingConfirm && activePlanId" class="continue-bar confirm-bar">
          <span class="plan-alive">Plan 待确认 · 请确认后开始逐题解答</span>
          <button
            type="button"
            class="cancel-btn"
            :disabled="sending || busyPlan"
            @click="onCancelPlan(activePlanId)"
          >
            取消任务
          </button>
          <button
            type="button"
            class="continue-btn"
            :disabled="sending || busyPlan"
            @click="onConfirmPlan(activePlanId)"
          >
            确认执行
          </button>
        </div>

        <div v-else-if="planModeOn && activePlanId" class="continue-bar">
          <span class="plan-alive">Plan 进行中 · 旁路提问不会关闭任务</span>
          <button
            type="button"
            class="continue-btn"
            :disabled="sending || busyPlan"
            @click="onContinuePlan(activePlanId)"
          >
            继续下一题
          </button>
          <button
            type="button"
            class="cancel-btn"
            :disabled="sending || busyPlan"
            @click="onCancelPlan(activePlanId)"
          >
            取消任务
          </button>
        </div>

        <ChatInput :seed="chatSeed" :sending="sending || busyPlan" @send="onSend" />
      </section>
    </div>
  </StudentLayout>
</template>

<style scoped lang="scss">
.chat-page {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  grid-template-rows: minmax(0, 1fr);
  height: 100%;
  min-height: 0;
  overflow: hidden;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

.chat-page.history-collapsed {
  grid-template-columns: 0 1fr;
}

.history-rail {
  overflow: hidden;
  min-height: 0;
  border-right: 1px solid var(--line, #e2e8f0);
  background: rgb(255 255 255 / 0.72);
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
}

.history-rail__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 14px 14px 10px;
  border-bottom: 1px solid var(--line, #e2e8f0);
}

.history-rail__head p {
  margin: 0;
  font-weight: 700;
  color: #0f172a;
}

.new-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: 1px solid #cbd5e1;
  background: #fff;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
}

.history-rail__list {
  flex: 1;
  overflow: auto;
  padding: 8px;
}

.history-item {
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  border-radius: 12px;
  padding: 10px 10px;
  cursor: pointer;
  display: grid;
  gap: 4px;
}

.history-item.is-active,
.history-item:hover {
  background: #ecfeff;
}

.history-item__title {
  font-size: 13px;
  font-weight: 650;
  color: #0f172a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-item__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  color: #94a3b8;
}

.del-btn {
  border: 0;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
}

.history-empty {
  padding: 24px 8px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

.chat-pane {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  height: 100%;
  overflow: hidden;
  background: rgb(248 250 252 / 0.55);
}

.chat-pane__bar {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 52px;
  padding: 0 16px;
  border-bottom: 1px solid var(--line, #e2e8f0);
  background: rgb(255 255 255 / 0.88);
  backdrop-filter: blur(8px);
  flex-shrink: 0;
}

.toggle-history {
  width: 34px;
  height: 34px;
  border: 1px solid var(--line, #e2e8f0);
  border-radius: 10px;
  background: #fff;
  color: #475569;
  display: grid;
  place-items: center;
  font-size: 18px;
}

.chat-pane__title {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-pane__title b {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ai-badge {
  flex-shrink: 0;
  font-size: 11px;
  color: #64748b;
  background: #f1f5f9;
  border-radius: 999px;
  padding: 2px 8px;
}

.plan-badge {
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 700;
  color: #0f766e;
  background: #ccfbf1;
  border: 1px solid #99f6e4;
  border-radius: 999px;
  padding: 2px 8px;
}

.continue-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 16px;
  border-top: 1px solid #e2e8f0;
  background: #f0fdfa;
  flex-shrink: 0;
  z-index: 5;
  position: relative;
}

.confirm-bar {
  background: #ecfeff;
  border-top-color: #a5f3fc;
}

.plan-alive {
  flex: 1;
  font-size: 12px;
  color: #0f766e;
  font-weight: 600;
}

.continue-btn,
.cancel-btn {
  border-radius: 10px;
  padding: 7px 12px;
  font-size: 13px;
  font-weight: 650;
  cursor: pointer;
}

.continue-btn {
  border: 1px solid #0f766e;
  background: #0f766e;
  color: #fff;
}

.cancel-btn {
  border: 1px solid #cbd5e1;
  background: #fff;
  color: #475569;
}

@media (max-width: 900px) {
  .chat-page {
    grid-template-columns: 1fr;
  }

  .chat-page.history-collapsed {
    grid-template-columns: 1fr;
  }

  .history-rail {
    position: fixed;
    top: 52px;
    left: 0;
    bottom: 64px;
    width: min(300px, 86vw);
    z-index: 25;
    transform: translateX(-105%);
    transition: transform 0.22s ease;
    box-shadow: 8px 0 24px rgb(0 0 0 / 0.12);
  }

  .chat-page:not(.history-collapsed) .history-rail {
    transform: translateX(0);
  }

  .chat-pane__bar {
    padding: 8px 10px;
  }

  .message-list {
    padding: 12px 12px 8px;
  }
}
</style>

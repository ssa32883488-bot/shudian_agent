<script setup lang="ts">
/**
 * 个性化加练：作答（文字+图片）→ AI 逐题判卷 → 本场报告 → 练习记录回看
 */
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import StudentLayout from '@/layouts/StudentLayout.vue'
import FormulaText from '@/components/markdown/FormulaText.vue'
import {
  generatePractice,
  getPracticeSession,
  listPracticeSessions,
  submitPractice,
  type PracticeItem,
  type PracticeResultItem,
  type PracticeSession,
  type PracticeSessionRecord,
  type PracticeSubmitResult,
} from '@/api/practice'
import { fileToDataUrl } from '@/utils/image'
import { tagsFromKnowledge } from '@/utils/learningOverview'
import { getStudentProfile } from '@/api/profile'

type Phase = 'idle' | 'answer' | 'report' | 'history' | 'detail'

interface DraftAnswer {
  text: string
  images: string[]
}

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const submitting = ref(false)
const historyLoading = ref(false)
const phase = ref<Phase>('idle')
const count = ref(5)
const mode = ref('auto')
const focusTags = ref<string[]>([])
const session = ref<PracticeSession | null>(null)
const drafts = ref<Record<number, DraftAnswer>>({})
const results = ref<PracticeResultItem[] | null>(null)
const submitMeta = ref<PracticeSubmitResult | null>(null)
const history = ref<PracticeSessionRecord[]>([])
const detailSession = ref<PracticeSessionRecord | null>(null)
const fileInputRefs = ref<Record<number, HTMLInputElement | null>>({})
const profileWeak = ref<string[]>([])
const profileHint = ref('')

const reportItems = computed((): PracticeResultItem[] => {
  if (results.value?.length) return results.value
  return (session.value?.items || []).map((q) => ({
    question_id: q.question_id,
    order_no: q.order_no,
    content: q.content,
    knowledge_tags: q.knowledge_tags,
    correct: null,
    answer_text: '',
    answer_images: [],
  }))
})

const modeLabel = computed(() => {
  const m = detailSession.value?.mode || mode.value
  if (m === 'probe') return '摸底'
  if (m === 'review') return '错题回炉'
  if (m === 'focus') return '针对加练'
  return '学情抽题'
})

const sourceLabel = computed(() => {
  const s = session.value?.source
  if (s === 'probe') return '摸底 · 题库分散抽题'
  if (s === 'review') return '错题回炉 · 按错题标签'
  if (s === 'focus' || s === 'weak_tags') return '薄弱知识点优先'
  if (s === 'random_bank') return '题库随机（未命中标签时兜底）'
  return s || '—'
})

function ensureDraft(qid: number): DraftAnswer {
  if (!drafts.value[qid]) drafts.value[qid] = { text: '', images: [] }
  return drafts.value[qid]
}

const answeredCount = computed(() => {
  if (!session.value) return 0
  return session.value.items.filter((q) => {
    const d = drafts.value[q.question_id]
    return Boolean(d && (d.text.trim() || d.images.length))
  }).length
})

const reportNotes = computed(() => {
  const fromMeta = submitMeta.value?.report_notes || detailSession.value?.report_notes
  if (fromMeta?.length) return fromMeta
  if (!results.value) return [] as string[]
  const tagMap = new Map<string, { ok: number; bad: number }>()
  for (const r of results.value) {
    const tags = tagsFromKnowledge(r.knowledge_tags)
    const keys = tags.length ? tags : ['未标注']
    const answered = Boolean((r.answer_text || '').trim() || (r.answer_images || []).length)
    for (const t of keys) {
      const cur = tagMap.get(t) || { ok: 0, bad: 0 }
      if (!answered || !r.correct) cur.bad += 1
      else cur.ok += 1
      tagMap.set(t, cur)
    }
  }
  return [...tagMap.entries()].map(([tag, s]) => {
    if (s.bad > 0 && s.ok === 0) return `${tag}：错/未作答 ${s.bad} 题 → 仍列薄弱`
    if (s.bad > 0) return `${tag}：对 ${s.ok} / 错 ${s.bad} → 仍需加练`
    return `${tag}：全对`
  })
})

function applyQuery() {
  const q = route.query
  const m = String(q.mode || 'auto')
  mode.value = ['probe', 'focus', 'review', 'auto'].includes(m) ? m : 'auto'
  const n = Number(q.count)
  if (Number.isFinite(n) && n >= 1) {
    count.value = Math.min(10, Math.max(1, Math.round(n)))
  } else if (mode.value === 'focus') {
    count.value = 3
  } else {
    count.value = 5
  }
  const raw = q.tags
  const list = Array.isArray(raw) ? raw : raw ? [raw] : []
  focusTags.value = list
    .flatMap((x) => String(x).split(','))
    .map((x) => x.trim())
    .filter(Boolean)
}

async function loadProfileHint() {
  try {
    const pf = await getStudentProfile()
    profileWeak.value = (pf.weak_points || []).map((w) =>
      typeof w === 'string' ? w : String((w as any)?.concept || w),
    )
    const last = pf.practice_stats?.last_session
    if (last?.accuracy != null) {
      profileHint.value = `最近正确率 ${Math.round(Number(last.accuracy) * 100)}%`
    } else if (profileWeak.value.length) {
      profileHint.value = `当前薄弱：${profileWeak.value.slice(0, 3).join('、')}`
    } else {
      profileHint.value = '尚无学情，建议先摸底 5 题'
    }
  } catch {
    profileHint.value = '学情暂不可用，仍可按题库抽题'
  }
}

function pickMode(m: string, tags?: string[]) {
  mode.value = m
  if (tags?.length) focusTags.value = tags
  else if (m === 'focus' && profileWeak.value[0]) {
    focusTags.value = [profileWeak.value[0]]
  } else if (m !== 'focus') {
    focusTags.value = []
  }
}

async function startPractice() {
  loading.value = true
  results.value = null
  submitMeta.value = null
  detailSession.value = null
  drafts.value = {}
  phase.value = 'answer'
  try {
    const tags =
      mode.value === 'focus'
        ? focusTags.value.length
          ? focusTags.value
          : profileWeak.value.slice(0, 2)
        : focusTags.value
    session.value = await generatePractice(count.value, {
      mode: mode.value,
      tags,
    })
    for (const q of session.value.items) ensureDraft(q.question_id)
    if (!session.value.items.length) {
      ElMessage.warning('题库暂无题目，请联系管理员维护题库')
      phase.value = 'idle'
    } else {
      await nextTick()
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  } catch (e: unknown) {
    phase.value = 'idle'
    const msg =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      '抽题失败，请确认后端已启动'
    ElMessage.error(typeof msg === 'string' ? msg : '抽题失败')
  } finally {
    loading.value = false
  }
}

async function onSubmit() {
  if (!session.value?.items.length || !session.value.session_id || submitting.value) return
  if (answeredCount.value === 0) {
    ElMessage.warning('请至少作答一题（文字或图片）再提交')
    return
  }
  submitting.value = true
  try {
    const payload = session.value.items.map((q: PracticeItem) => {
      const d = drafts.value[q.question_id] || { text: '', images: [] }
      return {
        question_id: q.question_id,
        answer_text: d.text || '',
        images: d.images || [],
      }
    })
    ElMessage.info('正在逐题 AI 判卷，请稍候…')
    const res = await submitPractice(session.value.session_id, payload, true)
    results.value = res.results
    submitMeta.value = res
    if (res.session) detailSession.value = res.session
    phase.value = 'report'
    await nextTick()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (e: unknown) {
    const msg =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || '提交失败'
    ElMessage.error(typeof msg === 'string' ? msg : '提交失败')
  } finally {
    submitting.value = false
  }
}

function pickImage(qid: number) {
  fileInputRefs.value[qid]?.click()
}

async function onImagePicked(qid: number, ev: Event) {
  const input = ev.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  const d = ensureDraft(qid)
  if (d.images.length >= 4) {
    ElMessage.warning('每题最多上传 4 张图')
    return
  }
  try {
    const url = await fileToDataUrl(file)
    d.images.push(url)
  } catch (e: unknown) {
    ElMessage.warning(e instanceof Error ? e.message : '图片读取失败')
  }
}

function removeImage(qid: number, idx: number) {
  const d = ensureDraft(qid)
  d.images.splice(idx, 1)
}

function itemStatus(r: PracticeResultItem): 'ok' | 'bad' | 'skip' {
  if (r.grade_method === 'unanswered') return 'skip'
  const has =
    Boolean((r.answer_text || '').trim()) || Boolean((r.answer_images || []).length)
  if (!has && r.correct == null) {
    const d = drafts.value[r.question_id]
    if (!d || (!d.text.trim() && !d.images.length)) return 'skip'
  }
  if (!has && r.correct === false) return 'skip'
  return r.correct ? 'ok' : 'bad'
}

function statusText(r: PracticeResultItem) {
  const s = itemStatus(r)
  if (s === 'ok') return '正确'
  if (s === 'skip') return '未作答'
  return '需订正'
}

function askAboutWrong(r: PracticeResultItem) {
  const stem = (r.content || r.question_snapshot || '').replace(/\s+/g, ' ').trim().slice(0, 120)
  router.push({
    path: '/chat',
    query: { q: `请讲解这道加练错题：${stem}` },
  })
}

function retrySame() {
  const tags = focusTags.value.length
    ? focusTags.value
    : session.value?.weak_points || detailSession.value?.weak_points || []
  router.push({
    path: '/practice',
    query: {
      mode: mode.value === 'probe' ? 'probe' : tags.length ? 'focus' : 'review',
      tags: tags.join(','),
      count: String(Math.min(5, count.value || 3)),
      _: String(Date.now()),
    },
  })
}

async function openHistory() {
  historyLoading.value = true
  phase.value = 'history'
  try {
    history.value = await listPracticeSessions(40)
  } catch {
    ElMessage.warning('加载练习记录失败')
    history.value = []
  } finally {
    historyLoading.value = false
  }
}

async function openDetail(id: number) {
  historyLoading.value = true
  try {
    const detail = await getPracticeSession(id)
    detailSession.value = detail.session
    results.value = detail.results || detail.items
    submitMeta.value = {
      ok: true,
      session_id: detail.session.id,
      total: detail.total ?? detail.items.length,
      correct: detail.correct ?? 0,
      accuracy: detail.accuracy ?? 0,
      report_notes: detail.report_notes,
      results: detail.results || detail.items,
      session: detail.session,
    }
    session.value = {
      ok: true,
      session_id: detail.session.id,
      title: detail.session.title,
      mode: detail.session.mode,
      weak_points: detail.session.weak_points || [],
      source: detail.session.source,
      count: detail.session.item_count,
      items: (detail.items || []).map((x) => ({
        question_id: x.question_id,
        order_no: x.order_no || 0,
        content: x.content || x.question_snapshot || '',
        knowledge_tags: x.knowledge_tags,
      })),
    }
    // 回填草稿展示（报告用 results 里的字段）
    const next: Record<number, DraftAnswer> = {}
    for (const r of detail.items || []) {
      next[r.question_id] = {
        text: r.answer_text || '',
        images: listPreviewImages(r),
      }
    }
    drafts.value = next
    phase.value = 'detail'
    await nextTick()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch {
    ElMessage.error('无法打开该场练习')
  } finally {
    historyLoading.value = false
  }
}

function listPreviewImages(r: PracticeResultItem): string[] {
  return (r.answer_images || []).map((p) => (p.startsWith('/media/') ? p : p))
}

function formatTime(iso?: string | null) {
  if (!iso) return '—'
  return iso.replace('T', ' ').slice(0, 19)
}

watch(
  () => [route.query.mode, route.query.tags, route.query.count, route.query._],
  async () => {
    applyQuery()
    if (route.query.mode) await startPractice()
    else if (phase.value === 'answer' || phase.value === 'report') {
      /* keep */
    } else {
      phase.value = 'idle'
      session.value = null
      results.value = null
      await loadProfileHint()
    }
  },
  { immediate: true },
)
</script>

<template>
  <StudentLayout active-nav="practice">
    <!-- 未开始 -->
    <template v-if="phase === 'idle'">
      <div class="head">
        <div>
          <p class="kicker">个性化加练</p>
          <h1 class="title">按总览瞄准，从题库抽短卷</h1>
          <p class="sub">
            支持文字与图片作答；交卷后 AI 逐题阅卷，并可回看练习记录与报告。
          </p>
        </div>
        <button class="btn ghost" type="button" @click="openHistory">练习记录</button>
      </div>
      <div class="idle-card">
        <p v-if="profileHint" class="profile-hint">{{ profileHint }}</p>
        <div class="mode-row">
          <button
            class="mode-chip"
            :class="{ on: mode === 'auto' }"
            type="button"
            @click="pickMode('auto')"
          >
            学情抽题
          </button>
          <button
            class="mode-chip"
            :class="{ on: mode === 'probe' }"
            type="button"
            @click="pickMode('probe')"
          >
            摸底
          </button>
          <button
            class="mode-chip"
            :class="{ on: mode === 'focus' }"
            type="button"
            @click="pickMode('focus')"
          >
            针对薄弱
          </button>
          <button
            class="mode-chip"
            :class="{ on: mode === 'review' }"
            type="button"
            @click="pickMode('review')"
          >
            错题回炉
          </button>
        </div>
        <div v-if="mode === 'focus' && profileWeak.length" class="weak-row">
          <button
            v-for="t in profileWeak.slice(0, 6)"
            :key="t"
            class="weak-chip"
            :class="{ on: focusTags.includes(t) }"
            type="button"
            @click="
              focusTags = focusTags.includes(t)
                ? focusTags.filter((x) => x !== t)
                : [...focusTags, t]
            "
          >
            {{ t }}
          </button>
        </div>
        <label class="count">
          题量
          <input v-model.number="count" type="number" min="1" max="10" />
        </label>
        <div class="idle-actions">
          <button class="btn primary" type="button" :disabled="loading" @click="startPractice">
            {{ loading ? '抽题中…' : '开始加练' }}
          </button>
          <button class="btn ghost" type="button" @click="router.push('/home')">
            先去总览看看该练什么
          </button>
        </div>
        <p class="hint">作答支持文字与图片；交卷后 AI 判卷，错题写入错题本并更新学情。</p>
      </div>
    </template>

    <!-- 练习记录列表 -->
    <template v-else-if="phase === 'history'">
      <div class="head">
        <div>
          <p class="kicker">练习记录</p>
          <h1 class="title">已提交的加练场次</h1>
          <p class="sub">可回看原题、你的作答（含图片）、AI 判卷与本场报告。</p>
        </div>
        <button class="btn ghost" type="button" @click="phase = 'idle'">返回</button>
      </div>
      <p v-if="historyLoading" class="muted">加载中…</p>
      <p v-else-if="!history.length" class="empty-line">暂无记录。完成一场加练后会出现在这里。</p>
      <ul v-else class="history-list">
        <li v-for="h in history" :key="h.id">
          <button class="history-row" type="button" @click="openDetail(h.id)">
            <span>
              <b>{{ h.title }}</b>
              <i
                >{{ formatTime(h.submitted_at) }} · {{ h.correct_count ?? '—' }}/{{
                  h.item_count
                }}
                · {{ Math.round(Number(h.accuracy || 0) * 100) }}%</i
              >
            </span>
            <em>查看</em>
          </button>
        </li>
      </ul>
    </template>

    <!-- 作答 -->
    <template v-else-if="phase === 'answer'">
      <div class="head">
        <div>
          <p class="kicker">作答中 · {{ modeLabel }}</p>
          <h1 class="title">{{ session?.title || '加练' }}</h1>
          <p class="sub">可写文字、上传作答图。交卷后 AI 会结合题目与全部作答内容逐题阅卷。</p>
        </div>
        <button class="btn ghost" type="button" :disabled="loading" @click="startPractice">
          重新抽题
        </button>
      </div>

      <div class="meta">
        <span>{{ sourceLabel }}</span>
        <span v-if="session?.weak_points?.length">
          本次依据：{{ session.weak_points.join('、') }}
        </span>
        <span>共 {{ session?.count || 0 }} 题 · 已作答 {{ answeredCount }}</span>
      </div>

      <div v-if="loading" class="muted">抽题中…</div>
      <div v-else-if="session?.items?.length" class="list">
        <article v-for="q in session.items" :key="q.question_id" class="q">
          <header>
            <b>第 {{ q.order_no }} 题</b>
          </header>
          <FormulaText :content="q.content" />
          <textarea
            :value="ensureDraft(q.question_id).text"
            rows="3"
            placeholder="输入文字答案（可选）"
            @input="
              ensureDraft(q.question_id).text = ($event.target as HTMLTextAreaElement).value
            "
          />
          <div class="img-row">
            <input
              :ref="(el) => (fileInputRefs[q.question_id] = el as HTMLInputElement)"
              class="hidden-file"
              type="file"
              accept="image/*"
              @change="onImagePicked(q.question_id, $event)"
            />
            <button class="btn ghost sm" type="button" @click="pickImage(q.question_id)">
              上传作答图
            </button>
            <span class="hint">最多 4 张 · ≤5MB</span>
          </div>
          <div v-if="ensureDraft(q.question_id).images.length" class="thumbs">
            <div
              v-for="(img, idx) in ensureDraft(q.question_id).images"
              :key="idx"
              class="thumb"
            >
              <img :src="img" alt="作答图" />
              <button type="button" class="thumb-x" @click="removeImage(q.question_id, idx)">
                ×
              </button>
            </div>
          </div>
        </article>

        <div class="submit-bar">
          <p class="hint">提交后将逐题 AI 判卷；未作答记为跳过；错题写入错题本。</p>
          <button
            class="btn primary"
            type="button"
            :disabled="submitting || answeredCount === 0"
            @click="onSubmit"
          >
            {{ submitting ? 'AI 判卷中…' : '提交本场' }}
          </button>
        </div>
      </div>
    </template>

    <!-- 报告 / 详情回看 -->
    <template
      v-else-if="(phase === 'report' || phase === 'detail') && session && submitMeta"
    >
      <div class="head">
        <div>
          <p class="kicker">{{ phase === 'detail' ? '练习记录详情' : '本场报告' }}</p>
          <h1 class="title">
            {{ submitMeta.correct }}/{{ submitMeta.total }}
            <span class="acc">· 正确率 {{ Math.round(Number(submitMeta.accuracy) * 100) }}%</span>
          </h1>
          <p class="sub">
            {{ modeLabel }}
            <template v-if="session.weak_points?.length">
              · 依据「{{ session.weak_points.join('、') }}」
            </template>
            <template v-if="detailSession?.submitted_at">
              · {{ formatTime(detailSession.submitted_at) }}
            </template>
          </p>
        </div>
        <button
          v-if="phase === 'detail'"
          class="btn ghost"
          type="button"
          @click="openHistory"
        >
          返回列表
        </button>
      </div>

      <section class="report-block">
        <h2>学情变化</h2>
        <ul v-if="reportNotes.length" class="notes">
          <li v-for="(n, i) in reportNotes" :key="i">{{ n }}</li>
        </ul>
        <p v-else class="muted">本场暂无知识点汇总。</p>
      </section>

      <section class="report-block">
        <h2>逐题结果（含 AI 判卷）</h2>
        <article v-for="r in reportItems" :key="r.question_id" class="q report-q">
          <header>
            <b>第 {{ r.order_no || '—' }} 题</b>
            <span class="tag" :class="itemStatus(r)">{{ statusText(r) }}</span>
          </header>
          <FormulaText :content="r.content || r.question_snapshot || ''" />
          <div class="ans-grid">
            <p>
              <b>你的答案</b>
              {{ (r.answer_text || drafts[r.question_id]?.text || '').trim() || '（无文字）' }}
            </p>
            <div
              v-if="(r.answer_images || drafts[r.question_id]?.images || []).length"
              class="thumbs"
            >
              <div
                v-for="(img, idx) in r.answer_images || drafts[r.question_id]?.images || []"
                :key="idx"
                class="thumb"
              >
                <img :src="img" alt="作答图" />
              </div>
            </div>
            <p v-if="r.ai_comment">
              <b>AI 判卷</b>
              {{ r.ai_comment }}
              <template v-if="r.ai_score != null">
                · 分 {{ Math.round(Number(r.ai_score) * 100) }}%
                <template v-if="r.grade_method">（{{ r.grade_method }}）</template>
              </template>
            </p>
            <p v-if="r.reference_answer">
              <b>参考答案</b>
              {{ r.reference_answer }}
            </p>
            <p v-if="r.analysis">
              <b>解析</b>
              {{ r.analysis }}
            </p>
          </div>
          <button
            v-if="itemStatus(r) === 'bad' || itemStatus(r) === 'skip'"
            class="link"
            type="button"
            @click="askAboutWrong(r)"
          >
            把这题拿去问小灵 →
          </button>
        </article>
      </section>

      <div class="cta-row">
        <button v-if="phase === 'report'" class="btn primary" type="button" @click="retrySame">
          再练同点
        </button>
        <button class="btn ghost" type="button" @click="router.push('/home')">回总览</button>
        <button class="btn ghost" type="button" @click="openHistory">练习记录</button>
        <button class="btn ghost" type="button" @click="router.push('/records')">错题本</button>
      </div>
    </template>
  </StudentLayout>
</template>

<style scoped>
.kicker {
  margin: 0;
  color: #0e7490;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}
.title {
  margin: 6px 0 0;
  font-size: 26px;
  letter-spacing: -0.02em;
  color: #0f172a;
}
.acc {
  font-size: 18px;
  font-weight: 600;
  color: #475569;
}
.sub {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 14px;
  max-width: 42rem;
  line-height: 1.6;
}
.head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}
.idle-card {
  margin-top: 28px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
}
.idle-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
}
.count {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
}
.count input {
  width: 64px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 8px;
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
  margin-top: 18px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 13px;
  color: #475569;
}
.list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}
.q {
  padding: 18px 0;
  border-bottom: 1px solid #e2e8f0;
}
.q header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.q textarea {
  box-sizing: border-box;
  width: 100%;
  margin-top: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 10px 12px;
  font: inherit;
  resize: vertical;
}
.q textarea:focus {
  outline: none;
  border-color: #0891b2;
}
.img-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
}
.hidden-file {
  display: none;
}
.thumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}
.thumb {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
}
.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.thumb-x {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 22px;
  height: 22px;
  border: 0;
  border-radius: 999px;
  background: rgb(15 23 42 / 0.75);
  color: #fff;
  cursor: pointer;
  line-height: 1;
}
.submit-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 0 24px;
}
.hint,
.muted,
.empty-line {
  margin: 0;
  color: #64748b;
  font-size: 13px;
}
.idle-card .hint {
  margin-top: 16px;
}
.empty-line {
  margin-top: 24px;
}
.btn {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 16px;
  background: #fff;
  color: #334155;
  font: inherit;
  font-weight: 650;
  cursor: pointer;
}
.btn.sm {
  padding: 6px 12px;
  font-size: 13px;
}
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
.btn.primary {
  border-color: #0f172a;
  background: #0f172a;
  color: #fff;
}
.btn.primary:hover:not(:disabled) {
  background: #1e293b;
}
.btn.ghost:hover:not(:disabled) {
  background: #f8fafc;
}
.report-block {
  margin-top: 28px;
}
.report-block h2 {
  margin: 0 0 10px;
  font-size: 15px;
  color: #0f172a;
}
.notes {
  margin: 0;
  padding-left: 1.1rem;
  color: #334155;
  font-size: 14px;
  line-height: 1.7;
}
.report-q .ans-grid {
  margin-top: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #f8fafc;
  font-size: 13px;
  color: #334155;
  line-height: 1.6;
}
.report-q .ans-grid p {
  margin: 0 0 8px;
}
.tag {
  font-size: 12px;
  font-weight: 700;
  border-radius: 999px;
  padding: 2px 8px;
}
.tag.ok {
  background: #ecfdf5;
  color: #047857;
}
.tag.bad {
  background: #fff1f2;
  color: #be123c;
}
.tag.skip {
  background: #f1f5f9;
  color: #64748b;
}
.link {
  margin-top: 10px;
  padding: 0;
  border: 0;
  background: none;
  color: #0e7490;
  font-size: 13px;
  font-weight: 650;
  cursor: pointer;
}
.cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
  padding-bottom: 24px;
}
.history-list {
  list-style: none;
  margin: 20px 0 0;
  padding: 0;
  border-top: 1px solid #e2e8f0;
}
.history-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border: 0;
  border-bottom: 1px solid #e2e8f0;
  background: none;
  text-align: left;
  cursor: pointer;
}
.history-row b {
  display: block;
  color: #0f172a;
  font-size: 14px;
}
.history-row i,
.history-row em {
  font-style: normal;
  font-size: 12px;
  color: #64748b;
}
.history-row em {
  color: #0e7490;
  font-weight: 650;
}
.profile-hint {
  margin: 0 0 12px;
  font-size: 13px;
  color: #0e7490;
  font-weight: 600;
}
.mode-row,
.weak-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}
.mode-chip,
.weak-chip {
  border: 1px solid #cbd5e1;
  background: #fff;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 650;
  color: #475569;
}
.mode-chip.on,
.weak-chip.on {
  border-color: #0891b2;
  background: #ecfeff;
  color: #0e7490;
}

@media (max-width: 900px) {
  .title {
    font-size: 22px;
  }
  .head {
    flex-direction: column;
  }
  .submit-bar {
    position: sticky;
    bottom: 72px;
    background: #f8fafc;
    padding: 12px 0;
    z-index: 5;
  }
}
</style>

<script setup lang="ts">
/**
 * 管理端：学情总览 / 题库 / 回流审核 / 系统观测
 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

import AdminLayout from '@/layouts/AdminLayout.vue'
import FormulaText from '@/components/markdown/FormulaText.vue'
import {
  approveReflow,
  createBankItem,
  deleteBankItem,
  rejectReflow,
  searchBank,
  suggestConcepts,
  listReflow,
  updateBankItem,
  type BankItem,
  type ReflowItem,
} from '@/api/admin'
import {
  exportClassLearningWord,
  getClassLearning,
  getStudentLearning,
  type ClassLearningData,
} from '@/api/learningMemory'
import {
  archiveClass,
  createClass,
  listClassMembers,
  listClasses,
  removeClassMember,
  renameClass,
  type ClassMember,
  type ClassRoomItem,
} from '@/api/adminClasses'
import {
  getAgentTrace,
  listAgentTraces,
  type AgentTraceItem,
  type TraceStatus,
} from '@/api/adminConfig'
import type { StudentProfileData } from '@/api/profile'

const route = useRoute()
const tab = computed(() => (route.params.tab as string) || 'class')

const loading = ref(false)
const classLearning = ref<ClassLearningData | null>(null)
const selectedStudentId = ref<number | null>(null)
const studentDetail = ref<StudentProfileData | null>(null)
const masteryChartRef = ref<HTMLDivElement | null>(null)
let masteryChart: echarts.ECharts | null = null

const myClasses = ref<ClassRoomItem[]>([])
const newClassName = ref('')
const activeClassCode = ref('')
const classMembers = ref<ClassMember[]>([])
const learningClassCode = ref('')

const bankItems = ref<BankItem[]>([])
const bankForm = ref({ content: '', answer: '', analysis: '' })
const showBankForm = ref(false)
const editingBankId = ref<number | null>(null)
const bankQuery = ref('')
const bankConcept = ref('')
const bankMode = ref<'latest' | 'search' | 'concept' | string>('latest')
const bankMatchedConcepts = ref<string[]>([])
const conceptSuggestions = ref<string[]>([])
const showConceptSuggest = ref(false)
const bankSearching = ref(false)
let bankSearchTimer: ReturnType<typeof setTimeout> | null = null
let conceptSuggestTimer: ReturnType<typeof setTimeout> | null = null

const reflowItems = ref<ReflowItem[]>([])
const reflowFilter = ref<'all' | 'memory' | 'solve'>('all')

const agentTraces = ref<AgentTraceItem[]>([])
const tracesPrivacyNote = ref('')
const traceFilterStatus = ref<string>('')
const traceFilterQ = ref('')
const selectedTrace = ref<AgentTraceItem | null>(null)
const traceDetailLoading = ref(false)

const bankListTitle = computed(() => {
  if (bankMode.value === 'latest') return '最新入库'
  if (bankMode.value === 'concept' || bankConcept.value) return '知识点相关题目'
  return '搜索结果'
})

const bankListHint = computed(() => {
  if (bankMode.value === 'latest') return `展示最近入库的 ${bankItems.value.length} 道题`
  const bits: string[] = []
  if (bankQuery.value.trim()) bits.push(`关键词「${bankQuery.value.trim()}」`)
  if (bankConcept.value.trim()) bits.push(`知识点「${bankConcept.value.trim()}」`)
  if (bankMatchedConcepts.value.length) {
    bits.push(`图谱命中：${bankMatchedConcepts.value.slice(0, 4).join('、')}`)
  }
  return bits.join(' · ') || '检索结果'
})

const learningProgress = computed(() => {
  const p = classLearning.value?.progress || {}
  return {
    n_students: Number(p.n_students ?? classLearning.value?.n_students ?? 0),
    chapter_completion_events: Number(p.chapter_completion_events ?? 0),
  }
})

function matchViaLabel(via?: string) {
  if (!via) return ''
  const parts = via.split('+').map((p) => p.trim()).filter(Boolean)
  const mapped = parts.map((p) => {
    if (p.includes('semantic')) return '语义'
    if (p.includes('concept')) return '图谱'
    if (p.includes('keyword')) return '关键词'
    return p
  })
  return [...new Set(mapped)].join('+')
}

function tagNames(tags?: Record<string, unknown> | null): string[] {
  if (!tags || typeof tags !== 'object') return []
  const raw = tags.tags
  if (!Array.isArray(raw)) return []
  return raw.map((t) => String(t || '').trim()).filter(Boolean).slice(0, 12)
}

function needsKgReview(q: { needs_kg_review?: boolean; knowledge_tags?: Record<string, unknown> | null }) {
  if (q.needs_kg_review) return true
  const t = q.knowledge_tags
  return Boolean(t && typeof t === 'object' && t.needs_kg_review)
}

async function loadBank(opts?: { q?: string; concept?: string }) {
  const q = (opts?.q ?? bankQuery.value).trim()
  const concept = (opts?.concept ?? bankConcept.value).trim()
  bankSearching.value = true
  loading.value = true
  try {
    const data = await searchBank({
      q: q || undefined,
      concept: concept || undefined,
      limit: 20,
      status: 'active',
    })
    bankItems.value = data.items || []
    bankMode.value = data.mode || (q || concept ? 'search' : 'latest')
    bankMatchedConcepts.value = data.matched_concepts || []
  } finally {
    loading.value = false
    bankSearching.value = false
  }
}

function scheduleBankSearch() {
  if (bankSearchTimer) clearTimeout(bankSearchTimer)
  bankSearchTimer = setTimeout(() => {
    void loadBank()
  }, 320)
}

function onBankQueryInput() {
  // 输入关键词时清除已选知识点，走联合检索
  if (bankQuery.value.trim()) bankConcept.value = ''
  scheduleBankSearch()
}

function scheduleConceptSuggest() {
  if (conceptSuggestTimer) clearTimeout(conceptSuggestTimer)
  conceptSuggestTimer = setTimeout(async () => {
    const q = bankQuery.value.trim()
    if (!q) {
      conceptSuggestions.value = []
      showConceptSuggest.value = false
      return
    }
    try {
      conceptSuggestions.value = await suggestConcepts(q, 10)
      showConceptSuggest.value = conceptSuggestions.value.length > 0
    } catch {
      conceptSuggestions.value = []
      showConceptSuggest.value = false
    }
  }, 220)
}

function onBankSearchKeyup() {
  onBankQueryInput()
  scheduleConceptSuggest()
}

async function applyConcept(name: string) {
  bankConcept.value = name
  bankQuery.value = ''
  showConceptSuggest.value = false
  conceptSuggestions.value = []
  await loadBank({ q: '', concept: name })
}

async function clearBankSearch() {
  bankQuery.value = ''
  bankConcept.value = ''
  bankMatchedConcepts.value = []
  showConceptSuggest.value = false
  conceptSuggestions.value = []
  await loadBank({ q: '', concept: '' })
}

async function submitBankSearch() {
  showConceptSuggest.value = false
  await loadBank()
}

async function ensureClassesForLearning() {
  if (myClasses.value.length) return
  myClasses.value = await listClasses()
}

function syncLearningClassCode() {
  if (learningClassCode.value) return
  learningClassCode.value =
    activeClassCode.value || myClasses.value[0]?.class_code || ''
}

async function loadClassLearning(refresh = false) {
  loading.value = true
  try {
    await ensureClassesForLearning()
    syncLearningClassCode()
    classLearning.value = await getClassLearning(
      refresh,
      learningClassCode.value || undefined,
    )
    await nextTick()
    renderMasteryChart()
  } finally {
    loading.value = false
  }
}

async function onLearningClassChange() {
  selectedStudentId.value = null
  studentDetail.value = null
  await loadClassLearning(false)
}

async function onExportLearningWord() {
  try {
    const blob = await exportClassLearningWord(learningClassCode.value || undefined)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `班级学情_${learningClassCode.value || 'export'}.docx`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('已导出 Word')
  } catch {
    ElMessage.error('导出失败')
  }
}

async function openStudent(id: number) {
  selectedStudentId.value = id
  studentDetail.value = await getStudentLearning(id)
}

function renderMasteryChart() {
  if (!masteryChartRef.value || !classLearning.value) return
  masteryChart?.dispose()
  masteryChart = echarts.init(masteryChartRef.value)
  const avg = classLearning.value.mastery_avg || {}
  const names = Object.keys(avg)
  const values = names.map((n) => Math.round((avg[n] || 0) * 100))
  masteryChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 16, top: 24, bottom: 48 },
    xAxis: {
      type: 'category',
      data: names.length ? names : ['暂无'],
      axisLabel: { rotate: 28, fontSize: 11 },
    },
    yAxis: { name: '%', max: 100 },
    series: [
      {
        type: 'bar',
        data: values.length ? values : [0],
        itemStyle: { color: '#0f766e' },
        barWidth: 28,
      },
    ],
  })
}

async function loadReflow() {
  loading.value = true
  try {
    const source =
      reflowFilter.value === 'memory'
        ? 'memory_summary'
        : undefined
    const items = await listReflow({ source, with_near_dup: true })
    if (reflowFilter.value === 'solve') {
      reflowItems.value = items.filter((x) => !x.from_memory)
    } else {
      reflowItems.value = items
    }
  } finally {
    loading.value = false
  }
}

function resetBankForm() {
  bankForm.value = { content: '', answer: '', analysis: '' }
  editingBankId.value = null
}

function startEditBank(q: BankItem) {
  editingBankId.value = q.id
  bankForm.value = {
    content: q.content || '',
    answer: q.answer || '',
    analysis: q.analysis || '',
  }
  showBankForm.value = true
}

function toggleBankForm() {
  if (showBankForm.value) {
    showBankForm.value = false
    resetBankForm()
    return
  }
  resetBankForm()
  showBankForm.value = true
}

async function onSaveBank() {
  if (!bankForm.value.content.trim() || !bankForm.value.answer.trim()) {
    ElMessage.warning('请填写题干与答案')
    return
  }
  if (editingBankId.value != null) {
    await updateBankItem(editingBankId.value, { ...bankForm.value })
    ElMessage.success('已更新')
  } else {
    await createBankItem({ ...bankForm.value })
    ElMessage.success('已入库')
  }
  showBankForm.value = false
  resetBankForm()
  await clearBankSearch()
}

async function onDeleteBank(id: number) {
  await deleteBankItem(id)
  ElMessage.success('已停用')
  if (editingBankId.value === id) {
    showBankForm.value = false
    resetBankForm()
  }
  await loadBank()
}

async function onApprove(id: number, force = false) {
  const res = await approveReflow(id, { force })
  if (res.needs_confirm && !force) {
    const top = res.near_dups?.[0]
    const tip = top
      ? `题库已有相近题 #${top.question_id}（相似度 ${(top.score * 100).toFixed(1)}%）。仍要入库吗？`
      : res.message || '存在相近题目，仍要入库吗？'
    if (window.confirm(tip)) {
      await onApprove(id, true)
    }
    return
  }
  if (!res.ok) {
    ElMessage.warning(res.message || '未能入库')
    return
  }
  ElMessage.success('已通过并入库')
  await loadReflow()
}

async function onReject(id: number) {
  await rejectReflow(id)
  ElMessage.success('已驳回')
  await loadReflow()
}

async function loadClasses() {
  loading.value = true
  try {
    myClasses.value = await listClasses()
    if (!activeClassCode.value && myClasses.value[0]) {
      activeClassCode.value = myClasses.value[0].class_code
      classMembers.value = await listClassMembers(activeClassCode.value)
    }
    if (!learningClassCode.value) {
      learningClassCode.value =
        activeClassCode.value || myClasses.value[0]?.class_code || ''
    }
  } finally {
    loading.value = false
  }
}

async function onCreateClass() {
  if (!newClassName.value.trim()) {
    ElMessage.warning('请填写班级名称')
    return
  }
  const room = await createClass(newClassName.value.trim())
  ElMessage.success(`已创建，班级码 ${room.class_code}`)
  newClassName.value = ''
  await loadClasses()
  activeClassCode.value = room.class_code
  classMembers.value = await listClassMembers(room.class_code)
}

async function openClass(code: string) {
  activeClassCode.value = code
  classMembers.value = await listClassMembers(code)
}

async function onRenameClass(c: ClassRoomItem) {
  const name = window.prompt('新的班级名称', c.name)
  if (name == null) return
  const trimmed = name.trim()
  if (!trimmed) {
    ElMessage.warning('名称不能为空')
    return
  }
  await renameClass(c.class_code, trimmed)
  ElMessage.success('已改名')
  await loadClasses()
  if (activeClassCode.value === c.class_code) {
    classMembers.value = await listClassMembers(c.class_code)
  }
}

async function onArchiveClass(c: ClassRoomItem) {
  if (!window.confirm(`确认归档班级「${c.name}」？归档后学生将无法继续加入。`)) return
  await archiveClass(c.class_code)
  ElMessage.success('已归档')
  const wasActive = activeClassCode.value === c.class_code
  if (wasActive) {
    activeClassCode.value = ''
    classMembers.value = []
  }
  await loadClasses()
}

async function onRemoveMember(m: ClassMember) {
  if (!activeClassCode.value) return
  if (!window.confirm(`确认将 ${m.nickname} 移出班级？`)) return
  await removeClassMember(activeClassCode.value, m.student_id)
  ElMessage.success('已移出')
  classMembers.value = await listClassMembers(activeClassCode.value)
}

async function loadObserve() {
  loading.value = true
  try {
    const traces = await listAgentTraces({
      limit: 80,
      status: traceFilterStatus.value || undefined,
      q: traceFilterQ.value.trim() || undefined,
    })
    agentTraces.value = traces.items
    tracesPrivacyNote.value = traces.privacy_note || ''
  } finally {
    loading.value = false
  }
}

async function openTraceDetail(t: AgentTraceItem) {
  traceDetailLoading.value = true
  selectedTrace.value = t
  try {
    selectedTrace.value = await getAgentTrace(t.id)
  } catch {
    ElMessage.error('加载轨迹详情失败')
  } finally {
    traceDetailLoading.value = false
  }
}

function closeTraceDetail() {
  selectedTrace.value = null
}

function formatTraceTime(iso?: string | null) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

function statusLabel(status?: TraceStatus | null, hit?: boolean) {
  const s = status || (hit ? 'bank_hit' : 'ok')
  const map: Record<string, string> = {
    ok: '正常',
    bank_hit: '题库命中',
    validate_fail: '评审未过',
    error: '异常失败',
    ai_reference: 'AI 参考答',
  }
  return map[s] || s
}

function statusClass(status?: TraceStatus | null, hit?: boolean) {
  const s = status || (hit ? 'bank_hit' : 'ok')
  if (s === 'error' || s === 'validate_fail') return 'warn'
  if (s === 'bank_hit') return 'memory'
  if (s === 'ai_reference') return 'concept'
  return 'score'
}

function formatDetailJson(detail?: Record<string, unknown> | null) {
  if (!detail) return ''
  return JSON.stringify(detail, null, 2)
}

async function refreshTab() {
  if (tab.value === 'class') await loadClasses()
  else if (tab.value === 'learning') await loadClassLearning()
  else if (tab.value === 'bank') await loadBank()
  else if (tab.value === 'reflow') await loadReflow()
  else if (tab.value === 'observe') await loadObserve()
}

watch(tab, () => {
  void refreshTab()
})

onMounted(() => {
  void refreshTab()
})

onBeforeUnmount(() => {
  masteryChart?.dispose()
  if (bankSearchTimer) clearTimeout(bankSearchTimer)
  if (conceptSuggestTimer) clearTimeout(conceptSuggestTimer)
})
</script>

<template>
  <AdminLayout>
    <div v-if="tab === 'class'" class="panel">
      <div class="panel__head">
        <div>
          <h1>班级管理</h1>
          <p>创建班级并生成班级码；学生注册时填写班级码加入</p>
        </div>
      </div>
      <div class="card" style="margin-bottom: 16px">
        <h3>新建班级</h3>
        <div style="display: flex; gap: 8px; margin-top: 8px">
          <input v-model="newClassName" placeholder="例如：数电 2024-1 班" style="flex:1;padding:8px 12px;border:1px solid #cbd5e1;border-radius:8px" />
          <button class="btn" type="button" :disabled="loading" @click="onCreateClass">创建并生成班级码</button>
        </div>
      </div>
      <div class="grid-2">
        <div class="card">
          <h3>我的班级</h3>
          <ul class="list">
            <li v-for="c in myClasses" :key="c.id" class="class-row">
              <button type="button" class="linkish" @click="openClass(c.class_code)">
                {{ c.name }} · 码 {{ c.class_code }} · {{ c.n_students }} 人
                <span v-if="c.status !== 'active'" class="muted"> · {{ c.status }}</span>
              </button>
              <div class="class-row__actions">
                <button class="btn" type="button" @click="onRenameClass(c)">改名</button>
                <button class="btn" type="button" @click="onArchiveClass(c)">归档</button>
                <button class="btn" type="button" @click="openClass(c.class_code)">查看成员</button>
              </div>
            </li>
          </ul>
          <p v-if="!myClasses.length" class="muted">暂无班级，先创建一个</p>
        </div>
        <div class="card">
          <h3>成员 · {{ activeClassCode || '未选择' }}</h3>
          <ul class="list">
            <li v-for="m in classMembers" :key="m.student_id" class="member-row">
              <span>{{ m.nickname }} · {{ m.phone }}</span>
              <button class="btn danger" type="button" @click="onRemoveMember(m)">移出</button>
            </li>
          </ul>
          <p v-if="activeClassCode && !classMembers.length" class="muted">暂无学生加入</p>
        </div>
      </div>
    </div>

    <div v-else-if="tab === 'learning'" class="panel">
      <div class="panel__head">
        <div>
          <h1>学情总览</h1>
          <p>班级掌握度与薄弱点（不含学生对话隐私）</p>
        </div>
        <div class="learning-toolbar">
          <select
            v-model="learningClassCode"
            class="filter"
            :disabled="loading || !myClasses.length"
            @change="onLearningClassChange"
          >
            <option disabled value="">选择班级</option>
            <option v-for="c in myClasses" :key="c.class_code" :value="c.class_code">
              {{ c.name }}（{{ c.class_code }}）
            </option>
          </select>
          <button class="btn" type="button" :disabled="loading" @click="onExportLearningWord">
            导出 Word
          </button>
          <button class="btn" type="button" :disabled="loading" @click="loadClassLearning(true)">
            刷新聚合
          </button>
        </div>
      </div>
      <div v-if="classLearning" class="grid-2">
        <div class="card">
          <h3>掌握度分布</h3>
          <div ref="masteryChartRef" class="chart" />
          <p class="muted">
            班级 {{ classLearning.class_code }} · {{ classLearning.n_students }} 人
          </p>
          <div class="stat-block">
            <h4>学习进度</h4>
            <p class="muted">
              学生数 {{ learningProgress.n_students }} · 章节完成事件
              {{ learningProgress.chapter_completion_events }}
            </p>
          </div>
          <div class="stat-block">
            <h4>薄弱知识点 Top</h4>
            <div v-if="classLearning.weak_top?.length" class="chip-row">
              <span
                v-for="w in classLearning.weak_top"
                :key="w.name"
                class="chip"
              >
                {{ w.name }} · {{ w.count }}
              </span>
            </div>
            <p v-else class="muted">暂无</p>
          </div>
          <div class="stat-block">
            <h4>高频错因</h4>
            <div v-if="classLearning.mistake_top?.length" class="chip-row">
              <span
                v-for="w in classLearning.mistake_top"
                :key="w.name"
                class="chip chip--warn"
              >
                {{ w.name }} · {{ w.count }}
              </span>
            </div>
            <p v-else class="muted">暂无</p>
          </div>
          <div class="stat-block">
            <h4>练习概况</h4>
            <p class="muted">
              场次 {{ classLearning.practice?.n_sessions ?? 0 }} · 参与学生
              {{ classLearning.practice?.n_students ?? 0 }} · 平均正确率
              {{
                classLearning.practice?.avg_accuracy != null
                  ? `${Math.round(Number(classLearning.practice.avg_accuracy) * 100)}%`
                  : '—'
              }}
            </p>
          </div>
        </div>
        <div class="card">
          <h3>学生名册</h3>
          <ul class="list">
            <li v-for="s in classLearning.roster" :key="s.student_id">
              <button type="button" class="linkish" @click="openStudent(s.student_id)">
                {{ s.nickname }}
              </button>
              <span class="muted">掌握均值 {{ Math.round(s.mastery_avg * 100) }}%</span>
            </li>
          </ul>
          <div v-if="studentDetail" class="detail">
            <h4>{{ studentDetail.nickname }} · 薄弱点</h4>
            <p>{{ (studentDetail.weak_points || []).join('、') || '暂无' }}</p>
            <p class="muted">{{ studentDetail.privacy_note }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="tab === 'bank'" class="panel">
      <div class="panel__head">
        <div>
          <h1>题库维护</h1>
          <p>支持关键词与知识点检索；默认展示最新入库题目</p>
        </div>
        <button class="btn primary" type="button" @click="toggleBankForm">
          {{ showBankForm ? '收起' : '新增题目' }}
        </button>
      </div>

      <div class="bank-search card">
        <div class="bank-search__row">
          <div class="bank-search__field">
            <input
              v-model="bankQuery"
              class="bank-search__input"
              type="search"
              placeholder="搜索题干 / 答案 / 来源，或输入知识点名称…"
              autocomplete="off"
              @keyup="onBankSearchKeyup"
              @keydown.enter.prevent="submitBankSearch"
              @focus="scheduleConceptSuggest"
            />
            <ul
              v-if="showConceptSuggest && conceptSuggestions.length"
              class="bank-suggest"
            >
              <li class="bank-suggest__hint">图谱知识点</li>
              <li
                v-for="c in conceptSuggestions"
                :key="c"
              >
                <button type="button" class="bank-suggest__item" @click="applyConcept(c)">
                  {{ c }}
                </button>
              </li>
            </ul>
          </div>
          <button
            class="btn primary"
            type="button"
            :disabled="bankSearching"
            @click="submitBankSearch"
          >
            搜索
          </button>
          <button
            v-if="bankQuery || bankConcept || bankMode !== 'latest'"
            class="btn"
            type="button"
            @click="clearBankSearch"
          >
            清除
          </button>
        </div>
        <div v-if="bankConcept" class="bank-search__chips">
          <span class="badge concept">知识点 · {{ bankConcept }}</span>
          <button type="button" class="linkish" @click="clearBankSearch">取消</button>
        </div>
        <p class="bank-search__tip muted">
          直接回车做关键词/语义联合检索；点选下方联想可按知识点从图谱找最相关题目
        </p>
      </div>

      <div v-if="showBankForm" class="card form">
        <h3>{{ editingBankId != null ? `编辑题目 #${editingBankId}` : '新增题目' }}</h3>
        <label>题干<textarea v-model="bankForm.content" rows="3" /></label>
        <label>答案<textarea v-model="bankForm.answer" rows="2" /></label>
        <label>解析<textarea v-model="bankForm.analysis" rows="2" /></label>
        <button class="btn primary" type="button" @click="onSaveBank">
          {{ editingBankId != null ? '保存修改' : '保存入库' }}
        </button>
      </div>

      <div class="card">
        <div class="bank-list__head">
          <div>
            <h3 class="bank-list__title">{{ bankListTitle }}</h3>
            <p class="muted">{{ bankListHint }}</p>
          </div>
          <span v-if="bankSearching" class="muted">检索中…</span>
        </div>
        <ul class="list dense">
          <li v-for="q in bankItems" :key="q.id">
            <div class="grow">
              <FormulaText :content="q.content" />
              <p class="muted bank-meta">
                #{{ q.id }}
                <span v-if="q.source"> · {{ q.source }}</span>
                <span v-if="q.status !== 'active'"> · {{ q.status }}</span>
                <span v-if="needsKgReview(q)" class="badge warn">缺图谱标</span>
                <span v-if="q.match_via" class="badge via">{{ matchViaLabel(q.match_via) }}</span>
                <span v-if="typeof q.score === 'number'" class="badge score">
                  {{ (q.score * 100).toFixed(0) }}%
                </span>
              </p>
              <p v-if="tagNames(q.knowledge_tags).length" class="tag-row">
                <span v-for="t in tagNames(q.knowledge_tags)" :key="t" class="badge tag">{{ t }}</span>
              </p>
              <details v-if="q.answer" class="bank-ans">
                <summary>查看答案</summary>
                <FormulaText :content="q.answer" />
              </details>
            </div>
            <div class="bank-item-actions">
              <button class="btn" type="button" @click="startEditBank(q)">编辑</button>
              <button
                v-if="q.status === 'active'"
                class="btn danger"
                type="button"
                @click="onDeleteBank(q.id)"
              >
                停用
              </button>
            </div>
          </li>
        </ul>
        <p v-if="!bankItems.length && !bankSearching" class="muted">
          {{ bankMode === 'latest' ? '暂无题目' : '未找到相关题目' }}
        </p>
      </div>
    </div>

    <div v-else-if="tab === 'reflow'" class="panel">
      <div class="panel__head">
        <div>
          <h1>回流审核</h1>
          <p>
            解题未命中回流 + 记忆压缩抽题候选；入库前若向量相似度 ≥ 0.95 会提示相近题，仍由管理员确认
          </p>
        </div>
        <div class="reflow-toolbar">
          <select v-model="reflowFilter" class="filter" @change="loadReflow">
            <option value="all">全部待审</option>
            <option value="memory">记忆抽题</option>
            <option value="solve">解题回流</option>
          </select>
          <button class="btn" type="button" :disabled="loading" @click="loadReflow">刷新</button>
        </div>
      </div>
      <div class="card">
        <ul class="list dense reflow-list">
          <li v-for="r in reflowItems" :key="r.id" class="reflow-item">
            <div class="grow">
              <p class="reflow-meta">
                #{{ r.id }} · {{ r.source || 'text' }} · 校验分 {{ r.validate_score ?? '—' }}
                <span v-if="r.from_memory" class="badge memory">记忆抽题</span>
                <span v-if="r.has_near_dup" class="badge warn">近重 ≥0.95</span>
                <span v-if="r.created_at"> · {{ r.created_at }}</span>
              </p>
              <p v-if="tagNames(r.knowledge_tags).length" class="tag-row">
                <span v-for="t in tagNames(r.knowledge_tags)" :key="t" class="badge tag">{{ t }}</span>
              </p>
              <h4 class="reflow-h">原题溯源（题干）</h4>
              <div v-if="r.image_path" class="stem-img-wrap">
                <img class="stem-img" :src="r.image_path" alt="题干原图" />
              </div>
              <div class="reflow-box">
                <FormulaText :content="r.question || '（无题干）'" />
              </div>
              <h4 class="reflow-h">AI 答案（待审）</h4>
              <div class="reflow-box">
                <FormulaText :content="r.ai_answer || '（无答案）'" />
              </div>
              <div v-if="r.near_dups?.length" class="near-dup">
                <h4 class="reflow-h">相近题库题（仅提示，不自动拦截）</h4>
                <ul>
                  <li v-for="d in r.near_dups" :key="d.question_id">
                    #{{ d.question_id }} · 分 {{ d.score.toFixed(3) }} —
                    {{ (d.content || '').slice(0, 120) }}{{ (d.content || '').length > 120 ? '…' : '' }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="reflow-actions">
              <button class="btn primary" type="button" @click="onApprove(r.id)">通过入库</button>
              <button class="btn" type="button" @click="onReject(r.id)">驳回</button>
            </div>
          </li>
        </ul>
        <p v-if="!reflowItems.length" class="muted">暂无待审</p>
      </div>
    </div>

    <div v-else-if="tab === 'observe'" class="panel">
      <div class="panel__head">
        <div>
          <h1>系统观测</h1>
          <p>按时间回溯用户解题回答，点击详情查看代码级流程以定位失败与错误</p>
        </div>
        <button class="btn" type="button" :disabled="loading" @click="loadObserve">刷新</button>
      </div>

      <div class="card observe-filters">
        <label>
          状态
          <select v-model="traceFilterStatus" class="filter" @change="loadObserve">
            <option value="">全部</option>
            <option value="error">异常失败</option>
            <option value="validate_fail">评审未过</option>
            <option value="ai_reference">AI 参考答</option>
            <option value="bank_hit">题库命中</option>
            <option value="ok">正常</option>
          </select>
        </label>
        <label class="grow">
          搜索
          <input
            v-model="traceFilterQ"
            type="search"
            placeholder="题面 / 昵称 / thread"
            @keydown.enter="loadObserve"
          />
        </label>
        <button class="btn primary" type="button" :disabled="loading" @click="loadObserve">
          查询
        </button>
      </div>

      <p v-if="tracesPrivacyNote" class="muted observe-note">{{ tracesPrivacyNote }}</p>

      <ul class="list dense observe-list">
        <li v-for="t in agentTraces" :key="t.id" class="trace-item">
          <div class="grow">
            <p class="reflow-meta">
              <time>{{ formatTraceTime(t.created_at) }}</time>
              <span> · #{{ t.id }}</span>
              <span v-if="t.nickname"> · {{ t.nickname }}</span>
              <span v-if="t.intent"> · intent={{ t.intent }}</span>
              <span class="badge" :class="statusClass(t.status, t.hit)">
                {{ statusLabel(t.status, t.hit) }}
              </span>
            </p>
            <p class="trace-preview">{{ t.question_preview || '（无题面预览）' }}</p>
            <p v-if="t.answer_preview" class="muted answer-preview">
              答：{{ t.answer_preview }}
            </p>
          </div>
          <button class="btn" type="button" @click="openTraceDetail(t)">查看详情</button>
        </li>
      </ul>
      <p v-if="!agentTraces.length" class="muted">暂无可观测轨迹</p>

      <div v-if="selectedTrace" class="trace-drawer-mask" @click.self="closeTraceDetail">
        <aside class="trace-drawer">
          <div class="trace-drawer__head">
            <div>
              <h2>回答详情 #{{ selectedTrace.id }}</h2>
              <p class="muted">
                {{ formatTraceTime(selectedTrace.created_at) }}
                <span v-if="selectedTrace.nickname"> · {{ selectedTrace.nickname }}</span>
                <span v-if="selectedTrace.thread_id"> · {{ selectedTrace.thread_id }}</span>
              </p>
            </div>
            <button class="btn" type="button" @click="closeTraceDetail">关闭</button>
          </div>

          <p v-if="traceDetailLoading" class="muted">加载中…</p>
          <template v-else>
            <div class="trace-meta-grid">
              <div>
                <span class="muted">状态</span>
                <b>{{ statusLabel(selectedTrace.status, selectedTrace.hit) }}</b>
              </div>
              <div>
                <span class="muted">意图</span>
                <b>{{ selectedTrace.intent || '—' }}</b>
              </div>
              <div>
                <span class="muted">权威评审</span>
                <b>
                  <template v-if="selectedTrace.validate_passed == null">—</template>
                  <template v-else>
                    {{ selectedTrace.validate_passed ? '通过' : '未过' }}
                    <span v-if="selectedTrace.validate_score != null">
                      · {{ Number(selectedTrace.validate_score).toFixed(3) }}
                    </span>
                  </template>
                </b>
              </div>
              <div>
                <span class="muted">交付标签</span>
                <b>{{ selectedTrace.trust_label || '—' }}</b>
              </div>
            </div>

            <section class="trace-section">
              <h3>题面摘要</h3>
              <p>{{ selectedTrace.question_preview || '—' }}</p>
            </section>
            <section v-if="selectedTrace.answer_preview" class="trace-section">
              <h3>答案摘要</h3>
              <p>{{ selectedTrace.answer_preview }}</p>
            </section>
            <section v-if="selectedTrace.error" class="trace-section error">
              <h3>异常信息</h3>
              <pre>{{ selectedTrace.error }}</pre>
            </section>

            <section class="trace-section">
              <h3>图节点流程（代码级）</h3>
              <ol v-if="selectedTrace.steps?.length" class="timeline">
                <li v-for="(step, idx) in selectedTrace.steps" :key="idx">
                  <span class="timeline__idx">{{ idx + 1 }}</span>
                  <code>{{ step }}</code>
                </li>
              </ol>
              <p v-else class="muted">无节点日志</p>
            </section>

            <section class="trace-section">
              <h3>工具调用链</h3>
              <ol v-if="selectedTrace.tool_trace?.length" class="timeline tools">
                <li v-for="(step, idx) in selectedTrace.tool_trace" :key="idx">
                  <span class="timeline__idx">{{ idx + 1 }}</span>
                  <code>{{ step }}</code>
                </li>
              </ol>
              <p v-else class="muted">本次无工具调用记录（旧轨迹或未走 ReAct）</p>
            </section>

            <section v-if="selectedTrace.detail" class="trace-section">
              <h3>结构化明细</h3>
              <pre class="detail-json">{{ formatDetailJson(selectedTrace.detail) }}</pre>
            </section>
          </template>
        </aside>
      </div>
    </div>
  </AdminLayout>
</template>

<style scoped>
.panel__head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 16px;
}
.panel__head h1 {
  margin: 0;
  font-size: 22px;
}
.panel__head p {
  margin: 6px 0 0;
  color: #64748b;
  font-size: 13px;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 16px;
}
.card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px;
}
.chart {
  height: 260px;
}
.list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.list.dense li {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f5f9;
}
.grow {
  flex: 1;
  min-width: 0;
}
.muted {
  color: #64748b;
  font-size: 12px;
}
.btn {
  border: 1px solid #cbd5e1;
  background: #fff;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
}
.btn.primary {
  background: #0f766e;
  border-color: #0f766e;
  color: #fff;
}
.btn.danger {
  color: #b91c1c;
  border-color: #fecaca;
}
.linkish {
  border: 0;
  background: transparent;
  color: #0f766e;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}
.form {
  display: grid;
  gap: 10px;
  margin-bottom: 16px;
}
.form label {
  display: grid;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
}
.form textarea,
.form input[type='number'] {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 10px;
  font: inherit;
}
.detail {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}
.reflow-list li.reflow-item {
  flex-direction: column;
  align-items: stretch;
  gap: 12px;
}
.reflow-meta {
  margin: 0 0 8px;
  color: #64748b;
  font-size: 12px;
}
.reflow-h {
  margin: 12px 0 6px;
  font-size: 13px;
  color: #0f766e;
}
.reflow-box {
  padding: 10px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #0f172a;
}
.bank-ans {
  margin-top: 8px;
  font-size: 13px;
}
.bank-ans summary {
  cursor: pointer;
  color: #0f766e;
}
.bank-search {
  margin-bottom: 16px;
}
.bank-search__row {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}
.bank-search__field {
  position: relative;
  flex: 1;
  min-width: 0;
}
.bank-search__input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 10px 12px;
  font: inherit;
  font-size: 14px;
}
.bank-search__input:focus {
  outline: 2px solid #99f6e4;
  border-color: #0f766e;
}
.bank-search__tip {
  margin: 10px 0 0;
}
.bank-search__chips {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}
.bank-suggest {
  position: absolute;
  z-index: 20;
  left: 0;
  right: 0;
  top: calc(100% + 4px);
  margin: 0;
  padding: 6px 0;
  list-style: none;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  max-height: 240px;
  overflow: auto;
}
.bank-suggest__hint {
  padding: 4px 12px;
  font-size: 11px;
  color: #94a3b8;
}
.bank-suggest__item {
  display: block;
  width: 100%;
  text-align: left;
  border: 0;
  background: transparent;
  padding: 8px 12px;
  font: inherit;
  font-size: 13px;
  cursor: pointer;
}
.bank-suggest__item:hover {
  background: #f0fdfa;
  color: #0f766e;
}
.bank-list__head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}
.bank-list__title {
  margin: 0;
  font-size: 15px;
}
.bank-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  margin-top: 6px;
}
.bank-item-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}
.stem-img-wrap {
  margin: 8px 0 12px;
  max-width: 420px;
}
.stem-img {
  display: block;
  width: 100%;
  max-height: 320px;
  object-fit: contain;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
}
.reflow-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.reflow-toolbar,
.learning-toolbar {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.filter {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 13px;
  background: #fff;
}
.badge {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
}
.badge.memory {
  background: #ecfdf5;
  color: #047857;
}
.badge.warn {
  background: #fff7ed;
  color: #c2410c;
}
.badge.concept {
  background: #ecfdf5;
  color: #0f766e;
  margin-left: 0;
}
.badge.via {
  background: #f1f5f9;
  color: #475569;
  margin-left: 0;
}
.badge.score {
  background: #fff7ed;
  color: #c2410c;
  margin-left: 0;
}
.badge.tag {
  background: #eef2ff;
  color: #4338ca;
  margin-left: 0;
}
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 6px 0 8px;
}
.near-dup {
  margin-top: 10px;
  padding: 10px 12px;
  background: #fffbeb;
  border-radius: 8px;
  font-size: 12px;
  color: #92400e;
}
.near-dup ul {
  margin: 6px 0 0;
  padding-left: 1.1em;
}
.class-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f5f9;
}
.class-row__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.member-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}
.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}
.chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: #ecfdf5;
  color: #0f766e;
  font-size: 12px;
  font-weight: 600;
}
.chip--warn {
  background: #fff7ed;
  color: #c2410c;
}
.stat-block {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}
.stat-block h4 {
  margin: 0 0 4px;
  font-size: 13px;
  color: #0f766e;
}
.trace-item {
  flex-direction: row;
  align-items: flex-start;
  gap: 12px;
}
.trace-preview {
  margin: 0 0 4px;
  font-size: 14px;
  color: #0f172a;
}
.answer-preview {
  margin: 0;
  font-size: 12px;
  line-height: 1.45;
}
.observe-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-end;
  margin-bottom: 12px;
}
.observe-filters label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
}
.observe-filters label.grow {
  flex: 1;
  min-width: 220px;
}
.observe-filters input[type='search'] {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 14px;
}
.observe-note {
  margin: 0 0 12px;
  font-size: 12px;
}
.observe-list .trace-item {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 14px;
}
.trace-drawer-mask {
  position: fixed;
  inset: 0;
  z-index: 40;
  background: rgba(15, 23, 42, 0.35);
  display: flex;
  justify-content: flex-end;
}
.trace-drawer {
  width: min(560px, 100%);
  height: 100%;
  overflow: auto;
  background: #fff;
  padding: 20px;
  box-shadow: -8px 0 24px rgba(15, 23, 42, 0.12);
}
.trace-drawer__head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
  margin-bottom: 16px;
}
.trace-drawer__head h2 {
  margin: 0;
  font-size: 18px;
}
.trace-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 16px;
}
.trace-meta-grid > div {
  background: #f8fafc;
  border-radius: 10px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.trace-meta-grid b {
  font-size: 13px;
  color: #0f172a;
}
.trace-section {
  margin-bottom: 18px;
}
.trace-section h3 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #0f766e;
}
.trace-section p {
  margin: 0;
  font-size: 13px;
  line-height: 1.55;
  color: #334155;
}
.trace-section.error pre,
.detail-json {
  margin: 0;
  padding: 10px 12px;
  border-radius: 10px;
  background: #0f172a;
  color: #e2e8f0;
  font-size: 12px;
  line-height: 1.45;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}
.trace-section.error pre {
  background: #7f1d1d;
}
.timeline {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.timeline li {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.timeline__idx {
  flex: 0 0 22px;
  height: 22px;
  border-radius: 999px;
  background: #ccfbf1;
  color: #0f766e;
  font-size: 11px;
  font-weight: 700;
  display: grid;
  place-items: center;
}
.timeline code {
  flex: 1;
  font-size: 12px;
  line-height: 1.45;
  color: #1e293b;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 8px 10px;
  white-space: pre-wrap;
  word-break: break-word;
}
.timeline.tools .timeline__idx {
  background: #e0e7ff;
  color: #3730a3;
}
</style>

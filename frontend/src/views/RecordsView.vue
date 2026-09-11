<script setup lang="ts">
/**
 * 错题与学情：错题本 CRUD/导入导出 + 多元学情可视化 + 学情 Word 导出
 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

import StudentLayout from '@/layouts/StudentLayout.vue'
import FormulaText from '@/components/markdown/FormulaText.vue'
import {
  createMistake,
  deleteMistake,
  exportMistakesWord,
  importMistakes,
  listMistakes,
  updateMistake,
  type MistakeItem,
} from '@/api/mistakes'
import {
  exportProfileWord,
  getStudentProfile,
  listMySummaries,
  rebuildStudentProfile,
  type StudentProfileData,
} from '@/api/profile'

const route = useRoute()
const tab = ref<'mistakes' | 'profile' | 'memory'>('mistakes')
const loading = ref(false)
const rebuilding = ref(false)
const exporting = ref(false)
const mistakes = ref<MistakeItem[]>([])
const profile = ref<StudentProfileData | null>(null)
const summaries = ref<
  Array<{
    id: number
    agent: string
    summary_text: string
    topics: string[]
    created_at?: string | null
  }>
>([])
const noteDrafts = ref<Record<number, string>>({})
const filterSource = ref<'all' | 'practice' | 'solve' | 'manual' | 'import'>('all')
const keyword = ref('')

const showCreate = ref(false)
const createForm = ref({ question: '', answer: '', reason: '', tags: '' })
const creating = ref(false)

const showImport = ref(false)
const importText = ref('')
const importing = ref(false)

const studyChartRef = ref<HTMLDivElement | null>(null)
const masterChartRef = ref<HTMLDivElement | null>(null)
const solvesChartRef = ref<HTMLDivElement | null>(null)
const mistakeTagChartRef = ref<HTMLDivElement | null>(null)
const topicChartRef = ref<HTMLDivElement | null>(null)
const accuracyChartRef = ref<HTMLDivElement | null>(null)

let studyChart: echarts.ECharts | null = null
let masterChart: echarts.ECharts | null = null
let solvesChart: echarts.ECharts | null = null
let mistakeTagChart: echarts.ECharts | null = null
let topicChart: echarts.ECharts | null = null
let accuracyChart: echarts.ECharts | null = null

const weekLabels = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

const filteredMistakes = computed(() => {
  const q = keyword.value.trim().toLowerCase()
  return mistakes.value.filter((m) => {
    const src = String(m.add_source || '')
    if (filterSource.value === 'practice' && src !== 'practice') return false
    if (filterSource.value === 'solve' && src !== 'solve') return false
    if (filterSource.value === 'manual' && src !== 'manual') return false
    if (
      filterSource.value === 'import' &&
      !['manual_import', 'exam_import', 'import'].includes(src)
    ) {
      return false
    }
    if (!q) return true
    const blob = `${m.question_snapshot || ''} ${m.answer_snapshot || ''} ${m.reason || ''}`.toLowerCase()
    return blob.includes(q)
  })
})

async function loadMistakes() {
  loading.value = true
  try {
    mistakes.value = await listMistakes()
    for (const m of mistakes.value) {
      noteDrafts.value[m.id] = m.reason || ''
    }
  } finally {
    loading.value = false
  }
}

async function loadProfile() {
  loading.value = true
  try {
    profile.value = await getStudentProfile()
  } finally {
    loading.value = false
  }
}

async function onRebuildProfile() {
  if (rebuilding.value) return
  rebuilding.value = true
  try {
    profile.value = await rebuildStudentProfile()
    ElMessage.success('学情已更新')
    await nextTick()
    renderCharts()
  } catch (e: unknown) {
    const msg =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      '更新失败，请稍后重试'
    ElMessage.warning(typeof msg === 'string' ? msg : '更新失败')
  } finally {
    rebuilding.value = false
  }
}

async function loadSummaries() {
  loading.value = true
  try {
    summaries.value = await listMySummaries()
  } finally {
    loading.value = false
  }
}

async function saveNote(id: number) {
  await updateMistake(id, { reason: noteDrafts.value[id] })
  ElMessage.success('复盘已保存')
  await loadMistakes()
}

async function remove(id: number) {
  await deleteMistake(id)
  ElMessage.success('已删除')
  await loadMistakes()
}

async function exportWord() {
  exporting.value = true
  try {
    const blob = await exportMistakesWord()
    downloadBlob(blob, 'mistakes.docx')
    ElMessage.success('错题本已导出')
  } catch {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

async function exportLearning() {
  exporting.value = true
  try {
    const blob = await exportProfileWord()
    downloadBlob(blob, 'learning_profile.docx')
    ElMessage.success('学情报告已导出')
  } catch {
    ElMessage.error('学情导出失败')
  } finally {
    exporting.value = false
  }
}

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

async function submitCreate() {
  const q = createForm.value.question.trim()
  if (!q) {
    ElMessage.warning('请填写题干')
    return
  }
  creating.value = true
  try {
    const tags = createForm.value.tags
      .split(/[,，、]/)
      .map((x) => x.trim())
      .filter(Boolean)
    await createMistake({
      question_snapshot: q,
      answer_snapshot: createForm.value.answer.trim() || undefined,
      reason: createForm.value.reason.trim() || undefined,
      knowledge_tags: tags.length ? { tags } : undefined,
    })
    ElMessage.success('已加入错题本')
    showCreate.value = false
    createForm.value = { question: '', answer: '', reason: '', tags: '' }
    await loadMistakes()
  } catch {
    ElMessage.error('新增失败')
  } finally {
    creating.value = false
  }
}

async function submitImport() {
  const raw = importText.value.trim()
  if (!raw) {
    ElMessage.warning('请粘贴要导入的内容')
    return
  }
  importing.value = true
  try {
    let items: Array<{ question: string; answer?: string; reason?: string }> = []
    if (raw.startsWith('[') || raw.startsWith('{')) {
      const parsed = JSON.parse(raw)
      const list = Array.isArray(parsed) ? parsed : parsed.items || []
      items = list
        .map((it: any) => ({
          question: String(it.question || it.question_snapshot || '').trim(),
          answer: String(it.answer || it.answer_snapshot || '').trim() || undefined,
          reason: String(it.reason || '批量导入').trim(),
        }))
        .filter((it: { question: string }) => it.question)
    } else {
      items = raw
        .split(/\n+/)
        .map((line) => line.trim())
        .filter(Boolean)
        .map((line) => {
          const [q, a] = line.split(/\t|\s\|\s/)
          return {
            question: (q || '').trim(),
            answer: (a || '').trim() || undefined,
            reason: '文本导入',
          }
        })
        .filter((it) => it.question)
    }
    if (!items.length) {
      ElMessage.warning('未解析到有效题目')
      return
    }
    const count = await importMistakes(items)
    ElMessage.success(`已导入 ${count} 道`)
    showImport.value = false
    importText.value = ''
    await loadMistakes()
  } catch {
    ElMessage.error('导入失败，请检查 JSON 或文本格式')
  } finally {
    importing.value = false
  }
}

function disposeCharts() {
  ;[
    studyChart,
    masterChart,
    solvesChart,
    mistakeTagChart,
    topicChart,
    accuracyChart,
  ].forEach((c) => c?.dispose())
  studyChart = null
  masterChart = null
  solvesChart = null
  mistakeTagChart = null
  topicChart = null
  accuracyChart = null
}

function renderCharts() {
  if (!profile.value) return
  disposeCharts()

  const weekly = profile.value.practice_stats?.weekly_minutes || [0, 0, 0, 0, 0, 0, 0]
  if (studyChartRef.value) {
    studyChart = echarts.init(studyChartRef.value)
    studyChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: 36, right: 12, top: 24, bottom: 28 },
      xAxis: { type: 'category', data: weekLabels },
      yAxis: { name: '分钟', splitLine: { lineStyle: { type: 'dashed' } } },
      series: [
        {
          type: 'bar',
          data: weekly,
          itemStyle: { color: '#06b6d4', borderRadius: [4, 4, 0, 0] },
          barWidth: 18,
        },
      ],
    })
  }

  const mastery = profile.value.mastery || {}
  const indicators = Object.keys(mastery).map((name) => ({ name, max: 100 }))
  const values = Object.values(mastery).map((v) => Math.round(Number(v) * 100))
  if (masterChartRef.value) {
    masterChart = echarts.init(masterChartRef.value)
    masterChart.setOption({
      tooltip: {},
      radar: {
        indicator: indicators.length ? indicators : [{ name: '暂无', max: 100 }],
        radius: '62%',
      },
      series: [
        {
          type: 'radar',
          data: [
            {
              value: values.length ? values : [0],
              areaStyle: { color: 'rgba(6,182,212,.25)' },
              lineStyle: { color: '#06b6d4' },
            },
          ],
        },
      ],
    })
  }

  const weeklySolves = profile.value.practice_stats?.weekly_solves || [0, 0, 0, 0, 0, 0, 0]
  if (solvesChartRef.value) {
    solvesChart = echarts.init(solvesChartRef.value)
    solvesChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: 36, right: 12, top: 24, bottom: 28 },
      xAxis: { type: 'category', data: weekLabels },
      yAxis: { name: '题数', minInterval: 1 },
      series: [
        {
          type: 'line',
          smooth: true,
          data: weeklySolves,
          areaStyle: { color: 'rgba(14,116,144,.12)' },
          lineStyle: { color: '#0e7490', width: 2 },
          itemStyle: { color: '#0e7490' },
        },
      ],
    })
  }

  const topTags =
    profile.value.practice_stats?.mistake_stats?.top_tags ||
    profile.value.mistake_stats?.top_tags ||
    []
  const tagNames = topTags.map((t: any) => (typeof t === 'string' ? t : t.name))
  const tagCounts = topTags.map((t: any) => (typeof t === 'string' ? 1 : Number(t.count) || 0))
  if (mistakeTagChartRef.value) {
    mistakeTagChart = echarts.init(mistakeTagChartRef.value)
    mistakeTagChart.setOption({
      tooltip: { trigger: 'axis' },
      grid: { left: 80, right: 16, top: 16, bottom: 24 },
      xAxis: { type: 'value', minInterval: 1 },
      yAxis: {
        type: 'category',
        data: tagNames.length ? tagNames.slice().reverse() : ['暂无'],
        axisLabel: { width: 72, overflow: 'truncate' },
      },
      series: [
        {
          type: 'bar',
          data: (tagCounts.length ? tagCounts : [0]).slice().reverse(),
          itemStyle: { color: '#f59e0b', borderRadius: [0, 4, 4, 0] },
          barWidth: 14,
        },
      ],
    })
  }

  const freq = profile.value.topic_freq || {}
  const topicEntries = Object.entries(freq)
    .sort((a, b) => Number(b[1]) - Number(a[1]))
    .slice(0, 8)
  if (topicChartRef.value) {
    topicChart = echarts.init(topicChartRef.value)
    topicChart.setOption({
      tooltip: { trigger: 'item' },
      series: [
        {
          type: 'pie',
          radius: ['42%', '68%'],
          data: topicEntries.length
            ? topicEntries.map(([name, value]) => ({ name, value }))
            : [{ name: '暂无话题', value: 1 }],
          label: { fontSize: 11 },
        },
      ],
    })
  }

  const acc = Math.round(Number(profile.value.practice_stats?.accuracy ?? 0) * 100)
  if (accuracyChartRef.value) {
    accuracyChart = echarts.init(accuracyChartRef.value)
    accuracyChart.setOption({
      series: [
        {
          type: 'gauge',
          min: 0,
          max: 100,
          progress: { show: true, width: 12 },
          axisLine: { lineStyle: { width: 12 } },
          axisTick: { show: false },
          splitLine: { length: 8, lineStyle: { width: 2 } },
          pointer: { length: '58%', width: 4 },
          detail: { valueAnimation: true, formatter: '{value}%', fontSize: 18 },
          data: [{ value: acc, name: '正确率' }],
        },
      ],
    })
  }
}

function onResize() {
  ;[
    studyChart,
    masterChart,
    solvesChart,
    mistakeTagChart,
    topicChart,
    accuracyChart,
  ].forEach((c) => c?.resize())
}

function tagLabel(item: MistakeItem): string {
  if (item.add_source === 'solve') return '答疑加入'
  if (item.add_source === 'exam' || item.add_source === 'exam_import') return '导入'
  if (item.add_source === 'manual_import') return '批量导入'
  if (item.add_source === 'practice') return '练习错题'
  if (item.add_source === 'manual') return '手动新增'
  return '需复盘'
}

function tagClass(item: MistakeItem): string {
  if (item.add_source === 'solve') return 'bg-violet-100 text-violet-700'
  if (item.add_source === 'practice') return 'bg-rose-50 text-rose-600'
  if (item.reason) return 'bg-emerald-50 text-emerald-600'
  return 'bg-amber-50 text-amber-700'
}

const totalSolves = () => profile.value?.practice_stats?.total_solves ?? 0
const weakCount = () => profile.value?.weak_points?.length ?? 0
const avgMastery = () => {
  const m = profile.value?.mastery
  if (!m || !Object.keys(m).length) return '—'
  const avg = Object.values(m).reduce((a, b) => a + Number(b), 0) / Object.values(m).length
  return `${Math.round(avg * 100)}%`
}
const lastSessionLabel = () => {
  const s = profile.value?.practice_stats?.last_session
  if (!s) return '尚无加练记录'
  return `最近一场 ${s.correct ?? '—'}/${s.total ?? '—'} · ${Math.round(Number(s.accuracy || 0) * 100)}%`
}

watch(tab, async (t) => {
  if (t === 'mistakes') await loadMistakes()
  if (t === 'profile') {
    await loadProfile()
    await nextTick()
    renderCharts()
  }
  if (t === 'memory') await loadSummaries()
})

onMounted(async () => {
  const q = String(route.query.tab || '')
  if (q === 'profile' || q === 'memory' || q === 'mistakes') tab.value = q
  await loadMistakes()
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  disposeCharts()
})
</script>

<template>
  <StudentLayout active-nav="records">
    <p class="page-kicker">数字电子技术 · 错题与学情</p>
    <h1 class="page-title">把错过的点变成下一次会做的依据</h1>
    <p class="page-desc">
      错题可增删导入导出；学情支持 Word 导出与多维图表。对话摘要仅本人可见。
    </p>

    <div class="tabs">
      <button
        class="tab"
        :class="{ active: tab === 'mistakes' }"
        type="button"
        @click="tab = 'mistakes'"
      >
        错题本
      </button>
      <button
        class="tab"
        :class="{ active: tab === 'profile' }"
        type="button"
        @click="tab = 'profile'"
      >
        学习档案
      </button>
      <button
        class="tab"
        :class="{ active: tab === 'memory' }"
        type="button"
        @click="tab = 'memory'"
      >
        我的摘要
      </button>
    </div>

    <section v-if="tab === 'mistakes'" class="mt-6">
      <div class="toolbar">
        <div>
          <h2 class="font-bold">错题本</h2>
          <p class="mt-1 text-sm text-slate-500">加练错题自动写入；也可手动新增或批量导入。</p>
        </div>
        <div class="toolbar-actions">
          <button class="btn ghost" type="button" @click="showCreate = true">新增</button>
          <button class="btn ghost" type="button" @click="showImport = true">导入</button>
          <button class="btn dark" type="button" :disabled="exporting" @click="exportWord">
            导出 Word
          </button>
        </div>
      </div>

      <div class="filters">
        <input
          v-model="keyword"
          class="search"
          type="search"
          placeholder="搜索题干 / 复盘…"
        />
        <select v-model="filterSource" class="select">
          <option value="all">全部来源</option>
          <option value="practice">练习错题</option>
          <option value="solve">答疑加入</option>
          <option value="manual">手动新增</option>
          <option value="import">导入</option>
        </select>
      </div>

      <div v-if="loading" class="mt-8 text-sm text-slate-400">加载中…</div>
      <div
        v-else-if="!filteredMistakes.length"
        class="mt-8 rounded-2xl border bg-white p-8 text-center text-slate-500"
      >
        {{ mistakes.length ? '没有符合筛选的错题' : '暂无错题。可新增，或在答疑页点「加入错题本」。' }}
      </div>
      <div v-else class="mistake-grid">
        <article v-for="item in filteredMistakes" :key="item.id" class="card">
          <span class="pill" :class="tagClass(item)">{{ tagLabel(item) }}</span>
          <h3 class="mt-3 font-bold">
            <FormulaText compact :content="item.question_snapshot" />
          </h3>
          <div v-if="item.answer_snapshot" class="mt-2 line-clamp-4 text-sm text-slate-500">
            <FormulaText compact :content="item.answer_snapshot" />
          </div>
          <textarea
            v-model="noteDrafts[item.id]"
            class="note"
            placeholder="写下复盘笔记…"
            rows="3"
          />
          <div class="card-actions">
            <button class="text-cyan" type="button" @click="saveNote(item.id)">保存复盘</button>
            <button class="text-muted" type="button" @click="remove(item.id)">删除</button>
          </div>
        </article>
      </div>
    </section>

    <section v-else-if="tab === 'profile'" class="mt-6">
      <div class="toolbar">
        <div>
          <h2 class="font-bold">学习档案</h2>
          <p class="mt-1 text-sm text-slate-500">
            每日 03:00 自动重建；也可手动更新。上次：
            {{
              profile?.last_rebuild_at
                ? profile.last_rebuild_at.replace('T', ' ').slice(0, 19)
                : '尚未重建'
            }}
          </p>
        </div>
        <div class="toolbar-actions">
          <button
            class="btn ghost"
            type="button"
            :disabled="exporting || loading"
            @click="exportLearning"
          >
            导出学情 Word
          </button>
          <button
            class="btn cyan"
            type="button"
            :disabled="rebuilding || loading"
            @click="onRebuildProfile"
          >
            {{ rebuilding ? '更新中…' : '更新学情' }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="text-sm text-slate-400">加载中…</div>
      <template v-else-if="profile">
        <div class="stat-grid">
          <div class="stat">
            <p>累计刷题</p>
            <b>{{ totalSolves() }}</b>
          </div>
          <div class="stat">
            <p>知识模块</p>
            <b>{{ Object.keys(profile.mastery || {}).length }}</b>
          </div>
          <div class="stat">
            <p>平均掌握度</p>
            <b>{{ avgMastery() }}</b>
          </div>
          <div class="stat">
            <p>薄弱点</p>
            <b class="amber">{{ weakCount() }}</b>
          </div>
        </div>
        <p class="last-session">{{ lastSessionLabel() }}</p>

        <div class="chart-grid">
          <div class="chart-card">
            <h2>近 7 天专注时长</h2>
            <div ref="studyChartRef" class="chart" />
          </div>
          <div class="chart-card">
            <h2>知识模块掌握度</h2>
            <div ref="masterChartRef" class="chart" />
          </div>
          <div class="chart-card">
            <h2>近 7 天加练题量</h2>
            <div ref="solvesChartRef" class="chart" />
          </div>
          <div class="chart-card">
            <h2>最近正确率</h2>
            <div ref="accuracyChartRef" class="chart" />
          </div>
          <div class="chart-card">
            <h2>错题标签分布</h2>
            <div ref="mistakeTagChartRef" class="chart" />
          </div>
          <div class="chart-card">
            <h2>答疑话题分布</h2>
            <div ref="topicChartRef" class="chart" />
          </div>
        </div>

        <div v-if="profile.weak_points?.length" class="panel">
          <h2 class="font-bold">薄弱知识点</h2>
          <div class="chips">
            <span v-for="wp in profile.weak_points" :key="String(wp)" class="chip">
              {{ typeof wp === 'string' ? wp : (wp as any)?.concept || wp }}
            </span>
          </div>
        </div>

        <div v-if="profile.recommendations?.length" class="panel">
          <h2 class="font-bold">学习建议</h2>
          <ul class="recs">
            <li v-for="(rec, i) in profile.recommendations" :key="i">· {{ rec.label }}</li>
          </ul>
        </div>
      </template>
    </section>

    <section v-else-if="tab === 'memory'" class="mt-6">
      <h2 class="font-bold">仅本人可见的对话摘要</h2>
      <p class="mt-1 text-sm text-slate-500">
        摘要用于沉淀学情；管理端只能看到画像，看不到这里的内容。
      </p>
      <div v-if="loading" class="mt-6 text-sm text-slate-400">加载中…</div>
      <div
        v-else-if="!summaries.length"
        class="mt-6 rounded-2xl border bg-white p-8 text-center text-slate-500"
      >
        尚无摘要。在答疑页连续对话满 10 轮后会自动生成。
      </div>
      <div v-else class="mt-5 space-y-3">
        <article v-for="s in summaries" :key="s.id" class="card">
          <p class="text-xs text-slate-400">
            #{{ s.id }} · {{ s.agent }} · {{ s.created_at?.replace('T', ' ').slice(0, 19) || '—' }}
          </p>
          <p class="mt-3 text-sm leading-relaxed text-slate-800">{{ s.summary_text }}</p>
          <div v-if="s.topics?.length" class="chips mt-3">
            <span v-for="t in s.topics" :key="t" class="chip cyan">{{ t }}</span>
          </div>
        </article>
      </div>
    </section>

    <!-- 新增弹层 -->
    <div v-if="showCreate" class="modal-mask" @click.self="showCreate = false">
      <div class="modal">
        <h3>新增错题</h3>
        <textarea v-model="createForm.question" rows="4" placeholder="题干（必填）" />
        <textarea v-model="createForm.answer" rows="2" placeholder="参考答案（可选）" />
        <textarea v-model="createForm.reason" rows="2" placeholder="错因 / 复盘（可选）" />
        <input v-model="createForm.tags" type="text" placeholder="知识点标签，逗号分隔" />
        <div class="modal-actions">
          <button class="btn ghost" type="button" @click="showCreate = false">取消</button>
          <button class="btn cyan" type="button" :disabled="creating" @click="submitCreate">
            {{ creating ? '保存中…' : '加入错题本' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 导入弹层 -->
    <div v-if="showImport" class="modal-mask" @click.self="showImport = false">
      <div class="modal">
        <h3>批量导入</h3>
        <p class="tip">
          支持 JSON 数组
          <code>[{"question":"...","answer":"..."}]</code>
          ，或每行一题：题干 | 答案
        </p>
        <textarea v-model="importText" rows="10" placeholder="粘贴内容…" />
        <div class="modal-actions">
          <button class="btn ghost" type="button" @click="showImport = false">取消</button>
          <button class="btn cyan" type="button" :disabled="importing" @click="submitImport">
            {{ importing ? '导入中…' : '开始导入' }}
          </button>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<style scoped>
.page-kicker {
  margin: 0;
  color: #0e7490;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}
.page-title {
  margin: 8px 0 0;
  font-size: clamp(22px, 4vw, 28px);
  letter-spacing: -0.02em;
}
.page-desc {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  max-width: 40rem;
}
.tabs {
  margin-top: 24px;
  display: flex;
  gap: 20px;
  border-bottom: 1px solid #e2e8f0;
  overflow-x: auto;
}
.tab {
  flex-shrink: 0;
  padding: 0 0 12px;
  border: 0;
  background: transparent;
  font-size: 14px;
  font-weight: 700;
  color: #64748b;
}
.tab.active {
  color: #0e7490;
  border-bottom: 2px solid #0891b2;
}
.toolbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}
.toolbar-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.btn {
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 700;
  border: 1px solid transparent;
}
.btn.ghost {
  background: #fff;
  border-color: #cbd5e1;
  color: #334155;
}
.btn.dark {
  background: #0f172a;
  color: #fff;
}
.btn.cyan {
  background: #0e7490;
  color: #fff;
}
.btn:disabled {
  opacity: 0.6;
}
.filters {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.search,
.select,
.modal input,
.modal textarea,
.note {
  box-sizing: border-box;
  width: 100%;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 10px;
  font: inherit;
}
.search {
  flex: 1;
  min-width: 160px;
}
.select {
  width: auto;
  min-width: 120px;
}
.mistake-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.card {
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  background: #fff;
  padding: 16px;
}
.pill {
  display: inline-block;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 700;
}
.note {
  margin-top: 12px;
  font-size: 12px;
}
.card-actions {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}
.text-cyan {
  border: 0;
  background: transparent;
  color: #0e7490;
  font-weight: 700;
  font-size: 13px;
}
.text-muted {
  border: 0;
  background: transparent;
  color: #94a3b8;
  font-size: 13px;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}
.stat {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #fff;
  padding: 14px;
}
.stat p {
  margin: 0;
  font-size: 12px;
  color: #64748b;
}
.stat b {
  display: block;
  margin-top: 6px;
  font-size: 22px;
}
.stat b.amber {
  color: #d97706;
}
.last-session {
  margin: 12px 0 0;
  font-size: 13px;
  color: #64748b;
}
.chart-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.chart-card {
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  background: #fff;
  padding: 14px;
}
.chart-card h2 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
}
.chart {
  height: 240px;
}
.panel {
  margin-top: 14px;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  background: #fff;
  padding: 16px;
}
.chips {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.chip {
  border-radius: 999px;
  background: #fffbeb;
  color: #b45309;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 600;
}
.chip.cyan {
  background: #ecfeff;
  color: #0e7490;
}
.recs {
  margin: 10px 0 0;
  padding: 0;
  list-style: none;
  font-size: 14px;
  color: #334155;
  line-height: 1.7;
}
.modal-mask {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: rgb(15 23 42 / 0.45);
  display: grid;
  place-items: center;
  padding: 16px;
}
.modal {
  width: min(520px, 100%);
  background: #fff;
  border-radius: 16px;
  padding: 18px;
  display: grid;
  gap: 10px;
}
.modal h3 {
  margin: 0;
  font-size: 16px;
}
.tip {
  margin: 0;
  font-size: 12px;
  color: #64748b;
  line-height: 1.5;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 4px;
}

@media (max-width: 900px) {
  .mistake-grid,
  .chart-grid,
  .stat-grid {
    grid-template-columns: 1fr;
  }
  .chart {
    height: 220px;
  }
}

@media (min-width: 901px) and (max-width: 1200px) {
  .mistake-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>

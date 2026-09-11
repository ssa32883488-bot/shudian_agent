<script setup lang="ts">
/**
 * 学生端知识图谱：Neo4j/JSON 力导向可视化 + 图谱问询 → 跳转答疑
 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

import StudentLayout from '@/layouts/StudentLayout.vue'
import {
  askKg,
  getKgConcept,
  getKgGraph,
  getKgStatus,
  type KgConceptDetail,
  type KgGraphPayload,
  type KgRelatedProblem,
  type KgStatus,
} from '@/api/kg'

const router = useRouter()

const loading = ref(false)
const asking = ref(false)
const status = ref<KgStatus | null>(null)
const graph = ref<KgGraphPayload | null>(null)
const detail = ref<KgConceptDetail | null>(null)
const chapter = ref('')
const keyword = ref('')
const askText = ref('')
const askResult = ref<{
  keywords?: string[]
  learning_chain?: string[]
  related_problems?: KgRelatedProblem[]
  ask_seed?: string
} | null>(null)

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

function problemKindLabel(p: KgRelatedProblem | { problem_id?: string; kind?: string | null; kind_label?: string }) {
  if (p.kind_label) return p.kind_label
  const k = String(p.kind || '').toLowerCase()
  if (k === 'example') return '例题'
  if (k === 'review') return '复习思考题'
  if (k === 'chapter_exercise') return '章末习题'
  const id = String(p.problem_id || '')
  if (id.startsWith('例')) return '例题'
  if (id.startsWith('R')) return '复习思考题'
  if (id.startsWith('题')) return '章末习题'
  return '习题'
}

function kindClass(p: KgRelatedProblem) {
  const label = problemKindLabel(p)
  if (label === '例题') return 'kind-ex'
  if (label === '复习思考题') return 'kind-rv'
  if (label === '章末习题') return 'kind-ch'
  return 'kind-other'
}

const engineLabel = computed(() => {
  const e = status.value?.engine || graph.value?.engine || '—'
  if (e === 'neo4j') return 'Neo4j'
  if (e === 'json') return 'JSON'
  if (e === 'builtin') return '内置兜底'
  return e
})

async function loadStatus() {
  try {
    status.value = await getKgStatus()
  } catch {
    status.value = null
  }
}

async function loadGraph(opts?: { focus?: string }) {
  loading.value = true
  try {
    graph.value = await getKgGraph({
      chapter: chapter.value || undefined,
      q: keyword.value || undefined,
      focus: opts?.focus,
      limit: opts?.focus ? 40 : 90,
      depth: opts?.focus ? 1 : 0,
    })
    await nextTick()
    renderChart()
  } catch (e: unknown) {
    const msg =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      '加载图谱失败'
    ElMessage.error(typeof msg === 'string' ? msg : '加载图谱失败')
  } finally {
    loading.value = false
  }
}

function renderChart() {
  if (!chartRef.value || !graph.value) return
  if (!chart) chart = echarts.init(chartRef.value)

  const cats = graph.value.categories || []
  const catIndex = new Map(cats.map((c, i) => [c.name, i]))
  const nodes = (graph.value.nodes || []).map((n) => ({
    id: n.id,
    name: n.name,
    category: catIndex.get(n.category) ?? 0,
    symbolSize: n.symbolSize || 26,
    chapter: n.chapter,
  }))
  const links = (graph.value.links || []).map((l) => ({
    source: l.source,
    target: l.target,
    lineStyle: { curveness: 0.12 },
  }))

  chart.setOption(
    {
      tooltip: {
        formatter: (p: any) => {
          if (p.dataType === 'edge') {
            return `${p.data.source} → ${p.data.target}`
          }
          return `${p.data.name}<br/>章节：${p.data.chapter || '—'}`
        },
      },
      legend: cats.length
        ? {
            type: 'scroll',
            orient: 'horizontal',
            bottom: 0,
            data: cats.map((c) => c.name),
            textStyle: { fontSize: 11 },
          }
        : undefined,
      series: [
        {
          type: 'graph',
          layout: 'force',
          roam: true,
          draggable: true,
          categories: cats,
          data: nodes,
          links,
          label: {
            show: true,
            position: 'right',
            fontSize: 11,
            color: '#334155',
          },
          force: {
            repulsion: 180,
            edgeLength: [48, 120],
            gravity: 0.08,
          },
          lineStyle: {
            color: '#94a3b8',
            width: 1.2,
            opacity: 0.75,
          },
          emphasis: {
            focus: 'adjacency',
            lineStyle: { width: 2.5, color: '#0891b2' },
          },
        },
      ],
    },
    true,
  )

  chart.off('click')
  chart.on('click', (params: any) => {
    if (params.dataType !== 'node') return
    const name = String(params.data?.name || params.name || '')
    if (!name) return
    void selectConcept(name)
  })
}

async function selectConcept(name: string) {
  loading.value = true
  try {
    detail.value = await getKgConcept(name)
    if (detail.value.subgraph) {
      graph.value = detail.value.subgraph
      await nextTick()
      renderChart()
    }
  } catch {
    ElMessage.warning('无法加载该知识点详情')
  } finally {
    loading.value = false
  }
}

async function onAsk() {
  const text = askText.value.trim()
  if (!text) {
    ElMessage.warning('请输入要查询的知识点或问题')
    return
  }
  asking.value = true
  try {
    const res = await askKg(text)
    if (!res.ok) {
      ElMessage.warning(res.detail || '查询失败')
      return
    }
    askResult.value = {
      keywords: res.network?.keywords,
      learning_chain: res.network?.learning_chain,
      related_problems: res.network?.related_problems,
      ask_seed: res.ask_seed,
    }
    if (res.subgraph) {
      graph.value = res.subgraph
      await nextTick()
      renderChart()
    }
    const kw = res.network?.keywords?.[0]
    if (kw) {
      try {
        detail.value = await getKgConcept(kw)
      } catch {
        /* ignore */
      }
    }
  } catch {
    ElMessage.error('图谱问询失败')
  } finally {
    asking.value = false
  }
}

function goChat(seed?: string) {
  const q = (seed || detail.value?.ask_seed || askResult.value?.ask_seed || '').trim()
  if (!q) {
    router.push('/chat')
    return
  }
  router.push({ path: '/chat', query: { q } })
}

function resetView() {
  detail.value = null
  askResult.value = null
  keyword.value = ''
  loadGraph()
}

function onResize() {
  chart?.resize()
}

watch([chapter], () => {
  detail.value = null
  loadGraph()
})

onMounted(async () => {
  await loadStatus()
  await loadGraph()
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  chart?.dispose()
  chart = null
})
</script>

<template>
  <StudentLayout active-nav="kg">
    <div class="kg-page">
      <header class="head">
        <div>
          <p class="kicker">数字电子技术 · 知识图谱</p>
          <h1>可视化知识网络</h1>
          <p class="sub">
            引擎：{{ engineLabel }}
            <template v-if="status">
              · 概念 {{ status.concept_count }} · 前置边 {{ status.edge_count }}
              <template v-if="status.neo4j_enabled">
                · Neo4j {{ status.neo4j_ready ? '已连接' : '未就绪(回落 JSON)' }}
              </template>
            </template>
          </p>
        </div>
        <button class="btn ghost" type="button" @click="goChat()">去答疑</button>
      </header>

      <p v-if="status?.hint" class="hint-bar">{{ status.hint }}</p>

      <div class="toolbar">
        <select v-model="chapter" class="select">
          <option value="">全部章节</option>
          <option
            v-for="ch in status?.chapters || []"
            :key="ch.id || ch.name"
            :value="ch.id || ch.name"
          >
            {{ ch.name || ch.id }}
          </option>
        </select>
        <input
          v-model="keyword"
          class="input"
          type="search"
          placeholder="筛选概念名…"
          @keyup.enter="loadGraph()"
        />
        <button class="btn ghost" type="button" :disabled="loading" @click="loadGraph()">
          刷新
        </button>
        <button class="btn ghost" type="button" @click="resetView">重置视图</button>
      </div>

      <div class="ask-row">
        <input
          v-model="askText"
          class="input grow"
          type="text"
          placeholder="图谱问询：例如「卡诺图的前置知识是什么」"
          @keyup.enter="onAsk"
        />
        <button class="btn primary" type="button" :disabled="asking" @click="onAsk">
          {{ asking ? '查询中…' : '问图谱' }}
        </button>
        <button
          class="btn cyan"
          type="button"
          :disabled="!(askResult?.ask_seed || detail?.ask_seed)"
          @click="goChat()"
        >
          带到答疑
        </button>
      </div>

      <div class="main">
        <section class="canvas-card">
          <div v-if="loading" class="loading">加载中…</div>
          <div ref="chartRef" class="chart" />
          <p class="canvas-foot">
            节点 {{ graph?.stats?.nodes ?? 0 }} · 边 {{ graph?.stats?.links ?? 0 }} ·
            点击节点查看详情；箭头表示前置依赖（PRE_REQUISITE_OF）
          </p>
        </section>

        <aside class="side">
          <div v-if="askResult" class="panel">
            <h2>问询结果</h2>
            <p v-if="askResult.keywords?.length" class="meta">
              考点：{{ askResult.keywords.join('、') }}
            </p>
            <p v-if="askResult.learning_chain?.length" class="chain">
              逻辑链：{{ askResult.learning_chain.join(' → ') }}
            </p>
            <ul v-if="askResult.related_problems?.length" class="plist">
              <li v-for="p in askResult.related_problems.slice(0, 6)" :key="p.problem_id">
                <span class="kind-tag" :class="kindClass(p)">{{ problemKindLabel(p) }}</span>
                <span class="pid">{{ p.problem_id }}</span>
              </li>
            </ul>
          </div>

          <div v-if="detail" class="panel">
            <h2>{{ detail.name }}</h2>
            <p v-if="detail.suggestion" class="meta">{{ detail.suggestion }}</p>
            <p v-if="detail.path?.length" class="chain">
              学习路径：{{ detail.path.join(' → ') }}
            </p>
            <p v-else-if="detail.learning_chain?.length" class="chain">
              逻辑链：{{ detail.learning_chain.join(' → ') }}
            </p>
            <h3 v-if="detail.related_problems?.length">相关习题</h3>
            <ul class="plist">
              <li v-for="p in (detail.related_problems || []).slice(0, 8)" :key="p.problem_id">
                <span class="kind-tag" :class="kindClass(p)">{{ problemKindLabel(p) }}</span>
                <span class="pid">{{ p.problem_id }}</span>
              </li>
            </ul>
            <button class="btn primary full" type="button" @click="goChat(detail.ask_seed)">
              让 AI 按图谱讲解此点
            </button>
          </div>

          <div v-else class="panel empty">
            <h2>知识点详情</h2>
            <p class="meta">点击图中节点，或上方「问图谱」后查看逻辑链与相关题。</p>
          </div>
        </aside>
      </div>
    </div>
  </StudentLayout>
</template>

<style scoped>
.kg-page {
  max-width: 1200px;
}
.kicker {
  margin: 0;
  color: #0e7490;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}
h1 {
  margin: 6px 0 0;
  font-size: clamp(22px, 3vw, 28px);
  letter-spacing: -0.02em;
}
.sub {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 13px;
}
.head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}
.hint-bar {
  margin: 12px 0 0;
  padding: 10px 12px;
  border-radius: 10px;
  background: #ecfeff;
  color: #0e7490;
  font-size: 13px;
  line-height: 1.5;
}
.toolbar,
.ask-row {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.select,
.input {
  box-sizing: border-box;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 10px;
  font: inherit;
  background: #fff;
}
.input {
  min-width: 160px;
}
.input.grow {
  flex: 1;
  min-width: 200px;
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
.btn.primary {
  background: #0f172a;
  color: #fff;
}
.btn.cyan {
  background: #0e7490;
  color: #fff;
}
.btn.full {
  width: 100%;
  margin-top: 12px;
}
.btn:disabled {
  opacity: 0.55;
}
.main {
  margin-top: 16px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 14px;
  align-items: start;
}
.canvas-card,
.panel {
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  background: #fff;
  padding: 12px;
}
.chart {
  height: min(62vh, 560px);
  width: 100%;
}
.loading {
  position: absolute;
  z-index: 2;
  margin: 12px;
  font-size: 13px;
  color: #64748b;
}
.canvas-card {
  position: relative;
}
.canvas-foot {
  margin: 8px 0 0;
  font-size: 12px;
  color: #94a3b8;
}
.side {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.panel h2 {
  margin: 0;
  font-size: 15px;
}
.panel h3 {
  margin: 12px 0 6px;
  font-size: 13px;
}
.meta,
.chain {
  margin: 8px 0 0;
  font-size: 13px;
  color: #475569;
  line-height: 1.55;
}
.plist {
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
  font-size: 13px;
  color: #334155;
  line-height: 1.6;
}
.plist li {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  border-bottom: 1px solid #f1f5f9;
}
.plist li:last-child {
  border-bottom: 0;
}
.kind-tag {
  flex-shrink: 0;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 700;
}
.kind-ex {
  background: #ecfeff;
  color: #0e7490;
}
.kind-rv {
  background: #eef2ff;
  color: #4338ca;
}
.kind-ch {
  background: #fff7ed;
  color: #c2410c;
}
.kind-other {
  background: #f1f5f9;
  color: #64748b;
}
.pid {
  font-weight: 600;
  color: #0f172a;
}
.panel.empty .meta {
  margin-top: 10px;
}

@media (max-width: 900px) {
  .main {
    grid-template-columns: 1fr;
  }
  .chart {
    height: 420px;
  }
  .head {
    flex-direction: column;
  }
}
</style>

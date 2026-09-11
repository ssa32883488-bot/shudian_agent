<script setup lang="ts">
/**
 * 学习总览：加练瞄准镜（空 / 足迹 / 已验证 三态）
 */
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { RouteLocationRaw } from 'vue-router'
import { ElMessage } from 'element-plus'

import StudentLayout from '@/layouts/StudentLayout.vue'
import { useUserStore } from '@/stores/user'
import { listMistakes, type MistakeItem } from '@/api/mistakes'
import { getStudentProfile, type StudentProfileData } from '@/api/profile'
import { buildOverview, type AimItem } from '@/utils/learningOverview'

const user = useUserStore()
const router = useRouter()

const loading = ref(true)
const mistakes = ref<MistakeItem[]>([])
const profile = ref<StudentProfileData | null>(null)
const classCodeInput = ref('')
const bindingClass = ref(false)

const needBindClass = computed(
  () =>
    Boolean(user.hasToken || user.isLoggedIn) &&
    user.isStudent &&
    !user.profile?.class_code,
)

async function submitBindClass() {
  const code = classCodeInput.value.trim()
  if (!code) {
    ElMessage.warning('请输入班级码')
    return
  }
  bindingClass.value = true
  try {
    await user.bindClass(code)
    ElMessage.success('已加入班级')
    classCodeInput.value = ''
  } catch (e: unknown) {
    const msg =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      '加入班级失败'
    ElMessage.error(typeof msg === 'string' ? msg : '加入班级失败')
  } finally {
    bindingClass.value = false
  }
}

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return '上午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

const name = computed(() => user.studentName || '同学')
const overview = computed(() => buildOverview(profile.value, mistakes.value))

const head = computed(() => {
  const s = overview.value.state
  if (s === 'empty') {
    return {
      title: '先用几道题，摸清该练什么',
      sub: '数电 · 问过的点和练过的题，会变成加练目标',
    }
  }
  if (s === 'footprint') {
    return {
      title: '你最近在碰这些点',
      sub: '还没做题验证，加练后才能判断是不是薄弱',
    }
  }
  return {
    title: '先补最容易再错的点',
    sub: '依据近几次加练与错题，不是聊天猜的',
  }
})

const hero = computed(() => {
  const o = overview.value
  if (o.state === 'empty') {
    return {
      kicker: '下一步',
      title: '先做一次摸底',
      body: '题库抽 5 道，覆盖不同知识点。做完后，这里才会出现「该练哪」。',
      primary: '开始摸底 · 5 题',
      primaryTo: { path: '/practice', query: { mode: 'probe', count: '5' } },
      secondary: '有卡住的题，先去问',
      secondaryTo: '/chat',
    }
  }
  if (o.state === 'footprint') {
    const topic = o.weak1
    const asked =
      o.askCount > 1
        ? `你问过 ${o.askCount} 次，但还没有练习记录。先练 3 道，确认是不是不会。`
        : topic
          ? `你问过「${topic}」，但还没有练习记录。先练 3 道，确认是不是不会。`
          : '先练 3 道，确认是不是不会。'
    return {
      kicker: '下一步',
      title: topic ? `确认一下：${topic}` : '确认一下你问过的点',
      body: o.aim.length > 1 && topic ? `优先验证最近问得最多的「${topic}」。` : asked,
      primary: topic ? `针对 ${topic} 练 3 题` : '练 3 题',
      primaryTo: {
        path: '/practice',
        query: topic
          ? { mode: 'focus', tags: topic, count: '3' }
          : { mode: 'probe', count: '3' },
      },
      secondary: '换成摸底',
      secondaryTo: { path: '/practice', query: { mode: 'probe', count: '5' } },
    }
  }
  const w1 = o.weak1
  const w2 = o.weak2
  if (!w1 && o.mistakeCount) {
    return {
      kicker: '下一步',
      title: '先复盘错过的题',
      body: '错题已进本，先按错题标签回炉。做完后会更新薄弱清单。',
      primary: '错题回炉',
      primaryTo: { path: '/practice', query: { mode: 'review', count: '5' } },
      secondary: '换成摸底',
      secondaryTo: { path: '/practice', query: { mode: 'probe', count: '5' } },
    }
  }
  let body = w1
    ? '近几次练习里，这个点错得最多。本次按该标签从题库抽题。'
    : '按已验证薄弱点从题库抽题。'
  if (w2) body = `近几次练习里，这个点错得最多。其次是 ${w2}。`
  return {
    kicker: '下一步',
    title: w1 ? `针对加练：${w1}` : '针对加练',
    body,
    primary: w1 ? `练 5 题 · ${w1}` : '练 5 题',
    primaryTo: {
      path: '/practice',
      query: w1
        ? { mode: 'focus', tags: w1, count: '5' }
        : { mode: 'probe', count: '5' },
    },
    secondary: o.mistakeCount ? '错题回炉' : '',
    secondaryTo: { path: '/practice', query: { mode: 'review', count: '5' } },
  }
})

const aimGroups = computed(() => {
  const groups: Array<{ key: AimItem['kind']; label: string; items: AimItem[] }> = [
    { key: 'verified', label: '已验证薄弱', items: [] },
    { key: 'suspected', label: '疑似', items: [] },
    { key: 'footprint', label: '最近足迹', items: [] },
  ]
  for (const item of overview.value.aim) {
    const g = groups.find((x) => x.key === item.kind)
    if (g) g.items.push(item)
  }
  return groups.filter((g) => g.items.length)
})

function goPractice(tag: string, kind: AimItem['kind']) {
  const count = kind === 'suspected' ? '3' : '5'
  router.push({
    path: '/practice',
    query: { mode: 'focus', tags: tag, count },
  })
}

function go(to: RouteLocationRaw) {
  router.push(to)
}

onMounted(async () => {
  try {
    const [ms, pf] = await Promise.all([
      listMistakes().catch(() => [] as MistakeItem[]),
      getStudentProfile().catch(() => null),
    ])
    mistakes.value = Array.isArray(ms) ? ms : []
    profile.value = pf
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <StudentLayout active-nav="home">
    <header class="head">
      <div>
        <p class="greet">{{ greeting }}，{{ name }}</p>
        <h1>{{ head.title }}</h1>
        <p class="sub">{{ head.sub }}</p>
      </div>
      <button class="btn ghost" type="button" @click="router.push('/chat')">去答疑</button>
    </header>

    <div v-if="needBindClass" class="bind-banner">
      <p class="bind-text">还没有加入班级。输入班级码即可加入，便于老师查看学情。</p>
      <div class="bind-row">
        <input
          v-model="classCodeInput"
          class="bind-input"
          type="text"
          placeholder="班级码"
          maxlength="32"
          @keyup.enter="submitBindClass"
        />
        <button
          class="btn bind"
          type="button"
          :disabled="bindingClass"
          @click="submitBindClass"
        >
          {{ bindingClass ? '加入中…' : '加入班级' }}
        </button>
      </div>
    </div>

    <section class="hero">
      <p class="kicker">{{ hero.kicker }}</p>
      <p v-if="overview.lastNote" class="echo">{{ overview.lastNote }}</p>
      <h2>{{ hero.title }}</h2>
      <p class="hero-body">{{ hero.body }}</p>
      <div class="hero-actions">
        <button class="btn primary" type="button" @click="go(hero.primaryTo)">
          {{ hero.primary }}
        </button>
        <button
          v-if="hero.secondary"
          class="btn link"
          type="button"
          @click="go(hero.secondaryTo)"
        >
          {{ hero.secondary }}
        </button>
      </div>
    </section>

    <section class="block">
      <div class="block-head">
        <div>
          <h2>加练瞄准</h2>
          <p>对话只记足迹；做题对错才算薄弱。</p>
        </div>
        <button
          v-if="overview.hasMoreAim"
          class="text-link"
          type="button"
          @click="router.push('/records')"
        >
          在档案中查看全部
        </button>
      </div>
      <p v-if="loading" class="muted">加载中…</p>
      <p v-else-if="!aimGroups.length" class="empty-line">
        还没有可瞄准的知识点。去答疑提问，或先做摸底。
      </p>
      <ul v-else class="aim-list">
        <li v-for="g in aimGroups" :key="g.key" class="aim-group">
          <p class="aim-label">{{ g.label }}</p>
          <button
            v-for="item in g.items"
            :key="item.kind + item.tag"
            class="aim-row"
            type="button"
            @click="goPractice(item.tag, item.kind)"
          >
            <span>
              <b>{{ item.tag }}</b>
              <i>{{ item.hint }}</i>
            </span>
            <em>{{ item.action }}</em>
          </button>
        </li>
      </ul>
    </section>

    <section class="block">
      <div class="block-head">
        <div>
          <h2>待复盘</h2>
          <p>加练做错的题会进这里，可导出打印。</p>
        </div>
      </div>
      <p v-if="!overview.pending.length" class="empty-line">
        还没有错题。加练做错后会出现在这里。
      </p>
      <ul v-else class="review-list">
        <li v-for="item in overview.pending" :key="item.id">
          <div>
            <b>{{ item.stem }}</b>
            <i v-if="item.tag">{{ item.tag }}</i>
          </div>
          <button class="text-link" type="button" @click="router.push('/records')">
            看解析
          </button>
        </li>
      </ul>
      <button
        v-if="overview.mistakeCount"
        class="text-link open-book"
        type="button"
        @click="router.push('/records')"
      >
        打开错题本 · {{ overview.mistakeCount }} 道
      </button>
    </section>

    <section class="stats">
      <button class="stat" type="button" @click="router.push('/records')">
        <span>本周加练</span>
        <b>{{ overview.weeklyLabel }}</b>
      </button>
      <button class="stat" type="button" @click="router.push('/records')">
        <span>最近正确率</span>
        <b>{{ overview.accuracyLabel }}</b>
      </button>
      <button class="stat" type="button" @click="router.push('/records')">
        <span>错题</span>
        <b>{{ overview.mistakeCount }}</b>
      </button>
    </section>
    <p class="stats-foot">完整记录在「错题与学情」</p>
  </StudentLayout>
</template>

<style scoped>
.head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.greet {
  margin: 0;
  color: #0e7490;
  font-size: 14px;
  font-weight: 600;
}

h1 {
  margin: 6px 0 0;
  font-size: 28px;
  letter-spacing: -0.03em;
  color: #0f172a;
}

.sub {
  margin: 8px 0 0;
  color: #64748b;
  font-size: 14px;
}

.bind-banner {
  margin-top: 20px;
  padding: 14px 16px;
  border: 1px solid #99f6e4;
  border-radius: 8px;
  background: #f0fdfa;
}

.bind-text {
  margin: 0;
  font-size: 13px;
  color: #0f766e;
}

.bind-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.bind-input {
  flex: 1;
  min-width: 140px;
  padding: 8px 12px;
  border: 1px solid #99f6e4;
  border-radius: 8px;
  background: #fff;
  font: inherit;
  font-size: 14px;
  color: #0f172a;
}

.bind-input:focus {
  outline: 2px solid #0f766e33;
  border-color: #0f766e;
}

.btn.bind {
  padding: 8px 16px;
  border-radius: 8px;
  background: #0f766e;
  color: #fff;
  font-size: 13px;
}

.btn.bind:hover:not(:disabled) {
  background: #0d9488;
}

.btn.bind:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.hero {
  margin-top: 28px;
  padding: 28px 32px;
  border-radius: 8px;
  background: #0f172a;
  color: #f8fafc;
}

.kicker {
  margin: 0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #67e8f9;
}

.echo {
  margin: 10px 0 0;
  font-size: 13px;
  color: #a5f3fc;
}

.hero h2 {
  margin: 12px 0 0;
  font-size: 22px;
}

.hero-body {
  margin: 10px 0 0;
  max-width: 40rem;
  font-size: 14px;
  line-height: 1.7;
  color: #cbd5e1;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  margin-top: 22px;
}

.btn {
  border: 0;
  cursor: pointer;
  font: inherit;
  font-weight: 650;
}

.btn.primary {
  padding: 10px 18px;
  border-radius: 8px;
  background: #fff;
  color: #0f172a;
}

.btn.primary:hover {
  background: #ecfeff;
}

.btn.ghost {
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #334155;
  font-size: 13px;
}

.btn.ghost:hover {
  background: #f8fafc;
}

.btn.link,
.text-link {
  padding: 0;
  border: 0;
  background: none;
  color: #0e7490;
  font-size: 13px;
  font-weight: 650;
  cursor: pointer;
}

.hero .btn.link {
  color: #a5f3fc;
}

.block {
  margin-top: 36px;
}

.block-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
}

.block h2 {
  margin: 0;
  font-size: 16px;
  color: #0f172a;
}

.block-head p,
.muted,
.empty-line {
  margin: 6px 0 0;
  color: #64748b;
  font-size: 13px;
}

.aim-list,
.review-list {
  list-style: none;
  margin: 14px 0 0;
  padding: 0;
  border-top: 1px solid #e2e8f0;
}

.aim-group {
  padding-top: 12px;
}

.aim-label {
  margin: 0 0 4px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #94a3b8;
}

.aim-row,
.review-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  width: 100%;
  padding: 12px 0;
  border-bottom: 1px solid #e2e8f0;
  background: none;
  border-left: 0;
  border-right: 0;
  border-top: 0;
  text-align: left;
  cursor: pointer;
}

.aim-row span,
.review-list li div {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.aim-row b,
.review-list li b {
  font-size: 14px;
  color: #0f172a;
}

.aim-row i,
.review-list li i {
  font-style: normal;
  font-size: 12px;
  color: #64748b;
}

.aim-row em {
  font-style: normal;
  font-size: 13px;
  font-weight: 650;
  color: #0e7490;
}

.open-book {
  margin-top: 12px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 36px;
}

.stat {
  padding: 4px 0;
  border: 0;
  background: none;
  text-align: left;
  cursor: pointer;
}

.stat span {
  display: block;
  font-size: 12px;
  color: #64748b;
}

.stat b {
  display: block;
  margin-top: 6px;
  font-size: 22px;
  color: #0f172a;
}

.stats-foot {
  margin: 8px 0 0;
  font-size: 12px;
  color: #94a3b8;
}

@media (max-width: 900px) {
  h1 {
    font-size: 22px;
  }
  .head {
    flex-direction: column;
  }
  .hero {
    padding: 18px 16px;
  }
  .stats {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  .aim-row,
  .review-list li {
    align-items: flex-start;
  }
}
</style>

import type { MistakeItem } from '@/api/mistakes'
import type { StudentProfileData } from '@/api/profile'

export type OverviewState = 'empty' | 'footprint' | 'evidence'

export interface AimItem {
  tag: string
  kind: 'verified' | 'suspected' | 'footprint'
  hint: string
  action: '练' | '验证'
}

export interface LastSession {
  correct?: number
  total?: number
  tags?: string[]
  missed_tags?: string[]
  at?: string
}

const SKIP_TAGS = new Set(['未标注', 'id', 'qid'])

export function tagsFromKnowledge(raw: unknown): string[] {
  if (!raw) return []
  if (Array.isArray(raw)) {
    return raw.flatMap((x) => tagsFromKnowledge(x))
  }
  if (typeof raw === 'string') {
    const s = raw.trim()
    return s && !SKIP_TAGS.has(s) ? [s] : []
  }
  if (typeof raw === 'object') {
    const o = raw as Record<string, unknown>
    const nested = o.tags ?? o.concepts ?? o.name
    if (nested !== undefined) return tagsFromKnowledge(nested)
    return Object.entries(o).flatMap(([k, v]) => {
      if (SKIP_TAGS.has(k)) return []
      if (typeof v === 'string' && v.trim() && !['true', 'false'].includes(v.toLowerCase())) {
        return [v.trim()]
      }
      if (Array.isArray(v)) return tagsFromKnowledge(v)
      return []
    })
  }
  return []
}

function uniqueKeep(items: string[]): string[] {
  const seen = new Set<string>()
  const out: string[] = []
  for (const x of items) {
    const t = x.trim()
    if (!t || SKIP_TAGS.has(t) || seen.has(t)) continue
    seen.add(t)
    out.push(t)
  }
  return out
}

export function stemPreview(text: string, max = 36): string {
  const flat = (text || '').replace(/\s+/g, ' ').trim()
  if (flat.length <= max) return flat || '（无题干）'
  return `${flat.slice(0, max)}…`
}

function firstTag(item: MistakeItem): string {
  return tagsFromKnowledge(item.knowledge_tags)[0] || ''
}

export function buildOverview(profile: StudentProfileData | null, mistakes: MistakeItem[]) {
  const stats = profile?.practice_stats || {}
  const freqRaw = (profile?.topic_freq || {}) as Record<string, unknown>
  const topicFreq: Record<string, number> = {}
  for (const [k, v] of Object.entries(freqRaw)) {
    const n = Number(v)
    if (k.trim()) topicFreq[k.trim()] = Number.isFinite(n) ? n : 0
  }

  const mistakeCounts = new Map<string, number>()
  if (mistakes.length) {
    for (const m of mistakes) {
      for (const t of tagsFromKnowledge(m.knowledge_tags)) {
        mistakeCounts.set(t, (mistakeCounts.get(t) || 0) + 1)
      }
    }
  } else {
    for (const row of stats.mistake_stats?.top_tags || []) {
      if (row?.name && row.name !== '未标注') {
        mistakeCounts.set(row.name, Number(row.count || 0))
      }
    }
  }

  const verified = [...mistakeCounts.entries()]
    .filter(([, n]) => n > 0)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'zh'))
    .map(([tag, count]) => ({ tag, count }))

  const verifiedSet = new Set(verified.map((x) => x.tag))
  const recent = uniqueKeep(profile?.recent_topics || [])
  const suspected = recent
    .filter((t) => !verifiedSet.has(t))
    .map((tag) => ({ tag, count: topicFreq[tag] || 0 }))

  const footprint = suspected.filter((x) => (x.count || 0) <= 1)
  const suspectedMulti = suspected.filter((x) => (x.count || 0) > 1)
  // 没有频次时，全部进足迹，避免空口说「疑似薄弱」
  const suspectedShow = suspectedMulti.length ? suspectedMulti : []
  const footprintShow = suspectedMulti.length ? footprint : suspected

  let state: OverviewState = 'empty'
  if (verified.length || mistakes.length) state = 'evidence'
  else if (recent.length) state = 'footprint'

  const aim: AimItem[] = []
  for (const v of verified.slice(0, 3)) {
    aim.push({
      tag: v.tag,
      kind: 'verified',
      hint: `练习中错过 ${v.count} 次`,
      action: '练',
    })
  }
  for (const s of suspectedShow.slice(0, 3)) {
    aim.push({
      tag: s.tag,
      kind: 'suspected',
      hint: s.count > 1 ? `问过 ${s.count} 次，尚未验证` : '问过，尚未验证',
      action: '验证',
    })
  }
  const aimTags = new Set(aim.map((x) => x.tag))
  for (const f of footprintShow.slice(0, 3)) {
    if (aimTags.has(f.tag)) continue
    aim.push({
      tag: f.tag,
      kind: 'footprint',
      hint: '上次问到',
      action: '练',
    })
    if (aim.filter((x) => x.kind === 'footprint').length >= 3) break
  }

  const last = (stats.last_session || null) as LastSession | null
  let lastNote = ''
  if (last?.at && last.total) {
    const t = Date.parse(last.at)
    if (Number.isFinite(t) && Date.now() - t < 24 * 60 * 60 * 1000) {
      const miss = last.missed_tags?.[0]
      if (miss) lastNote = `上次加练 ${last.correct}/${last.total}。${miss} 仍列入薄弱。`
      else lastNote = `上次加练 ${last.correct}/${last.total}。`
    }
  }

  const weeklySolves = (stats.weekly_solves || []).reduce(
    (a: number, b: unknown) => a + Number(b || 0),
    0,
  )
  const totalSolves = Number(stats.total_solves || 0)
  const weeklyLabel =
    weeklySolves > 0 ? `${weeklySolves} 题` : totalSolves > 0 ? `${totalSolves} 题` : '还没练'

  let accuracyLabel = '—'
  if (stats.accuracy != null) {
    const a = Number(stats.accuracy)
    if (Number.isFinite(a)) accuracyLabel = `${Math.round(a * (a <= 1 ? 100 : 1))}%`
  }

  const pending = mistakes.slice(0, 3).map((m) => ({
    id: m.id,
    stem: stemPreview(m.question_snapshot || ''),
    tag: firstTag(m),
  }))

  const weak1 = verified[0]?.tag || suspected[0]?.tag || ''
  const weak2 = verified[1]?.tag || suspected[1]?.tag || ''
  const askCount = weak1 ? topicFreq[weak1] || 0 : 0

  return {
    state,
    aim,
    pending,
    mistakeCount: mistakes.length,
    weeklyLabel,
    accuracyLabel,
    lastNote,
    weak1,
    weak2,
    askCount,
    hasMoreAim: verified.length + suspected.length > 6,
  }
}

import http from '@/api/http'

export interface KgStatus {
  ok: boolean
  neo4j_enabled: boolean
  neo4j_ready: boolean
  engine: string
  source?: string
  concept_count: number
  edge_count: number
  chapters: Array<{ id?: string; name?: string; num?: number }>
  agent_tool?: string
  hint?: string
}

export interface KgGraphNode {
  id: string
  name: string
  category: string
  symbolSize?: number
  chapter?: string
}

export interface KgGraphLink {
  source: string
  target: string
  relation?: string
  confidence?: string
}

export interface KgGraphPayload {
  ok: boolean
  engine?: string
  source?: string
  focus?: string | null
  categories: Array<{ name: string }>
  nodes: KgGraphNode[]
  links: KgGraphLink[]
  stats: { nodes: number; links: number }
}

export interface KgRelatedProblem {
  problem_id: string
  kind?: string | null
  kind_label?: string
  stem?: string
  chapter_id?: string
}

export interface KgConceptDetail {
  ok: boolean
  name: string
  resolved?: string
  path?: string[]
  suggestion?: string
  learning_chain?: string[]
  related_problems?: KgRelatedProblem[]
  prompt_block?: string
  ask_seed?: string
  subgraph?: KgGraphPayload
}

export interface KgAskResult {
  ok: boolean
  query: string
  network?: {
    keywords?: string[]
    learning_chain?: string[]
    related_problems?: KgRelatedProblem[]
    prompt_block?: string
  }
  subgraph?: KgGraphPayload
  ask_seed?: string
  detail?: string
}

export async function getKgStatus(): Promise<KgStatus> {
  const { data } = await http.get<KgStatus>('/api/student/kg/status')
  return data
}

export async function getKgGraph(params: {
  chapter?: string
  q?: string
  focus?: string
  limit?: number
  depth?: number
}): Promise<KgGraphPayload> {
  const { data } = await http.get<KgGraphPayload>('/api/student/kg/graph', { params })
  return data
}

export async function searchKgConcepts(q: string, limit = 30): Promise<string[]> {
  const { data } = await http.get<{ ok: boolean; items: string[] }>('/api/student/kg/concepts', {
    params: { q, limit },
  })
  return data.items || []
}

export async function getKgConcept(name: string): Promise<KgConceptDetail> {
  const { data } = await http.get<KgConceptDetail>('/api/student/kg/concept', {
    params: { name },
  })
  return data
}

export async function askKg(text: string, topK = 6): Promise<KgAskResult> {
  const { data } = await http.post<KgAskResult>('/api/student/kg/ask', {
    text,
    top_k: topK,
  })
  return data
}

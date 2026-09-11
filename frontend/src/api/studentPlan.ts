import http from '@/api/http'

export interface PlanTaskItem {
  id: string
  title: string
  kind: string
  text: string
  allow_draw: boolean
  status: string
}

export interface RoutePayload {
  task_type: string
  task_mode: 'react_short' | 'plan_execute'
  difficulty: string
  capacity_fit: string
  estimated_items: number
  reason: string
  needs_hitl: boolean
  plan_summary: string
  items: PlanTaskItem[]
  this_turn_ids: string[]
  continuation_hint?: string
  answer_this_round?: number
  total_detected?: number
  source?: string
  blocked?: boolean
  block_message?: string
}

export interface PerceiveRouteResponse {
  ok: boolean
  continue: boolean
  blocked?: boolean
  plan_id: string | null
  needs_confirm: boolean
  plan_status?: string
  utterance_intent?: string
  perceived_text: string
  perception_summary: string
  bubble_markdown: string
  max_tasks?: number
  route: RoutePayload
  next_item?: PlanTaskItem | null
  remaining_count?: number
}

export async function perceiveAndRoute(body: {
  text?: string
  image_base64?: string | null
  has_file?: boolean
  file_kind?: string | null
  file_text?: string | null
  intent_hint?: string | null
  thread_id?: string | null
}): Promise<PerceiveRouteResponse> {
  const { data } = await http.post<PerceiveRouteResponse>(
    '/api/student/plan/perceive-route',
    body,
    { timeout: 120_000 },
  )
  return data
}

export async function confirmStudentPlan(body: {
  plan_id: string
  selected_ids: string[]
  cancel?: boolean
}) {
  const { data } = await http.post('/api/student/plan/confirm', body)
  return data as {
    ok: boolean
    cancelled: boolean
    plan_id?: string
    execute_ids: string[]
    items: PlanTaskItem[]
    next_item?: PlanTaskItem | null
    task_mode?: string
    plan_status?: string
    remaining_count?: number
    message?: string
  }
}

export async function classifyPlanIntent(body: {
  plan_id?: string | null
  thread_id?: string | null
  text: string
}) {
  const { data } = await http.post('/api/student/plan/intent', body)
  return data as {
    ok: boolean
    has_plan: boolean
    intent: 'confirm' | 'continue' | 'cancel' | 'side_qa'
    plan_id: string | null
    plan_status?: string
    plan_stays_open?: boolean
  }
}

export async function fetchNextPlanItem(planId: string) {
  const { data } = await http.post('/api/student/plan/next', { plan_id: planId })
  return data as {
    ok: boolean
    has_more: boolean
    plan_status: string
    next_item: PlanTaskItem | null
    perceived_text?: string
    stem_image_path?: string
    remaining_count?: number
    done_count?: number
    total?: number
    message?: string
  }
}

export async function markPlanDone(planId: string, doneIds: string[]) {
  const { data } = await http.post('/api/student/plan/mark-done', {
    plan_id: planId,
    done_ids: doneIds,
  })
  return data as {
    ok: boolean
    remaining_ids: string[]
    has_more: boolean
    plan_status?: string
    message?: string
  }
}

export async function cancelStudentPlan(planId: string) {
  const { data } = await http.post('/api/student/plan/cancel', { plan_id: planId })
  return data as { ok: boolean; plan_status: string; message?: string }
}

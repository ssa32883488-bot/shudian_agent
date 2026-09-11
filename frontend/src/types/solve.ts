/**
 * 解题相关类型。
 * 前端统一使用 NormalizedSolveResult；原始后端响应经适配层转换。
 */

/** 信任分级（宪法红线）：题库命中 vs AI 现解 */
export type TrustSource = 'answer_bank' | 'ai_solve'

/** 前端发出的规范化请求 */
export interface SolveRequestPayload {
  text?: string
  /** 图片：base64（可含 data URL 前缀）或可访问 URL */
  image?: string
  student_id: string
  /** 会话线程 id（短期记忆服务端权威） */
  thread_id?: string
  /** 用户消息幂等 id */
  client_message_id?: string
  /** Plan 子题：回流用干净题干（不含完整识读包装） */
  reflow_stem?: string
  /** Plan 子题：已落盘原图路径 */
  reflow_image_path?: string
}

/** 前端统一消费的规范化响应 */
export interface NormalizedSolveResult {
  /** 信任来源，决定角标 */
  source: TrustSource
  /** Markdown 答案正文 */
  answer: string
  /** 附加图片 URL（可选） */
  images: string[]
  /** 提示语（如「AI解答，仅供参考」） */
  note: string
  /** 角标展示文案 */
  trustLabel: string
  /** 是否命中题库 */
  hit: boolean
  /** 知识图谱锚定（关键词 / 逻辑链） */
  kgContext?: {
    keywords?: string[]
    learning_chain?: string[]
    related_problems?: Array<{ problem_id: string }>
  } | null
  /** 原始响应用于调试 */
  raw?: unknown
}

/** 对话消息 */
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  /** 用户文字或助手 Markdown */
  content: string
  /** 用户上传的本地预览图（object URL 或 data URL） */
  imagePreview?: string
  /** 助手侧信任分级 */
  trustSource?: TrustSource
  trustLabel?: string
  images?: string[]
  note?: string
  /** 是否正在加载 / 流式中 */
  loading?: boolean
  /** 流式阶段状态文案（思考 / 调工具） */
  statusText?: string
  /** 错误提示 */
  error?: string
  createdAt: number
  /** Plan 模式卡片（气泡内确认，非弹窗） */
  planCard?: {
    planId: string
    summary: string
    mode: 'plan_execute' | 'react_short'
    totalDetected: number
    answerThisRound: number
    items: Array<{
      id: string
      title: string
      kind: string
      allow_draw?: boolean
      status?: string
    }>
    awaitingConfirm?: boolean
    active?: boolean
  }
}

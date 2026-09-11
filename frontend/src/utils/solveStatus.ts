/**
 * 将后端 SSE status / 工具名映射为气泡可读状态文案
 */

const TOOL_STATUS: Record<string, string> = {
  retrieve_multi_rerank: '正在检索教材…',
  search_question_bank: '正在搜索题库…',
  graph_query: '正在查询知识图谱…',
  draw_with_workflow: '正在生成示意图…',
}

const STATUS_EXACT: Record<string, string> = {
  'ReAct 助学导师开始推理…': '正在分析题目…',
  '生成回答…': '正在组织回答…',
  '返回权威答案': '已命中题库，正在返回权威答案…',
  '未命中题库，进入 AI 助学求解…': '题库未命中，正在启动 AI 求解…',
  '正在权威校验…': '正在校验答案…',
  'OCR/视模型识别完成': '题目识别完成…',
  '使用文本题面': '正在理解题意…',
  '题库未命中': '题库未命中，继续求解…',
  '题面为空，跳过检索': '正在准备解题…',
}

/** 从工具名得到状态句 */
export function statusForTool(name: string, phase: 'start' | 'end' = 'start'): string {
  const key = (name || '').trim()
  const mapped = TOOL_STATUS[key]
  if (phase === 'end') {
    if (mapped) return mapped.replace('正在', '已完成').replace('…', '，继续作答…')
    return '工具已完成，正在继续作答…'
  }
  if (mapped) return mapped
  if (/retrieve|教材/.test(key)) return '正在检索教材…'
  if (/search|bank|题库/.test(key)) return '正在搜索题库…'
  if (/graph|图谱/.test(key)) return '正在查询知识图谱…'
  if (/draw|kmap|workflow/.test(key)) return '正在调用绘图工具…'
  return `正在调用：${key || '工具'}…`
}

/** 将后端原始 status 文案转为用户可读句 */
export function friendlySolveStatus(raw: string): string {
  const msg = (raw || '').trim()
  if (!msg) return '正在思考…'

  if (STATUS_EXACT[msg]) return STATUS_EXACT[msg]

  const toolCall = msg.match(/^正在调用工具[：:]\s*(.+)$/)
  if (toolCall) return statusForTool(toolCall[1].trim(), 'start')

  const toolDone = msg.match(/^工具完成[：:]\s*(.+)$/)
  if (toolDone) return statusForTool(toolDone[1].trim(), 'end')

  if (/输入归一/.test(msg)) return '正在接收题目…'
  if (/OCR|视模型|识别/.test(msg)) return '正在识别题目…'
  if (/题库命中|命中题库|权威/.test(msg)) return '正在返回权威答案…'
  if (/题库未命中|未命中/.test(msg)) return '题库未命中，正在 AI 求解…'
  if (/图谱锚定|知识点/.test(msg)) return '正在关联知识点…'
  if (/ReAct|推理/.test(msg)) return '正在分析题目…'
  if (/校验/.test(msg)) return '正在校验答案…'
  if (/回流|入库/.test(msg)) return '正在整理结果…'
  if (/生成回答|组织回答/.test(msg)) return '正在组织回答…'
  if (/嵌入配图|绘制卡诺/.test(msg)) return msg
  if (/准备调用绘图/.test(msg)) return '正在准备绘图工具…'
  if (/继续组织解答/.test(msg)) return '正在继续作答…'

  // 已是面向用户的短句则直接用
  if (/^正在/.test(msg) || /…$/.test(msg) || /完成/.test(msg)) return msg
  return msg
}

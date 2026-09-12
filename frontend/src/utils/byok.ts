/**
 * BYOK：API Key 仅存浏览器本地，不上业务服务器。
 * 填写后前端直连模型商时应读取此处；勿把 key 放进 axios 默认头发往本后端。
 */
const KEY_STORAGE = 'shudian_byok_api_key'
const BASE_STORAGE = 'shudian_byok_base_url'
const MODEL_STORAGE = 'shudian_byok_model'

export function getByokKey(): string {
  try {
    return sessionStorage.getItem(KEY_STORAGE) || localStorage.getItem(KEY_STORAGE) || ''
  } catch {
    return ''
  }
}

export function setByokKey(key: string, persist = false) {
  const v = (key || '').trim()
  sessionStorage.removeItem(KEY_STORAGE)
  localStorage.removeItem(KEY_STORAGE)
  if (!v) return
  if (persist) localStorage.setItem(KEY_STORAGE, v)
  else sessionStorage.setItem(KEY_STORAGE, v)
}

export function clearByokKey() {
  sessionStorage.removeItem(KEY_STORAGE)
  localStorage.removeItem(KEY_STORAGE)
}

export function hasByokKey(): boolean {
  return Boolean(getByokKey())
}

export function getByokBaseUrl(): string {
  return localStorage.getItem(BASE_STORAGE) || 'https://api.deepseek.com/v1'
}

export function setByokBaseUrl(url: string) {
  localStorage.setItem(BASE_STORAGE, (url || '').trim())
}

export function getByokModel(): string {
  return localStorage.getItem(MODEL_STORAGE) || 'deepseek-flash'
}

export function setByokModel(model: string) {
  localStorage.setItem(MODEL_STORAGE, (model || '').trim())
}

/** 文件上传前校验：无 Key 则阻断 */
export function assertByokForFile(): void {
  if (!hasByokKey()) {
    throw new Error('上传 Word/PDF/PPT 前请先在设置中填写自己的 API Key（仅保存在本机）')
  }
}

import axios from 'axios'
import { ElMessage } from 'element-plus'

/**
 * Axios 实例：鉴权仅 Bearer Token。
 */
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 120_000,
  headers: {
    'Content-Type': 'application/json',
  },
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('shudian_auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (res) => res,
  (error) => {
    const status = error?.response?.status
    const url: string = error?.config?.url || ''
    if (status === 401 && !url.includes('/api/auth/login')) {
      localStorage.removeItem('shudian_auth_token')
      localStorage.removeItem('shudian_auth_user')
      if (!window.location.pathname.startsWith('/login')) {
        const redirect = encodeURIComponent(
          window.location.pathname + window.location.search,
        )
        window.location.href = `/login?redirect=${redirect}`
      }
    }
    if (!url.includes('/api/student/solve')) {
      const msg =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        error?.message ||
        '网络请求失败'
      ElMessage.error(typeof msg === 'string' ? msg : '请求失败，请稍后重试')
    }
    return Promise.reject(error)
  },
)

export default http

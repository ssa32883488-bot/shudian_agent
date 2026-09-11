/**
 * 用户状态：必须真实登录（Bearer Token）；不再提供免登录演示身份。
 */
import { defineStore, getActivePinia } from 'pinia'
import { computed, ref } from 'vue'

import { bindClassCode, loginStudent, registerStudent } from '@/api/auth'
import type { LoginPayload, RegisterPayload, UserProfile } from '@/types/auth'

const USER_KEY = 'shudian_auth_user'
const TOKEN_KEY = 'shudian_auth_token'

function loadStoredUser(): UserProfile | null {
  try {
    const raw = localStorage.getItem(USER_KEY)
    if (!raw) return null
    return JSON.parse(raw) as UserProfile
  } catch {
    return null
  }
}

/** 同步清空会话内存态，避免换号后仍展示上一账号线程 */
function clearChatSessions() {
  const pinia = getActivePinia()
  const store = pinia?._s.get('chatSessions') as { reset?: () => void } | undefined
  store?.reset?.()
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem(TOKEN_KEY) || '')
  const profile = ref<UserProfile | null>(token.value ? loadStoredUser() : null)

  const isLoggedIn = computed(() => Boolean(token.value && profile.value))
  const studentId = computed(() =>
    profile.value ? String(profile.value.id) : '',
  )
  const studentName = computed(() => profile.value?.nickname || '')
  const avatarChar = computed(() =>
    (profile.value?.nickname || '学').slice(0, 1),
  )
  const role = computed(() => profile.value?.role || 'student')
  const isAdmin = computed(
    () => role.value === 'admin' || role.value === 'teacher',
  )
  const isTeacher = computed(() => isAdmin.value)
  const isStudent = computed(() => role.value === 'student')
  const homePath = computed(() => (isAdmin.value ? '/admin/class' : '/home'))
  const hasToken = computed(() => Boolean(token.value))

  function persist(user: UserProfile, tok?: string) {
    profile.value = user
    localStorage.setItem(USER_KEY, JSON.stringify(user))
    if (tok !== undefined) {
      token.value = tok
      if (tok) localStorage.setItem(TOKEN_KEY, tok)
      else localStorage.removeItem(TOKEN_KEY)
    }
  }

  function logout() {
    clearChatSessions()
    token.value = ''
    profile.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem('shudian_dev_persona')
  }

  async function register(payload: RegisterPayload) {
    clearChatSessions()
    const role =
      payload.role === 'teacher' || payload.role === 'admin' ? 'teacher' : 'student'
    const data = await registerStudent({
      ...payload,
      role: role === 'teacher' ? 'teacher' : 'student',
    })
    persist(data.user, data.token)
  }

  async function login(payload: LoginPayload) {
    clearChatSessions()
    const data = await loginStudent(payload)
    persist(data.user, data.token)
  }

  async function bindClass(classCode: string) {
    const user = await bindClassCode(classCode)
    persist(user, token.value)
  }

  // 无 token 时清掉残留的演示用户缓存，避免误入业务页
  if (!token.value) {
    profile.value = null
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem('shudian_dev_persona')
  }

  return {
    token,
    profile,
    isLoggedIn,
    hasToken,
    studentId,
    studentName,
    avatarChar,
    role,
    isAdmin,
    isTeacher,
    isStudent,
    homePath,
    register,
    login,
    bindClass,
    logout,
    persist,
  }
})

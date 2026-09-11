<script setup lang="ts">
/**
 * 登录 / 注册：布局对齐学灵伴 login（居中白卡片 + cyan 渐变底）
 * 学生登录 / 教师登录 / 注册
 */
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { useUserStore } from '@/stores/user'

const user = useUserStore()
const router = useRouter()
const route = useRoute()

const mode = ref<'login' | 'register'>('login')
const loading = ref(false)
/** 登录入口身份：学生 or 教师（管理端） */
const loginRole = ref<'student' | 'teacher'>('student')
const registerRole = ref<'student' | 'teacher'>('student')

const nickname = ref('')
const phone = ref('')
const password = ref('')
const classCode = ref('')

const submitLabel = computed(() => {
  if (loading.value) return '请稍候…'
  if (mode.value === 'register') return '注册并进入'
  return loginRole.value === 'teacher' ? '教师登录' : '登录'
})

const accentCyan = computed(
  () =>
    mode.value === 'register'
      ? registerRole.value === 'student'
      : loginRole.value === 'student',
)

function friendlyError(err: unknown): string {
  const ax = err as { response?: { data?: { detail?: unknown } }; message?: string }
  const detail = ax?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail[0]?.msg) return String(detail[0].msg)
  if (!ax?.response) return '无法连接后端，请确认服务已启动'
  return ax.message || '操作失败，请稍后重试'
}

async function submit() {
  if (loading.value) return
  loading.value = true
  try {
    if (mode.value === 'register') {
      if (!nickname.value.trim()) {
        ElMessage.warning('请输入昵称')
        return
      }
      await user.register({
        nickname: nickname.value.trim(),
        phone: phone.value.trim(),
        password: password.value,
        class_code: classCode.value.trim() || undefined,
        role: registerRole.value,
      })
      ElMessage.success('注册成功，欢迎加入学灵伴')
    } else {
      await user.login({
        phone: phone.value.trim(),
        password: password.value,
      })
      const role = user.role
      const isTeacherAccount = role === 'teacher' || role === 'admin'
      if (loginRole.value === 'teacher' && !isTeacherAccount) {
        user.logout()
        ElMessage.error('该账号不是教师账号，请使用学生登录或注册教师管理员')
        return
      }
      if (loginRole.value === 'student' && isTeacherAccount) {
        ElMessage.warning('检测到教师账号，已进入管理端')
      } else {
        ElMessage.success('登录成功')
      }
    }
    const redirect =
      typeof route.query.redirect === 'string' ? route.query.redirect : user.homePath
    router.replace(redirect || user.homePath)
  } catch (err) {
    ElMessage.error(friendlyError(err))
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main
    class="m-0 flex min-h-screen min-w-0 items-center justify-center bg-gradient-to-br from-cyan-50 via-white to-indigo-50 p-4 sm:p-8 text-slate-800"
  >
    <section
      class="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-6 sm:p-10 shadow-xl shadow-cyan-100/50"
    >
      <div class="flex items-center justify-center gap-3 text-2xl font-bold text-slate-900">
        <span
          class="grid h-12 w-12 place-items-center rounded-2xl text-white"
          :class="accentCyan ? 'bg-cyan-600' : 'bg-indigo-600'"
        >
          <iconify-icon class="text-2xl" icon="solar:book-2-bold" />
        </span>
        学灵伴
      </div>
      <p class="mt-3 text-center text-sm text-slate-500">数字电子技术 · 助学智能体</p>

      <div class="mt-8 flex rounded-xl bg-slate-100 p-1 text-sm font-bold">
        <button
          type="button"
          class="flex-1 rounded-lg py-2.5 transition"
          :class="mode === 'login' ? 'bg-white text-cyan-700 shadow-sm' : 'text-slate-500'"
          @click="mode = 'login'"
        >
          登录
        </button>
        <button
          type="button"
          class="flex-1 rounded-lg py-2.5 transition"
          :class="mode === 'register' ? 'bg-white text-cyan-700 shadow-sm' : 'text-slate-500'"
          @click="mode = 'register'"
        >
          注册
        </button>
      </div>

      <form class="mt-6" @submit.prevent="submit">
        <div v-if="mode === 'login'" class="mb-4 flex gap-2">
          <button
            type="button"
            class="flex-1 rounded-xl border px-3 py-2.5 text-sm font-bold"
            :class="
              loginRole === 'student'
                ? 'border-cyan-500 bg-cyan-50 text-cyan-700'
                : 'border-slate-200 text-slate-500'
            "
            @click="loginRole = 'student'"
          >
            学生登录
          </button>
          <button
            type="button"
            class="flex-1 rounded-xl border px-3 py-2.5 text-sm font-bold"
            :class="
              loginRole === 'teacher'
                ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                : 'border-slate-200 text-slate-500'
            "
            @click="loginRole = 'teacher'"
          >
            教师登录
          </button>
        </div>

        <div v-if="mode === 'register'" class="mb-4 flex gap-2">
          <button
            type="button"
            class="flex-1 rounded-xl border px-3 py-2.5 text-sm font-bold"
            :class="
              registerRole === 'student'
                ? 'border-cyan-500 bg-cyan-50 text-cyan-700'
                : 'border-slate-200 text-slate-500'
            "
            @click="registerRole = 'student'"
          >
            学生
          </button>
          <button
            type="button"
            class="flex-1 rounded-xl border px-3 py-2.5 text-sm font-bold"
            :class="
              registerRole === 'teacher'
                ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                : 'border-slate-200 text-slate-500'
            "
            @click="registerRole = 'teacher'"
          >
            教师管理员
          </button>
        </div>

        <input
          v-if="mode === 'register'"
          v-model="nickname"
          class="box-border mb-4 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-cyan-500"
          maxlength="32"
          placeholder="昵称（例如：林知夏）"
          required
        />

        <input
          v-model="phone"
          class="box-border w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-cyan-500"
          inputmode="tel"
          maxlength="11"
          pattern="[0-9]{11}"
          placeholder="手机号（11 位，无需短信验证）"
          required
        />

        <input
          v-model="password"
          class="mt-4 box-border w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-cyan-500"
          minlength="6"
          placeholder="密码（至少 6 位）"
          required
          type="password"
        />

        <input
          v-if="mode === 'register' && registerRole === 'student'"
          v-model="classCode"
          class="mt-4 box-border w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-cyan-500"
          maxlength="32"
          placeholder="班级码（选填，向教师管理员索取）"
        />

        <button
          class="mt-7 w-full rounded-xl py-3 text-sm font-bold text-white shadow-sm disabled:opacity-60"
          :class="
            accentCyan
              ? 'bg-cyan-600 hover:bg-cyan-700'
              : 'bg-indigo-600 hover:bg-indigo-700'
          "
          :disabled="loading"
          type="submit"
        >
          {{ submitLabel }}
        </button>
      </form>
    </section>
  </main>
</template>

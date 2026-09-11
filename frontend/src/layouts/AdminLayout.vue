<script setup lang="ts">
/**
 * 管理控制台：班级 / 学情 / 题库 / 回流 / 观测
 */
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useUserStore } from '@/stores/user'

const user = useUserStore()
const route = useRoute()
const router = useRouter()

const tabs = [
  { key: 'class', label: '班级管理', icon: 'solar:users-group-two-rounded-linear' },
  { key: 'learning', label: '班级学情', icon: 'solar:chart-square-linear' },
  { key: 'bank', label: '题库维护', icon: 'solar:clipboard-list-linear' },
  { key: 'reflow', label: '回流审核', icon: 'solar:inbox-archive-linear' },
  { key: 'observe', label: '系统观测', icon: 'solar:eye-linear' },
] as const

const activeTab = computed(() => {
  const tab = route.params.tab as string
  return tabs.some((t) => t.key === tab) ? tab : 'class'
})

function goTab(key: string) {
  router.push(`/admin/${key}`)
}

function goLogin() {
  user.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-shell">
    <header class="admin-shell__header">
      <RouterLink class="brand" to="/admin/bank">
        <span class="brand__mark">
          <iconify-icon icon="solar:settings-bold" />
        </span>
        <span class="brand__name">学灵伴 · 管理控制台</span>
      </RouterLink>
      <div class="admin-shell__meta">
        <span class="ai-badge">AI 生成内容</span>
        <div class="user-chip">
          <span class="user-chip__avatar">{{ user.avatarChar }}</span>
          <div class="user-chip__info">
            <b>{{ user.studentName || '管理员' }}</b>
            <span>班级 · 题库 · 学情 · 观测</span>
          </div>
          <button class="ghost-btn" type="button" @click="goLogin">退出登录</button>
        </div>
      </div>
    </header>

    <div class="admin-shell__body">
      <aside class="admin-shell__rail">
        <p class="rail-label">管理空间</p>
        <nav class="rail-nav">
          <button
            v-for="item in tabs"
            :key="item.key"
            class="rail-link"
            :class="{ 'is-active': activeTab === item.key }"
            type="button"
            @click="goTab(item.key)"
          >
            <iconify-icon :icon="item.icon" />
            {{ item.label }}
          </button>
        </nav>
      </aside>
      <main class="admin-shell__main">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-shell {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100%;
  min-width: 1024px;
  overflow: hidden;
  background: #f1f5f9;
  color: #0f172a;
}
.admin-shell__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 64px;
  padding: 0 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #fff;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
}
.brand__mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #0f766e;
  color: #fff;
  font-size: 18px;
}
.brand__name {
  font-weight: 700;
  letter-spacing: -0.02em;
}
.admin-shell__meta {
  display: flex;
  align-items: center;
  gap: 12px;
}
.ai-badge {
  border-radius: 999px;
  background: #ecfdf5;
  color: #047857;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
}
.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
}
.user-chip__avatar {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: #0f766e;
  color: #fff;
  font-weight: 700;
}
.user-chip__info {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}
.user-chip__info span {
  font-size: 12px;
  color: #64748b;
}
.ghost-btn {
  border: 1px solid #cbd5e1;
  background: #fff;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 12px;
  cursor: pointer;
}
.admin-shell__body {
  display: flex;
  flex: 1;
  min-height: 0;
}
.admin-shell__rail {
  width: 220px;
  border-right: 1px solid #e2e8f0;
  background: #0f172a;
  color: #e2e8f0;
  padding: 16px 12px;
}
.rail-label {
  margin: 0 8px 12px;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #94a3b8;
}
.rail-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.rail-link {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: #cbd5e1;
  padding: 10px 12px;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
}
.rail-link.is-active,
.rail-link:hover {
  background: rgba(45, 212, 191, 0.16);
  color: #5eead4;
}
.admin-shell__main {
  flex: 1;
  overflow: auto;
  padding: 24px;
}
</style>

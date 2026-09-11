<script setup lang="ts">
/**
 * 学生端壳层：桌面侧栏 + 移动底栏
 */
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useUserStore } from '@/stores/user'

const props = withDefaults(
  defineProps<{
    activeNav?: 'home' | 'chat' | 'practice' | 'records' | 'kg'
    flush?: boolean
  }>(),
  { activeNav: undefined, flush: false },
)

const user = useUserStore()
const route = useRoute()
const router = useRouter()
const drawerOpen = ref(false)

const navItems = [
  { key: 'home', label: '学习总览', short: '总览', to: '/home', icon: 'solar:home-2-linear' },
  { key: 'chat', label: 'AI答疑', short: '答疑', to: '/chat', icon: 'solar:chat-round-line-linear' },
  {
    key: 'kg',
    label: '知识图谱',
    short: '图谱',
    to: '/kg',
    icon: 'solar:share-circle-linear',
  },
  {
    key: 'practice',
    label: '个性化加练',
    short: '加练',
    to: '/practice',
    icon: 'solar:document-text-linear',
  },
  {
    key: 'records',
    label: '错题与学情',
    short: '学情',
    to: '/records',
    icon: 'solar:history-linear',
  },
] as const

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return '上午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

const active = computed(() => {
  if (props.activeNav) return props.activeNav
  if (route.path.startsWith('/home')) return 'home'
  if (route.path.startsWith('/chat')) return 'chat'
  if (route.path.startsWith('/kg')) return 'kg'
  if (route.path.startsWith('/practice') || route.path.startsWith('/exam')) return 'practice'
  if (route.path.startsWith('/records')) return 'records'
  return 'home'
})

function goLogin() {
  user.logout()
  router.push('/login')
}

function goNav(to: string) {
  drawerOpen.value = false
  router.push(to)
}
</script>

<template>
  <div class="student-shell" :class="{ 'is-flush': flush }">
    <header class="mobile-top">
      <button class="icon-btn" type="button" aria-label="菜单" @click="drawerOpen = true">
        <iconify-icon icon="solar:hamburger-menu-linear" />
      </button>
      <RouterLink class="mobile-brand" to="/home">学灵伴</RouterLink>
      <button class="icon-btn" type="button" aria-label="登录" @click="goLogin">
        <iconify-icon icon="solar:user-circle-linear" />
      </button>
    </header>

    <div
      v-if="drawerOpen"
      class="drawer-mask"
      @click="drawerOpen = false"
    />
    <aside class="student-shell__rail" :class="{ 'is-open': drawerOpen }">
      <RouterLink class="brand" to="/home" @click="drawerOpen = false">
        <span class="brand__mark">
          <iconify-icon icon="solar:book-2-bold" />
        </span>
        <span class="brand__name">学灵伴</span>
      </RouterLink>

      <p class="rail-label">学习空间</p>
      <nav class="rail-nav">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="rail-link"
          :class="{ 'is-active': active === item.key }"
          type="button"
          @click="goNav(item.to)"
        >
          <iconify-icon :icon="item.icon" />
          {{ item.label }}
        </button>
      </nav>

      <div class="rail-footer">
        <span class="ai-badge">AI 生成内容</span>
        <div class="user-chip">
          <span class="user-chip__avatar">{{ user.avatarChar }}</span>
          <div class="user-chip__info">
            <b>{{ user.studentName || '同学' }}</b>
            <span>{{ greeting }}</span>
          </div>
        </div>
        <div class="rail-actions">
          <button class="ghost-btn" type="button" @click="goLogin">退出登录</button>
        </div>
      </div>
    </aside>

    <main class="student-shell__main" :class="{ 'is-flush': flush }">
      <slot />
    </main>

    <nav class="mobile-tab" aria-label="主导航">
      <button
        v-for="item in navItems"
        :key="item.key"
        class="tab-item"
        :class="{ 'is-active': active === item.key }"
        type="button"
        @click="goNav(item.to)"
      >
        <iconify-icon :icon="item.icon" />
        <span>{{ item.short }}</span>
      </button>
    </nav>
  </div>
</template>

<style scoped>
.student-shell {
  display: flex;
  height: 100%;
  min-height: 100%;
  min-height: 100dvh;
  overflow: hidden;
  background: #f8fafc;
  color: #1e293b;
}

.mobile-top,
.mobile-tab,
.drawer-mask {
  display: none;
}

.student-shell__rail {
  width: 196px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  padding: 16px 10px 12px;
  background: #0f172a;
  color: #cbd5e1;
  z-index: 40;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin: 0 4px 18px;
  padding: 4px 2px;
}

.brand__mark {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: #0891b2;
  color: #fff;
  font-size: 16px;
  flex-shrink: 0;
}

.brand__name {
  font-size: 16px;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: 0.02em;
}

.rail-label {
  margin: 0 0 8px;
  padding: 0 10px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #64748b;
}

.rail-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-height: 0;
}

.rail-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: 8px;
  border: 0;
  background: transparent;
  font-size: 13px;
  font-weight: 500;
  color: #cbd5e1;
  line-height: 1.3;
  text-align: left;
  width: 100%;
}

.rail-link:hover {
  background: #1e293b;
  color: #fff;
}

.rail-link.is-active {
  background: #0891b2;
  color: #fff;
  font-weight: 600;
}

.rail-link iconify-icon {
  font-size: 17px;
  flex-shrink: 0;
}

.rail-footer {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rail-footer .ai-badge {
  align-self: flex-start;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.user-chip__avatar {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: #fef3c7;
  color: #b45309;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-chip__info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  font-size: 12px;
  line-height: 1.25;
  color: #e2e8f0;
}

.user-chip__info b {
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-chip__info span {
  color: #94a3b8;
  font-size: 11px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.ghost-btn {
  padding: 6px 8px;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #1e293b;
  color: #cbd5e1;
  font-size: 11px;
  font-weight: 600;
}

.ghost-btn:hover {
  background: #334155;
  color: #fff;
}

.student-shell__main {
  flex: 1;
  min-width: 0;
  overflow: auto;
  padding: 32px;
  -webkit-overflow-scrolling: touch;
}

.student-shell__main.is-flush {
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
  flex: 1;
}

.student-shell__main.is-flush > :deep(*) {
  flex: 1;
  min-height: 0;
}

@media (max-width: 900px) {
  .student-shell {
    flex-direction: column;
  }

  .mobile-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    flex-shrink: 0;
    height: 52px;
    padding: 0 12px;
    background: #0f172a;
    color: #f8fafc;
    z-index: 30;
  }

  .mobile-brand {
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.02em;
  }

  .icon-btn {
    display: grid;
    place-items: center;
    width: 40px;
    height: 40px;
    border: 0;
    border-radius: 10px;
    background: transparent;
    color: #e2e8f0;
    font-size: 22px;
  }

  .drawer-mask {
    display: block;
    position: fixed;
    inset: 0;
    background: rgb(15 23 42 / 0.45);
    z-index: 35;
  }

  .student-shell__rail {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: min(280px, 82vw);
    transform: translateX(-105%);
    transition: transform 0.22s ease;
    box-shadow: 8px 0 24px rgb(0 0 0 / 0.2);
  }

  .student-shell__rail.is-open {
    transform: translateX(0);
  }

  .student-shell__main {
    padding: 16px 14px 88px;
  }

  .student-shell.is-flush .student-shell__main,
  .student-shell__main.is-flush {
    padding: 0 0 64px;
  }

  .mobile-tab {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 30;
    height: calc(56px + env(safe-area-inset-bottom, 0px));
    padding-bottom: env(safe-area-inset-bottom, 0px);
    background: #fff;
    border-top: 1px solid #e2e8f0;
  }

  .tab-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    border: 0;
    background: transparent;
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
  }

  .tab-item iconify-icon {
    font-size: 20px;
  }

  .tab-item.is-active {
    color: #0891b2;
  }
}
</style>

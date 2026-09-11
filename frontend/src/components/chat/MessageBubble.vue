<script setup lang="ts">
/**
 * 单条消息气泡：用户（右）/ 助手（左）
 */
import { Loading, Picture, WarningFilled } from '@element-plus/icons-vue'

import MarkdownRenderer from '@/components/markdown/MarkdownRenderer.vue'
import TrustBadge from '@/components/chat/TrustBadge.vue'
import type { ChatMessage } from '@/types/solve'

const props = defineProps<{
  message: ChatMessage
}>()

const emit = defineEmits<{
  confirmPlan: [planId: string]
  cancelPlan: [planId: string]
  continuePlan: [planId: string]
  addMistake: [message: ChatMessage]
}>()

const canAddMistake = () =>
  props.message.role === 'assistant' &&
  !props.message.loading &&
  !props.message.error &&
  Boolean(props.message.content?.trim()) &&
  !props.message.planCard?.awaitingConfirm
</script>

<template>
  <div
    class="bubble-row"
    :class="message.role === 'user' ? 'bubble-row--user' : 'bubble-row--assistant'"
  >
    <div class="bubble">
      <div
        v-if="message.planCard"
        class="plan-mode-tag"
      >
        Plan 模式
      </div>

      <TrustBadge
        v-if="message.role === 'assistant' && message.trustSource && !message.loading && !message.error"
        :source="message.trustSource"
        :label="message.trustLabel"
      />

      <div v-if="message.loading && !message.content && !message.error && !message.planCard" class="bubble-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span :key="message.statusText || 'default'" class="bubble-loading__text">
          {{ message.statusText || '正在思考…' }}
        </span>
      </div>

      <div v-else-if="message.error" class="bubble-error">
        <el-icon><WarningFilled /></el-icon>
        <span>{{ message.error }}</span>
      </div>

      <div v-else-if="message.role === 'user'" class="bubble-user-text">
        <MarkdownRenderer v-if="message.content" :content="message.content" />
        <div v-if="message.imagePreview" class="bubble-thumb">
          <el-image
            :src="message.imagePreview"
            :preview-src-list="[message.imagePreview]"
            fit="cover"
            class="thumb-img"
          >
            <template #error>
              <div class="thumb-fallback">
                <el-icon><Picture /></el-icon>
              </div>
            </template>
          </el-image>
        </div>
      </div>

      <div v-else class="bubble-assistant-body">
        <div v-if="message.loading && !message.content" class="bubble-loading">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span :key="message.statusText || 'default'" class="bubble-loading__text">
            {{ message.statusText || '正在读取内容…' }}
          </span>
        </div>
        <MarkdownRenderer
          v-if="message.content"
          :content="message.content"
          :images="message.images"
        />
        <div v-if="message.planCard" class="plan-card">
          <div class="plan-card__meta">
            识别约 {{ message.planCard.totalDetected }} 道 · 本回合
            {{ message.planCard.answerThisRound }} 道
          </div>
          <ol class="plan-card__list">
            <li v-for="(it, idx) in message.planCard.items" :key="it.id">
              <span class="idx">{{ idx + 1 }}</span>
              <span class="title">{{ it.title }}</span>
              <span class="kind">{{ it.kind }}{{ it.allow_draw ? ' · 图' : '' }}</span>
              <span class="st">{{ it.status || 'pending' }}</span>
            </li>
          </ol>
          <div v-if="message.planCard.awaitingConfirm" class="plan-card__actions">
            <button
              type="button"
              class="btn-ghost"
              @click="emit('cancelPlan', message.planCard!.planId)"
            >
              取消任务
            </button>
            <button
              type="button"
              class="btn-primary"
              @click="emit('confirmPlan', message.planCard!.planId)"
            >
              确认执行
            </button>
          </div>
          <div v-else class="plan-card__actions">
            <button
              type="button"
              class="btn-ghost"
              @click="emit('cancelPlan', message.planCard!.planId)"
            >
              取消任务
            </button>
            <button
              type="button"
              class="btn-primary"
              @click="emit('continuePlan', message.planCard!.planId)"
            >
              继续下一题
            </button>
          </div>
          <p class="plan-card__hint">也可直接回复「确认 / 继续 / 取消任务」</p>
        </div>
        <span v-if="message.loading && message.content" class="stream-caret" aria-hidden="true">|</span>
        <div v-if="canAddMistake()" class="bubble-actions">
          <button type="button" class="btn-add-mistake" @click="emit('addMistake', message)">
            加入错题本
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.bubble-row {
  display: flex;
  margin-bottom: 16px;
  padding: 0 4px;

  &--user {
    justify-content: flex-end;
  }
  &--assistant {
    justify-content: flex-start;
  }
}

.bubble {
  max-width: min(720px, 92%);
  position: relative;
}

.plan-mode-tag {
  display: inline-flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #0f766e;
  background: #ccfbf1;
  border: 1px solid #99f6e4;
}

.bubble-row--user .bubble {
  background: #ecfeff;
  border: 1px solid #a5f3fc;
  border-radius: 16px 16px 4px 16px;
  padding: 12px 14px;
}

.bubble-row--assistant .bubble {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px 16px 16px 4px;
  padding: 12px 14px;
}

.bubble-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 13px;
  min-height: 1.5em;
}

.bubble-loading__text {
  display: inline-block;
  animation: status-fade-in 0.28s ease;
}

@keyframes status-fade-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.bubble-error {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #b91c1c;
  font-size: 13px;
}

.bubble-thumb {
  margin-top: 8px;
  width: 160px;
  height: 120px;
  border-radius: 10px;
  overflow: hidden;
}

.thumb-img {
  width: 100%;
  height: 100%;
}

.thumb-fallback {
  display: grid;
  place-items: center;
  width: 100%;
  height: 100%;
  background: #f1f5f9;
  color: #94a3b8;
}

.stream-caret {
  color: #0891b2;
  font-weight: 700;
}

.plan-card {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px dashed #cbd5e1;
}

.plan-card__meta {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 8px;
}

.plan-card__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 6px;
}

.plan-card__list li {
  display: grid;
  grid-template-columns: 22px 1fr auto auto;
  gap: 8px;
  align-items: center;
  font-size: 13px;
  padding: 6px 8px;
  border-radius: 8px;
  background: #f8fafc;
}

.plan-card__list .idx {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  display: grid;
  place-items: center;
  background: #ecfeff;
  color: #0e7490;
  font-size: 11px;
  font-weight: 700;
}

.plan-card__list .title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #0f172a;
}

.plan-card__list .kind,
.plan-card__list .st {
  font-size: 11px;
  color: #64748b;
}

.plan-card__actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.btn-ghost,
.btn-primary {
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 650;
  cursor: pointer;
}

.btn-ghost {
  border: 1px solid #cbd5e1;
  background: #fff;
  color: #475569;
}

.btn-primary {
  border: 1px solid #0f766e;
  background: #0f766e;
  color: #fff;
}

.plan-card__hint {
  margin: 8px 0 0;
  font-size: 12px;
  color: #94a3b8;
}

.bubble-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

.btn-add-mistake {
  border: 1px solid #a5f3fc;
  background: #ecfeff;
  color: #0e7490;
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.btn-add-mistake:hover {
  background: #cffafe;
}
</style>

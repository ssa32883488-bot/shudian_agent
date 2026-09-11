<script setup lang="ts">
/**
 * 消息列表：自动滚到底部
 */
import { nextTick, ref, watch } from 'vue'

import MessageBubble from '@/components/chat/MessageBubble.vue'
import type { ChatMessage } from '@/types/solve'

const props = defineProps<{
  messages: ChatMessage[]
}>()

defineEmits<{
  confirmPlan: [planId: string]
  cancelPlan: [planId: string]
  continuePlan: [planId: string]
  addMistake: [message: ChatMessage]
}>()

const listRef = ref<HTMLElement | null>(null)

async function scrollToBottom() {
  await nextTick()
  const el = listRef.value
  if (el) el.scrollTop = el.scrollHeight
}

watch(
  () => props.messages.length,
  () => scrollToBottom(),
)

watch(
  () =>
    props.messages
      .map(
        (m) =>
          `${m.id}:${m.loading}:${m.content?.length}:${m.statusText || ''}:${(m.images || []).length}`,
      )
      .join('|'),
  () => scrollToBottom(),
)
</script>

<template>
  <div ref="listRef" class="message-list">
    <div v-if="!messages.length" class="message-list__empty">
      <span class="empty-mark">
        <iconify-icon icon="solar:camera-bold" />
      </span>
      <p class="title">拍下电路题，和 AI 一起拆解</p>
      <p class="desc">
        支持逻辑表达式、真值表与电路图；命中题库给权威答案，AI 现解会标注「仅供参考」。
      </p>
      <ul class="hints">
        <li>什么是竞争冒险？如何消除？</li>
        <li>用卡诺图化简 F(A,B,C,D)=Σm(0,2,5,7)</li>
        <li>拍一张时序电路题开始拆解</li>
      </ul>
    </div>
    <MessageBubble
      v-for="msg in messages"
      :key="msg.id"
      :message="msg"
      @confirm-plan="(id) => $emit('confirmPlan', id)"
      @cancel-plan="(id) => $emit('cancelPlan', id)"
      @continue-plan="(id) => $emit('continuePlan', id)"
      @add-mistake="(m) => $emit('addMistake', m)"
    />
  </div>
</template>

<style scoped lang="scss">
.message-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 20px 22px 12px;
  scroll-behavior: smooth;
}

.message-list__empty {
  max-width: 440px;
  margin: 10vh auto 0;
  text-align: center;
  color: #64748b;
}

.empty-mark {
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  margin: 0 auto 14px;
  border-radius: 18px;
  background: var(--brand-soft, #ecfeff);
  color: var(--brand, #0891b2);
  font-size: 26px;
}

.title {
  margin: 0 0 8px;
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  color: var(--ink, #0f172a);
}

.desc {
  margin: 0;
  font-size: 14px;
  line-height: 1.7;
}

.hints {
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
  text-align: left;
}

.hints li {
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
  background: #fff;
  font-size: 13px;
  color: #475569;
}

@media (max-width: 900px) {
  .message-list {
    padding: 12px 12px 8px;
  }

  .hints {
    display: none;
  }
}
</style>

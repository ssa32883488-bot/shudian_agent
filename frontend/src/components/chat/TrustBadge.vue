<script setup lang="ts">
/**
 * 信任分级角标（宪法红线）
 * - answer_bank：已收录权威答案（冷静绿）
 * - ai_solve：AI解答，仅供参考·不一定准确（醒目琥珀）
 */
import type { TrustSource } from '@/types/solve'
import { TRUST_LABELS } from '@/api/adapters/solve'
import { computed } from 'vue'

const props = defineProps<{
  source: TrustSource
  /** 后端自定义文案；缺省用宪法默认 */
  label?: string
}>()

const text = computed(
  () => props.label?.trim() || TRUST_LABELS[props.source],
)

const isAi = computed(() => props.source === 'ai_solve')
</script>

<template>
  <div
    class="trust-badge"
    :class="isAi ? 'trust-badge--ai' : 'trust-badge--bank'"
    role="status"
  >
    <span class="trust-badge__dot" aria-hidden="true" />
    <span class="trust-badge__text">{{ text }}</span>
  </div>
</template>

<style scoped lang="scss">
.trust-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
  line-height: 1.4;
  margin-bottom: 8px;
  border: 1px solid transparent;
}

.trust-badge__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 题库命中：权威、冷静 */
.trust-badge--bank {
  color: #065f46;
  background: #ecfdf5;
  border-color: #a7f3d0;

  .trust-badge__dot {
    background: #059669;
  }
}

/* AI 现解：醒目警示，宪法要求「显著标注」 */
.trust-badge--ai {
  color: #92400e;
  background: #fffbeb;
  border-color: #fcd34d;
  box-shadow: 0 0 0 1px #fbbf2466;

  .trust-badge__dot {
    background: #d97706;
  }
}
</style>

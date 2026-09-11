<script setup lang="ts">
/**
 * 任意可能含公式的文本统一渲染（题干、解析、推荐卡片等）
 */
import { computed } from 'vue'

import { renderMarkdown } from '@/utils/markdown'

const props = withDefaults(
  defineProps<{
    content?: string | null
    /** 紧凑模式：减少段间距，适合卡片摘要 */
    compact?: boolean
  }>(),
  { content: '', compact: false },
)

const html = computed(() => renderMarkdown(props.content || ''))
</script>

<template>
  <div class="formula-text" :class="{ 'is-compact': compact }" v-html="html" />
</template>

<style scoped>
.formula-text {
  font-size: inherit;
  line-height: 1.7;
  color: inherit;
  word-break: break-word;
  overflow-wrap: anywhere;
}

.formula-text :deep(p) {
  margin: 0 0 0.55em;
}

.formula-text :deep(p:last-child) {
  margin-bottom: 0;
}

.formula-text.is-compact :deep(p) {
  margin: 0 0 0.35em;
}

.formula-text :deep(ul),
.formula-text :deep(ol) {
  margin: 0.35em 0 0.55em;
  padding-left: 1.35em;
}

.formula-text :deep(.katex) {
  font-size: 1.05em;
}

.formula-text :deep(.katex-display) {
  margin: 0.55em 0;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 2px 0;
}

.formula-text :deep(.math-fallback) {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.9em;
  background: rgb(15 23 42 / 0.06);
  padding: 0.1em 0.35em;
  border-radius: 4px;
}

.formula-text :deep(img) {
  display: block;
  max-width: min(100%, 720px);
  height: auto;
  margin: 0.5em 0 0.75em;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
}

.formula-text :deep(.md-html-table) {
  margin: 0.65em 0 0.85em;
  overflow-x: auto;
}

.formula-text :deep(.md-html-table table) {
  border-collapse: collapse;
  width: max-content;
  max-width: 100%;
  font-size: 0.92em;
}

.formula-text :deep(.md-html-table th),
.formula-text :deep(.md-html-table td) {
  border: 1px solid #cbd5e1;
  padding: 0.28em 0.55em;
  vertical-align: middle;
  white-space: nowrap;
}

.formula-text :deep(.md-html-table .katex) {
  font-size: 1em;
}
</style>

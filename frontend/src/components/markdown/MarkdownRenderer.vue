<script setup lang="ts">
/**
 * Markdown + KaTeX 展示组件（助手气泡 / 长文）
 */
import { computed } from 'vue'

import { renderMarkdown } from '@/utils/markdown'

const props = defineProps<{
  content: string
  /** 后端附带的图片 URL 列表，追加到正文下方 */
  images?: string[]
}>()

const html = computed(() => renderMarkdown(props.content || ''))
</script>

<template>
  <div class="md-body">
    <div class="md-html" v-html="html" />
    <div v-if="images?.length" class="md-images">
      <p class="md-images__label">教材相关图</p>
      <el-image
        v-for="(src, idx) in images"
        :key="idx"
        :src="src"
        :preview-src-list="images"
        :initial-index="idx"
        fit="contain"
        class="md-image"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.md-body {
  font-size: 14px;
  line-height: 1.7;
  color: #1f2937;
  word-break: break-word;
}

.md-html {
  :deep(h1),
  :deep(h2),
  :deep(h3),
  :deep(h4) {
    margin: 0.9em 0 0.35em;
    font-weight: 650;
    line-height: 1.35;
    color: #0f172a;
  }

  :deep(h1) {
    font-size: 1.15em;
  }
  :deep(h2) {
    font-size: 1.08em;
  }
  :deep(h3),
  :deep(h4) {
    font-size: 1em;
  }

  :deep(h1:first-child),
  :deep(h2:first-child),
  :deep(h3:first-child),
  :deep(h4:first-child) {
    margin-top: 0;
  }

  :deep(p) {
    margin: 0 0 0.65em;
    &:last-child {
      margin-bottom: 0;
    }
  }

  :deep(ul),
  :deep(ol) {
    margin: 0.35em 0 0.75em;
    padding-left: 1.35em;
  }

  :deep(li) {
    margin: 0.2em 0;
  }

  :deep(li > p) {
    margin: 0.15em 0;
  }

  :deep(hr) {
    border: 0;
    border-top: 1px solid #e5e7eb;
    margin: 0.9em 0;
  }

  :deep(strong) {
    font-weight: 650;
    color: #0f172a;
  }

  :deep(blockquote) {
    margin: 0.5em 0;
    padding: 0.35em 0.85em;
    border-left: 3px solid #67e8f9;
    background: #ecfeff;
    color: #155e75;
  }

  :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 0.55em 0 0.85em;
    font-size: 13px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
  }

  :deep(th),
  :deep(td) {
    border: 1px solid #e5e7eb;
    padding: 6px 10px;
    text-align: left;
    vertical-align: top;
  }

  :deep(th) {
    background: #f8fafc;
    font-weight: 650;
    color: #0f172a;
  }

  :deep(tr:nth-child(even) td) {
    background: #fafafa;
  }

  :deep(.md-html-table) {
    overflow-x: auto;
    margin: 0.55em 0 0.85em;
  }

  :deep(.md-html-table table) {
    margin: 0;
  }

  :deep(pre) {
    background: #0f172a0d;
    padding: 10px 12px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 13px;
  }

  :deep(code) {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.92em;
    background: #0f172a0d;
    padding: 0.1em 0.35em;
    border-radius: 4px;
  }

  :deep(pre code) {
    background: transparent;
    padding: 0;
  }

  :deep(img) {
    max-width: 100%;
    border-radius: 8px;
    margin: 8px 0;
  }

  :deep(a) {
    color: #0891b2;
  }

  :deep(.katex-display) {
    margin: 0.75em 0;
    overflow-x: auto;
    overflow-y: hidden;
  }

  :deep(.katex-error) {
    color: #64748b !important;
    background: #f1f5f9;
    padding: 0 2px;
    border-radius: 3px;
  }

  :deep(.math-fallback) {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.9em;
    color: #334155;
    background: #f1f5f9;
  }
}

.md-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid #eef2f7;
}

.md-images__label {
  flex: 0 0 100%;
  margin: 0 0 2px;
  font-size: 12px;
  color: #64748b;
}

.md-image {
  width: 160px;
  max-height: 160px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}
</style>

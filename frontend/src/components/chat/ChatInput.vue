<script setup lang="ts">
/**
 * 底部输入区：文字 + 图片 / 文件上传 + 发送
 */
import { computed, ref, watch } from 'vue'
import { Close, Document, Picture, Paperclip, Promotion } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { fileToDataUrl } from '@/utils/image'
import { parseUploadFile } from '@/api/student'

export interface ChatSendPayload {
  text: string
  imageDataUrl?: string
  imagePreview?: string
  fileName?: string
  fileText?: string
  fileKind?: 'docx' | 'pdf' | 'ppt' | 'txt' | null
}

const props = defineProps<{
  disabled?: boolean
  sending?: boolean
  /** 外部预填（如从加练报告「拿去问」带入） */
  seed?: string
}>()

const emit = defineEmits<{
  send: [payload: ChatSendPayload]
}>()

const text = ref('')
const imageDataUrl = ref<string | null>(null)
const imagePreview = ref<string | null>(null)
const fileName = ref<string | null>(null)
const fileText = ref<string | null>(null)
const fileKind = ref<ChatSendPayload['fileKind']>(null)
const parsingFile = ref(false)
const imageInputRef = ref<HTMLInputElement | null>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)

const MAX_FILE_BYTES = 25 * 1024 * 1024

const canSend = computed(() => {
  if (props.disabled || props.sending || parsingFile.value) return false
  if (fileName.value && !fileText.value && !imageDataUrl.value && !text.value.trim()) {
    return false
  }
  return Boolean(text.value.trim() || imageDataUrl.value || (fileName.value && fileText.value))
})

watch(
  () => props.seed,
  (v) => {
    if (v && v.trim()) text.value = v.trim()
  },
  { immediate: true },
)
function pickImage() {
  imageInputRef.value?.click()
}

function pickFile() {
  fileInputRef.value?.click()
}

function clearAttachment() {
  imageDataUrl.value = null
  imagePreview.value = null
  fileName.value = null
  fileText.value = null
  fileKind.value = null
  parsingFile.value = false
}

async function attachImageFile(file: File, fromPaste = false) {
  try {
    const dataUrl = await fileToDataUrl(file)
    clearAttachment()
    imageDataUrl.value = dataUrl
    imagePreview.value = dataUrl
    if (fromPaste) ElMessage.success('已从剪贴板粘贴图片')
  } catch (e) {
    ElMessage.warning(e instanceof Error ? e.message : '图片读取失败')
  }
}

async function onImageChange(ev: Event) {
  const input = ev.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return
  await attachImageFile(file)
}

/** 支持 Ctrl+V / 右键粘贴截图或剪贴板图片 */
async function onPaste(e: ClipboardEvent) {
  if (props.disabled || props.sending || parsingFile.value) return
  const items = e.clipboardData?.items
  if (!items?.length) return

  for (const item of Array.from(items)) {
    if (!item.type.startsWith('image/')) continue
    const file = item.getAsFile()
    if (!file) continue
    e.preventDefault()
    await attachImageFile(file, true)
    return
  }

  const files = e.clipboardData?.files
  if (files?.length) {
    for (const file of Array.from(files)) {
      if (!file.type.startsWith('image/')) continue
      e.preventDefault()
      await attachImageFile(file, true)
      return
    }
  }
}

async function onFileChange(ev: Event) {
  const input = ev.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return

  if (file.size > MAX_FILE_BYTES) {
    ElMessage.warning('文件不能超过 25MB')
    return
  }

  if (file.type.startsWith('image/')) {
    await attachImageFile(file)
    return
  }

  const name = file.name
  if (/\.(xlsx|xls|csv)$/i.test(name)) {
    ElMessage.warning('不支持 Excel 文件，请上传 Word / PDF / PPT')
    return
  }

  let kind: ChatSendPayload['fileKind'] = null
  if (/\.docx?$/i.test(name)) kind = 'docx'
  else if (/\.pdf$/i.test(name)) kind = 'pdf'
  else if (/\.pptx?$/i.test(name)) kind = 'ppt'
  else if (/\.(txt|md)$/i.test(name) || file.type.startsWith('text/')) kind = 'txt'

  try {
    clearAttachment()
    fileName.value = name
    fileKind.value = kind

    if (kind === 'txt' || file.type.startsWith('text/')) {
      const extracted = await file.text()
      fileText.value = extracted.slice(0, 180000) || null
      if (!fileText.value) ElMessage.warning('文本文件为空')
      return
    }

    parsingFile.value = true
    ElMessage.info('正在用 MinerU 解析文档，请稍候…')
    const res = await parseUploadFile(file)
    fileText.value = (res.text || '').slice(0, 180000) || null
    if (res.kind === 'docx' || res.kind === 'pdf' || res.kind === 'ppt' || res.kind === 'txt') {
      fileKind.value = res.kind
    }
    parsingFile.value = false
    if (!fileText.value) {
      ElMessage.warning('解析结果为空，请换文件或粘贴题干')
      return
    }
    ElMessage.success(`解析完成（${res.chars || fileText.value.length} 字）`)
  } catch (e: unknown) {
    parsingFile.value = false
    clearAttachment()
    const detail =
      e && typeof e === 'object' && 'response' in e
        ? String(
            (e as { response?: { data?: { detail?: string } } }).response?.data?.detail ||
              '',
          )
        : ''
    ElMessage.warning(detail || '文件解析失败，请稍后重试')
  }
}

function submit() {
  if (!canSend.value) return
  if (parsingFile.value) {
    ElMessage.warning('文档仍在解析，请稍候')
    return
  }
  if (fileName.value && !fileText.value && fileKind.value && fileKind.value !== 'txt') {
    ElMessage.warning('附件尚未解析出正文，请重新上传或粘贴题干')
    return
  }
  emit('send', {
    text: text.value.trim(),
    imageDataUrl: imageDataUrl.value || undefined,
    imagePreview: imagePreview.value || undefined,
    fileName: fileName.value || undefined,
    fileText: fileText.value || undefined,
    fileKind: fileKind.value,
  })
  text.value = ''
  clearAttachment()
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <div class="chat-input">
    <div v-if="imagePreview || fileName" class="chat-input__attach">
      <div v-if="imagePreview" class="preview-wrap">
        <el-image :src="imagePreview" fit="cover" class="preview-img" />
        <button type="button" class="preview-clear" aria-label="移除图片" @click="clearAttachment">
          <el-icon><Close /></el-icon>
        </button>
      </div>
      <div v-else-if="fileName" class="file-chip">
        <el-icon><Document /></el-icon>
        <span>{{ fileName }}</span>
        <span v-if="parsingFile" class="file-parsing">解析中…</span>
        <button type="button" class="file-clear" aria-label="移除文件" @click="clearAttachment">
          <el-icon><Close /></el-icon>
        </button>
      </div>
    </div>

    <div class="chat-input__bar" @paste="onPaste">
      <input
        ref="imageInputRef"
        type="file"
        accept="image/*"
        class="hidden-file"
        @change="onImageChange"
      />
      <input
        ref="fileInputRef"
        type="file"
        accept=".pdf,.doc,.docx,.ppt,.pptx,.txt,.md,application/pdf"
        class="hidden-file"
        @change="onFileChange"
      />

      <button
        class="icon-btn"
        type="button"
        title="上传图片"
        :disabled="disabled || sending"
        @click="pickImage"
      >
        <el-icon :size="18"><Picture /></el-icon>
      </button>
      <button
        class="icon-btn"
        type="button"
        title="上传文件"
        :disabled="disabled || sending || parsingFile"
        @click="pickFile"
      >
        <el-icon :size="18"><Paperclip /></el-icon>
      </button>

      <el-input
        v-model="text"
        type="textarea"
        :autosize="{ minRows: 1, maxRows: 5 }"
        :disabled="disabled || sending"
        placeholder="输入问题，或回复「确认 / 继续 / 取消任务」"
        resize="none"
        @keydown="onKeydown"
      />

      <el-button type="primary" :loading="sending" :disabled="!canSend" @click="submit">
        <el-icon v-if="!sending" class="el-icon--left"><Promotion /></el-icon>
        发送
      </el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-input {
  border-top: 1px solid var(--line, #e2e8f0);
  background: rgb(255 255 255 / 0.96);
  padding: 12px 16px 14px;
  backdrop-filter: blur(8px);
  flex-shrink: 0;
  position: relative;
  z-index: 5;
}

.chat-input__attach {
  margin-bottom: 10px;
}

.preview-wrap {
  position: relative;
  display: inline-block;
}

.preview-img {
  width: 72px;
  height: 72px;
  border-radius: 10px;
  border: 1px solid var(--line, #e2e8f0);
  overflow: hidden;
}

.preview-clear,
.file-clear {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 22px;
  height: 22px;
  border: none;
  border-radius: 50%;
  background: #334155;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.file-chip {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 100%;
  padding: 8px 32px 8px 12px;
  border-radius: 12px;
  border: 1px solid var(--line, #e2e8f0);
  background: #f8fafc;
  font-size: 13px;
  color: #334155;
}

.file-parsing {
  color: #0891b2;
  font-size: 12px;
  flex-shrink: 0;
}

.file-chip .file-clear {
  top: 50%;
  right: 8px;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  background: #94a3b8;
}

.chat-input__bar {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.icon-btn {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border: 1px solid var(--line, #e2e8f0);
  border-radius: 10px;
  background: #fff;
  color: #475569;
  display: grid;
  place-items: center;
}

.icon-btn:hover:not(:disabled) {
  border-color: var(--brand, #0891b2);
  color: var(--brand, #0891b2);
}

.icon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.hidden-file {
  display: none;
}
</style>

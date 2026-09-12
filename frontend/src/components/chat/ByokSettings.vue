<script setup lang="ts">
/**
 * BYOK 本机设置：Key 只存浏览器，不上业务服务器。
 */
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'

import {
  clearByokKey,
  getByokBaseUrl,
  getByokKey,
  getByokModel,
  hasByokKey,
  setByokBaseUrl,
  setByokKey,
  setByokModel,
} from '@/utils/byok'

const open = ref(false)
const keyInput = ref(getByokKey())
const baseUrl = ref(getByokBaseUrl())
const model = ref(getByokModel())
const persist = ref(false)

const statusLabel = computed(() =>
  hasByokKey() ? '已配置本机 API Key' : '未配置（图文可用平台默认）',
)

function save() {
  setByokKey(keyInput.value, persist.value)
  setByokBaseUrl(baseUrl.value)
  setByokModel(model.value)
  ElMessage.success(
    keyInput.value.trim()
      ? '已保存到本机（不会上传到我们的服务器）'
      : '已清除本机 Key',
  )
  open.value = false
}

function clearKey() {
  clearByokKey()
  keyInput.value = ''
  ElMessage.success('已清除本机 Key')
}
</script>

<template>
  <div class="byok">
    <button class="byok-toggle" type="button" @click="open = !open">
      {{ statusLabel }}
    </button>
    <div v-if="open" class="byok-panel">
      <p class="byok-tip">
        Key 仅保存在本浏览器。填写后，本机相关调用应使用你的 Key；我们的业务接口不会接收该字段。
      </p>
      <label>
        API Key
        <input v-model="keyInput" type="password" autocomplete="off" placeholder="sk-…" />
      </label>
      <label>
        Base URL
        <input v-model="baseUrl" type="text" placeholder="https://api.deepseek.com/v1" />
      </label>
      <label>
        Model
        <input v-model="model" type="text" placeholder="deepseek-flash" />
      </label>
      <label class="row">
        <input v-model="persist" type="checkbox" />
        持久化到 localStorage（关闭标签后仍保留；否则仅 session）
      </label>
      <div class="actions">
        <button type="button" @click="clearKey">清除</button>
        <button type="button" class="primary" @click="save">保存</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.byok {
  position: relative;
}
.byok-toggle {
  border: 1px solid #cbd5e1;
  background: #fff;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  color: #334155;
  cursor: pointer;
}
.byok-panel {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  width: min(360px, 92vw);
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 12px 40px rgba(15, 23, 42, 0.12);
  z-index: 40;
  display: grid;
  gap: 8px;
}
.byok-tip {
  margin: 0;
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}
label {
  display: grid;
  gap: 4px;
  font-size: 12px;
  color: #475569;
}
input[type='text'],
input[type='password'] {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 10px;
  font-size: 13px;
}
.row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.actions button {
  border-radius: 8px;
  padding: 6px 12px;
  border: 1px solid #cbd5e1;
  background: #fff;
  cursor: pointer;
}
.actions .primary {
  background: #0f766e;
  border-color: #0f766e;
  color: #fff;
}
</style>

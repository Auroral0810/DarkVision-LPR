<template>
  <div class="app-container">
    <el-card shadow="never" class="log-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-radio-group v-model="logType" @change="fetchLogs">
              <el-radio-button label="app">应用日志</el-radio-button>
              <el-radio-button label="error">错误日志</el-radio-button>
            </el-radio-group>
            <el-input-number v-model="lines" :min="10" :max="1000" step="50" @change="fetchLogs" class="line-input" />
            <span class="tip">显示最后 {{ lines }} 行</span>
          </div>
          <div class="header-right">
            <el-button type="primary" icon="Refresh" @click="fetchLogs" :loading="loading">刷新</el-button>
          </div>
        </div>
      </template>

      <div class="log-terminal" ref="logTerminal">
        <pre v-if="logContent">{{ logContent }}</pre>
        <div v-else class="empty-log">暂无日志内容</div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import SystemAPI from '@/api/system-api'

const logType = ref<'app' | 'error'>('app')
const lines = ref(200)
const loading = ref(false)
const logContent = ref('')
const logTerminal = ref<HTMLElement | null>(null)

const fetchLogs = async () => {
  loading.value = true
  try {
    const res = await SystemAPI.getSystemLogs({ log_type: logType.value, lines: lines.value })
    logContent.value = res.content
    // 自动滚动到底部
    await nextTick()
    if (logTerminal.value) {
      logTerminal.value.scrollTop = logTerminal.value.scrollHeight
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchLogs()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.log-card {
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}
:deep(.el-card__body) {
  flex: 1;
  overflow: hidden;
  padding: 0;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}
.line-input {
  width: 120px;
}
.tip {
  font-size: 13px;
  color: #909399;
}
.log-terminal {
  height: 100%;
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  line-height: 1.5;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
.empty-log {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #666;
}
</style>

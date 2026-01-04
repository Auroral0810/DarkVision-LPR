<template>
  <div class="app-container">
    <el-alert title="实时任务监控" type="info" :closable="false" class="mb-4">
      当前有 {{ activeTasks.length }} 个任务正在处理中
    </el-alert>

    <el-card title="正在处理的任务">
      <el-table :data="activeTasks" v-loading="loading">
        <el-table-column label="任务ID" prop="task_uuid" width="200" />
        <el-table-column label="用户ID" prop="user_id" width="100" />
        <el-table-column label="类型" width="120">
          <template #default="scope">
            <el-tag>{{ getTaskTypeLabel(scope.row.task_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="200">
          <template #default="scope">
            <el-progress :percentage="scope.row.progress" :status="scope.row.progress === 100 ? 'success' : ''" />
          </template>
        </el-table-column>
        <el-table-column label="总数/成功/失败">
          <template #default="scope">
            {{ scope.row.total_items }} / {{ scope.row.success_count }} / {{ scope.row.failed_count }}
          </template>
        </el-table-column>
        <el-table-column label="开始时间" prop="started_at" width="160" />
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button v-if="scope.row.status === 'failed'" type="warning" link @click="handleRetry(scope.row.id)">
              重试
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card title="任务历史" class="mt-4">
      <el-table :data="historyTasks">
        <el-table-column label="任务ID" prop="task_uuid" width="200" />
        <el-table-column label="用户ID" prop="user_id" width="100" />
        <el-table-column label="类型" width="120">
          <template #default="scope">
            <el-tag>{{ getTaskTypeLabel(scope.row.task_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="耗时">
          <template #default="scope">
            {{ calculateDuration(scope.row.started_at, scope.row.finished_at) }}
          </template>
        </el-table-column>
        <el-table-column label="完成时间" prop="finished_at" width="160" />
      </el-table>

      <pagination v-if="total > 0" v-model:total="total" v-model:page="queryParams.page" v-model:limit="queryParams.pageSize" @pagination="fetchHistory" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import LprAPI from '@/api/lpr-api'

const activeTasks = ref([])
const historyTasks = ref([])
const loading = ref(false)
const total = ref(0)
const queryParams = reactive({ page: 1, pageSize: 10 })
let pollingTimer: NodeJS.Timeout | null = null

async function fetchActiveTasks() {
  try {
    activeTasks.value = await LprAPI.getActiveTasks()
  } catch (error) {
    console.error('获取活跃任务失败', error)
  }
}

async function fetchHistory() {
  loading.value = true
  try {
    const data = await LprAPI.getTaskList(queryParams)
    historyTasks.value = data.list
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function handleRetry(taskId: number) {
  try {
    await LprAPI.retryTask(taskId)
    ElMessage.success('任务已重新提交')
    fetchActiveTasks()
  } catch (error) {
    ElMessage.error('重试失败')
  }
}

function getTaskTypeLabel(type: string) {
  const map: Record<string, string> = {
    single: '单图',
    batch: '批量',
    video: '视频',
    realtime: '实时'
  }
  return map[type] || type
}

function getStatusType(status: string) {
  const map: Record<string, any> = {
    pending: 'info',
    processing: '',
    completed: 'success',
    failed: 'danger'
  }
  return map[status] || ''
}

function calculateDuration(start?: string, end?: string) {
  if (!start || !end) return '-'
  const diff = new Date(end).getTime() - new Date(start).getTime()
  return `${(diff / 1000).toFixed(1)}s`
}

onMounted(() => {
  fetchActiveTasks()
  fetchHistory()
  // 轮询获取活跃任务
  pollingTimer = setInterval(fetchActiveTasks, 3000)
})

onUnmounted(() => {
  if (pollingTimer) clearInterval(pollingTimer)
})
</script>

<style scoped>
.mt-4 {
  margin-top: 20px;
}
.mb-4 {
  margin-bottom: 20px;
}
</style>

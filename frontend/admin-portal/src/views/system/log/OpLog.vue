<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-card shadow="never" class="search-container">
      <el-form :model="queryParams" ref="queryFormRef" :inline="true">
        <el-form-item label="模块">
          <el-input v-model="queryParams.module" placeholder="模块名称" clearable style="width: 200px" @keyup.enter="handleQuery" />
        </el-form-item>
        <el-form-item label="操作时间">
          <el-date-picker
            v-model="dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 380px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card shadow="never" class="table-container">
      <el-table 
        v-loading="loading" 
        :data="logList" 
        border 
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" align="center" sortable="custom" />
        <el-table-column prop="module" label="模块" width="120" align="center" />
        <el-table-column prop="action" label="操作" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getActionType(row.action)">{{ row.action }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="admin_username" label="操作人" width="120" align="center" />
        <el-table-column prop="ip_address" label="IP" width="140" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center" sortable="custom">
          <template #default="{ row }">
            <el-tag :type="row.status >= 400 ? 'danger' : 'success'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="耗时(ms)" width="120" align="center" sortable="custom">
          <template #default="{ row }">
            <span :class="{'text-danger': row.duration > 1000}">{{ row.duration ?? '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="180" align="center" sortable="custom">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.page_size"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleQuery"
          @current-change="handleQuery"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailsVisible" title="日志详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="请求方法">{{ currentLog.method }}</el-descriptions-item>
        <el-descriptions-item label="请求路径">{{ currentLog.path }}</el-descriptions-item>
        <el-descriptions-item label="请求参数" :span="2">
          <pre class="json-pre">{{ formatJson(currentLog.params) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="响应结果" :span="2">
          <pre class="json-pre">{{ formatJson(currentLog.result) }}</pre>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import dayjs from 'dayjs'
import SystemAPI, { OperationLog } from '@/api/system-api'

const loading = ref(false)
const total = ref(0)
const logList = ref<OperationLog[]>([])
const dateRange = ref<[string, string] | null>(null)

const queryParams = reactive<{
  page: number
  page_size: number
  module?: string
  start_time?: string
  end_time?: string
  order_by?: string
  order_type?: string
}>({
  page: 1,
  page_size: 20,
  module: undefined,
  start_time: undefined,
  end_time: undefined,
  order_by: 'created_at',
  order_type: 'desc'
})

const getLogList = async () => {
  loading.value = true
  try {
    const params: any = { ...queryParams }
    if (dateRange.value) {
      params.start_time = dateRange.value[0]
      params.end_time = dateRange.value[1]
    } else {
      params.start_time = undefined
      params.end_time = undefined
    }
    const res = await SystemAPI.getLogs(params)
    // 根据 request.ts 的封装，这里 res 是解构后的 data 字段，即 { list, total, ... }
    const data = res as any
    logList.value = data.list
    total.value = data.total
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryParams.page = 1
  getLogList()
}

const resetQuery = () => {
  queryParams.module = undefined
  queryParams.page = 1
  queryParams.order_by = 'created_at'
  queryParams.order_type = 'desc'
  dateRange.value = null
  handleQuery()
}

const handleSortChange = ({ prop, order }: { prop: string, order: string }) => {
  queryParams.order_by = prop
  queryParams.order_type = order === 'ascending' ? 'asc' : 'desc'
  handleQuery()
}

const getActionType = (action: string) => {
  const map: any = {
    login: '',
    create: 'success',
    update: 'warning',
    delete: 'danger'
  }
  return map[action] || 'info'
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

// 详情逻辑
const detailsVisible = ref(false)
const currentLog = ref<any>({})

const viewDetail = (row: OperationLog) => {
  currentLog.value = row
  detailsVisible.value = true
}

const formatJson = (val: string) => {
  if (!val) return '-'
  try {
    return JSON.stringify(JSON.parse(val), null, 2)
  } catch (e) {
    return val
  }
}

onMounted(() => {
  getLogList()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.search-container {
  margin-bottom: 20px;
}
.table-container {
  background: #fff;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.json-pre {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 12px;
  max-height: 300px;
  overflow-y: auto;
}
</style>

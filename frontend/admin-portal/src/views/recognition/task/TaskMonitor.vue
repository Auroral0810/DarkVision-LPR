<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="hover">
      <el-form :inline="true" :model="queryParams" ref="queryFormRef">
        <el-form-item label="任务类型" prop="task_type">
          <el-select v-model="queryParams.task_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="单次识别" value="single" />
            <el-option label="批量识别" value="batch" />
            <el-option label="视频分析" value="video" />
            <el-option label="实时监控" value="realtime" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="queryParams.status" placeholder="任务状态" clearable style="width: 150px">
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item label="用户ID" prop="user_id">
          <el-input v-model="queryParams.user_id" placeholder="用户ID" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-container" shadow="hover" style="margin-top: 20px">
      <el-table v-loading="loading" :data="taskList">
        <el-table-column prop="id" label="ID" width="80" align="center" sortable />
        <el-table-column prop="task_uuid" label="任务UUID" width="180" align="center" show-overflow-tooltip sortable />
        <el-table-column prop="task_type" label="类型" width="100" align="center" sortable>
          <template #default="scope">
            <el-tag>{{ getTaskTypeText(scope.row.task_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center" sortable>
          <template #default="scope">
            <el-tag :type="getStatusTag(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="180" align="center">
          <template #default="scope">
            <el-progress 
              :percentage="Number(scope.row.progress)" 
              :status="scope.row.status === 'failed' ? 'exception' : (scope.row.status === 'completed' ? 'success' : '')"
            />
          </template>
        </el-table-column>
        <el-table-column prop="success_count" label="成功/总数" width="120" align="center" sortable>
          <template #default="scope">
            {{ scope.row.success_count }} / {{ scope.row.total_items }}
          </template>
        </el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100" align="center" sortable />
        <el-table-column prop="created_at" label="创建时间" width="180" align="center" sortable>
          <template #default="scope">
            {{ formatTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" fixed="right">
          <template #default="scope">
            <el-button
              type="danger"
              link
              icon="Delete"
              @click="handleDelete(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-show="total > 0"
          :total="total"
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.page_size"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="getList"
          @current-change="getList"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTasks, deleteTask, type RecognitionTask } from '@/api/recognition-api'
import dayjs from 'dayjs'

const loading = ref(false)
const total = ref(0)
const taskList = ref<RecognitionTask[]>([])

const queryParams = reactive({
  page: 1,
  page_size: 20,
  task_type: undefined,
  status: undefined,
  user_id: undefined
})

const getList = async () => {
  loading.value = true
  try {
    const res: any = await getTasks(queryParams)
    taskList.value = res.list
    total.value = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryParams.page = 1
  getList()
}

const resetQuery = () => {
  queryParams.task_type = undefined
  queryParams.status = undefined
  queryParams.user_id = undefined
  handleQuery()
}

const handleDelete = (row: RecognitionTask) => {
  ElMessageBox.confirm('是否确认删除该任务及其所有关联记录？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await deleteTask(row.id)
    ElMessage.success('删除成功')
    getList()
  }).catch(() => {})
}

const getTaskTypeText = (type: string) => {
  const map: any = {
    'single': '单次识别',
    'batch': '批量识别',
    'video': '视频分析',
    'realtime': '实时监控'
  }
  return map[type] || type
}

const getStatusText = (status: string) => {
  const map: any = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'failed': '失败'
  }
  return map[status] || status
}

const getStatusTag = (status: string): any => {
  switch (status) {
    case 'pending': return 'info'
    case 'processing': return 'primary'
    case 'completed': return 'success'
    case 'failed': return 'danger'
    default: return 'info'
  }
}

const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  return dayjs(timeStr).format('YYYY-MM-DD HH:mm:ss')
}

onMounted(() => {
  getList()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

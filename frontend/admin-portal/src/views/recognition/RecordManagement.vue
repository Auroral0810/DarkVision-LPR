<template>
  <div class="app-container">
    <!-- 搜索区 -->
    <div class="search-container">
      <el-form :model="queryParams" :inline="true">
        <el-form-item label="用户ID">
          <el-input v-model="queryParams.user_id" placeholder="输入用户ID" clearable />
        </el-form-item>
        <el-form-item label="车牌号">
          <el-input v-model="queryParams.keyword" placeholder="车牌号搜索" clearable />
        </el-form-item>
        <el-form-item label="识别时间">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="~"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card>
      <div class="data-table__toolbar">
        <div>
          <el-button type="danger" icon="Delete" :disabled="!hasSelection" @click="handleBatchDelete">
            批量删除
          </el-button>
          <el-button icon="Download" @click="handleExport">导出记录</el-button>
        </div>
      </div>

      <el-table :data="pageData" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" />
        <el-table-column label="ID" prop="id" width="80" />
        <el-table-column label="原图" width="120">
          <template #default="scope">
            <el-image
              :src="scope.row.original_image_url"
              style="width: 100px; height: 60px"
              fit="cover"
              :preview-src-list="[scope.row.original_image_url, scope.row.enhanced_image_url].filter(Boolean)"
            />
          </template>
        </el-table-column>
        <el-table-column label="车牌号" prop="license_plate" width="140">
          <template #default="scope">
            <span style="font-weight: 600; font-family: monospace">{{ scope.row.license_plate }}</span>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="100">
          <template #default="scope">
            <el-tag :type="getPlateTypeColor(scope.row.plate_type)">
              {{ getPlateTypeLabel(scope.row.plate_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="置信度" width="120">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.confidence"
              :color="getConfidenceColor(scope.row.confidence)"
            />
          </template>
        </el-table-column>
        <el-table-column label="耗时" width="100">
          <template #default="scope">{{ scope.row.processing_time_ms }}ms</template>
        </el-table-column>
        <el-table-column label="识别时间" prop="created_at" width="160" />
        <el-table-column label="质量审核" width="150">
          <template #default="scope">
            <template v-if="scope.row.is_correct === null">
              <el-button type="success" link size="small" @click="handleAudit(scope.row.id, true)">
                正确
              </el-button>
              <el-button type="danger" link size="small" @click="handleAudit(scope.row.id, false)">
                错误
              </el-button>
            </template>
            <el-tag v-else :type="scope.row.is_correct ? 'success' : 'danger'">
              {{ scope.row.is_correct ? '已确认正确' : '已标记错误' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <pagination
        v-if="total > 0"
        v-model:total="total"
        v-model:page="queryParams.page"
        v-model:limit="queryParams.pageSize"
        @pagination="fetchList"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import LprAPI from '@/api/lpr-api'

const queryParams = reactive({ page: 1, pageSize: 10, user_id: '', keyword: '', start_date: '', end_date: '' })
const dateRange = ref([])
const pageData = ref([])
const total = ref(0)
const loading = ref(false)
const selectedIds = ref<number[]>([])
const hasSelection = computed(() => selectedIds.value.length > 0)

async function fetchList() {
  loading.value = true
  try {
    if (dateRange.value?.length === 2) {
      queryParams.start_date = dateRange.value[0]
      queryParams.end_date = dateRange.value[1]
    }
    const data = await LprAPI.getRecognitionList(queryParams)
    pageData.value = data.list
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function handleQuery() {
  queryParams.page = 1
  fetchList()
}

function handleReset() {
  Object.assign(queryParams, { page: 1, pageSize: 10, user_id: '', keyword: '', start_date: '', end_date: '' })
  dateRange.value = []
  fetchList()
}

function handleSelectionChange(selection: any[]) {
  selectedIds.value = selection.map((item) => item.id)
}

async function handleAudit(id: number, isCorrect: boolean) {
  try {
    await LprAPI.auditRecognition(id, isCorrect)
    ElMessage.success('审核成功')
    fetchList()
  } catch (error) {
    ElMessage.error('审核失败')
  }
}

async function handleBatchDelete() {
  ElMessageBox.confirm(`确认删除选中的 ${selectedIds.value.length} 条记录吗？`, '批量删除', {
    type: 'warning'
  })
    .then(async () => {
      try {
        await LprAPI.batchDeleteRecognitions(selectedIds.value)
        ElMessage.success('删除成功')
        fetchList()
      } catch (error) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
}

async function handleExport() {
  try {
    await LprAPI.exportRecognitions(queryParams)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

function getPlateTypeLabel(type: string) {
  const map: Record<string, string> = {
    blue: '蓝牌',
    yellow: '黄牌',
    green: '绿牌',
    new_energy: '新能源',
    other: '其他'
  }
  return map[type] || type
}

function getPlateTypeColor(type: string) {
  const map: Record<string, string> = {
    blue: '',
    yellow: 'warning',
    green: 'success',
    new_energy: 'success',
    other: 'info'
  }
  return map[type] || ''
}

function getConfidenceColor(val: number) {
  if (val >= 90) return '#67c23a'
  if (val >= 75) return '#e6a23c'
  return '#f56c6c'
}

onMounted(() => {
  fetchList()
})
</script>

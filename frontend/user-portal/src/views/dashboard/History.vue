<template>
  <div class="history-view">
    <div class="view-header">
      <div class="header-left">
        <h2>{{ t.title }}</h2>
        <p class="subtitle">{{ t.subtitle }}</p>
      </div>
      <div class="header-right">
        <el-radio-group v-model="userStore.lang" size="small" @change="userStore.setLang" style="margin-right: 16px;">
          <el-radio-button label="zh-cn">中文</el-radio-button>
          <el-radio-button label="en">EN</el-radio-button>
        </el-radio-group>
        <el-button type="primary" plain icon="Download" v-if="userStore.isVIP">{{ t.export }}</el-button>
      </div>
    </div>

    <div class="filter-card">
      <el-form :inline="true" class="filter-form">
        <el-form-item :label="t.dateRange">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            :range-separator="t.to"
            :start-placeholder="t.startDate"
            :end-placeholder="t.endDate"
            :shortcuts="shortcuts"
            @change="handleFilter"
          />
        </el-form-item>
        <el-form-item :label="t.plateNumber">
          <el-input 
            v-model="searchKeyword" 
            :placeholder="t.searchPlaceholder" 
            prefix-icon="Search"
            clearable
            @keyup.enter="handleFilter"
          />
        </el-form-item>
        <el-form-item :label="t.type">
          <el-select v-model="filterType" :placeholder="t.allTypes" clearable style="width: 120px" @change="handleFilter">
            <el-option label="蓝牌" value="blue" />
            <el-option label="绿牌" value="green" />
            <el-option label="黄牌" value="yellow" />
            <el-option label="白牌" value="white" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">{{ t.query }}</el-button>
          <el-button @click="resetSearch">{{ t.reset }}</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table 
        v-loading="loading"
        :data="tableData" 
        style="width: 100%" 
        class="data-table" 
        :row-class-name="tableRowClassName"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column :label="t.image" width="120">
          <template #default="scope">
            <el-image 
              class="image-preview" 
              :src="scope.row.original_image_url" 
              :preview-src-list="[scope.row.original_image_url]"
              fit="cover"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        
        <el-table-column prop="license_plate" :label="t.plateNumber" min-width="120">
          <template #default="scope">
            <div class="plate-cell">
              <span class="plate-text">{{ scope.row.license_plate }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="plate_type" :label="t.type" width="100">
          <template #default="scope">
            <el-tag :type="getPlateTypeColor(scope.row.plate_type)" effect="light" size="small">
              {{ formatPlateType(scope.row.plate_type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="confidence" :label="t.confidence" width="180">
          <template #default="scope">
            <div class="confidence-bar">
              <span class="val">{{ (scope.row.confidence * 100).toFixed(1) }}%</span>
              <el-progress 
                :percentage="scope.row.confidence * 100" 
                :show-text="false" 
                :color="getConfidenceColor(scope.row.confidence * 100)"
                :stroke-width="6"
              />
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" :label="t.time" width="180" sortable>
          <template #default="scope">
            <span class="time-text">{{ formatDate(scope.row.created_at) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column :label="t.actions" width="150" fixed="right">
          <template #default="scope">
            <el-button link type="primary" size="small" @click="handleShowDetail(scope.row)">{{ t.detail }}</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(scope.row)">{{ t.delete }}</el-button>
          </template>
        </el-table-column>
        
        <template #empty>
          <el-empty :description="t.noData" :image-size="100" />
        </template>
      </el-table>
      
      <div class="pagination-footer">
        <div class="selection-info">
          {{ t.selected.replace('{n}', String(selectedRows.length)) }}
        </div>
        <el-pagination 
          background 
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[5, 10, 20]"
          layout="total, sizes, prev, pager, next, jumper" 
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog 
      v-model="detailVisible" 
      :title="t.detailTitle" 
      width="900px"
      :close-on-click-modal="false"
      class="detail-dialog"
    >
      <div v-if="currentRecord" class="detail-content">
        <div class="detail-images">
          <div class="image-item">
            <div class="image-label">{{ t.originalImage }}</div>
            <div class="image-wrapper">
              <el-image 
                :src="currentRecord.original_image_url" 
                :preview-src-list="[currentRecord.original_image_url]"
                fit="contain"
                class="detail-image"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon :size="50"><Picture /></el-icon>
                    <p>{{ t.imageLoadFailed }}</p>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
          <div class="image-item" v-if="currentRecord.enhanced_image_url">
            <div class="image-label">{{ t.resultImage }}</div>
            <div class="image-wrapper">
              <el-image 
                :src="currentRecord.enhanced_image_url" 
                :preview-src-list="[currentRecord.enhanced_image_url]"
                fit="contain"
                class="detail-image"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon :size="50"><Picture /></el-icon>
                    <p>{{ t.imageLoadFailed }}</p>
                  </div>
                </template>
              </el-image>
            </div>
          </div>
        </div>
        
        <el-descriptions :column="2" border class="detail-info">
          <el-descriptions-item :label="t.plateNumber">
            <span class="plate-number-large">{{ currentRecord.license_plate }}</span>
          </el-descriptions-item>
          <el-descriptions-item :label="t.type">
            <el-tag :type="getPlateTypeColor(currentRecord.plate_type)" effect="light">
              {{ formatPlateType(currentRecord.plate_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item :label="t.confidence">
            <div class="confidence-detail">
              <span class="confidence-value">{{ (currentRecord.confidence * 100).toFixed(2) }}%</span>
              <el-progress 
                :percentage="currentRecord.confidence * 100" 
                :color="getConfidenceColor(currentRecord.confidence * 100)"
                :stroke-width="8"
                style="margin-top: 8px;"
              />
            </div>
          </el-descriptions-item>
          <el-descriptions-item :label="t.time">
            {{ formatDate(currentRecord.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item :label="t.recordId" v-if="currentRecord.id">
            {{ currentRecord.id }}
          </el-descriptions-item>
          <el-descriptions-item :label="t.taskId" v-if="currentRecord.task_id">
            {{ currentRecord.task_id }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">{{ t.close }}</el-button>
        <el-button type="danger" @click="handleDeleteFromDetail">{{ t.delete }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { Search, Picture, Download } from '@element-plus/icons-vue'
import { getRecognitionHistory } from '@/api/history'
import { ElMessageBox, ElMessage } from 'element-plus'

const userStore = useUserStore()

// Localization
const locales = {
  'zh-cn': {
    title: '识别历史',
    subtitle: '查看和管理您的所有识别记录',
    export: '导出数据',
    dateRange: '日期范围',
    to: '至',
    startDate: '开始日期',
    endDate: '结束日期',
    plateNumber: '车牌号码',
    searchPlaceholder: '输入车牌号搜索',
    type: '类型',
    allTypes: '全部类型',
    query: '查询',
    reset: '重置',
    image: '原图',
    confidence: '置信度',
    time: '识别时间',
    actions: '操作',
    detail: '详情',
    delete: '删除',
    noData: '暂无识别记录',
    selected: '已选择 {n} 项',
    lastWeek: '最近一周',
    lastMonth: '最近一月',
    lastYear: '最近一年',
    detailTitle: '识别详情',
    originalImage: '原始图片',
    resultImage: '识别结果图',
    imageLoadFailed: '图片加载失败',
    recordId: '记录ID',
    taskId: '任务ID',
    close: '关闭'
  },
  'en': {
    title: 'History',
    subtitle: 'View and manage your recognition records',
    export: 'Export Data',
    dateRange: 'Date Range',
    to: 'To',
    startDate: 'Start Date',
    endDate: 'End Date',
    plateNumber: 'Plate Number',
    searchPlaceholder: 'Search plate number',
    type: 'Type',
    allTypes: 'All Types',
    query: 'Query',
    reset: 'Reset',
    image: 'Original',
    confidence: 'Confidence',
    time: 'Time',
    actions: 'Actions',
    detail: 'Detail',
    delete: 'Delete',
    noData: 'No Records Found',
    selected: 'Selected {n} items',
    lastWeek: 'Last Week',
    lastMonth: 'Last Month',
    lastYear: 'Last Year',
    detailTitle: 'Recognition Detail',
    originalImage: 'Original Image',
    resultImage: 'Result Image',
    imageLoadFailed: 'Failed to load image',
    recordId: 'Record ID',
    taskId: 'Task ID',
    close: 'Close'
  }
}

const t = computed(() => locales[userStore.lang as keyof typeof locales])

// Data Handling
const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dateRange = ref<any>([])
const searchKeyword = ref('')
const filterType = ref('')
const selectedRows = ref<any[]>([])
const detailVisible = ref(false)
const currentRecord = ref<any>(null)

const shortcuts = computed(() => [
  { text: t.value.lastWeek, value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 7); return [start, end] } },
  { text: t.value.lastMonth, value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 30); return [start, end] } },
  { text: t.value.lastYear, value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 365); return [start, end] } },
])

const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }
    if (searchKeyword.value) params.license_plate = searchKeyword.value
    if (filterType.value) params.plate_type = filterType.value
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0].toISOString()
      params.end_date = dateRange.value[1].toISOString()
    }
    
    const res = await getRecognitionHistory(params) as any
    if (res.code === 20000) {
      tableData.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    console.error('Fetch history error:', error)
    ElMessage.error(userStore.lang === 'zh-cn' ? '获取历史记录失败' : 'Failed to fetch history')
  } finally {
    loading.value = false
  }
}

const handleFilter = () => {
  currentPage.value = 1
  fetchData()
}

const resetSearch = () => {
  dateRange.value = []
  searchKeyword.value = ''
  filterType.value = ''
  currentPage.value = 1
  fetchData()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchData()
}

const handleSelectionChange = (val: any) => {
  selectedRows.value = val
}

const handleDelete = (row: any) => {
  const msg = userStore.lang === 'zh-cn' 
    ? `确定要删除车牌 ${row.license_plate} 的记录吗？` 
    : `Are you sure to delete the record for ${row.license_plate}?`
  ElMessageBox.confirm(
    msg,
    userStore.lang === 'zh-cn' ? '提示' : 'Warning',
    {
      confirmButtonText: userStore.lang === 'zh-cn' ? '确定' : 'Confirm',
      cancelButtonText: userStore.lang === 'zh-cn' ? '取消' : 'Cancel',
      type: 'warning',
    }
  ).then(() => {
    ElMessage.success(userStore.lang === 'zh-cn' ? '删除成功' : 'Delete successfully')
    // TODO: Implement real delete call
  }).catch(() => {})
}

const handleShowDetail = (row: any) => {
  currentRecord.value = row
  detailVisible.value = true
}

const handleDeleteFromDetail = () => {
  if (!currentRecord.value) return
  
  const msg = userStore.lang === 'zh-cn' 
    ? `确定要删除车牌 ${currentRecord.value.license_plate} 的记录吗？` 
    : `Are you sure to delete the record for ${currentRecord.value.license_plate}?`
  
  ElMessageBox.confirm(
    msg,
    userStore.lang === 'zh-cn' ? '提示' : 'Warning',
    {
      confirmButtonText: userStore.lang === 'zh-cn' ? '确定' : 'Confirm',
      cancelButtonText: userStore.lang === 'zh-cn' ? '取消' : 'Cancel',
      type: 'warning',
    }
  ).then(() => {
    detailVisible.value = false
    ElMessage.success(userStore.lang === 'zh-cn' ? '删除成功' : 'Delete successfully')
    // TODO: Implement real delete call
  }).catch(() => {})
}

const getPlateTypeColor = (type: string) => {
  switch (type) {
    case 'blue': return ''
    case 'green': return 'success'
    case 'yellow': return 'warning'
    case 'white': return 'info'
    default: return 'info'
  }
}

const formatPlateType = (type: string) => {
  const map: any = {
    'blue': '蓝牌',
    'green': '绿牌',
    'yellow': '黄牌',
    'white': '白牌',
    'other': '其他'
  }
  return map[type] || type
}

const getConfidenceColor = (val: number) => {
  if (val >= 90) return '#10b981'
  if (val >= 80) return '#f59e0b'
  return '#ef4444'
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString(userStore.lang === 'zh-cn' ? 'zh-CN' : 'en-US')
}

const tableRowClassName = () => ''

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.history-view {
  width: 100%;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  h2 { margin: 0 0 8px; font-size: 24px; color: #0f172a; }
  .subtitle { margin: 0; color: #64748b; }
}

.filter-card {
  background: white;
  padding: 24px 24px 0;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  margin-bottom: 24px;
}

.table-container {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.data-table {
  :deep(.el-table__header) {
    th {
      background: #f8fafc;
      color: #64748b;
      font-weight: 600;
      height: 50px;
    }
  }
  
  :deep(.el-table__row) {
    td { padding: 12px 0; }
  }
}

.image-preview {
  width: 80px;
  height: 50px;
  background: #f1f5f9;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    transform: scale(1.05);
  }
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-placeholder);
}

.plate-text {
  font-family: monospace;
  font-weight: 700;
  font-size: 15px;
  color: #0f172a;
}

.confidence-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  
  .val {
    width: 48px;
    font-size: 13px;
    color: #64748b;
    font-family: monospace;
  }
  
  .el-progress {
    flex: 1;
  }
}

.time-text {
  color: #64748b;
  font-size: 13px;
}

.pagination-footer {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e2e8f0;
  
  .selection-info {
    color: #64748b;
    font-size: 13px;
  }
}

:deep(.detail-dialog) {
  .el-dialog__body {
    max-height: 80vh;
    overflow-y: auto;
  }
}

.detail-content {
  .detail-images {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
    
    .image-item {
      .image-label {
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 12px;
        font-size: 14px;
      }
      
      .image-wrapper {
        width: 100%;
        min-height: 200px;
        max-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f8fafc;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        position: relative;
      }
      
      .detail-image {
        width: 100%;
        height: auto;
        max-height: 500px;
        
        :deep(.el-image__inner) {
          width: 100% !important;
          height: auto !important;
          max-height: 500px;
          object-fit: contain;
        }
        
        :deep(.el-image__wrapper) {
          width: 100% !important;
          height: auto !important;
        }
      }
      
      .image-error {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 200px;
        background: #f8fafc;
        border-radius: 8px;
        color: #94a3b8;
        
        p {
          margin-top: 12px;
          font-size: 14px;
        }
      }
    }
  }
  
  .detail-info {
    margin-top: 24px;
    
    .plate-number-large {
      font-family: monospace;
      font-weight: 700;
      font-size: 20px;
      color: #0f172a;
    }
    
    .confidence-detail {
      .confidence-value {
        font-weight: 600;
        font-size: 16px;
        color: #0f172a;
      }
    }
  }
}
</style>
<template>
  <div class="history-view">
    <div class="view-header">
      <div class="header-left">
        <h2>识别历史</h2>
        <p class="subtitle">查看和管理您的所有识别记录</p>
      </div>
      <div class="header-right">
        <el-button type="primary" plain icon="Download" v-if="userStore.isVIP">导出数据</el-button>
      </div>
    </div>

    <div class="filter-card">
      <el-form :inline="true" class="filter-form">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :shortcuts="shortcuts"
          />
        </el-form-item>
        <el-form-item label="车牌号">
          <el-input v-model="searchKeyword" placeholder="输入车牌号搜索" prefix-icon="Search" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="filterType" placeholder="全部类型" clearable style="width: 120px">
            <el-option label="蓝牌" value="blue" />
            <el-option label="绿牌" value="green" />
            <el-option label="黄牌" value="yellow" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="tableData" style="width: 100%" class="data-table" :row-class-name="tableRowClassName">
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="原图" width="120">
          <template #default>
            <div class="image-preview">
              <el-icon><Picture /></el-icon>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="plate" label="车牌号码" min-width="120">
          <template #default="scope">
            <div class="plate-cell">
              <span class="plate-text">{{ scope.row.plate }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag :type="getPlateTypeColor(scope.row.type)" effect="light" size="small">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="confidence" label="置信度" width="180">
          <template #default="scope">
            <div class="confidence-bar">
              <span class="val">{{ scope.row.confidence }}%</span>
              <el-progress 
                :percentage="scope.row.confidence" 
                :show-text="false" 
                :color="getConfidenceColor(scope.row.confidence)"
                :stroke-width="6"
              />
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="date" label="识别时间" width="180" sortable>
          <template #default="scope">
            <span class="time-text">{{ scope.row.date }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" fixed="right">
          <template #default>
            <el-button link type="primary" size="small">详情</el-button>
            <el-button link type="primary" size="small">下载</el-button>
            <el-button link type="danger" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-footer">
        <div class="selection-info">
          已选择 0 项
        </div>
        <el-pagination 
          background 
          layout="prev, pager, next, jumper" 
          :total="100" 
          :page-size="10"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { Search, Picture, Download } from '@element-plus/icons-vue'

const userStore = useUserStore()

const dateRange = ref('')
const searchKeyword = ref('')
const filterType = ref('')

const shortcuts = [
  { text: '最近一周', value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 7); return [start, end] } },
  { text: '最近一月', value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 30); return [start, end] } },
]

const tableData = [
  { date: '2026-01-04 14:23:01', plate: '京A·88888', type: '蓝牌', confidence: 99.2 },
  { date: '2026-01-04 14:20:15', plate: '沪C·12345', type: '蓝牌', confidence: 95.5 },
  { date: '2026-01-04 13:55:42', plate: '苏E·67890', type: '绿牌', confidence: 98.1 },
  { date: '2026-01-04 12:30:11', plate: '浙B·54321', type: '黄牌', confidence: 88.4 },
  { date: '2026-01-04 11:15:33', plate: '粤A·00001', type: '蓝牌', confidence: 99.9 },
]

const getPlateTypeColor = (type: string) => {
  if (type === '蓝牌') return ''
  if (type === '绿牌') return 'success'
  if (type === '黄牌') return 'warning'
  return 'info'
}

const getConfidenceColor = (val: number) => {
  if (val >= 90) return '#10b981'
  if (val >= 80) return '#f59e0b'
  return '#ef4444'
}

const handleSearch = () => { console.log('Search') }
const resetSearch = () => { dateRange.value = ''; searchKeyword.value = ''; filterType.value = '' }
const tableRowClassName = () => '' // Helper
</script>

<style scoped lang="scss">
.history-view {
  max-width: 1200px;
  margin: 0 auto;
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
    td { padding: 16px 0; }
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
    background: #e2e8f0;
    color: #94a3b8;
  }
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
</style>
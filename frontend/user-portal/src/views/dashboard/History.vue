<template>
  <div class="history-view">
    <div class="filter-bar">
      <el-form :inline="true">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item label="车牌号">
          <el-input v-model="searchKeyword" placeholder="请输入车牌号" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="date" label="识别时间" width="180" />
      <el-table-column prop="plate" label="车牌号码" width="150" />
      <el-table-column prop="type" label="类型" width="120" />
      <el-table-column prop="confidence" label="置信度" width="120">
        <template #default="scope">
          <el-tag :type="scope.row.confidence > 90 ? 'success' : 'warning'">
            {{ scope.row.confidence }}%
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="image" label="缩略图" width="120">
        <template #default>
          <div class="thumbnail">原图</div>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default>
          <el-button link type="primary" size="small">查看详情</el-button>
          <el-button link type="danger" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div class="pagination">
      <el-pagination background layout="prev, pager, next" :total="100" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const dateRange = ref('')
const searchKeyword = ref('')

const tableData = [
  { date: '2026-01-04 14:23:01', plate: '京A·88888', type: '蓝牌', confidence: 99.2 },
  { date: '2026-01-04 14:20:15', plate: '沪C·12345', type: '蓝牌', confidence: 95.5 },
  { date: '2026-01-04 13:55:42', plate: '苏E·67890', type: '绿牌', confidence: 98.1 },
  { date: '2026-01-04 12:30:11', plate: '浙B·54321', type: '黄牌', confidence: 88.4 },
]

const handleSearch = () => {
  console.log('Search triggered')
}
</script>

<style scoped lang="scss">
.history-view {
  background: white;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.filter-bar {
  margin-bottom: 24px;
}

.thumbnail {
  width: 60px;
  height: 40px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #94a3b8;
  border-radius: 4px;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}
</style>

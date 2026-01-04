<template>
  <div class="app-container">
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>用户增长分析</span>
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="7d">近7天</el-radio-button>
            <el-radio-button label="30d">近30天</el-radio-button>
            <el-radio-button label="90d">近90天</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div style="height: 400px; display: flex; align-items: center; justify-content: center; color: #999;">
        [ ECharts: 用户每日增长曲线图 ]
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header><span>用户地域分布</span></template>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999;">
            [ ECharts: 中国地图分布 ]
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><span>用户留存分析</span></template>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999;">
            [ ECharts: 留存率热力图 ]
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const timeRange = ref('7d')
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.mb-4 {
  margin-bottom: 20px;
}
</style>

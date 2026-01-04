<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6" v-for="item in resourceStats" :key="item.name">
        <el-card shadow="hover" class="status-card">
          <div class="card-content">
            <div class="label">{{ item.name }}</div>
            <div class="value">{{ item.value }}{{ item.unit }}</div>
            <el-progress :percentage="item.percentage" :color="getProgressColor(item.percentage)" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card>
          <template #header><span>GPU 使用率 (推理服务)</span></template>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999;">
            [ ECharts: GPU 多核负载曲线 ]
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header><span>接口响应时间 (P99)</span></template>
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999;">
            [ ECharts: API Latency 柱状图 ]
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="mt-4">
      <template #header><span>Redis & 数据库状态</span></template>
      <el-descriptions border :column="3">
        <el-descriptions-item label="Redis 命中率">94.2%</el-descriptions-item>
        <el-descriptions-item label="数据库连接数">42 / 100</el-descriptions-item>
        <el-descriptions-item label="慢查询数量 (24h)">3</el-descriptions-item>
        <el-descriptions-item label="应用版本">v1.2.4-build082</el-descriptions-item>
        <el-descriptions-item label="系统运行时间">12天 4小时</el-descriptions-item>
        <el-descriptions-item label="健康状态"><el-tag type="success">Excellent</el-tag></el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
const resourceStats = ref([
  { name: 'CPU 使用率', value: 24, unit: '%', percentage: 24 },
  { name: '内存 使用率', value: 3.2, unit: 'GB', percentage: 40 },
  { name: 'GPU 显存', value: 1.8, unit: 'GB', percentage: 22 },
  { name: '磁盘 占用', value: 156, unit: 'GB', percentage: 15 }
])

function getProgressColor(p: number) {
  if (p > 90) return '#F56C6C'
  if (p > 70) return '#E6A23C'
  return '#67C23A'
}
</script>

<style scoped>
.status-card { text-align: center; }
.card-content .label { font-size: 14px; color: #666; margin-bottom: 8px; }
.card-content .value { font-size: 24px; font-weight: bold; margin-bottom: 12px; }
.mt-4 { margin-top: 20px; }
</style>

<template>
  <div class="app-container">
    <!-- KPI 卡片 -->
    <el-row :gutter="20" class="mb-4">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover">
          <el-statistic title="总用户数" :value="stats.total_users">
            <template #suffix>人</template>
          </el-statistic>
          <div class="trend">今日新增: +{{ stats.today_registrations }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover">
          <el-statistic title="总识别量" :value="stats.total_recognitions">
            <template #suffix>次</template>
          </el-statistic>
          <div class="trend">今日: +{{ stats.today_recognitions }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover">
          <el-statistic title="总收入" :value="stats.total_revenue" :precision="2">
            <template #prefix>¥</template>
          </el-statistic>
          <div class="trend">今日: +¥{{ stats.today_revenue }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover">
          <el-statistic title="活跃用户(30天)" :value="stats.active_users_30d">
            <template #suffix>人</template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card title="用户注册趋势">
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999">
            图表占位 - 用户注册趋势折线图
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card title="识别量趋势">
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999">
            图表占位 - 识别量趋势折线图
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card title="用户类型分布">
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999">
            图表占位 - 用户类型饼图
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card title="车牌类型分布">
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; color: #999">
            图表占位 - 车牌类型饼图
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LprAPI from '@/api/lpr-api'
import type { DashboardStats } from '@/types/lpr'

defineOptions({ name: 'AnalyticsOverview' })

const stats = ref<DashboardStats>({
  total_users: 0,
  today_registrations: 0,
  total_recognitions: 0,
  today_recognitions: 0,
  total_revenue: 0,
  today_revenue: 0,
  active_users_30d: 0
})

async function fetchStats() {
  try {
    stats.value = await LprAPI.getDashboardStats()
  } catch (error) {
    console.error('获取统计数据失败', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.trend {
  margin-top: 10px;
  font-size: 14px;
  color: #67c23a;
}
.mt-4 {
  margin-top: 20px;
}
.mb-4 {
  margin-bottom: 20px;
}
</style>

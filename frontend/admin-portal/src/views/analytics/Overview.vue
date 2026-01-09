<template>
  <div class="app-container">
    <!-- KPI 卡片 -->
    <el-row :gutter="20" class="mb-5">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover" class="kpi-card">
          <div class="kpi-icon user-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="kpi-info">
            <el-statistic title="总用户数" :value="stats.total_users" />
            <div class="kpi-trend">今日新增: <span class="trend-up">+{{ stats.today_registrations }}</span></div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover" class="kpi-card">
          <div class="kpi-icon recog-icon">
            <el-icon><View /></el-icon>
          </div>
          <div class="kpi-info">
            <el-statistic title="总识别量" :value="stats.total_recognitions" />
            <div class="kpi-trend">今日识别: <span class="trend-up">+{{ stats.today_recognitions }}</span></div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover" class="kpi-card">
          <div class="kpi-icon revenue-icon">
            <el-icon><Money /></el-icon>
          </div>
          <div class="kpi-info">
            <el-statistic title="总收入" :value="stats.total_revenue" :precision="2">
              <template #prefix>¥</template>
            </el-statistic>
            <div class="kpi-trend">今日收入: <span class="trend-up">+¥{{ stats.today_revenue }}</span></div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="hover" class="kpi-card">
          <div class="kpi-icon active-icon">
            <el-icon><Histogram /></el-icon>
          </div>
          <div class="kpi-info">
            <el-statistic title="活跃用户(30天)" :value="stats.active_users_30d" />
            <div class="kpi-trend">保持活跃提高留存</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 趋势图表区 -->
    <el-row :gutter="20" class="mb-5">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户注册趋势</span>
              <el-tag type="info" effect="plain">最近7天</el-tag>
            </div>
          </template>
          <ECharts :options="userTrendOption" height="350px" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>识别量趋势</span>
              <el-tag type="info" effect="plain">最近7天</el-tag>
            </div>
          </template>
          <ECharts :options="recogTrendOption" height="350px" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 分布图表区 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户类型分布</span>
            </div>
          </template>
          <ECharts :options="userTypeOption" height="350px" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>车牌类型分布</span>
            </div>
          </template>
          <ECharts :options="plateTypeOption" height="350px" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { User, View, Money, Histogram } from '@element-plus/icons-vue'
import LprAPI from '@/api/lpr-api'
import type { DashboardStats, UserTrendData, RecognitionTrendData } from '@/types/lpr'
import ECharts from '@/components/ECharts/index.vue'

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

// 图表配置
const userTrendOption = reactive({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', boundaryGap: false, data: [] as string[] },
  yAxis: { type: 'value' },
  series: [{
    name: '新增用户',
    type: 'line',
    smooth: true,
    showSymbol: false,
    areaStyle: {
      color: {
        type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [{ offset: 0, color: 'rgba(64, 158, 255, 0.3)' }, { offset: 1, color: 'rgba(64, 158, 255, 0)' }]
      }
    },
    itemStyle: { color: '#409eff' },
    data: [] as number[]
  }]
})

const recogTrendOption = reactive({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', boundaryGap: false, data: [] as string[] },
  yAxis: { type: 'value' },
  series: [{
    name: '识别次数',
    type: 'line',
    smooth: true,
    showSymbol: false,
    itemStyle: { color: '#67c23a' },
    areaStyle: {
      color: {
        type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [{ offset: 0, color: 'rgba(103, 194, 58, 0.3)' }, { offset: 1, color: 'rgba(103, 194, 58, 0)' }]
      }
    },
    data: [] as number[]
  }]
})

const userTypeOption = reactive({
  tooltip: { trigger: 'item' },
  legend: { bottom: '5%', left: 'center' },
  series: [{
    name: '用户类型',
    type: 'pie',
    radius: ['40%', '70%'],
    avoidLabelOverlap: false,
    itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
    label: { show: false, position: 'center' },
    emphasis: { label: { show: true, fontSize: '20', fontWeight: 'bold' } },
    labelLine: { show: false },
    data: [] as any[]
  }]
})

const plateTypeOption = reactive({
  tooltip: { trigger: 'item' },
  legend: { bottom: '5%', left: 'center' },
  series: [{
    name: '车牌类型',
    type: 'pie',
    radius: ['40%', '70%'],
    itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
    data: [] as any[]
  }]
})

async function fetchAllData() {
  try {
    // 1. 获取核心统计
    const resStats = await LprAPI.getDashboardStats()
    stats.value = resStats

    // 2. 获取用户趋势 (近7天)
    const end = new Date()
    const start = new Date()
    start.setDate(start.getDate() - 6)
    const userTrends = await LprAPI.getUserTrend({ 
      start_date: start.toISOString().split('T')[0], 
      end_date: end.toISOString().split('T')[0] 
    })
    userTrendOption.xAxis.data = userTrends.map(item => item.date.slice(5))
    userTrendOption.series[0].data = userTrends.map(item => item.count)

    // 3. 获取识别趋势
    const recogTrends = await LprAPI.getRecognitionTrend({
      start_date: start.toISOString().split('T')[0],
      end_date: end.toISOString().split('T')[0]
    })
    recogTrendOption.xAxis.data = recogTrends.map(item => item.date.slice(5))
    recogTrendOption.series[0].data = recogTrends.map(item => item.total)

    // 4. 用户分布
    const userDist = await LprAPI.getUserTypeDistribution()
    const userTypeNames: any = { 
      'free': '免费用户', 'UserType.FREE': '免费用户',
      'vip': 'VIP用户', 'UserType.VIP': 'VIP用户',
      'enterprise': '企业用户', 'UserType.ENTERPRISE': '企业用户',
      'admin': '管理员', 'UserType.ADMIN': '管理员'
    }
    userTypeOption.series[0].data = userDist.map(item => ({
      name: userTypeNames[item.user_type] || '其他',
      value: item.count
    }))

    // 5. 车牌分布
    const plateDist = await LprAPI.getPlateTypeDistribution()
    const plateNames: any = { 
      'blue': '蓝牌', 'yellow': '黄牌', 'green': '绿牌', 'white': '白牌', 'other': '其他',
      'unknown': '未知'
    }
    plateTypeOption.series[0].data = plateDist.map(item => ({
      name: plateNames[item.plate_type] || item.plate_type || '其他',
      value: item.count
    }))
  } catch (error) {
    console.error('获取统计数据失败', error)
  }
}

onMounted(() => {
  fetchAllData()
})
</script>

<style scoped>
.mb-5 {
  margin-bottom: 24px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.kpi-card {
  display: flex;
  align-items: center;
  padding: 10px;
}
:deep(.el-card__body) {
  width: 100%;
  display: flex;
  align-items: center;
}
.kpi-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-right: 20px;
  flex-shrink: 0;
}
.user-icon { background: rgba(64, 158, 255, 0.1); color: #409eff; }
.recog-icon { background: rgba(103, 194, 58, 0.1); color: #67c23a; }
.revenue-icon { background: rgba(230, 162, 60, 0.1); color: #e6a23c; }
.active-icon { background: rgba(144, 147, 153, 0.1); color: #909399; }

.kpi-info {
  flex-grow: 1;
}
.kpi-trend {
  margin-top: 5px;
  font-size: 13px;
  color: #909399;
}
.trend-up {
  color: #67c23a;
  font-weight: bold;
}
</style>

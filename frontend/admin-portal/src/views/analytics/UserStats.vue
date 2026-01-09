<template>
  <div class="app-container">
    <el-card class="mb-4 shadow-sm">
      <template #header>
        <div class="card-header">
          <span class="title-with-icon">
            <el-icon><TrendCharts /></el-icon> 用户增长分析
          </span>
          <el-radio-group v-model="timeRange" size="small" @change="fetchGrowthData">
            <el-radio-button label="7d">近7天</el-radio-button>
            <el-radio-button label="30d">近30天</el-radio-button>
            <el-radio-button label="90d">近90天</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <ECharts :options="growthOption" height="400px" />
    </el-card>

    <el-row :gutter="20">
      <el-col :span="10">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户等级分布</span>
            </div>
          </template>
          <ECharts :options="typeDistOption" height="400px" />
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户 24/7 活跃度分析 (30天)</span>
            </div>
          </template>
          <ECharts :options="activityOption" height="400px" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'
import ECharts from '@/components/ECharts/index.vue'
import LprAPI from '@/api/lpr-api'

const timeRange = ref('7d')

const hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', '10a', '11a', '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p']
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const growthOption = reactive({
  tooltip: { trigger: 'axis' },
  legend: { data: ['累计用户', '新增用户'], bottom: 0 },
  grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
  xAxis: { type: 'category', boundaryGap: false, data: [] as string[] },
  yAxis: { type: 'value' },
  series: [
    {
      name: '新增用户',
      type: 'bar',
      barWidth: '40%',
      itemStyle: { color: '#409eff', borderRadius: [4, 4, 0, 0] },
      data: [] as number[]
    },
    {
      name: '累计用户',
      type: 'line',
      smooth: true,
      itemStyle: { color: '#f56c6c' },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(245, 108, 108, 0.2)' }, { offset: 1, color: 'rgba(245, 108, 108, 0)' }]
        }
      },
      data: [] as number[]
    }
  ]
})

const typeDistOption = reactive({
  tooltip: { trigger: 'item' },
  legend: { bottom: '5%', left: 'center' },
  series: [{
    type: 'pie',
    radius: ['45%', '70%'],
    center: ['50%', '45%'],
    roseType: 'area',
    itemStyle: { borderRadius: 8 },
    data: [] as any[]
  }]
})

const activityOption = reactive({
  tooltip: { position: 'top' },
  grid: { height: '70%', top: '10%' },
  xAxis: { type: 'category', data: hours, splitArea: { show: true } },
  yAxis: { type: 'category', data: days, splitArea: { show: true } },
  visualMap: {
    min: 0,
    max: 10,
    calculable: true,
    orient: 'horizontal',
    left: 'center',
    bottom: '5%',
    inRange: { color: ['rgba(64, 158, 255, 0.1)', '#409eff'] }
  },
  series: [{
    name: '活跃密度',
    type: 'heatmap',
    data: [] as any[],
    label: { show: false },
    emphasis: {
      itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' }
    }
  }]
})

async function fetchGrowthData() {
  const daysNum = timeRange.value === '7d' ? 7 : timeRange.value === '30d' ? 30 : 90
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - (daysNum - 1))
  
  try {
    const trends = await LprAPI.getUserTrend({
      start_date: start.toISOString().split('T')[0],
      end_date: end.toISOString().split('T')[0]
    })
    
    growthOption.xAxis.data = trends.map(t => t.date.slice(5))
    growthOption.series[0].data = trends.map(t => t.count)
    
    let total = 0
    growthOption.series[1].data = trends.map(t => {
      total += t.count
      return total
    })
  } catch (error) {
    console.error('获取增长数据失败', error)
  }
}

async function fetchTypeDist() {
  try {
    const dist = await LprAPI.getUserTypeDistribution()
    const names: any = { 
      'free': '免费用户', 'UserType.FREE': '免费用户',
      'vip': 'VIP用户', 'UserType.VIP': 'VIP用户',
      'enterprise': '企业用户', 'UserType.ENTERPRISE': '企业用户',
      'admin': '管理员', 'UserType.ADMIN': '管理员'
    }
    typeDistOption.series[0].data = dist.map(item => ({
      name: names[item.user_type] || '其他',
      value: item.count
    }))
  } catch (error) {
    console.error('获取分布数据失败', error)
  }
}

async function fetchActivityHeatmap() {
  try {
    const data = await LprAPI.getUserActivityHeatmap()
    activityOption.series[0].data = data
    const maxVal = Math.max(...data.map(d => d[2]), 1)
    activityOption.visualMap.max = maxVal
  } catch (error) {
    console.error('获取活跃热力图失败', error)
  }
}

onMounted(() => {
  fetchGrowthData()
  fetchTypeDist()
  fetchActivityHeatmap()
})
</script>

<style scoped>
.mb-4 { margin-bottom: 20px; }
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title-with-icon {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}
.empty-chart {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

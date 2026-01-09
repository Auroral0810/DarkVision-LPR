<template>
  <div class="app-container">
    <el-row :gutter="20" class="mb-5">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="平均识别成功率" :value="recogStats.success_rate" :precision="1">
            <template #suffix>
              <span class="unit">%</span>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="平均响应耗时" :value="recogStats.avg_time" :precision="0">
            <template #suffix>
              <span class="unit">ms</span>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="今日并发峰值" :value="recogStats.peak_qps">
            <template #suffix>
              <span class="unit">qps</span>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="mb-5">
      <template #header>
        <div class="card-header">
          <span>识别性能趋势</span>
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="small"
            @change="fetchTrendData"
          />
        </div>
      </template>
      <ECharts :options="perfTrendOption" height="400px" />
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span>异常分析 (Mock)</span></template>
          <ECharts :options="errorPieOption" height="300px" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span>车牌分布详情</span></template>
          <ECharts :options="plateDistOption" height="300px" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import ECharts from '@/components/ECharts/index.vue'
import LprAPI from '@/api/lpr-api'

const recogStats = reactive({
  success_rate: 98.2,
  avg_time: 156,
  peak_qps: 12
})

const dateRange = ref<[Date, Date]>([
  new Date(new Date().setDate(new Date().getDate() - 7)),
  new Date()
])

const perfTrendOption = reactive({
  tooltip: { trigger: 'axis' },
  legend: { data: ['识别总量', '成功率'], top: 10 },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: [] as string[] },
  yAxis: [
    { type: 'value', name: '次数' },
    { type: 'value', name: '成功率', min: 0, max: 100, axisLabel: { formatter: '{value}%' } }
  ],
  series: [
    {
      name: '识别总量',
      type: 'bar',
      barWidth: '40%',
      itemStyle: { color: '#409eff' },
      data: [] as number[]
    },
    {
      name: '成功率',
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      itemStyle: { color: '#67c23a' },
      data: [] as number[]
    }
  ]
})

const errorPieOption = reactive({
  tooltip: { trigger: 'item' },
  series: [{
    type: 'pie',
    radius: '60%',
    data: [
      { value: 65, name: '车牌遮挡' },
      { value: 20, name: '反光干扰' },
      { value: 10, name: '模糊无法识别' },
      { value: 5, name: '其他' }
    ]
  }]
})

const plateDistOption = reactive({
  tooltip: { trigger: 'item' },
  series: [{
    type: 'pie',
    radius: ['45%', '70%'],
    data: [] as any[]
  }]
})

async function fetchTrendData() {
  if (!dateRange.value) return
  
  try {
    const trends = await LprAPI.getRecognitionTrend({
      start_date: dateRange.value[0].toISOString().split('T')[0],
      end_date: dateRange.value[1].toISOString().split('T')[0]
    })
    
    perfTrendOption.xAxis.data = trends.map(t => t.date.slice(5))
    perfTrendOption.series[0].data = trends.map(t => t.count)
    perfTrendOption.series[1].data = trends.map(t => {
      return t.count > 0 ? Math.round((t.success_count / t.count) * 100) : 100
    })
    
    // 汇总 KPI (简单计算)
    const total = trends.reduce((acc, curr) => acc + curr.count, 0)
    const success = trends.reduce((acc, curr) => acc + curr.success_count, 0)
    recogStats.success_rate = total > 0 ? (success / total) * 100 : 100
  } catch (error) {
    console.error('获取识别趋势失败', error)
  }
}

async function fetchPlateDist() {
  try {
    const dist = await LprAPI.getPlateTypeDistribution()
    const names: any = { 
      'blue': '蓝牌', 'yellow': '黄牌', 'green': '绿牌', 'white': '白牌', 'other': '其他',
      'unknown': '未知'
    }
    plateDistOption.series[0].data = dist.map(item => ({
      name: names[item.plate_type] || item.plate_type || '其他',
      value: item.count
    }))
  } catch (error) {
    console.error('获取车牌分布失败', error)
  }
}

onMounted(() => {
  fetchTrendData()
  fetchPlateDist()
})
</script>

<style scoped>
.mb-5 { margin-bottom: 24px; }
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.stat-card {
  text-align: center;
}
.unit {
  font-size: 14px;
  color: #909399;
  margin-left: 4px;
}
</style>

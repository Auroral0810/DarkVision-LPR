<template>
  <div class="analysis-view">
    <!-- VIP Lock Screen -->
    <div class="vip-lock-screen" v-if="!userStore.isVIP">
      <div class="lock-content">
        <div class="icon-box">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <h2>解锁数据分析中心</h2>
        <p>升级到 VIP，获取深度的业务洞察报表，优化您的识别策略。</p>
        <div class="features-preview">
          <div class="preview-item">
            <span class="dot"></span> 识别趋势分析
          </div>
          <div class="preview-item">
            <span class="dot"></span> 车牌类型分布
          </div>
          <div class="preview-item">
            <span class="dot"></span> 高频车辆统计
          </div>
          <div class="preview-item">
            <span class="dot"></span> 导出 PDF 报告
          </div>
        </div>
        <el-button type="primary" size="large" round class="upgrade-btn">
          升级解锁
        </el-button>
      </div>
    </div>

    <!-- Actual Content for VIPs -->
    <div class="analysis-content" v-else>
      <div class="view-header">
        <div class="header-left">
          <h2>数据分析</h2>
          <p class="subtitle">您的识别数据深度洞察</p>
        </div>
        <div class="header-actions">
          <el-radio-group v-model="timeRange" size="small">
            <el-radio-button label="week">本周</el-radio-button>
            <el-radio-button label="month">本月</el-radio-button>
            <el-radio-button label="year">全年</el-radio-button>
          </el-radio-group>
          <el-button :icon="Refresh" circle plain @click="fetchData" />
          <el-button :icon="Download" plain>导出报告</el-button>
        </div>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-grid" v-loading="loading">
        <div class="kpi-card">
          <div class="label">总识别次数</div>
          <div class="value">{{ kpiData.total_count }}</div>
          <div class="trend" :class="kpiData.total_count_trend >= 0 ? 'up' : 'down'">
            {{ kpiData.total_count_trend >= 0 ? '+' : '' }}{{ kpiData.total_count_trend }}%
          </div>
        </div>
        <div class="kpi-card">
          <div class="label">平均置信度</div>
          <div class="value">{{ kpiData.avg_confidence }}%</div>
          <div class="trend" :class="kpiData.avg_confidence_trend >= 0 ? 'up' : 'down'">
            {{ kpiData.avg_confidence_trend >= 0 ? '+' : '' }}{{ kpiData.avg_confidence_trend }}%
          </div>
        </div>
        <div class="kpi-card">
          <div class="label">异常车牌</div>
          <div class="value">{{ kpiData.error_count }}</div>
          <div class="trend" :class="kpiData.error_count_trend <= 0 ? 'up' : 'down'">
             <!-- Error trend: lower is better (usually), but simpler to just show change -->
            {{ kpiData.error_count_trend >= 0 ? '+' : '' }}{{ kpiData.error_count_trend }}%
          </div>
        </div>
        <div class="kpi-card">
          <div class="label">平均耗时</div>
          <div class="value">{{ kpiData.avg_time_ms }}ms</div>
          <div class="trend flat">0.0%</div>
        </div>
      </div>

      <!-- Charts Area -->
      <div class="charts-row">
        <el-card class="chart-card main-chart">
          <template #header>
            <div class="card-header">
              <span>识别趋势</span>
              <el-tag size="small" type="success" effect="plain">近7天</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <v-chart class="chart" :option="trendOption" autoresize />
        </div>
      </el-card>

        <el-card class="chart-card pie-chart-card">
          <template #header>
            <div class="card-header">
              <span>车牌类型分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart class="chart" :option="pieOption" autoresize />
          </div>
        </el-card>
      </div>

      <!-- Top Plates -->
      <el-card class="top-plates-card">
        <template #header>
          <div class="card-header">
            <span>高频车牌 Top 5</span>
        </div>
        </template>
        <el-table :data="topPlates" :border="false" class="simple-table">
          <el-table-column type="index" label="排名" width="80" align="center">
            <template #default="scope">
              <span class="rank-badge" :class="'rank-' + (scope.$index + 1)">{{ scope.$index + 1 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="plate" label="车牌号">
            <template #default="scope">
              <span class="plate-font">{{ scope.row.plate }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="识别次数" align="right" />
          <el-table-column prop="last_seen" label="最近出现" align="right" />
          <el-table-column label="趋势" width="100" align="center">
            <template #default>
              <el-icon color="#ef4444"><Top /></el-icon>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted, watch } from 'vue'
import { useUserStore } from '@/store/user'
import { TrendCharts, Download, Top, Refresh } from '@element-plus/icons-vue'
import VChart, { THEME_KEY } from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent
} from 'echarts/components'
import { getAnalysisData, type AnalysisParams } from '@/api/analysis'
import { ElMessage } from 'element-plus'

// Register ECharts components
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent
])

provide(THEME_KEY, 'light')

const userStore = useUserStore()
const timeRange = ref<AnalysisParams['time_range']>('week')
const loading = ref(false)

// Data State
const kpiData = ref({
  total_count: 0,
  avg_confidence: 0,
  error_count: 0,
  avg_time_ms: 0,
  total_count_trend: 0,
  avg_confidence_trend: 0,
  error_count_trend: 0,
  avg_time_trend: 0
})

const topPlates = ref<any[]>([])

// Chart Options (Reactive)
const trendOption = ref<any>({})
const pieOption = ref<any>({})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getAnalysisData({ time_range: timeRange.value })
    const data = res as any // Type assertion if needed, or define full response type
    
    // Update KPI
    kpiData.value = data.kpi
    
    // Update Top Plates
    topPlates.value = data.top_plates

    // Update Trend Chart
    const dates = data.trend.map((item: any) => item.date)
    const counts = data.trend.map((item: any) => item.count)
    const rates = data.trend.map((item: any) => item.success_rate)
    
    trendOption.value = {
      tooltip: {
        trigger: 'axis',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#e2e8f0',
        textStyle: { color: '#1e293b' }
      },
      grid: {
        left: '3%', right: '4%', bottom: '3%', containLabel: true
      },
      xAxis: {
        type: 'category',
        data: dates,
        axisLine: { lineStyle: { color: '#e2e8f0' } },
        axisLabel: { color: '#64748b' }
      },
      yAxis: [
        {
          type: 'value',
          splitLine: { lineStyle: { type: 'dashed', color: '#f1f5f9' } },
          axisLabel: { color: '#64748b' }
        },
        {
          type: 'value',
          name: '成功率',
          min: 0, max: 100,
          position: 'right',
          splitLine: { show: false },
          axisLabel: { formatter: '{value}%', color: '#64748b' }
        }
      ],
      series: [
        {
          name: '识别量',
          type: 'bar',
          barWidth: '40%',
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: '#3b82f6' },
                { offset: 1, color: '#60a5fa' }
              ]
            },
            borderRadius: [4, 4, 0, 0]
          },
          data: counts
        },
        {
          name: '成功率',
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          itemStyle: { color: '#10b981' },
          areaStyle: {
            color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                    { offset: 0, color: 'rgba(16, 185, 129, 0.2)' },
                    { offset: 1, color: 'rgba(16, 185, 129, 0)' }
                ]
            }
          },
          data: rates
        }
      ]
    }

    // Update Distribution Chart
    pieOption.value = {
      tooltip: { trigger: 'item' },
      legend: { bottom: '0%', left: 'center', icon: 'circle' },
      series: [
        {
          name: '车牌类型',
          type: 'pie',
          radius: ['45%', '70%'],
          center: ['50%', '45%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
          label: { show: false, position: 'center' },
          emphasis: {
            label: { show: true, fontSize: '20', fontWeight: 'bold' }
          },
          data: data.distribution.map((item: any) => ({
             value: item.value, 
             name: item.name,
             itemStyle: { color: getPlateColor(item.name) } 
          }))
        }
      ]
    }

  } catch (error) {
    console.error(error)
    ElMessage.error('获取分析数据失败')
  } finally {
    loading.value = false
  }
}

const getPlateColor = (name: string) => {
  const map: Record<string, string> = {
    '蓝牌': '#3b82f6',
    '绿牌': '#10b981',
    '黄牌': '#f59e0b',
    '白牌': '#64748b',
    '其他': '#94a3b8'
  }
  return map[name] || '#94a3b8'
}

watch(timeRange, () => {
  fetchData()
})

onMounted(() => {
  if (userStore.isVIP) {
    fetchData()
  }
})
</script>

<style scoped lang="scss">
.analysis-view {
  width: 100%;
  position: relative;
  min-height: 80vh;
}

.vip-lock-screen {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  
  .lock-content {
    text-align: center;
    max-width: 480px;
    padding: 40px;
    
    .icon-box {
      width: 80px;
      height: 80px;
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 40px;
      color: white;
      margin: 0 auto 32px;
      box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
    }
    
    h2 { font-size: 28px; color: #0f172a; margin-bottom: 16px; }
    p { color: #64748b; margin-bottom: 32px; font-size: 16px; line-height: 1.6; }
    
    .features-preview {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 40px;
      text-align: left;
      
      .preview-item {
        background: #f8fafc;
        padding: 12px 16px;
        border-radius: 8px;
        color: #334155;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
        
        .dot {
          width: 6px;
          height: 6px;
          background: #3b82f6;
          border-radius: 50%;
        }
      }
    }
    
    .upgrade-btn {
      width: 200px;
      font-weight: 600;
    }
  }
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  
  h2 { margin: 0 0 8px; font-size: 24px; color: #0f172a; }
  .subtitle { margin: 0; color: #64748b; }
  
  .header-actions {
    display: flex;
    gap: 16px;
  }
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 24px;
  
  .kpi-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    
    .label { font-size: 14px; color: #64748b; margin-bottom: 8px; }
    .value { font-size: 28px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
    .trend {
      font-size: 13px;
      font-weight: 500;
      &.up { color: #10b981; }
      &.down { color: #ef4444; }
      &.flat { color: #94a3b8; }
    }
  }
}

.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: none !important;
  
  .card-header { font-weight: 600; color: #0f172a; }
}

.chart-container {
  height: 240px;
  position: relative;
  
  &.flex-center {
    display: flex;
    align-items: center;
    justify-content: space-around;
  }
}

/* Chart Styles */
.chart {
  height: 100%;
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #0f172a;
}

.top-plates-card {
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: none !important;
}

.rank-badge {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  
  &.rank-1 { background: #fee2e2; color: #ef4444; }
  &.rank-2 { background: #ffedd5; color: #f97316; }
  &.rank-3 { background: #fef9c3; color: #eab308; }
}

.plate-font {
  font-family: monospace;
  font-weight: 600;
  color: #0f172a;
}
</style>
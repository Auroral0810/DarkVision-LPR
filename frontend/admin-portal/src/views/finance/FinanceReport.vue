<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="kpi-label">今日收入</div>
          <div class="kpi-value">￥{{ stats?.kpis?.today_revenue || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="kpi-label">本月总额</div>
          <div class="kpi-value">￥{{ stats?.kpis?.month_revenue || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="kpi-label">待支付订单</div>
          <div class="kpi-value">{{ stats?.kpis?.pending_orders || 0 }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="kpi-label">退款申请</div>
          <div class="kpi-value">{{ stats?.kpis?.refund_pending || 0 }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="16">
        <el-card header="营收走势 (最近30天)">
          <div id="revenue-chart" style="height: 350px; width: 100%;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="套餐销售占比">
          <div id="package-pie" style="height: 350px; width: 100%;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import request from '@/utils/request'
import * as echarts from 'echarts'

const stats = ref<any>({})

async function fetchStats() {
  try {
    const data = await request.get('/api/admin/finance/report')
    if (data) {
      stats.value = data
      nextTick(() => {
        initCharts()
      })
    }
  } catch (err) {
    console.error('Fetch finance report failed:', err)
  }
}

function initCharts() {
  // Revenue Chart
  const revDom = document.getElementById('revenue-chart')
  if (revDom) {
    const revChart = echarts.init(revDom)
    revChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: stats.value.daily_revenue?.map((d: any) => d.date) || [] },
      yAxis: { type: 'value' },
      series: [{ data: stats.value.daily_revenue?.map((d: any) => d.amount) || [], type: 'line', smooth: true, areaStyle: {} }]
    })
  }

  // Package Pie
  const pieDom = document.getElementById('package-pie')
  if (pieDom) {
    const pieChart = echarts.init(pieDom)
    pieChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: '5%', left: 'center' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: stats.value.package_distribution?.map((p: any) => ({ name: p.package_name, value: Number(p.revenue) })) || []
      }]
    })
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.kpi-label { font-size: 14px; color: #666; }
.kpi-value { font-size: 24px; font-weight: bold; margin: 8px 0; color: #409EFF; }
.mt-4 { margin-top: 20px; }
</style>

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
          <el-button icon="Download" plain>导出报告</el-button>
        </div>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="label">总识别次数</div>
          <div class="value">12,543</div>
          <div class="trend up">+12.5%</div>
        </div>
        <div class="kpi-card">
          <div class="label">平均置信度</div>
          <div class="value">98.2%</div>
          <div class="trend up">+0.4%</div>
        </div>
        <div class="kpi-card">
          <div class="label">异常车牌</div>
          <div class="value">23</div>
          <div class="trend down">-2.1%</div>
        </div>
        <div class="kpi-card">
          <div class="label">平均耗时</div>
          <div class="value">45ms</div>
          <div class="trend flat">0.0%</div>
        </div>
      </div>

      <!-- Charts Area -->
      <div class="charts-row">
        <el-card class="chart-card main-chart">
          <template #header>
            <div class="card-header">
              <span>识别趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <!-- Mock Bar Chart -->
            <div class="bar-chart">
              <div class="bar-group" v-for="(h, i) in [40, 65, 35, 85, 55, 75, 90]" :key="i">
                <div class="bar" :style="{ height: h + '%' }">
                  <div class="tooltip">{{ h * 10 }}</div>
                </div>
                <span class="x-label">{{ getDateLabel(i) }}</span>
              </div>
            </div>
        </div>
      </el-card>

        <el-card class="chart-card pie-chart-card">
          <template #header>
            <div class="card-header">
              <span>车牌类型分布</span>
            </div>
          </template>
          <div class="chart-container flex-center">
            <!-- CSS Pie Chart -->
            <div class="pie-chart">
              <div class="slice blue" style="--p: 60; --r: 0;"></div>
              <div class="slice green" style="--p: 30; --r: 216;"></div>
              <div class="slice yellow" style="--p: 10; --r: 324;"></div>
              <div class="center-hole"></div>
            </div>
          <div class="legend">
              <div class="legend-item"><span class="color-dot blue"></span> 蓝牌 (60%)</div>
              <div class="legend-item"><span class="color-dot green"></span> 绿牌 (30%)</div>
              <div class="legend-item"><span class="color-dot yellow"></span> 黄牌 (10%)</div>
            </div>
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
          <el-table-column prop="lastSeen" label="最近出现" align="right" />
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
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { TrendCharts, Download, Top } from '@element-plus/icons-vue'

const userStore = useUserStore()
const timeRange = ref('week')

const getDateLabel = (index: number) => {
  const date = new Date()
  date.setDate(date.getDate() - (6 - index))
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${month}-${day}`
}

const topPlates = [
  { plate: '京A·88888', count: 42, lastSeen: '10分钟前' },
  { plate: '沪C·12345', count: 38, lastSeen: '2小时前' },
  { plate: '苏E·67890', count: 25, lastSeen: '昨天' },
  { plate: '浙B·54321', count: 18, lastSeen: '3天前' },
  { plate: '粤B·99999', count: 12, lastSeen: '1周前' },
]
</script>

<style scoped lang="scss">
.analysis-view {
  max-width: 1200px;
  margin: 0 auto;
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

/* CSS Bar Chart */
.bar-chart {
  height: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding-bottom: 24px;
  
  .bar-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
    justify-content: flex-end;
    margin: 0 8px;
  
  .bar {
      width: 100%;
      max-width: 40px;
    background: #3b82f6;
      border-radius: 6px 6px 0 0;
      transition: height 0.5s ease;
      position: relative;
      cursor: pointer;
    opacity: 0.8;
      
      &:hover {
        opacity: 1;
        .tooltip { opacity: 1; transform: translateX(-50%) translateY(-8px); }
      }
      
      .tooltip {
        position: absolute;
        top: -30px;
        left: 50%;
        transform: translateX(-50%);
        background: #1e293b;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        opacity: 0;
        transition: all 0.2s;
        pointer-events: none;
        white-space: nowrap;
        
        &::after {
          content: '';
          position: absolute;
          bottom: -4px;
          left: 50%;
          transform: translateX(-50%);
          border-left: 4px solid transparent;
          border-right: 4px solid transparent;
          border-top: 4px solid #1e293b;
        }
      }
    }
    
    .x-label {
      margin-top: 8px;
      font-size: 12px;
      color: #94a3b8;
    }
  }
}

/* CSS Pie Chart */
.pie-chart {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  position: relative;
  background: #f1f5f9;
  
  .slice {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: conic-gradient(var(--c) calc(var(--p) * 1%), transparent 0);
    transform: rotate(calc(var(--r) * 1deg));
    
    &.blue { --c: #3b82f6; }
    &.green { --c: #10b981; }
    &.yellow { --c: #f59e0b; }
  }
  
  .center-hole {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 60%; height: 60%;
    background: white;
    border-radius: 50%;
  }
}

.legend {
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #64748b;
    margin-bottom: 8px;
    
    .color-dot {
      width: 8px; height: 8px; border-radius: 50%;
      &.blue { background: #3b82f6; }
      &.green { background: #10b981; }
      &.yellow { background: #f59e0b; }
    }
  }
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
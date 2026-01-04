<template>
  <div class="analysis-view">
    <div class="header">
      <h2>数据分析</h2>
      <p>您的识别数据深度洞察</p>
    </div>

    <!-- Charts Grid -->
    <div class="charts-grid">
      <el-card class="chart-card">
        <template #header>识别趋势 (近7天)</template>
        <div class="chart-placeholder">
          <div class="bar" style="height: 40%"></div>
          <div class="bar" style="height: 60%"></div>
          <div class="bar" style="height: 30%"></div>
          <div class="bar" style="height: 80%"></div>
          <div class="bar" style="height: 50%"></div>
          <div class="bar" style="height: 70%"></div>
          <div class="bar" style="height: 90%"></div>
        </div>
      </el-card>

      <el-card class="chart-card">
        <template #header>车牌类型分布</template>
        <div class="pie-placeholder">
          <div class="slice" style="--c: #3b82f6; --deg: 0deg; --p: 60%"></div>
          <div class="slice" style="--c: #10b981; --deg: 216deg; --p: 30%"></div>
          <div class="slice" style="--c: #f59e0b; --deg: 324deg; --p: 10%"></div>
          <div class="legend">
            <span><i style="background: #3b82f6"></i> 蓝牌 (60%)</span>
            <span><i style="background: #10b981"></i> 绿牌 (30%)</span>
            <span><i style="background: #f59e0b"></i> 黄牌 (10%)</span>
          </div>
        </div>
      </el-card>
    </div>

    <el-card class="top-plates">
      <template #header>高频车牌 Top 5</template>
      <el-table :data="topPlates" border>
        <el-table-column type="index" label="排名" width="80" />
        <el-table-column prop="plate" label="车牌号" />
        <el-table-column prop="count" label="识别次数" />
        <el-table-column prop="lastSeen" label="最近出现" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">


const topPlates = [
  { plate: '京A·88888', count: 12, lastSeen: '2026-01-04 10:23' },
  { plate: '沪C·12345', count: 8, lastSeen: '2026-01-03 15:45' },
  { plate: '苏E·67890', count: 5, lastSeen: '2026-01-02 09:12' },
  { plate: '浙B·54321', count: 3, lastSeen: '2026-01-04 11:30' },
  { plate: '粤B·99999', count: 2, lastSeen: '2026-01-01 14:20' },
]
</script>

<style scoped lang="scss">
.analysis-view {
  max-width: 1200px;
}

.header {
  margin-bottom: 32px;
  h2 { margin: 0 0 8px; color: #0f172a; }
  p { margin: 0; color: #64748b; }
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.chart-placeholder {
  height: 200px;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  padding: 20px 0;
  
  .bar {
    width: 30px;
    background: #3b82f6;
    border-radius: 4px 4px 0 0;
    opacity: 0.8;
  }
}

.pie-placeholder {
  height: 200px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .slice {
    position: absolute;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: conic-gradient(var(--c) calc(var(--p) * 3.6deg), transparent 0);
    transform: rotate(var(--deg));
  }
  
  .legend {
    position: absolute;
    right: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    
    span {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #64748b;
      
      i {
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }
    }
  }
}
</style>

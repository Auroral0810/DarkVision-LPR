<template>
  <div class="overview-view">
    <!-- Welcome Section -->
    <div class="welcome-card">
      <div class="welcome-content">
        <div class="text-group">
          <h2>早安, {{ userStore.userInfo.nickname }} 👋</h2>
          <p class="subtitle">今天是 {{ currentDate }}，准备好开始新的识别任务了吗？</p>
        </div>
        <div class="action-group">
          <el-button type="primary" size="large" icon="Plus" round @click="router.push('/dashboard/recognition')">
            开始识别
          </el-button>
        </div>
      </div>
      <div class="decoration-bg"></div>
    </div>

    <div class="dashboard-grid">
      <!-- Left Column: Stats & Charts (Future) & History -->
      <div class="main-column">
        <!-- Stats Grid -->
        <div class="stats-grid">
          <div class="stat-card blue">
            <div class="card-header-row">
              <span class="label">今日识别</span>
              <div class="icon-bg">
                <el-icon><Camera /></el-icon>
              </div>
            </div>
            <div class="card-value-row">
              <div class="value-group">
                <span class="value">{{ todayUsage }}</span>
                <span class="unit">次</span>
              </div>
            </div>
            <div class="stat-progress">
              <div class="progress-info">
                <span>使用率</span>
                <span>{{ usagePercentage }}%</span>
              </div>
              <el-progress 
                :percentage="usagePercentage" 
                :show-text="false" 
                :stroke-width="6" 
                color="#3b82f6"
              />
            </div>
          </div>

          <div class="stat-card green">
            <div class="card-header-row">
              <span class="label">识别成功率</span>
              <div class="icon-bg">
                <el-icon><CircleCheck /></el-icon>
              </div>
            </div>
            <div class="card-value-row">
              <div class="value-group">
                <span class="value">99.8</span>
                <span class="unit">%</span>
              </div>
            </div>
            <div class="trend up">
              <el-icon><Top /></el-icon>
              <span>较昨日 +0.2%</span>
            </div>
          </div>

          <div class="stat-card purple">
            <div class="card-header-row">
              <span class="label">剩余额度</span>
              <div class="icon-bg">
                <el-icon><Files /></el-icon>
              </div>
            </div>
            <div class="card-value-row">
              <div class="value-group">
                <span class="value">{{ remainingUsageDisplay }}</span>
                <span class="unit">次</span>
              </div>
            </div>
            <div class="action-link" v-if="userStore.userInfo.role === 'FREE'" @click="handleUpgrade">
              提升额度 <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
        </div>

        <!-- Recent History -->
        <div class="section-container">
          <div class="section-header">
            <div class="header-title">
              <h3>最近识别记录</h3>
              <span class="header-subtitle">您最近的 5 条识别结果</span>
            </div>
            <el-button link type="primary" @click="router.push('/dashboard/history')">
              查看全部 <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
          
          <el-table :data="recentRecords" style="width: 100%" class="custom-table" :header-cell-style="{ background: '#f8fafc', color: '#64748b' }">
            <el-table-column prop="date" label="时间" width="180">
              <template #default="scope">
                <div class="date-cell">
                  <span class="time">{{ scope.row.date.split(' ')[1] }}</span>
                  <span class="date">{{ scope.row.date.split(' ')[0] }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="预览图" width="120">
               <template #default>
                 <div class="thumbnail-placeholder">
                   <el-icon><Picture /></el-icon>
                 </div>
               </template>
            </el-table-column>
            <el-table-column prop="plate" label="车牌号">
              <template #default="scope">
                <span class="plate-number">{{ scope.row.plate }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag :type="getPlateTypeColor(scope.row.type)" size="small" effect="light" round>
                  {{ scope.row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="confidence" label="置信度" width="150">
              <template #default="scope">
                <div class="confidence-wrapper">
                  <span class="conf-val">{{ scope.row.confidence }}%</span>
                  <el-progress 
                    :percentage="scope.row.confidence" 
                    :color="getConfidenceColor(scope.row.confidence)"
                    :show-text="false"
                    :stroke-width="4"
                  />
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" align="right">
              <template #default>
                <el-button link type="primary" size="small">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <!-- Right Column: Membership & Tips -->
      <div class="side-column">
        <!-- Upgrade Banner -->
        <div class="side-card upgrade-card" v-if="userStore.userInfo.role === 'FREE'">
          <div class="card-icon">
            <el-icon><Trophy /></el-icon>
          </div>
          <h3>升级到 VIP</h3>
          <p>解锁批量识别、视频分析、无限历史记录。</p>
          <el-button type="warning" block round @click="handleUpgrade">立即升级</el-button>
        </div>

        <div class="side-card quota-card">
          <div class="card-title">当前套餐</div>
          <div class="plan-name">{{ userStore.membershipInfo.name }}</div>
          
          <div class="usage-list">
            <div class="usage-item">
              <div class="usage-label">
                <span>每日额度</span>
                <span>{{ todayUsage }} / {{ maxUsageDisplay }}</span>
              </div>
              <el-progress :percentage="usagePercentage" :show-text="false" status="primary" />
            </div>
            <div class="usage-item">
              <div class="usage-label">
                <span>存储空间</span>
                <span>12%</span>
              </div>
              <el-progress :percentage="12" :show-text="false" color="#10b981" />
            </div>
          </div>
        </div>

        <div class="side-card tips-card">
          <div class="card-title">💡 识别小贴士</div>
          <ul class="tips-list">
            <li>确保光线充足，避免强反光</li>
            <li>拍摄角度尽量正对车牌</li>
            <li>支持 JPG/PNG 格式，最大 5MB</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { 
  Camera, CircleCheck, Files, Plus, ArrowRight, Top, 
  Trophy, Picture 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const currentDate = new Date().toLocaleDateString('zh-CN', { 
  year: 'numeric', 
  month: 'long', 
  day: 'numeric',
  weekday: 'long'
})

// Mock Data
const todayUsage = 12

const maxUsageDisplay = computed(() => {
  return userStore.quota.daily === Infinity ? '无限' : userStore.quota.daily
})

const remainingUsageDisplay = computed(() => {
  if (userStore.quota.daily === Infinity) return '无限'
  return Math.max(0, userStore.quota.daily - todayUsage)
})

const usagePercentage = computed(() => {
  if (userStore.quota.daily === Infinity) return 0
  return Math.min(100, Math.round((todayUsage / userStore.quota.daily) * 100))
})

const recentRecords = [
  { date: '2026-01-04 14:23:01', plate: '京A·88888', type: '蓝牌', confidence: 99.2 },
  { date: '2026-01-04 14:20:15', plate: '沪C·12345', type: '蓝牌', confidence: 95.5 },
  { date: '2026-01-04 13:55:42', plate: '苏E·67890', type: '绿牌', confidence: 98.1 },
  { date: '2026-01-04 12:30:11', plate: '浙B·54321', type: '黄牌', confidence: 88.4 },
]

const getPlateTypeColor = (type: string) => {
  if (type === '蓝牌') return ''
  if (type === '绿牌') return 'success'
  if (type === '黄牌') return 'warning'
  return 'info'
}

const getConfidenceColor = (val: number) => {
  if (val >= 90) return '#10b981'
  if (val >= 80) return '#f59e0b'
  return '#ef4444'
}

const handleUpgrade = () => {
  ElMessage.info('正在跳转至订阅页面...')
  // router.push('/subscription')
}
</script>

<style scoped lang="scss">
.overview-view {
  width: 100%;
}

.welcome-card {
  background: linear-gradient(120deg, #2563eb, #1d4ed8);
  border-radius: 16px;
  padding: 32px;
  color: white;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.4);

  .welcome-content {
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .text-group {
      h2 {
        margin: 0 0 8px;
        font-size: 28px;
        font-weight: 700;
      }
      .subtitle {
        margin: 0;
        opacity: 0.9;
        font-size: 15px;
      }
    }
  }

  .decoration-bg {
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    background-image: 
      radial-gradient(circle at 90% 10%, rgba(255,255,255,0.1) 0%, transparent 40%),
      radial-gradient(circle at 10% 90%, rgba(255,255,255,0.1) 0%, transparent 40%);
    z-index: 1;
  }
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
  
  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 140px;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 12px -3px rgba(0, 0, 0, 0.05);
  }

  .card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    
    .label {
      color: #64748b;
      font-size: 13px;
      font-weight: 500;
    }
    
    .icon-bg {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }
  }

  .card-value-row {
    margin-bottom: 12px;
    .value { font-size: 28px; font-weight: 700; color: #0f172a; line-height: 1; }
    .unit { font-size: 13px; color: #94a3b8; margin-left: 4px; }
  }

  &.blue {
    .icon-bg { background: #eff6ff; color: #3b82f6; }
    border-bottom: 3px solid #3b82f6;
  }
  &.green {
    .icon-bg { background: #f0fdf4; color: #10b981; }
    border-bottom: 3px solid #10b981;
  }
  &.purple {
    .icon-bg { background: #f5f3ff; color: #8b5cf6; }
    border-bottom: 3px solid #8b5cf6;
  }

  .stat-progress {
    .progress-info {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #64748b;
      margin-bottom: 4px;
    }
  }
  
  .trend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    &.up { color: #10b981; }
  }

  .action-link {
    font-size: 12px;
    color: #8b5cf6;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
    &:hover { text-decoration: underline; }
  }
}

.section-container {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  
  .section-header {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid #f1f5f9;
    
    .header-title {
      h3 { margin: 0 0 4px; font-size: 16px; color: #0f172a; }
      .header-subtitle { font-size: 12px; color: #64748b; }
    }
  }
}

.custom-table {
  .date-cell {
    display: flex;
    flex-direction: column;
    .time { font-weight: 600; color: #0f172a; font-size: 13px; }
    .date { font-size: 12px; color: #94a3b8; }
  }
  
  .plate-number {
    font-family: monospace;
    font-weight: 700;
    color: #0f172a;
    font-size: 15px;
    letter-spacing: 0.5px;
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 4px;
  }
  
  .confidence-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    .conf-val { font-size: 12px; color: #64748b; width: 32px; }
    .el-progress { flex: 1; }
  }
  
  .thumbnail-placeholder {
    width: 50px; height: 36px;
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #cbd5e1;
    font-size: 16px;
  }
}

.side-column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.side-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

  &.upgrade-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
    border: none;
    text-align: center;
    padding: 24px;
    
    .card-icon {
      width: 40px; height: 40px;
      background: rgba(255,255,255,0.1);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; color: #fbbf24;
      margin: 0 auto 12px;
    }
    
    h3 { margin: 0 0 6px; font-size: 16px; }
    p { margin: 0 0 20px; font-size: 12px; color: #94a3b8; line-height: 1.5; }
    
    .el-button {
      font-weight: 600;
    }
  }

  .card-title {
    font-size: 14px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 12px;
  }

  &.quota-card {
    .plan-name {
      font-size: 20px;
      font-weight: 700;
      color: #2563eb;
      margin-bottom: 20px;
    }
    
    .usage-item {
      margin-bottom: 12px;
      &:last-child { margin-bottom: 0; }
      
      .usage-label {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: #64748b;
        margin-bottom: 4px;
      }
    }
  }

  &.tips-card {
    background: #fffbeb;
    border-color: #fef3c7;
    
    .card-title { color: #b45309; }
    
    .tips-list {
      margin: 0; padding-left: 20px;
      li {
        font-size: 12px;
        color: #92400e;
        margin-bottom: 6px;
        &:last-child { margin-bottom: 0; }
      }
    }
  }
}
</style>
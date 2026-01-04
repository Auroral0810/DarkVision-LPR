<template>
  <div class="overview-view">
    <!-- Welcome Section -->
    <div class="welcome-section">
      <div class="welcome-text">
        <h2>早安, {{ userStore.userInfo.nickname }} 👋</h2>
        <p class="subtitle">今天是 {{ currentDate }}，准备好开始新的识别任务了吗？</p>
      </div>
      <div class="quota-summary">
        <div class="quota-item">
          <span class="label">今日额度</span>
          <span class="value">{{ todayUsage }} / {{ maxUsageDisplay }}</span>
        </div>
      </div>
    </div>

    <!-- Upgrade Banner for FREE users -->
    <div class="upgrade-banner" v-if="userStore.userInfo.role === 'FREE'">
      <div class="banner-content">
        <div class="icon-wrapper">
          <el-icon><Trophy /></el-icon>
        </div>
        <div class="text-content">
          <h3>升级到 VIP 解锁专业功能</h3>
          <p>解锁批量识别、视频分析、无限历史记录以及更多高级功能。</p>
        </div>
      </div>
      <el-button type="warning" round @click="handleUpgrade">立即升级</el-button>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card blue">
        <div class="stat-icon">
          <el-icon><Camera /></el-icon>
        </div>
        <div class="stat-info">
          <span class="label">今日识别</span>
          <div class="value-group">
            <span class="value">{{ todayUsage }}</span>
            <span class="unit">次</span>
          </div>
        </div>
        <div class="stat-progress">
          <el-progress 
            :percentage="usagePercentage" 
            :show-text="false" 
            :stroke-width="6" 
            color="#3b82f6"
          />
        </div>
      </div>

      <div class="stat-card green">
        <div class="stat-icon">
          <el-icon><CircleCheck /></el-icon>
        </div>
        <div class="stat-info">
          <span class="label">识别成功率</span>
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
        <div class="stat-icon">
          <el-icon><Files /></el-icon>
        </div>
        <div class="stat-info">
          <span class="label">剩余额度</span>
          <div class="value-group">
            <span class="value">{{ remainingUsageDisplay }}</span>
            <span class="unit">次</span>
          </div>
        </div>
        <div class="action-link" v-if="userStore.userInfo.role === 'FREE'" @click="handleUpgrade">
          提升额度 <el-icon><ArrowRight /></el-icon>
        </div>
      </div>
      
      <!-- Quick Action Card -->
      <div class="quick-action-card" @click="router.push('/dashboard/recognition')">
        <div class="action-icon">
          <el-icon><Plus /></el-icon>
        </div>
        <span>开始新任务</span>
      </div>
    </div>

    <!-- Recent History -->
    <div class="section-container">
      <div class="section-header">
        <h3>最近识别记录</h3>
        <el-button link type="primary" @click="router.push('/dashboard/history')">
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      
      <el-table :data="recentRecords" style="width: 100%" class="custom-table">
        <el-table-column prop="date" label="时间" width="180">
          <template #default="scope">
            <span class="text-secondary">{{ scope.row.date }}</span>
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
            <el-tag :type="getPlateTypeColor(scope.row.type)" size="small" effect="plain">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="confidence" label="置信度" width="150">
          <template #default="scope">
            <div class="confidence-wrapper">
              <el-progress 
                :percentage="scope.row.confidence" 
                :color="getConfidenceColor(scope.row.confidence)"
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
  day: 'numeric' 
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
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
  
  .welcome-text {
    h2 {
      margin: 0 0 8px;
      font-size: 28px;
      color: #0f172a;
    }
    .subtitle {
      margin: 0;
      color: #64748b;
      font-size: 16px;
    }
  }
  
  .quota-summary {
    background: white;
    padding: 12px 24px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    
    .quota-item {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      
      .label {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 4px;
      }
      .value {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        font-family: monospace;
      }
    }
  }
}

.upgrade-banner {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 16px;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: radial-gradient(circle at 80% 50%, rgba(245, 158, 11, 0.15), transparent 60%);
  }
  
  .banner-content {
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    z-index: 1;
    
    .icon-wrapper {
      width: 48px;
      height: 48px;
      background: rgba(255,255,255,0.1);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: #fbbf24;
    }
    
    .text-content {
      h3 {
        margin: 0 0 4px;
        font-size: 18px;
        font-weight: 600;
      }
      p {
        margin: 0;
        color: #94a3b8;
        font-size: 14px;
      }
    }
  }
  
  .el-button {
    position: relative;
    z-index: 1;
    font-weight: 600;
    padding: 20px 32px;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
  
  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 16px;
  }
  
  .stat-info {
    margin-bottom: 16px;
    
    .label {
      font-size: 14px;
      color: #64748b;
      display: block;
      margin-bottom: 4px;
    }
    
    .value-group {
      display: flex;
      align-items: baseline;
      gap: 4px;
      
      .value {
        font-size: 28px;
        font-weight: 700;
        color: #0f172a;
      }
      
      .unit {
        font-size: 14px;
        color: #94a3b8;
      }
    }
  }
  
  &.blue .stat-icon { background: #eff6ff; color: #3b82f6; }
  &.green .stat-icon { background: #f0fdf4; color: #10b981; }
  &.purple .stat-icon { background: #f5f3ff; color: #8b5cf6; }
  
  .stat-progress {
    margin-top: auto;
  }
  
  .trend {
    margin-top: auto;
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    
    &.up { color: #10b981; }
  }
  
  .action-link {
    margin-top: auto;
    font-size: 13px;
    color: #8b5cf6;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
    
    &:hover { text-decoration: underline; }
  }
}

.quick-action-card {
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
  
  &:hover {
    border-color: #3b82f6;
    color: #3b82f6;
    background: #eff6ff;
    
    .action-icon {
      background: white;
      color: #3b82f6;
    }
  }
  
  .action-icon {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-bottom: 12px;
    transition: all 0.2s;
  }
  
  span {
    font-weight: 600;
    font-size: 14px;
  }
}

.section-container {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  padding: 24px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    h3 {
      margin: 0;
      font-size: 18px;
      color: #0f172a;
    }
  }
}

.custom-table {
  :deep(.el-table__cell) {
    padding: 16px 0;
  }
  
  .text-secondary {
    color: #64748b;
    font-size: 13px;
  }
  
  .plate-number {
    font-family: monospace;
    font-weight: 700;
    color: #0f172a;
    font-size: 15px;
    background: #f1f5f9;
    padding: 4px 8px;
    border-radius: 4px;
  }
  
  .thumbnail-placeholder {
    width: 60px;
    height: 36px;
    background: #f1f5f9;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #cbd5e1;
  }
  
  .confidence-wrapper {
    width: 100%;
  }
}
</style>
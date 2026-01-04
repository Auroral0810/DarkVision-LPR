<template>
  <div class="overview-view">
    <div class="welcome-section">
      <h2>欢迎回来, {{ userStore.userInfo.nickname }}</h2>
      <p class="subtitle">今日已使用 {{ todayUsage }} / {{ maxUsage }} 次识别额度</p>
    </div>

    <!-- Usage Stats Cards -->
    <div class="stats-grid">
      <el-card shadow="hover" class="stat-card">
        <template #header>
          <div class="card-header">
            <span>今日识别</span>
            <el-tag size="small" type="success">实时</el-tag>
          </div>
        </template>
        <div class="stat-value">{{ todayUsage }}</div>
        <div class="stat-label">次</div>
        <el-progress :percentage="usagePercentage" :status="usagePercentage > 90 ? 'exception' : ''" />
      </el-card>

      <el-card shadow="hover" class="stat-card">
        <template #header>
          <div class="card-header">
            <span>剩余额度</span>
          </div>
        </template>
        <div class="stat-value">{{ remainingUsage }}</div>
        <div class="stat-label">次</div>
        <div class="stat-desc" v-if="userStore.userInfo.role === 'FREE'">
          升级 VIP 解锁更多额度
        </div>
      </el-card>

      <el-card shadow="hover" class="stat-card" v-if="userStore.isVIP">
        <template #header>
          <div class="card-header">
            <span>本月累计</span>
          </div>
        </template>
        <div class="stat-value">1,284</div>
        <div class="stat-label">次</div>
      </el-card>
      
      <el-card shadow="hover" class="stat-card action-card" @click="router.push('/dashboard/recognition')">
        <div class="action-content">
          <el-icon :size="32"><Camera /></el-icon>
          <span>开始识别</span>
        </div>
      </el-card>
    </div>

    <!-- VIP Feature Promotion for FREE users -->
    <div class="vip-promo" v-if="userStore.userInfo.role === 'FREE'">
      <el-alert
        title="升级到 VIP 解锁批量识别和数据分析"
        type="warning"
        description="支持单次50张图片批量处理，视频识别，以及详细的数据分析报表。"
        show-icon
        :closable="false"
      >
        <el-button type="primary" size="small" plain class="upgrade-btn">立即升级</el-button>
      </el-alert>
    </div>

    <!-- Recent History -->
    <div class="recent-history">
      <h3>最近识别记录</h3>
      <el-table :data="recentRecords" style="width: 100%">
        <el-table-column prop="date" label="时间" width="180" />
        <el-table-column prop="plate" label="车牌号" width="180" />
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="confidence" label="置信度">
          <template #default="scope">
            <el-tag :type="scope.row.confidence > 90 ? 'success' : 'warning'">
              {{ scope.row.confidence }}%
            </el-tag>
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
import { Camera } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// Mock data
const todayUsage = 12
const maxUsage = computed(() => userStore.quota.daily === Infinity ? '∞' : userStore.quota.daily)
const remainingUsage = computed(() => {
  if (userStore.quota.daily === Infinity) return '∞'
  return userStore.quota.daily - todayUsage
})

const usagePercentage = computed(() => {
  if (userStore.quota.daily === Infinity) return 0
  return Math.round((todayUsage / userStore.quota.daily) * 100)
})

const recentRecords = [
  { date: '2026-01-04 14:23:01', plate: '京A·88888', type: '蓝牌', confidence: 99.2 },
  { date: '2026-01-04 14:20:15', plate: '沪C·12345', type: '蓝牌', confidence: 95.5 },
  { date: '2026-01-04 13:55:42', plate: '苏E·67890', type: '绿牌', confidence: 98.1 },
]
</script>

<style scoped lang="scss">
.overview-view {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 32px;
  
  h2 {
    margin: 0 0 8px;
    font-size: 24px;
    color: #0f172a;
  }
  
  .subtitle {
    color: #64748b;
    margin: 0;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #64748b;
  }
  
  .stat-value {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
    display: inline-block;
    margin-right: 4px;
  }
  
  .stat-label {
    display: inline-block;
    color: #94a3b8;
    font-size: 14px;
  }
  
  .stat-desc {
    font-size: 12px;
    color: #f59e0b;
    margin-top: 8px;
  }
}

.action-card {
  background: #eff6ff;
  border-color: #bfdbfe;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  
  &:hover {
    background: #dbeafe;
    transform: translateY(-2px);
  }
  
  :deep(.el-card__body) {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .action-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    color: #2563eb;
    font-weight: 600;
  }
}

.vip-promo {
  margin-bottom: 32px;
  
  .upgrade-btn {
    margin-top: 12px;
  }
}

.recent-history {
  h3 {
    margin: 0 0 16px;
    font-size: 18px;
    color: #0f172a;
  }
}
</style>

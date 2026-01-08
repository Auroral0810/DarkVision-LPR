<template>
  <div class="config-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="page-header">
          <h2 class="page-title">限额配置</h2>
          <p class="page-subtitle">设定不同会员层级的每日识别次数上限</p>
        </div>
      </el-col>

      <el-col :span="24">
        <el-card v-loading="loading" class="config-card shadow-sm">
          <div class="quota-grid">
            <!-- 免费用户 -->
            <div class="quota-tier-card">
              <div class="tier-header">
                <div class="tier-icon free"><el-icon><User /></el-icon></div>
                <div class="tier-info">
                  <span class="tier-name">普通/免费用户</span>
                  <span class="tier-desc">基础体验层级</span>
                </div>
              </div>
              <div class="tier-body">
                <el-form-item label="每日识别上限">
                  <el-input-number v-model="form['free_daily_limit']" :min="0" />
                </el-form-item>
              </div>
            </div>

            <!-- 月卡用户 -->
            <div class="quota-tier-card">
              <div class="tier-header">
                <div class="tier-icon monthly"><el-icon><Calendar /></el-icon></div>
                <div class="tier-info">
                  <span class="tier-name">月卡 VIP</span>
                  <span class="tier-desc">标准订阅层级</span>
                </div>
              </div>
              <div class="tier-body">
                <el-form-item label="每日识别上限">
                  <el-input-number v-model="form['vip_monthly_limit']" :min="0" />
                </el-form-item>
              </div>
            </div>

            <!-- 年卡用户 -->
            <div class="quota-tier-card">
              <div class="tier-header">
                <div class="tier-icon yearly"><el-icon><Medal /></el-icon></div>
                <div class="tier-info">
                  <span class="tier-name">年卡 VIP</span>
                  <span class="tier-desc">尊享订阅层级</span>
                </div>
              </div>
              <div class="tier-body">
                <el-form-item label="每日识别上限">
                  <el-input-number v-model="form['vip_yearly_limit']" :min="0" />
                </el-form-item>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <el-button type="primary" size="large" @click="handleSave" :loading="saving">
              应用限额
            </el-button>
            <el-button size="large" @click="resetForm">重置</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { User, Calendar, Medal } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const systemStore = useSystemConfigStore()
const { configs, loading } = storeToRefs(systemStore)

const form = ref<any>({
  free_daily_limit: 10,
  vip_monthly_limit: 50,
  vip_yearly_limit: 100
})
const saving = ref(false)

const initData = () => {
  if (configs.value.quota) {
    const data = configs.value.quota
    form.value.free_daily_limit = parseInt(data.free_daily_limit || '0')
    form.value.vip_monthly_limit = parseInt(data.vip_monthly_limit || '0')
    form.value.vip_yearly_limit = parseInt(data.vip_yearly_limit || '0')
  }
}

onMounted(async () => {
  if (!configs.value.quota || Object.keys(configs.value.quota).length === 0) {
    await systemStore.fetchConfigs()
  }
  initData()
})

watch(configs, () => {
  initData()
}, { deep: true })

const resetForm = () => {
  initData()
}

const handleSave = async () => {
  saving.value = true
  try {
    const updateData: Record<string, string> = {
      'quota.free_daily_limit': form.value.free_daily_limit.toString(),
      'quota.vip_monthly_limit': form.value.vip_monthly_limit.toString(),
      'quota.vip_yearly_limit': form.value.vip_yearly_limit.toString()
    }
    
    await systemStore.updateConfigs(updateData)
    ElMessage.success('限额配置已成功应用')
  } catch (err) {
    ElMessage.error('应用失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.config-container {
  padding: 24px;
  background-color: #f8fafc;
  min-height: calc(100vh - 84px);
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.config-card {
  border-radius: 12px;
  border: none;
}

.quota-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.quota-tier-card {
  padding: 24px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.quota-tier-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.tier-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.tier-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.tier-icon.free { background: #f1f5f9; color: #64748b; }
.tier-icon.monthly { background: #eff6ff; color: #3b82f6; }
.tier-icon.yearly { background: #fefce8; color: #eab308; }

.tier-info {
  display: flex;
  flex-direction: column;
}

.tier-name {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.tier-desc {
  font-size: 12px;
  color: #64748b;
}

.tier-body {
  padding-top: 16px;
  border-top: 1px dashed #e2e8f0;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item) {
  margin-bottom: 0;
  flex-direction: column;
  align-items: flex-start;
}

:deep(.el-form-item__label) {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px !important;
  line-height: 1;
}

:deep(.el-input-number) {
  width: 100%;
}
</style>

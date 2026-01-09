<template>
  <div class="config-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="page-header">
          <h2 class="page-title">基础配置</h2>
          <p class="page-subtitle">管理网站全局信息、对象存储及实名认证参数</p>
        </div>
      </el-col>

      <el-col :span="24">
        <el-card v-loading="loading" class="config-card shadow-sm">
          <el-form :model="form" label-width="140px" label-position="left">
            <!-- 网站信息组 -->
            <div class="config-section">
              <div class="section-header">
                <el-icon><Monitor /></el-icon>
                <span>网站信息</span>
              </div>
              <el-row :gutter="40">
                <el-col :md="12" :sm="24">
                  <el-form-item label="项目标题">
                    <el-input v-model="form['seo_title']" placeholder="例如: DarkVision-LPR" />
                  </el-form-item>
                </el-col>
                <el-col :md="12" :sm="24">
                  <el-form-item label="环境标识">
                    <el-tag :type="debugMode ? 'warning' : 'success'">{{ debugMode ? 'Development' : 'Production' }}</el-tag>
                  </el-form-item>
                </el-col>
                <el-col :md="12" :sm="24">
                  <el-form-item label="服务可用性">
                    <el-input v-model="form['service_availability']" placeholder="例如: 99.9%" />
                  </el-form-item>
                </el-col>
                <el-col :md="12" :sm="24">
                  <el-form-item label="企业客户数">
                    <el-input v-model="form['enterprise_clients']" placeholder="例如: 500+" />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <el-divider />

            <!-- 认证组 -->
            <div class="config-section">
              <div class="section-header">
                <el-icon><Checked /></el-icon>
                <span>实名认证 (阿里云市场)</span>
              </div>
              <el-row :gutter="40">
                <el-col :span="24">
                  <el-form-item label="Market AppCode">
                    <el-input v-model="form['aliyun_market_appcode']" />
                    <div class="help-text">用于身份核验 API 的身份凭证</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <div class="form-actions">
              <el-button type="primary" size="large" @click="handleSave" :loading="saving">
                提交修改
              </el-button>
              <el-button size="large" @click="resetForm">重置</el-button>
            </div>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { Monitor, Files, Checked } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const systemStore = useSystemConfigStore()
const { configs, loading } = storeToRefs(systemStore)

const form = ref<any>({})
const saving = ref(false)
const debugMode = ref(import.meta.env.DEV)

const initData = () => {
  form.value = { ...configs.value.base }
}

onMounted(async () => {
  if (!configs.value.base || Object.keys(configs.value.base).length === 0) {
    await systemStore.fetchConfigs()
  }
  initData()
})

watch(configs, () => {
  initData()
}, { deep: true })

const resetForm = () => {
  initData()
  ElMessage.info('表单已重置')
}

const handleSave = async () => {
  saving.value = true
  try {
    const updateData: Record<string, string> = {}
    Object.keys(form.value).forEach(key => {
      const fullKey = key.includes('.') ? key : `base.${key}`
      updateData[fullKey] = String(form.value[key])
    })
    
    await systemStore.updateConfigs(updateData)
    ElMessage.success('基础配置更新成功')
  } catch (err) {
    ElMessage.error('更新失败')
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

.config-section {
  padding: 8px 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
}

.section-header .el-icon {
  font-size: 20px;
  color: #3b82f6;
}

.help-text {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
  line-height: 1.5;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #475569;
}

:deep(.el-input__inner) {
  border-radius: 8px;
}
</style>

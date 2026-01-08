<template>
  <div class="config-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="page-header">
          <h2 class="page-title">邮件 & 短信</h2>
          <p class="page-subtitle">配置系统告警、通知及验证码发送服务</p>
        </div>
      </el-col>

      <el-col :span="24">
        <el-form :model="form" label-width="120px" label-position="left">
          <el-row :gutter="24">
            <!-- 邮件服务 -->
            <el-col :md="12" :sm="24">
              <el-card class="config-card shadow-sm service-card">
                <template #header>
                  <div class="card-header">
                    <div class="header-tit">
                      <el-icon class="icon mail"><Message /></el-icon>
                      <span>SMTP 邮件服务</span>
                    </div>
                    <el-tag size="small" type="success">Active</el-tag>
                  </div>
                </template>
                
                <el-form-item label="SMTP 主机">
                  <el-input v-model="form['mail_host']" placeholder="smtp.163.com" />
                </el-form-item>
                <el-form-item label="SMTP 端口">
                  <el-input v-model="form['mail_port']" placeholder="465" />
                </el-form-item>
                <el-form-item label="SMTP 用户">
                  <el-input v-model="form['mail_username']" placeholder="example@163.com" />
                </el-form-item>
                <el-form-item label="SMTP 密码">
                  <el-input v-model="form['mail_password']" type="password" show-password />
                </el-form-item>
                <el-form-item label="发件邮箱">
                  <el-input v-model="form['mail_from']" />
                </el-form-item>
                <el-form-item label="发件人名称">
                  <el-input v-model="form['mail_from_name']" />
                </el-form-item>
                <el-form-item label="安全选项">
                  <el-checkbox v-model="form['mail_use_ssl']">SSL</el-checkbox>
                  <el-checkbox v-model="form['mail_use_tls']">TLS</el-checkbox>
                </el-form-item>
              </el-card>
            </el-col>

            <!-- 短信服务 -->
            <el-col :md="12" :sm="24">
              <el-card class="config-card shadow-sm service-card">
                <template #header>
                  <div class="card-header">
                    <div class="header-tit">
                      <el-icon class="icon sms"><ChatDotRound /></el-icon>
                      <span>短信服务 (SMS)</span>
                    </div>
                  </div>
                </template>
                
                <el-form-item label="服务商">
                  <el-select v-model="form['sms_provider']" style="width: 100%">
                    <el-option label="短信宝 (SMSBao)" value="smsbao" />
                  </el-select>
                </el-form-item>
                <el-form-item label="SMS 账号">
                  <el-input v-model="form['sms_user']" />
                </el-form-item>
                <el-form-item label="SMS 密码/Key">
                  <el-input v-model="form['sms_password']" type="password" show-password />
                  <div class="help-text">短信宝用户建议使用 MD5 后的 API 密码</div>
                </el-form-item>
                <el-form-item label="短信签名">
                  <el-input v-model="form['sms_sign_name']" />
                </el-form-item>
                
                <div class="service-status-info">
                  <div class="status-item">
                    <span class="label">可用余额:</span>
                    <span class="value success">-- 条</span>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <div class="form-actions-bar">
            <el-button type="info" plain @click="testConnection">测试连接</el-button>
            <div class="main-actions">
              <el-button size="large" @click="resetForm">取消重置</el-button>
              <el-button type="primary" size="large" @click="handleSave" :loading="saving">
                更新配置
              </el-button>
            </div>
          </div>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { Message, ChatDotRound } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const systemStore = useSystemConfigStore()
const { configs, loading } = storeToRefs(systemStore)

const form = ref<any>({})
const saving = ref(false)

const initData = () => {
  form.value = { ...configs.value.notice }
  // 转换布尔值
  if (form.value.mail_use_ssl) form.value.mail_use_ssl = form.value.mail_use_ssl === 'true' || form.value.mail_use_ssl === true
  if (form.value.mail_use_tls) form.value.mail_use_tls = form.value.mail_use_tls === 'true' || form.value.mail_use_tls === true
}

onMounted(async () => {
  if (!configs.value.notice || Object.keys(configs.value.notice).length === 0) {
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
    const updateData: Record<string, string> = {}
    Object.keys(form.value).forEach(key => {
      const fullKey = key.includes('.') ? key : `notice.${key}`
      updateData[fullKey] = String(form.value[key])
    })
    
    await systemStore.updateConfigs(updateData)
    ElMessage.success('通讯配置已更新')
  } catch (err) {
    ElMessage.error('更新保存失败')
  } finally {
    saving.value = false
  }
}

const testConnection = () => {
  ElMessage.warning('连接测试功能暂未开启，请先保存配置并查看后端日志记录')
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
  height: 100%;
}

.service-card :deep(.el-card__header) {
  padding: 16px 24px;
  background: #fafafa;
  border-bottom: 1px solid #f1f5f9;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-tit {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  color: #334155;
  font-size: 16px;
}

.icon {
  font-size: 20px;
}
.icon.mail { color: #3b82f6; }
.icon.sms { color: #8b5cf6; }

.help-text {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.service-status-info {
  margin-top: 24px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.status-item .label { color: #64748b; }
.status-item .value.success { color: #10b981; font-weight: 600; }

.form-actions-bar {
  margin-top: 32px;
  padding: 20px 24px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.main-actions {
  display: flex;
  gap: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #475569;
}
</style>

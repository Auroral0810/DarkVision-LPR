<template>
  <div class="app-container">
    <el-card header="第三方登录配置">
      <el-row :gutter="20">
        <!-- GitHub Login -->
        <el-col :span="12">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <span>GitHub 登录</span>
                <el-switch v-model="form.github_enabled" />
              </div>
            </template>
            <el-form label-position="top">
              <el-form-item label="Client ID">
                <el-input v-model="form.github_client_id" placeholder="GitHub OAuth App Client ID" />
              </el-form-item>
              <el-form-item label="Client Secret">
                <el-input v-model="form.github_client_secret" type="password" show-password placeholder="GitHub OAuth App Client Secret" />
              </el-form-item>
              <el-form-item label="回调地址 (Callback URL)">
                <el-input :model-value="callbackUrls.github" readonly />
                <div class="form-tip">请在 GitHub OAuth App 配置中填写此地址</div>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="loading" @click="handleSave('github')">保存 GitHub 配置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <!-- WeChat Login -->
        <el-col :span="12">
          <el-card shadow="never">
            <template #header>
              <div class="card-header">
                <span>微信登录</span>
                <el-switch v-model="form.wechat_enabled" />
              </div>
            </template>
            <el-form label-position="top">
              <el-form-item label="AppID">
                <el-input v-model="form.wechat_app_id" placeholder="微信开放平台 AppID" />
              </el-form-item>
              <el-form-item label="AppSecret">
                <el-input v-model="form.wechat_app_secret" type="password" show-password placeholder="微信开放平台 AppSecret" />
              </el-form-item>
              <el-form-item label="回调域名 (Callback Domain)">
                <el-input placeholder="请在微信开放平台配置授权回调域名" readonly />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="loading" @click="handleSave('wechat')">保存微信配置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    
    <el-alert
      title="配置提示"
      type="info"
      description="配置第三方登录前，请先在对应的开放平台完成应用申请。启用后，系统登录页面将自动出现对应的登录入口。"
      show-icon
      style="margin-top: 20px;"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, watch } from 'vue'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus'

const store = useSystemConfigStore()
const { configs, loading } = storeToRefs(store)

const form = reactive({
  github_enabled: false,
  github_client_id: '',
  github_client_secret: '',
  wechat_enabled: false,
  wechat_app_id: '',
  wechat_app_secret: ''
})

const callbackUrls = {
  github: `${window.location.origin}/api/v1/auth/github/callback`
}

function handleReset() {
  const login = configs.value.login || {}
  form.github_enabled = login.github_enabled === 'true'
  form.github_client_id = login.github_client_id || ''
  form.github_client_secret = login.github_client_secret || ''
  
  form.wechat_enabled = login.wechat_enabled === 'true'
  form.wechat_app_id = login.wechat_app_id || ''
  form.wechat_app_secret = login.wechat_app_secret || ''
}

async function handleSave(type: 'github' | 'wechat') {
  const updateData: Record<string, string> = {}
  
  if (type === 'github') {
    updateData['login.github_enabled'] = String(form.github_enabled)
    updateData['login.github_client_id'] = form.github_client_id
    updateData['login.github_client_secret'] = form.github_client_secret
  } else {
    updateData['login.wechat_enabled'] = String(form.wechat_enabled)
    updateData['login.wechat_app_id'] = form.wechat_app_id
    updateData['login.wechat_app_secret'] = form.wechat_app_secret
  }

  await store.updateConfigs(updateData)
}

onMounted(async () => {
  if (Object.keys(configs.value.login || {}).length === 0) {
    await store.fetchConfigs()
  }
  handleReset()
})

watch(() => configs.value.login, () => {
  handleReset()
}, { deep: true })
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>

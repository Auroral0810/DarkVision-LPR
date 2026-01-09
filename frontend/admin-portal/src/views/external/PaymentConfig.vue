<template>
  <div class="app-container">
    <el-tabs type="border-card">
      <!-- Alipay -->
      <el-tab-pane label="支付宝 (Alipay)">
        <el-form label-width="140px" style="max-width: 800px; margin-top: 20px;">
          <el-form-item label="启用支付宝">
            <el-switch v-model="form.alipay_enabled" />
          </el-form-item>
          <el-form-item label="AppID">
            <el-input v-model="form.alipay_app_id" placeholder="请输入支付宝 AppID" />
          </el-form-item>
          <el-form-item label="应用私钥 (Private Key)">
            <el-input v-model="form.alipay_private_key" type="textarea" :rows="4" placeholder="请输入应用私钥" />
          </el-form-item>
          <el-form-item label="支付宝公钥 (Public Key)">
            <el-input v-model="form.alipay_public_key" type="textarea" :rows="4" placeholder="请输入支付宝公钥" />
          </el-form-item>
          <el-form-item label="签名方式">
            <el-select v-model="form.alipay_sign_type" style="width: 100%;">
              <el-option label="RSA2" value="RSA2" />
              <el-option label="RSA" value="RSA" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleSave('alipay')">保存支付宝配置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- WeChat Pay -->
      <el-tab-pane label="微信支付 (WeChat Pay)">
        <el-form label-width="140px" style="max-width: 800px; margin-top: 20px;">
          <el-form-item label="启用微信支付">
            <el-switch v-model="form.wechat_enabled" />
          </el-form-item>
          <el-form-item label="AppID">
            <el-input v-model="form.wechat_app_id" placeholder="请输入微信开放平台 AppID" />
          </el-form-item>
          <el-form-item label="商户号 (MchID)">
            <el-input v-model="form.wechat_mch_id" placeholder="请输入微信支付商户号" />
          </el-form-item>
          <el-form-item label="API 密钥 (V2/V3 Key)">
            <el-input v-model="form.wechat_api_key" type="password" show-password placeholder="请输入 API 密钥" />
          </el-form-item>
          <el-form-item label="证书路径 (Cert Path)">
            <el-input v-model="form.wechat_cert_path" placeholder="例如: /path/to/apiclient_cert.p12" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="loading" @click="handleSave('wechat')">保存微信支付配置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <el-alert
      title="配置说明"
      type="warning"
      description="支付配置涉及敏感财务数据，请务必从官方支付平台获取正确的参数。配置不正确将导致订单无法正常支付。"
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
  // Alipay
  alipay_enabled: false,
  alipay_app_id: '',
  alipay_private_key: '',
  alipay_public_key: '',
  alipay_sign_type: 'RSA2',
  // WeChat
  wechat_enabled: false,
  wechat_app_id: '',
  wechat_mch_id: '',
  wechat_api_key: '',
  wechat_cert_path: ''
})

function handleReset() {
  const payment = configs.value.payment || {}
  form.alipay_enabled = payment.alipay_enabled === 'true'
  form.alipay_app_id = payment.alipay_app_id || ''
  form.alipay_private_key = payment.alipay_private_key || ''
  form.alipay_public_key = payment.alipay_public_key || ''
  form.alipay_sign_type = payment.alipay_sign_type || 'RSA2'
  
  form.wechat_enabled = payment.wechat_enabled === 'true'
  form.wechat_app_id = payment.wechat_app_id || ''
  form.wechat_mch_id = payment.wechat_mch_id || ''
  form.wechat_api_key = payment.wechat_api_key || ''
  form.wechat_cert_path = payment.wechat_cert_path || ''
}

async function handleSave(type: 'alipay' | 'wechat') {
  const updateData: Record<string, string> = {}
  
  if (type === 'alipay') {
    updateData['payment.alipay_enabled'] = String(form.alipay_enabled)
    updateData['payment.alipay_app_id'] = form.alipay_app_id
    updateData['payment.alipay_private_key'] = form.alipay_private_key
    updateData['payment.alipay_public_key'] = form.alipay_public_key
    updateData['payment.alipay_sign_type'] = form.alipay_sign_type
  } else {
    updateData['payment.wechat_enabled'] = String(form.wechat_enabled)
    updateData['payment.wechat_app_id'] = form.wechat_app_id
    updateData['payment.wechat_mch_id'] = form.wechat_mch_id
    updateData['payment.wechat_api_key'] = form.wechat_api_key
    updateData['payment.wechat_cert_path'] = form.wechat_cert_path
  }

  await store.updateConfigs(updateData)
}

onMounted(async () => {
  if (Object.keys(configs.value.payment || {}).length === 0) {
    await store.fetchConfigs()
  }
  handleReset()
})

watch(() => configs.value.payment, () => {
  handleReset()
}, { deep: true })
</script>

<style scoped>
.app-container {
  padding: 20px;
}
</style>

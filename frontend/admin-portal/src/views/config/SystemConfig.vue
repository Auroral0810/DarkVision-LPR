<template>
  <div class="app-container">
    <el-card v-loading="loading">
      <el-tabs v-model="activeTab" type="border-card" @tab-click="handleTabClick">
        <!-- 基础配置 -->
        <el-tab-pane label="基础配置" name="base">
          <el-form :model="formData.base" label-width="140px" style="max-width: 800px">
            <el-divider content-position="left">网站信息</el-divider>
            <el-form-item label="项目标题">
              <el-input v-model="formData.base['seo_title']" placeholder="例如: DarkVision-LPR - 高精度车牌识别系统" />
            </el-form-item>
            <el-form-item label="服务可用性">
              <el-input v-model="formData.base['service_availability']" placeholder="例如: 99.9%" />
            </el-form-item>
            <el-form-item label="企业客户数">
              <el-input v-model="formData.base['enterprise_clients']" placeholder="例如: 500+" />
            </el-form-item>

            <el-divider content-position="left">阿里云 OSS 存储</el-divider>
            <el-form-item label="OSS 域名">
              <el-input v-model="formData.base['oss_url']" placeholder="例如: https://lucky-yyf.oss-cn-beijing.aliyuncs.com" />
            </el-form-item>
            <el-form-item label="OSS Endpoint">
              <el-input v-model="formData.base['oss_endpoint']" placeholder="例如: oss-cn-beijing.aliyuncs.com" />
            </el-form-item>
            <el-form-item label="OSS Bucket">
              <el-input v-model="formData.base['oss_bucket_name']" />
            </el-form-item>
            <el-form-item label="OSS AccessKey">
              <el-input v-model="formData.base['oss_access_key_id']" />
            </el-form-item>
            <el-form-item label="OSS SecretKey">
              <el-input v-model="formData.base['oss_access_key_secret']" type="password" show-password />
            </el-form-item>

            <el-divider content-position="left">实名认证 (阿里云市场)</el-divider>
            <el-form-item label="Market AppCode">
              <el-input v-model="formData.base['aliyun_market_appcode']" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handleSave('base')">保存基础设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 识别参数 -->
        <el-tab-pane label="识别参数" name="recognition">
          <el-form :model="formData.recognition" label-width="140px" style="max-width: 800px">
            <el-form-item label="默认置信度">
              <el-slider v-model="recognitionParams.confidence" :min="0" :max="1" :step="0.05" show-input />
              <div class="help-block">检测结果低于此阈值将标记为低置信度</div>
            </el-form-item>
            <el-form-item label="模型版本">
              <el-select v-model="recognitionParams.modelVersion" placeholder="选择默认模型">
                <el-option label="v2.1.0 (最新稳定版)" value="v2.1.0" />
                <el-option label="v2.0.5" value="v2.0.5" />
                <el-option label="v1.8.0 (兼容版本)" value="v1.8.0" />
              </el-select>
            </el-form-item>
            <el-form-item label="并发限制">
              <el-input-number v-model="recognitionParams.maxThreads" :min="1" :max="64" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave('recognition')">保存识别参数</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 限额配置 -->
        <el-tab-pane label="限额配置" name="quota">
          <el-form :model="formData.quota" label-width="140px" style="max-width: 800px">
            <el-form-item label="免费用户每日限额">
              <el-input-number v-model="formData.quota['free_daily_limit']" :min="0" />
            </el-form-item>
            <el-form-item label="月卡VIP每日限额">
              <el-input-number v-model="formData.quota['vip_monthly_limit']" :min="0" />
            </el-form-item>
            <el-form-item label="年卡VIP每日限额">
              <el-input-number v-model="formData.quota['vip_yearly_limit']" :min="0" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave('quota')">保存限额配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 邮件 & 短信 -->
        <el-tab-pane label="邮件 & 短信" name="notice">
          <el-form :model="formData.notice" label-width="140px" style="max-width: 800px">
            <el-divider content-position="left">SMTP 邮件服务</el-divider>
            <el-form-item label="SMTP 主机">
              <el-input v-model="formData.notice['mail_host']" placeholder="例如: smtp.163.com" />
            </el-form-item>
            <el-form-item label="SMTP 端口">
              <el-input v-model="formData.notice['mail_port']" placeholder="例如: 465" />
            </el-form-item>
            <el-form-item label="SMTP 用户">
              <el-input v-model="formData.notice['mail_username']" />
            </el-form-item>
            <el-form-item label="SMTP 密码">
              <el-input v-model="formData.notice['mail_password']" type="password" show-password />
            </el-form-item>
            <el-form-item label="发件邮箱">
              <el-input v-model="formData.notice['mail_from']" />
            </el-form-item>
            <el-form-item label="发件人名称">
              <el-input v-model="formData.notice['mail_from_name']" />
            </el-form-item>
            <el-form-item label="安全选项">
              <el-checkbox v-model="formData.notice['mail_use_ssl']" label="使用 SSL" />
              <el-checkbox v-model="formData.notice['mail_use_tls']" label="使用 TLS" />
            </el-form-item>

            <el-divider content-position="left">短信服务 (SMS)</el-divider>
            <el-form-item label="服务提供商">
              <el-input v-model="formData.notice['sms_provider']" disabled />
            </el-form-item>
            <el-form-item label="SMS 用户">
              <el-input v-model="formData.notice['sms_user']" />
            </el-form-item>
            <el-form-item label="SMS 密钥">
              <el-input v-model="formData.notice['sms_password']" type="password" show-password />
            </el-form-item>
            <el-form-item label="短信签名">
              <el-input v-model="formData.notice['sms_sign_name']" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave('notice')">保存通讯配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const systemStore = useSystemConfigStore()
const { configs, loading } = storeToRefs(systemStore)

const activeTab = ref('base')

// 本地表单数据模型
const formData = reactive({
  base: {} as any,
  recognition: {} as any,
  quota: {} as any,
  notice: {} as any
})

// 特殊处理 JSON 类型或复杂项（如识别参数可能是 JSON 字符串存储，也可能是分项）
const recognitionParams = reactive({
  confidence: 0.8,
  modelVersion: 'v2.1.0',
  maxThreads: 8
})

// 初始化数据
const initFormData = () => {
  formData.base = { ...configs.value.base }
  formData.quota = { ...configs.value.quota }
  formData.notice = { ...configs.value.notice }
  // 转换布尔值字符串
  if (formData.notice.mail_use_ssl) formData.notice.mail_use_ssl = formData.notice.mail_use_ssl === 'true'
  if (formData.notice.mail_use_tls) formData.notice.mail_use_tls = formData.notice.mail_use_tls === 'true'
  
  // 识别参数可能作为单独 key 存储在 recognition 分组下，或者作为一个 recognition.params JSON
  if (configs.value.recognition) {
    formData.recognition = { ...configs.value.recognition }
    if (formData.recognition.confidence) recognitionParams.confidence = parseFloat(formData.recognition.confidence)
    if (formData.recognition.modelVersion) recognitionParams.modelVersion = formData.recognition.modelVersion
    if (formData.recognition.maxThreads) recognitionParams.maxThreads = parseInt(formData.recognition.maxThreads)
  }
}

onMounted(async () => {
  await systemStore.fetchConfigs()
  initFormData()
  
  // 根据路由 query 切换 tab
  if (route.query.tab) {
    activeTab.value = route.query.tab as string
  }
})

// 监听 store 数据变化（同步到本地表单）
watch(configs, () => {
  initFormData()
}, { deep: true })

const handleTabClick = (tab: any) => {
  // 同步到 URL
  router.push({ query: { tab: tab.props.name } })
}

const handleSave = async (group: string) => {
  const updateData: Record<string, any> = {}
  let source = formData[group as keyof typeof formData]
  
  // 特殊处理 recognition 
  if (group === 'recognition') {
    updateData[`recognition.confidence`] = recognitionParams.confidence.toString()
    updateData[`recognition.modelVersion`] = recognitionParams.modelVersion
    updateData[`recognition.maxThreads`] = recognitionParams.maxThreads.toString()
  } else {
    // 通用处理：将 key 加上前缀
    Object.keys(source).forEach(key => {
      // 如果 key 已经包含前缀（老数据兼容性处理在 Service 层完成，这里补充前缀）
      const fullKey = key.includes('.') ? key : `${group}.${key}`
      updateData[fullKey] = source[key]
    })
  }

  await systemStore.updateConfigs(updateData)
}
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.help-block {
  font-size: 13px;
  color: #909399;
  margin-top: 5px;
}
</style>

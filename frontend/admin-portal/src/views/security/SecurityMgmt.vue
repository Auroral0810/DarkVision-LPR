<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- IP 规则管理 -->
      <el-tab-pane label="IP 黑白名单" name="ip">
        <div class="tab-header">
          <div class="header-left">
            <el-radio-group v-model="ruleTypeFilter" @change="fetchIpRules">
              <el-radio-button label="">全部</el-radio-button>
              <el-radio-button label="allow">白名单</el-radio-button>
              <el-radio-button label="deny">黑名单</el-radio-button>
            </el-radio-group>
          </div>
          <el-button type="primary" icon="Plus" @click="handleAddRule">添加规则</el-button>
        </div>

        <el-table v-loading="loadingIp" :data="ipRules" border style="width: 100%">
          <el-table-column prop="ip_address" label="IP 地址" width="180" align="center" />
          <el-table-column prop="type" label="类型" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="row.type === 'allow' ? 'success' : 'danger'">
                {{ row.type === 'allow' ? '白名单' : '黑名单' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" min-width="200" show-overflow-tooltip />
          <el-table-column prop="created_at" label="创建时间" width="180" align="center">
            <template #default="{ row }">
              {{ formatTime(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="center">
            <template #default="{ row }">
              <el-button type="danger" link @click="handleDeleteRule(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 安全配置管理 -->
      <el-tab-pane label="安全策略配置" name="config">
        <el-form :model="config" label-width="160px" class="config-form" v-loading="loadingConfig">
          <el-divider content-position="left">登录安全</el-divider>
          <el-form-item label="登录上限重试次数">
            <el-input-number v-model="config.login_fail_limit" :min="1" :max="20" />
            <span class="form-tip">连续登录失败达到次数后将锁定</span>
          </el-form-item>
          <el-form-item label="登录锁定时间(分钟)">
            <el-input-number v-model="config.login_lock_duration" :min="1" :max="1440" />
            <span class="form-tip">账号锁定的时长</span>
          </el-form-item>

          <el-divider content-position="left">访问控制</el-divider>
          <el-form-item label="API 访问频率限制">
            <el-input-number v-model="config.api_rate_limit" :min="10" :max="10000" />
            <span class="form-tip">单 IP 每分钟允许的请求次数</span>
          </el-form-item>
          <el-form-item label="开启 IP 白名单验证">
            <el-switch v-model="config.enable_ip_whitelist" />
            <span class="form-tip">开启后，只有白名单中的 IP 可以访问系统</span>
          </el-form-item>

          <el-form-item style="margin-top: 40px">
            <el-button type="primary" @click="handleSaveConfig" :loading="saving">保存配置</el-button>
            <el-button @click="fetchConfig">重置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <!-- 添加 IP 规则弹窗 -->
    <el-dialog v-model="ruleDialogVisible" title="添加 IP 规则" width="450px">
      <el-form :model="ruleForm" ref="ruleFormRef" :rules="ruleRules" label-width="80px">
        <el-form-item label="IP 地址" prop="ip_address">
          <el-input v-model="ruleForm.ip_address" placeholder="例如: 192.168.1.1" />
        </el-form-item>
        <el-form-item label="规则类型" prop="type">
          <el-select v-model="ruleForm.type" style="width: 100%">
            <el-option label="白名单" value="allow" />
            <el-option label="黑名单" value="deny" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="ruleForm.remark" type="textarea" placeholder="规则备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ruleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRule" :loading="submittingRule">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'
import SystemAPI, { IpRule, SecurityConfig } from '@/api/system-api'

const activeTab = ref('ip')
const loadingIp = ref(false)
const ipRules = ref<IpRule[]>([])
const ruleTypeFilter = ref('')

const fetchIpRules = async () => {
  loadingIp.value = true
  try {
    ipRules.value = await SystemAPI.getIpRules(ruleTypeFilter.value)
  } finally {
    loadingIp.value = false
  }
}

const handleDeleteRule = (row: IpRule) => {
  ElMessageBox.confirm(`确定要删除 IP 规则 ${row.ip_address} 吗?`, '警告', {
    type: 'warning'
  }).then(async () => {
    await SystemAPI.deleteIpRule(row.id)
    ElMessage.success('删除成功')
    fetchIpRules()
  })
}

// 添加规则逻辑
const ruleDialogVisible = ref(false)
const submittingRule = ref(false)
const ruleFormRef = ref()
const ruleForm = reactive({
  ip_address: '',
  type: 'deny',
  remark: ''
})
const ruleRules = {
  ip_address: [{ required: true, message: '请输入 IP 地址', trigger: 'blur' }],
  type: [{ required: true, message: '请选择规则类型', trigger: 'change' }]
}

const currentLog = ref<any | null>(null) // Assuming OperationLog is similar to 'any' for this context
const detailsVisible = ref(false)

const viewDetail = (row: any) => { // Assuming OperationLog is similar to 'any' for this context
  currentLog.value = row
  detailsVisible.value = true
}

const handleAddRule = () => {
  ruleForm.ip_address = ''
  ruleForm.type = 'deny'
  ruleForm.remark = ''
  ruleDialogVisible.value = true
}

const submitRule = async () => {
  await ruleFormRef.value.validate()
  submittingRule.value = true
  try {
    await SystemAPI.addIpRule(ruleForm as any)
    ElMessage.success('添加成功')
    ruleDialogVisible.value = false
    fetchIpRules()
  } finally {
    submittingRule.value = false
  }
}

// 安全配置逻辑
const loadingConfig = ref(false)
const saving = ref(false)
const config = reactive<SecurityConfig>({
  login_fail_limit: 5,
  login_lock_duration: 30,
  api_rate_limit: 100,
  enable_ip_whitelist: false
})

const fetchConfig = async () => {
  loadingConfig.value = true
  try {
    const data = await SystemAPI.getSecurityConfig()
    Object.assign(config, data)
  } finally {
    loadingConfig.value = false
  }
}

const handleSaveConfig = async () => {
  saving.value = true
  try {
    await SystemAPI.updateSecurityConfig(config)
    ElMessage.success('保存成功')
  } finally {
    saving.value = false
  }
}

const formatTime = (time: string) => dayjs(time).format('YYYY-MM-DD HH:mm:ss')

onMounted(() => {
  fetchIpRules()
  fetchConfig()
})
</script>

<style scoped>
.app-container {
  padding: 20px;
}
.tab-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.config-form {
  max-width: 600px;
  padding: 20px;
}
.form-tip {
  display: block;
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  margin-top: 5px;
}
</style>

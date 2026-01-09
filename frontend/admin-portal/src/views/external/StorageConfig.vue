<template>
  <div class="app-container">
    <el-card header="对象存储 (OSS) 配置">
      <el-form label-width="140px" style="max-width: 800px; margin-top: 20px;">
        <el-form-item label="存储类型">
          <el-radio-group v-model="form.type">
            <el-radio label="aliyun">阿里云 OSS</el-radio>
            <el-radio label="minio">MinIO (内置)</el-radio>
            <el-radio label="tencent">腾讯云 COS</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="Endpoint">
          <el-input v-model="form.endpoint" placeholder="例如: oss-cn-beijing.aliyuncs.com" />
        </el-form-item>
        
        <el-form-item label="AccessKey ID">
          <el-input v-model="form.ak" type="password" show-password placeholder="请输入 AccessKey ID" />
        </el-form-item>
        
        <el-form-item label="AccessKey Secret">
          <el-input v-model="form.sk" type="password" show-password placeholder="请输入 AccessKey Secret" />
        </el-form-item>
        
        <el-form-item label="Bucket 名称">
          <el-input v-model="form.bucket" placeholder="请输入存储桶名称" />
        </el-form-item>
        
        <el-form-item label="外网预览域名">
          <el-input v-model="form.domain" placeholder="例如: https://bucket.oss-cn-beijing.aliyuncs.com" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSave">保存配置</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-alert
        title="配置提示"
        type="info"
        description="存储配置用于系统识别结果图片的保存和管理。修改配置后，请确保新的存储服务已正确开启相应的 Bucket 权限。"
        show-icon
        style="margin-top: 20px;"
      />
    </el-card>
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
  type: 'aliyun',
  endpoint: '',
  ak: '',
  sk: '',
  bucket: '',
  domain: ''
})

function handleReset() {
  const oss = configs.value.oss || {}
  form.type = oss.type || 'aliyun'
  form.endpoint = oss.endpoint || ''
  form.ak = oss.ak || ''
  form.sk = oss.sk || ''
  form.bucket = oss.bucket || ''
  form.domain = oss.domain || ''
}

async function handleSave() {
  await store.updateConfigs({
    'oss.type': form.type,
    'oss.endpoint': form.endpoint,
    'oss.ak': form.ak,
    'oss.sk': form.sk,
    'oss.bucket': form.bucket,
    'oss.domain': form.domain
  })
}

onMounted(async () => {
  if (Object.keys(configs.value.oss || {}).length === 0) {
    await store.fetchConfigs()
  }
  handleReset()
})

// Watch for store changes to update local form if needed
watch(() => configs.value.oss, () => {
  handleReset()
}, { deep: true })
</script>

<style scoped>
.app-container {
  padding: 20px;
}
</style>

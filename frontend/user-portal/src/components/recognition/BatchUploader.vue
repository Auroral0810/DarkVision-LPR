<template>
  <div class="batch-uploader">
    <div class="header">
      <div class="info">
        <h3>批量识别</h3>
        <p>VIP 尊享功能，支持单次最多 {{ userStore.quota.maxBatch }} 张图片</p>
      </div>
      <div class="actions">
        <el-button type="primary" :disabled="!files.length" @click="startBatch">开始处理</el-button>
        <el-button @click="files = []" :disabled="!files.length">清空</el-button>
      </div>
    </div>

    <el-upload
      v-model:file-list="files"
      class="upload-demo"
      action="#"
      multiple
      :auto-upload="false"
      list-type="picture"
      :limit="userStore.quota.maxBatch"
    >
      <el-button type="primary">选择多张图片</el-button>
      <template #tip>
        <div class="el-upload__tip">
          支持 JPG/PNG，单次最多 {{ userStore.quota.maxBatch }} 张
        </div>
      </template>
    </el-upload>
    
    <div class="batch-progress" v-if="processing">
      <h4>处理进度 ({{ processedCount }} / {{ files.length }})</h4>
      <el-progress :percentage="percentage" :status="percentage === 100 ? 'success' : ''" />
    </div>
    
    <div class="results-table" v-if="results.length">
      <el-table :data="results" style="width: 100%" height="400">
        <el-table-column prop="name" label="文件名" width="180" />
        <el-table-column prop="plate" label="识别结果" width="180" />
        <el-table-column prop="confidence" label="置信度" />
        <el-table-column prop="status" label="状态">
          <template #default>
            <el-tag type="success">完成</el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <div style="margin-top: 16px; text-align: right">
        <el-button type="success" plain>导出 Excel 报表</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const files = ref<any[]>([])
const results = ref<any[]>([])
const processing = ref(false)
const processedCount = ref(0)

const percentage = computed(() => {
  if (!files.value.length) return 0
  return Math.round((processedCount.value / files.value.length) * 100)
})

const startBatch = async () => {
  if (files.value.length === 0) return
  
  processing.value = true
  results.value = []
  processedCount.value = 0
  
  for (const file of files.value) {
    await new Promise(resolve => setTimeout(resolve, 500)) // Simulate network
    results.value.push({
      name: file.name,
      plate: '沪A·' + Math.floor(Math.random() * 90000 + 10000),
      confidence: '98.5%',
      status: 'done'
    })
    processedCount.value++
  }
  
  ElMessage.success('批量处理完成')
  processing.value = false
}
</script>

<style scoped lang="scss">
.batch-uploader {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  h3 {
    margin: 0 0 4px;
  }
  
  p {
    margin: 0;
    color: #64748b;
    font-size: 14px;
  }
}

.batch-progress {
  margin: 24px 0;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
}
</style>

<template>
  <div class="single-uploader">
    <div class="upload-area" v-if="!result">
      <el-upload
        class="upload-demo"
        drag
        action="#"
        :auto-upload="false"
        :on-change="handleFileChange"
        accept=".jpg,.png,.bmp"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            jpg/png files with a size less than 5MB
          </div>
        </template>
      </el-upload>
    </div>

    <div class="result-area" v-else>
      <div class="image-preview">
        <el-image :src="imageUrl" fit="contain" style="max-height: 400px; width: 100%" />
      </div>
      
      <div class="result-details">
        <h3>识别结果</h3>
        <div class="result-card">
          <div class="plate-number">{{ result.plate }}</div>
          <div class="meta-info">
            <el-tag :type="getPlateColor(result.type)">{{ result.type }}</el-tag>
            <span class="confidence">置信度: {{ result.confidence }}%</span>
          </div>
        </div>
        
        <el-button type="primary" plain @click="reset">识别下一张</el-button>
      </div>
    </div>
    
    <el-dialog v-model="loading" title="Processing" width="30%" center :show-close="false">
      <div style="text-align: center">
        <el-progress type="circle" :percentage="progress" />
        <p>正在识别中...</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const progress = ref(0)
const imageUrl = ref('')
const result = ref<any>(null)

const handleFileChange = (file: any) => {
  imageUrl.value = URL.createObjectURL(file.raw)
  simulateRecognition()
}

const simulateRecognition = () => {
  loading.value = true
  progress.value = 0
  
  const timer = setInterval(() => {
    progress.value += 10
    if (progress.value >= 100) {
      clearInterval(timer)
      loading.value = false
      result.value = {
        plate: '京A·' + Math.floor(Math.random() * 90000 + 10000),
        type: Math.random() > 0.5 ? '蓝牌' : '绿牌',
        confidence: (90 + Math.random() * 9).toFixed(1)
      }
      ElMessage.success('识别成功')
    }
  }, 200)
}

const reset = () => {
  result.value = null
  imageUrl.value = ''
}

const getPlateColor = (type: string) => {
  if (type.includes('蓝')) return ''
  if (type.includes('绿')) return 'success'
  if (type.includes('黄')) return 'warning'
  return 'info'
}
</script>

<style scoped lang="scss">
.single-uploader {
  max-width: 800px;
  margin: 0 auto;
}

.result-area {
  display: flex;
  gap: 32px;
  
  .image-preview {
    flex: 1;
    background: #000;
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .result-details {
    width: 300px;
    
    h3 {
      margin-top: 0;
    }
    
    .result-card {
      background: white;
      padding: 24px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      margin-bottom: 24px;
      text-align: center;
      
      .plate-number {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
        font-family: monospace;
        letter-spacing: 2px;
        margin-bottom: 16px;
        background: #f1f5f9;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #0f172a;
      }
      
      .meta-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }
  }
}
</style>

<template>
  <div class="single-uploader">
    <el-card class="main-card" shadow="hover">
      <div class="content-wrapper">
        <!-- Left: Upload Area -->
        <div class="upload-section">
          <div 
            class="upload-area" 
            :class="{ 'has-image': imageUrl, 'is-dragover': isDragOver }"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleDrop"
            @click="triggerUpload"
          >
            <input 
              type="file" 
              ref="fileInput" 
              style="display: none" 
              accept=".jpg,.jpeg,.png,.bmp"
              @change="handleFileSelect" 
            />
            
            <template v-if="imageUrl">
              <el-image :src="previewUrl" fit="contain" class="preview-image" />
              <div class="upload-overlay">
                <el-icon><Refresh /></el-icon>
                <span>点击更换图片</span>
              </div>
            </template>
            
            <template v-else>
              <div class="upload-placeholder">
                <el-icon class="upload-icon"><UploadFilled /></el-icon>
                <div class="upload-text">拖拽图片到此处 或 <em>点击上传</em></div>
                <div class="upload-tip">支持 JPG/PNG/BMP，大小不超过 5MB</div>
              </div>
            </template>
          </div>
        </div>

        <!-- Right: Control & Result -->
        <div class="control-section">
          <div class="header">
            <h3>识别控制台</h3>
            <el-tag v-if="connectionStatus === 'connected'" type="success" size="small" effect="plain">实时连接</el-tag>
            <el-tag v-else-if="connectionStatus === 'connecting'" type="warning" size="small" effect="plain">连接中...</el-tag>
          </div>

          <div class="status-panel">
            <!-- Initial State -->
            <div v-if="!imageUrl" class="empty-state">
              <el-empty description="请先上传图片" :image-size="100" />
            </div>

            <!-- Ready State -->
            <div v-else-if="!isProcessing && !result" class="ready-state">
              <div class="file-info">
                <el-icon><Picture /></el-icon>
                <span>{{ fileName }}</span>
              </div>
              <el-button 
                type="primary" 
                size="large" 
                class="start-btn" 
                @click="startRecognition"
                :loading="uploading"
              >
                开始识别
              </el-button>
            </div>

            <!-- Processing State -->
            <div v-else-if="isProcessing" class="processing-state">
              <el-progress 
                type="dashboard" 
                :percentage="progress" 
                :color="progressColor"
              >
                <template #default="{ percentage }">
                  <span class="percentage-value">{{ percentage }}%</span>
                  <span class="percentage-label">{{ progressStatus }}</span>
                </template>
              </el-progress>
              <div class="progress-steps">
                <el-steps direction="vertical" :active="activeStep" finish-status="success">
                  <el-step title="图片上传" />
                  <el-step title="车牌检测" />
                  <el-step title="图像增强" />
                  <el-step title="字符识别" />
                </el-steps>
              </div>
            </div>

            <!-- Result State -->
            <div v-else-if="result" class="result-state">
              <div class="plate-display" :class="getPlateColor(result.type)">
                {{ result.plate }}
              </div>
              
              <div class="result-grid">
                <div class="grid-item">
                  <label>车牌类型</label>
                  <span>{{ getPlateTypeText(result.type) }}</span>
                </div>
                <div class="grid-item">
                  <label>置信度</label>
                  <span class="confidence">{{ result.confidence }}%</span>
                </div>
              </div>

              <el-divider />
              
              <el-button @click="reset" plain class="reset-btn">识别下一张</el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import { UploadFilled, Refresh, Picture } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { uploadImage, startRecognitionTask } from '@/api/recognition'

// State
const fileInput = ref<HTMLInputElement | null>(null)
const isDragOver = ref(false)
const uploading = ref(false)
const imageUrl = ref('') // OSS URL
const previewUrl = ref('') // Local/OSS Preview URL
const fileName = ref('')

const isProcessing = ref(false)
const progress = ref(0)
const progressStatus = ref('准备中')
const connectionStatus = ref('disconnected')
const activeStep = ref(0)

const result = ref<any>(null)
let ws: WebSocket | null = null

// Colors
const progressColor = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 },
]

// Actions
const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    processFile(input.files[0])
  }
}

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    processFile(event.dataTransfer.files[0])
  }
}

const processFile = async (file: File) => {
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请上传图片文件')
    return
  }
  
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 5MB')
    return
  }

  // Reset
  resetState()
  
  // Preview (先用本地URL)
  previewUrl.value = URL.createObjectURL(file)
  fileName.value = file.name
  uploading.value = true
  
  try {
    const res = await uploadImage(file)
    // 保存原始OSS URL用于识别
    imageUrl.value = res.data.url
    // 如果有签名URL，用于预览显示
    if (res.data.signed_url) {
      previewUrl.value = res.data.signed_url
    }
    ElMessage.success('图片上传成功')
  } catch (error) {
    console.error(error)
    ElMessage.error('上传失败')
    imageUrl.value = ''
  } finally {
    uploading.value = false
  }
}

const startRecognition = async () => {
  if (!imageUrl.value) return
  
  isProcessing.value = true
  progress.value = 0
  progressStatus.value = '请求任务...'
  activeStep.value = 0
  
  try {
    const res = await startRecognitionTask(imageUrl.value)
    const taskUuid = res.data?.task_uuid || res.task_uuid
    
    if (taskUuid) {
      connectWebSocket(taskUuid)
    } else {
      throw new Error('No task UUID returned')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '启动识别失败')
    isProcessing.value = false
  }
}

const connectWebSocket = (taskUuid: string) => {
  connectionStatus.value = 'connecting'
  
  // Connect directly to backend WebSocket (bypass Vite proxy)
  const wsUrl = `ws://localhost:8000/api/v1/recognition/ws/${taskUuid}`
  
  console.log('Connecting to WebSocket:', wsUrl)
  ws = new WebSocket(wsUrl)
  
  ws.onopen = () => {
    connectionStatus.value = 'connected'
    console.log('WS Connected successfully')
  }
  
  ws.onmessage = (event) => {
    try {
      const data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data
      console.log('WS Message received:', data)
      handleWsMessage(data)
    } catch (e) {
      if (typeof event.data === 'string') {
          console.warn('WS received non-JSON message:', event.data)
      } else {
          console.error('WS Parse error', e)
      }
    }
  }
  
  ws.onerror = (error) => {
    console.error('WS Error', error)
    connectionStatus.value = 'error'
    if (isProcessing.value) {
        ElMessage.error('WebSocket 连接失败')
        isProcessing.value = false
    }
  }
  
  ws.onclose = (event) => {
    console.log('WS Closed', event.code, event.reason)
    connectionStatus.value = 'disconnected'
  }
}

const handleWsMessage = (msg: any) => {
  if (msg.type === 'progress') {
    progress.value = Math.floor(msg.progress)
    progressStatus.value = msg.message || '处理中...'
    
    // Update step based on progress or status
    if (msg.status === 'downloading') activeStep.value = 1
    else if (msg.status === 'detecting') activeStep.value = 2
    else if (msg.status === 'enhancing') activeStep.value = 3
    else if (msg.status === 'recognizing') activeStep.value = 4
    
  } else if (msg.type === 'result') {
    progress.value = 100
    progressStatus.value = '识别成功'
    activeStep.value = 4
    
    // Ensure data is set before changing view state
    if (msg.data) {
        result.value = msg.data
    }
    
    // Give a small delay for the progress bar to look complete
    setTimeout(() => {
      isProcessing.value = false
      ElMessage.success('识别完成')
      closeWs()
    }, 500)
  } else if (msg.type === 'error') {
    isProcessing.value = false
    ElMessage.error(msg.message || '识别出错')
    closeWs()
  }
}

const closeWs = () => {
  if (ws) {
    ws.close()
    ws = null
  }
}

const resetState = () => {
  result.value = null
  isProcessing.value = false
  progress.value = 0
  activeStep.value = 0
  closeWs()
}

const reset = () => {
  resetState()
  imageUrl.value = ''
  previewUrl.value = ''
  fileName.value = ''
}

const getPlateColor = (type: string) => {
  // Map backend type to CSS class
  if (!type) return 'blue'
  if (type.includes('green') || type.includes('新能源')) return 'green'
  if (type.includes('yellow') || type.includes('黄')) return 'yellow'
  if (type.includes('white') || type.includes('白')) return 'white'
  return 'blue'
}

const getPlateTypeText = (type: string) => {
  const map: Record<string, string> = {
    'blue': '蓝牌 (普通燃油)',
    'green': '绿牌 (新能源)',
    'yellow': '黄牌 (大型车辆)',
    'white': '白牌 (警/军)',
  }
  return map[type] || type || '未知'
}

onBeforeUnmount(() => {
  closeWs()
})
</script>

<style scoped lang="scss">
.single-uploader {
  max-width: 1000px;
  margin: 0 auto;
}

.main-card {
  border-radius: 16px;
  overflow: hidden;
  
  :deep(.el-card__body) {
    padding: 0;
  }
}

.content-wrapper {
  display: flex;
  min-height: 500px;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.upload-section {
  flex: 1.5;
  background: #f8fafc;
  padding: 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-right: 1px solid #e2e8f0;
  
  .upload-area {
    background: white;
    border: 2px dashed #cbd5e1;
    border-radius: 16px;
    height: 100%;
    min-height: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    
    &:hover, &.is-dragover {
      border-color: #3b82f6;
      background: #eff6ff;
    }
    
    &.has-image {
      border-style: solid;
      border-color: transparent;
      padding: 0;
      background: black;
    }
    
    .upload-placeholder {
      text-align: center;
      padding: 20px;
      
      .upload-icon {
        font-size: 64px;
        color: #94a3b8;
        margin-bottom: 16px;
      }
      
      .upload-text {
        font-size: 16px;
        color: #334155;
        margin-bottom: 8px;
        
        em {
          color: #3b82f6;
          font-style: normal;
          font-weight: 600;
        }
      }
      
      .upload-tip {
        font-size: 12px;
        color: #94a3b8;
      }
    }
    
    .preview-image {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
    
    .upload-overlay {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.6);
      color: white;
      padding: 8px 16px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      opacity: 0;
      transition: opacity 0.3s;
    }
    
    &:hover .upload-overlay {
      opacity: 1;
    }
  }
}

.control-section {
  flex: 1;
  padding: 32px;
  display: flex;
  flex-direction: column;
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    
    h3 {
      margin: 0;
      font-size: 18px;
      color: #0f172a;
    }
  }
  
  .status-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
}

.ready-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  margin-top: 40px;
  
  .file-info {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #64748b;
    font-size: 14px;
    background: #f1f5f9;
    padding: 8px 16px;
    border-radius: 8px;
  }
  
  .start-btn {
    width: 100%;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
  }
}

.processing-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  
  .percentage-value {
    display: block;
    font-size: 24px;
    font-weight: 700;
    color: #334155;
  }
  
  .percentage-label {
    display: block;
    font-size: 12px;
    color: #94a3b8;
    margin-top: 4px;
  }
  
  .progress-steps {
    width: 100%;
    padding-left: 20px;
  }
}

.result-state {
  text-align: center;
  animation: slideUp 0.5s ease-out;
  
  .plate-display {
    font-family: monospace;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 16px 24px;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 32px;
    border: 2px solid #000;
    
    &.blue {
      background: #1989fa;
      color: white;
      border-color: #1989fa;
    }
    &.green {
      background: linear-gradient(180deg, #f0f9eb 0%, #e1f3d8 100%);
      color: #0f172a;
      border-color: #529b2e;
      box-shadow: 0 0 10px rgba(82, 155, 46, 0.2);
    }
    &.yellow {
      background: #fdf6ec;
      color: #0f172a;
      border-color: #e6a23c;
    }
  }
  
  .result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin-bottom: 24px;
    
    .grid-item {
      display: flex;
      flex-direction: column;
      gap: 8px;
      
      label {
        font-size: 12px;
        color: #94a3b8;
      }
      
      span {
        font-size: 16px;
        font-weight: 600;
        color: #334155;
        
        &.confidence {
          color: #10b981;
        }
      }
    }
  }
  
  .reset-btn {
    width: 100%;
    margin-top: 16px;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

<template>
  <div class="batch-wrapper">
    <!-- Header -->
    <div class="batch-header">
      <div class="header-content">
        <h3>批量识别</h3>
        <p>VIP 尊享功能，支持单次最多 50 张图片批量处理</p>
      </div>
      <div class="header-actions">
        <el-button 
          type="primary" 
          size="large"
          :disabled="!canStart" 
          :loading="status === 'uploading' || status === 'processing'"
          @click="startBatch"
        >
          {{ getActionButtonText }}
        </el-button>
        <el-button @click="reset" :disabled="status !== 'idle' && status !== 'finished'">清空列表</el-button>
      </div>
    </div>

    <!-- Upload Area (Drag & Drop) -->
    <div 
      class="upload-area"
      :class="{ 'is-dragover': isDragOver, 'has-files': files.length > 0 }"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @drop.prevent="handleDrop"
      v-if="status === 'idle' || files.length === 0"
    >
      <input 
        type="file" 
        ref="fileInput" 
        style="display: none" 
        multiple
        accept=".jpg,.jpeg,.png,.bmp"
        @change="handleFileSelect" 
      />
      <div class="upload-content" @click="triggerFileSelect">
        <el-icon class="upload-icon"><UploadFilled /></el-icon>
        <div class="upload-text">拖拽图片到此处 或 <em>点击选择图片</em></div>
        <div class="upload-tip">支持 JPG/PNG，单次最多 50 张</div>
      </div>
    </div>

    <!-- Overall Progress -->
    <div class="progress-bar-container" v-if="status !== 'idle' && files.length > 0">
      <div class="progress-info">
        <span class="status-text">{{ statusText }}</span>
        <span class="count-text">{{ completedCount }} / {{ files.length }}</span>
      </div>
      <el-progress 
        :percentage="overallPercentage" 
        :status="status === 'finished' ? 'success' : ''"
        :stroke-width="12"
        striped
        :striped-flow="status === 'processing'"
      />
    </div>

    <!-- File Grid (During Processing or before clearing) -->
    <div class="file-grid" v-if="(status === 'idle' || status === 'uploading' || status === 'processing') && files.length > 0">
      <div 
        v-for="(file, index) in files" 
        :key="file.id" 
        class="file-card"
        :class="file.status"
      >
        <div class="card-image">
          <el-image :src="file.previewUrl" fit="cover" loading="lazy" />
          <div class="status-overlay" v-if="file.status !== 'pending'">
             <el-icon v-if="file.status === 'success'" class="success-icon"><CircleCheckFilled /></el-icon>
             <el-icon v-if="file.status === 'error'" class="error-icon"><CircleCloseFilled /></el-icon>
             <el-loading v-if="file.status === 'uploading' || file.status === 'processing'" class="loading-icon" />
          </div>
        </div>
        
        <div class="card-info">
          <div class="file-name" :title="file.file.name">{{ file.file.name }}</div>
          
          <!-- Result -->
          <div class="result-box" v-if="file.result">
             <div class="plate-number" :class="getPlateColor(file.result.type)">
               {{ file.result.plate }}
             </div>
             <div class="confidence">置信度: {{ file.result.confidence }}%</div>
          </div>
          
          <!-- Error -->
          <div class="error-msg" v-else-if="file.error">
            {{ file.error }}
          </div>
          
          <!-- State -->
          <div class="state-tag" v-else>
             <el-tag size="small" :type="getStatusType(file.status)">{{ getStatusText(file.status) }}</el-tag>
          </div>
        </div>
        
        <!-- Remove Button (Only in Idle) -->
        <div class="remove-btn" v-if="status === 'idle'" @click.stop="removeFile(index)">
          <el-icon><Close /></el-icon>
        </div>
      </div>
      
      <!-- Add More Card -->
      <div 
        class="add-card" 
        @click="triggerFileSelect"
        v-if="status === 'idle' && files.length < 50"
      >
        <el-icon><Plus /></el-icon>
        <span>添加图片</span>
      </div>
    </div>
    
    <!-- Results Table (After Completed) -->
    <div class="results-container" v-if="status === 'finished'">
      <div class="results-header">
        <h4>识别结果 (成功: {{ successCount }}, 失败: {{ failedCount }})</h4>
        <!-- Export Placeholder -->
        <el-button type="success" plain @click="ElMessage.info('导出功能开发中')">导出结果</el-button>
      </div>
      
      <el-table :data="files" style="width: 100%" border stripe>
        <el-table-column label="图片" width="120">
          <template #default="scope">
            <el-image 
              style="width: 80px; height: 50px; border-radius: 4px;" 
              :src="scope.row.previewUrl" 
              :preview-src-list="[scope.row.previewUrl]"
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column label="文件名" prop="file.name" show-overflow-tooltip />
        <el-table-column label="识别车牌" width="150">
          <template #default="scope">
             <span v-if="scope.row.result" class="plate-text" :class="scope.row.result.type">
               {{ scope.row.result.plate }}
             </span>
             <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="车牌类型" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.result" :type="(getPlateTypeColor(scope.row.result.type) as 'primary'|'success'|'warning'|'info'|'danger')" effect="light">
              {{ formatPlateType(scope.row.result.type) }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="置信度" width="120">
          <template #default="scope">
            <span v-if="scope.row.result" class="confidence-text">
               {{ scope.row.result.confidence }}%
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
           <template #default="scope">
             <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column label="备注" min-width="150" show-overflow-tooltip>
           <template #default="scope">
             <span class="error-text" v-if="scope.row.error">{{ scope.row.error }}</span>
             <span v-else>-</span>
           </template>
        </el-table-column>
      </el-table>
      
      <div class="restart-action">
         <el-button type="primary" size="large" @click="reset">处理下一批</el-button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import { UploadFilled, CircleCheckFilled, CircleCloseFilled, Close, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { uploadImage, startBatchRecognitionTask } from '@/api/recognition'

// Types
interface BatchFile {
  id: string
  file: File
  previewUrl: string
  status: 'pending' | 'uploading' | 'uploaded' | 'processing' | 'success' | 'error'
  ossUrl?: string
  result?: {
    plate: string
    type?: string
    confidence: string
  }
  error?: string
}

type BatchStatus = 'idle' | 'uploading' | 'processing' | 'finished'

// State
const status = ref<BatchStatus>('idle')
const files = ref<BatchFile[]>([])
const fileInput = ref<HTMLInputElement | null>(null)
const isDragOver = ref(false)
let ws: WebSocket | null = null

// Computed
const canStart = computed(() => {
  return status.value === 'idle' && files.value.length > 0
})

const completedCount = computed(() => {
  return files.value.filter(f => f.status === 'success' || f.status === 'error').length
})

const overallPercentage = computed(() => {
  if (files.value.length === 0) return 0
  
  if (status.value === 'uploading') {
    // 假设上传占 30% 总进度
    const uploadedCount = files.value.filter(f => f.status === 'uploaded' || f.status === 'processing' || f.status === 'success' || f.status === 'error').length
    return Math.floor((uploadedCount / files.value.length) * 30)
  }
  
  if (status.value === 'processing' || status.value === 'finished') {
    // 处理占 70%
    const processed = files.value.filter(f => f.status === 'success' || f.status === 'error').length
    return 30 + Math.floor((processed / files.value.length) * 70) 
  }
  
  return 0
})

const statusText = computed(() => {
  if (status.value === 'uploading') return '正在上传图片...'
  if (status.value === 'processing') return '正在识别中...'
  if (status.value === 'finished') return '处理完成'
  return '准备就绪'
})

const getActionButtonText = computed(() => {
  if (status.value === 'uploading') return '上传中...'
  if (status.value === 'processing') return '识别中...'
  return '开始处理'
})

// Methods
const triggerFileSelect = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files) {
    addFiles(Array.from(input.files))
  }
  // Clear input
  input.value = ''
}

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false
  if (event.dataTransfer?.files) {
    addFiles(Array.from(event.dataTransfer.files))
  }
}

const addFiles = (newFiles: File[]) => {
  if (files.value.length + newFiles.length > 50) {
    ElMessage.warning('单次最多支持 50 张图片')
    return
  }

  const batchFiles: BatchFile[] = newFiles
    .filter(f => f.type.startsWith('image/'))
    .map(f => ({
      id: Math.random().toString(36).substring(7),
      file: f,
      previewUrl: URL.createObjectURL(f),
      status: 'pending'
    }))
    
  files.value.push(...batchFiles)
}

const removeFile = (index: number) => {
  files.value.splice(index, 1)
}

const reset = () => {
  files.value = []
  status.value = 'idle'
  closeWs()
}

const startBatch = async () => {
  if (files.value.length === 0) return
  
  status.value = 'uploading'
  
  try {
    // Phase 1: Upload (Concurrent limit 5)
    // Simple concurrent implementation
    const pendingUploads = files.value.filter(f => f.status === 'pending')
    const ossUrls: string[] = []
    
    // Upload in chunks
    const chunkSize = 5
    for (let i = 0; i < pendingUploads.length; i += chunkSize) {
      const chunk = pendingUploads.slice(i, i + chunkSize)
      await Promise.all(chunk.map(async (fileItem) => {
        fileItem.status = 'uploading'
        try {
          const res = await uploadImage(fileItem.file)
          fileItem.ossUrl = res.data.url
          fileItem.status = 'uploaded'
          ossUrls.push(res.data.url)
        } catch (e) {
          console.error(e)
          fileItem.status = 'error'
          fileItem.error = '上传失败'
        }
      }))
    }
    
    // Check if any uploaded successfully
    const readyFiles = files.value.filter(f => f.status === 'uploaded' && f.ossUrl)
    if (readyFiles.length === 0) {
      ElMessage.error('没有图片上传成功')
      status.value = 'idle'
      return
    }
    
    // Phase 2: Start Task
    status.value = 'processing'
    const urls = readyFiles.map(f => f.ossUrl!)
    const res = await startBatchRecognitionTask(urls)
    const taskUuid = (res.data as any)?.task_uuid || (res as any).task_uuid
    
    if (taskUuid) {
      // Set all uploaded to processing
      readyFiles.forEach(f => f.status = 'processing')
      connectWs(taskUuid)
    }
    
  } catch (e: any) {
    ElMessage.error(e.message || '启动失败')
    status.value = 'idle'
  }
}

const connectWs = (taskUuid: string) => {
  const wsUrl = `ws://localhost:8000/api/v1/recognition/ws/${taskUuid}`
  ws = new WebSocket(wsUrl)
  
  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      handleWsMessage(msg)
    } catch (e) {
      console.error(e)
    }
  }
  
  ws.onerror = () => {
    ElMessage.error('WebSocket 连接错误')
    status.value = 'finished' // Stop UI loading
  }
}

const handleWsMessage = (msg: any) => {
  if (msg.type === 'item_complete') {
      // Single item update
      const item = msg.data
      const fileItem = files.value.find(f => f.ossUrl === item.url)
      
      if (fileItem) {
          if (item.status === 'success') {
             fileItem.status = 'success'
             fileItem.result = {
                 plate: item.plate,
                 confidence: (item.confidence * 100).toFixed(1),
                 type: item.type
             }
          } else {
             fileItem.status = 'error'
             fileItem.error = item.error || '识别失败'
          }
      }
      
  } else if (msg.type === 'result') {
      // Final completion
      status.value = 'finished'
      ElMessage.success(msg.message)
      closeWs()
  } else if (msg.type === 'error') {
      ElMessage.error(msg.message)
      status.value = 'finished'
      closeWs()
  }
}

const closeWs = () => {
    if (ws) {
        ws.close()
        ws = null
    }
}

// Table Helpers
const successCount = computed(() => files.value.filter(f => f.status === 'success').length)
const failedCount = computed(() => files.value.filter(f => f.status === 'error').length)

const getPlateTypeColor = (type?: string) => {
  if (!type) return 'info'
  switch (type) {
    case 'blue': return 'primary'
    case 'green': return 'success'
    case 'yellow': return 'warning'
    case 'white': return 'info'
    default: return 'info'
  }
}

const formatPlateType = (type?: string) => {
  if(!type) return '-'
  const map: any = {
    'blue': '蓝牌',
    'green': '绿牌',
    'yellow': '黄牌',
    'white': '白牌',
    'other': '其他'
  }
  return map[type] || type
}

const getStatusType = (s: string) => {
    if(s === 'success') return 'success'
    if(s === 'error') return 'danger'
    if(s === 'processing' || s === 'uploading') return 'warning'
    return 'info'
}

const getStatusText = (s: string) => {
    const map: any = {
        pending: '等待中',
        uploading: '上传中',
        uploaded: '已上传',
        processing: '识别中',
        success: '成功',
        error: '失败'
    }
    return map[s] || s
}

const getPlateColor = (type: string = 'blue') => type // Simplify for now

onBeforeUnmount(() => {
    files.value.forEach(f => URL.revokeObjectURL(f.previewUrl))
    closeWs()
})

</script>

<style scoped lang="scss">
.batch-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.batch-header {
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
  }
}

.upload-area {
  background: white;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover, &.is-dragover {
    border-color: #3b82f6;
    background: #eff6ff;
  }
  
  .upload-icon {
    font-size: 48px;
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
    font-size: 14px;
    color: #94a3b8;
  }
}

.progress-bar-container {
  margin-bottom: 24px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  
  .progress-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
    color: #64748b;
  }
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  
  .file-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    position: relative;
    transition: all 0.2s;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      
      .remove-btn {
        opacity: 1;
      }
    }
    
    &.success { border-color: #22c55e; }
    &.error { border-color: #ef4444; }
    
    .card-image {
      height: 140px;
      width: 100%;
      position: relative;
      background: #f1f5f9;
      
      .status-overlay {
          position: absolute;
          inset: 0;
          background: rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 24px;
          
          .success-icon { color: #22c55e; }
          .error-icon { color: #ef4444; }
      }
    }
    
    .card-info {
      padding: 12px;
      
      .file-name {
        font-size: 13px;
        color: #334155;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 8px;
      }
      
      .result-box {
          .plate-number {
              font-family: monospace;
              font-weight: 700;
              font-size: 16px;
              color: #0f172a;
              margin-bottom: 4px;
              
              &.blue { color: #1e3a8a; }
          }
          .confidence {
              font-size: 12px;
              color: #22c55e;
          }
      }
      
      .error-msg {
          color: #ef4444;
          font-size: 12px;
      }
    }
    
    .remove-btn {
      position: absolute;
      top: 4px;
      right: 4px;
      background: rgba(0,0,0,0.5);
      color: white;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 12px;
      opacity: 0;
      transition: opacity 0.2s;
      z-index: 2;
      
      &:hover {
        background: #ef4444;
      }
    }
  }
  
  .add-card {
    border: 2px dashed #cbd5e1;
    border-radius: 8px;
    background: #f8fafc;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 220px; // Match rough height of file card
    color: #94a3b8;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
        border-color: #3b82f6;
        color: #3b82f6;
        background: #eff6ff;
    }
    
    .el-icon {
        font-size: 24px;
        margin-bottom: 8px;
    }
  }
}

.results-container {
    background: white;
    padding: 24px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    
    .results-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        
        h4 { margin: 0; }
    }
    
    .plate-text {
        font-family: monospace;
        font-weight: 700;
        
        &.blue { color: #1e3a8a; }
    }
    
    .confidence-text {
        font-family: monospace;
        color: #059669;
    }
    
    .error-text {
        color: #ef4444;
        font-size: 13px;
    }
    
    .restart-action {
        margin-top: 24px;
        text-align: center;
    }
}
</style>


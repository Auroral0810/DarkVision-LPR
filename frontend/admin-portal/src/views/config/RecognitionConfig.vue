<template>
  <div class="config-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="page-header">
          <h2 class="page-title">识别参数</h2>
          <p class="page-subtitle">优化 AI 识别精度、模型版本与并发执行效率</p>
        </div>
      </el-col>

      <el-col :span="24">
        <el-card v-loading="loading" class="config-card shadow-sm">
          <el-form label-width="140px" label-position="top">
            <!-- 核心算法参数 -->
            <div class="config-section">
              <div class="section-header">
                <el-icon><Operation /></el-icon>
                <span>核心算法参数</span>
              </div>
              
              <el-row :gutter="60">
                <el-col :md="14" :sm="24">
                  <el-form-item label="默认识别置信度阈值">
                    <div class="slider-container">
                      <el-slider 
                        v-model="params.confidence" 
                        :min="0" :max="1" :step="0.01" 
                        show-input
                        range-start="0.5"
                      />
                    </div>
                    <div class="help-text">
                      <el-alert 
                        v-if="params.confidence < 0.5" 
                        title="提示: 置信度设置过低可能会增加误报率" 
                        type="warning" :closable="false" show-icon 
                      />
                      <p>检测结果置信度低于此阈值的车牌将被标记为“待复核”或直接舍弃。</p>
                    </div>
                  </el-form-item>
                </el-col>

                <el-col :md="10" :sm="24">
                  <el-form-item label="默认模型版本">
                    <el-radio-group v-model="params.modelVersion" class="model-selector">
                      <el-radio-button label="v2.1.0">
                        <div class="model-item">
                          <span class="version">v2.1.0</span>
                          <span class="tag">最新稳定</span>
                        </div>
                      </el-radio-button>
                      <el-radio-button label="v2.0.5">
                        <div class="model-item">
                          <span class="version">v2.0.5</span>
                        </div>
                      </el-radio-button>
                      <el-radio-button label="v1.8.0">
                        <div class="model-item">
                          <span class="version">v1.8.0</span>
                          <span class="tag low">Legacy</span>
                        </div>
                      </el-radio-button>
                    </el-radio-group>
                    <div class="help-text">指定系统全局默认调用的推理模型。</div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <el-divider />

            <!-- 性能与并发 -->
            <div class="config-section">
              <div class="section-header">
                <el-icon><Cpu /></el-icon>
                <span>性能与并发处理</span>
              </div>
              
              <el-row :gutter="40">
                <el-col :md="12" :sm="24">
                  <el-form-item label="并发识别线程限制">
                    <el-input-number v-model="params.maxThreads" :min="1" :max="64" controls-position="right" />
                    <div class="help-text">
                      根据服务器 CPU 核心数进行调整。推荐设置：物理核心数 x 2。
                      <br/>当前系统建议值：<strong>16</strong>
                    </div>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>

            <div class="form-actions">
              <el-button type="primary" size="large" @click="handleSave" :loading="saving">
                保存参数
              </el-button>
              <el-button size="large" @click="resetForm">撤销更改</el-button>
            </div>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useSystemConfigStore } from '@/store/modules/system-config-store'
import { storeToRefs } from 'pinia'
import { Operation, Cpu } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const systemStore = useSystemConfigStore()
const { configs, loading } = storeToRefs(systemStore)

const params = reactive({
  confidence: 0.8,
  modelVersion: 'v2.1.0',
  maxThreads: 8
})
const saving = ref(false)

const initData = () => {
  if (configs.value.recognition) {
    const data = configs.value.recognition
    if (data.confidence) params.confidence = parseFloat(data.confidence)
    if (data.modelVersion) params.modelVersion = data.modelVersion
    if (data.maxThreads) params.maxThreads = parseInt(data.maxThreads)
  }
}

onMounted(async () => {
  if (!configs.value.recognition || Object.keys(configs.value.recognition).length === 0) {
    await systemStore.fetchConfigs()
  }
  initData()
})

watch(configs, () => {
  initData()
}, { deep: true })

const resetForm = () => {
  initData()
  ElMessage.info('已恢复至原始设置')
}

const handleSave = async () => {
  saving.value = true
  try {
    const updateData: Record<string, string> = {
      'recognition.confidence': params.confidence.toString(),
      'recognition.modelVersion': params.modelVersion,
      'recognition.maxThreads': params.maxThreads.toString()
    }
    
    await systemStore.updateConfigs(updateData)
    ElMessage.success('识别参数已更新')
  } catch (err) {
    ElMessage.error('更新失败')
  } finally {
    saving.value = false
  }
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
}

.config-section {
  padding: 8px 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 32px;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
}

.section-header .el-icon {
  font-size: 20px;
  color: #3b82f6;
}

.slider-container {
  padding: 0 12px 0 0;
  margin-bottom: 16px;
}

.model-selector {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.model-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
}

.model-item .version {
  font-weight: 600;
}

.model-item .tag {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  background: #dcfce7;
  color: #166534;
  line-height: 1;
}

.model-item .tag.low {
  background: #f1f5f9;
  color: #64748b;
}

.help-text {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 12px;
  line-height: 1.6;
}

.form-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #475569;
  font-size: 15px;
  margin-bottom: 12px !important;
}

:deep(.el-radio-button__inner) {
  border-radius: 8px !important;
  border: 1px solid #e2e8f0 !important;
  margin-bottom: 10px;
  width: 100%;
  text-align: left;
}

:deep(.el-radio-button:first-child .el-radio-button__inner) {
  border-radius: 8px !important;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background-color: #eff6ff !important;
  border-color: #3b82f6 !important;
  color: #1d4ed8 !important;
  box-shadow: none !important;
}
</style>

<template>
  <div class="recognition-view">
    <div class="view-header">
      <h2>开始识别</h2>
      <p class="subtitle">选择识别模式，体验极致准确的 LPR 服务</p>
    </div>

    <div class="mode-tabs">
      <el-tabs v-model="activeTab" class="custom-tabs">
        <!-- Single Image Recognition -->
        <el-tab-pane name="single">
          <template #label>
            <div class="tab-label">
              <el-icon><Picture /></el-icon>
              <span>单张识别</span>
            </div>
          </template>
          
          <div class="tab-content">
            <SingleUploader />
          </div>
        </el-tab-pane>
        
        <!-- Batch Recognition (VIP) -->
        <el-tab-pane name="batch">
          <template #label>
            <div class="tab-label">
              <el-icon><Files /></el-icon>
              <span>批量识别</span>
              <el-tag v-if="!userStore.isVIP" size="small" type="warning" effect="dark" class="vip-tag">VIP</el-tag>
            </div>
          </template>
          
          <div class="tab-content">
            <div v-if="userStore.isVIP">
              <BatchUploader />
            </div>
            <div v-else class="lock-overlay">
              <div class="lock-content">
                <div class="lock-icon">
                  <el-icon><Lock /></el-icon>
                </div>
                <h3>批量识别是 VIP 专属功能</h3>
                <p>一次性上传多达 50 张图片，支持自动导出 Excel 报表。</p>
                <div class="features-list">
                  <div class="feature-item"><el-icon><Check /></el-icon> 批量并行处理</div>
                  <div class="feature-item"><el-icon><Check /></el-icon> 一键导出报表</div>
                  <div class="feature-item"><el-icon><Check /></el-icon> 优先处理队列</div>
                </div>
                <el-button type="primary" size="large" round class="upgrade-btn">
                  立即升级 VIP
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- Video Recognition (VIP) -->
        <el-tab-pane name="video">
          <template #label>
            <div class="tab-label">
              <el-icon><VideoCamera /></el-icon>
              <span>视频识别</span>
              <el-tag v-if="!userStore.isVIP" size="small" type="warning" effect="dark" class="vip-tag">VIP</el-tag>
            </div>
          </template>
          
          <div class="tab-content">
            <div v-if="userStore.isVIP" class="video-placeholder">
              <el-empty description="视频识别功能开发中..." />
            </div>
            <div v-else class="lock-overlay">
              <div class="lock-content">
                <div class="lock-icon">
                  <el-icon><Lock /></el-icon>
                </div>
                <h3>视频识别是 VIP 专属功能</h3>
                <p>上传视频文件，自动抽帧识别车牌，并生成时间轴报告。</p>
                <div class="features-list">
                  <div class="feature-item"><el-icon><Check /></el-icon> 支持 MP4/AVI 格式</div>
                  <div class="feature-item"><el-icon><Check /></el-icon> 自动抽帧分析</div>
                  <div class="feature-item"><el-icon><Check /></el-icon> 轨迹追踪</div>
                </div>
                <el-button type="primary" size="large" round class="upgrade-btn">
                  立即升级 VIP
                </el-button>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import SingleUploader from '@/components/recognition/SingleUploader.vue'
import BatchUploader from '@/components/recognition/BatchUploader.vue'
import { Picture, Files, VideoCamera, Lock, Check } from '@element-plus/icons-vue'

const userStore = useUserStore()
const activeTab = ref('single')
</script>

<style scoped lang="scss">
.recognition-view {
  width: 100%;
}

.view-header {
  margin-bottom: 32px;
  text-align: center;
  
  h2 {
    font-size: 28px;
    color: #0f172a;
    margin: 0 0 8px;
  }
  
  .subtitle {
    color: #64748b;
    font-size: 16px;
    margin: 0;
  }
}

.mode-tabs {
  background: white;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.custom-tabs {
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
  
  :deep(.el-tabs__header) {
    margin-bottom: 0;
  }
  
  :deep(.el-tabs__nav) {
    width: 100%;
    display: flex;
  }
  
  :deep(.el-tabs__item) {
    flex: 1;
    height: 56px;
    font-size: 16px;
    color: #64748b;
    transition: all 0.3s;
    border-radius: 8px;
    margin: 4px;
    
    &.is-active {
      background: #eff6ff;
      color: #2563eb;
      font-weight: 600;
    }
    
    &:hover:not(.is-active) {
      color: #334155;
      background: #f8fafc;
    }
  }
  
  :deep(.el-tabs__active-bar) {
    display: none;
  }
}

.tab-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  
  .vip-tag {
    transform: scale(0.8);
    margin-left: 4px;
  }
}

.tab-content {
  padding: 32px;
  min-height: 400px;
  position: relative;
}

.lock-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  
  .lock-content {
    text-align: center;
    max-width: 400px;
    
    .lock-icon {
      width: 64px;
      height: 64px;
      background: #fff7ed;
      color: #f59e0b;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      margin: 0 auto 24px;
    }
    
    h3 {
      font-size: 24px;
      color: #0f172a;
      margin: 0 0 12px;
    }
    
    p {
      color: #64748b;
      margin: 0 0 24px;
      line-height: 1.6;
    }
    
    .features-list {
      text-align: left;
      background: #f8fafc;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 32px;
      
      .feature-item {
        display: flex;
        align-items: center;
        gap: 12px;
        color: #334155;
        margin-bottom: 12px;
        
        &:last-child { margin-bottom: 0; }
        
        .el-icon {
          color: #10b981;
        }
      }
    }
    
    .upgrade-btn {
      width: 100%;
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      border: none;
      font-weight: 600;
      
      &:hover {
        opacity: 0.9;
        transform: translateY(-2px);
      }
    }
  }
}

.video-placeholder {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
</style>
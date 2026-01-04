<template>
  <div class="download-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>{{ $t('download.title') }}</h1>
        <p>下载 DarkVision 客户端，体验极致性能</p>
      </div>
    </div>

    <div class="page-container">
      <div class="download-cards">
        <div class="download-card windows">
          <div class="os-icon">
            <svg viewBox="0 0 24 24" width="64" height="64" class="svg-icon">
              <path fill="#0078D4" d="M0 3.449L9.388 2.147v9.422H0V3.449zm0 9.942h9.388v9.421L0 21.55v-8.159zm10.702-9.605L24 2.227v9.342H10.702V3.786zm0 9.605H24v9.34L10.702 21.43v-8.039z"/>
            </svg>
          </div>
          <h2>{{ $t('download.windows') }}</h2>
          <div class="version-info">
            <div class="info-row">
              <span class="label">{{ $t('download.version') }}</span>
              <span class="value">v1.0.0</span>
            </div>
            <div class="info-row">
              <span class="label">{{ $t('download.size') }}</span>
              <span class="value">45.2 MB</span>
            </div>
          </div>
          <div class="requirements">
            <p><strong>{{ $t('download.requirements') }}:</strong></p>
            <p>Windows 10 / 11 (64-bit)</p>
          </div>
          <button class="download-btn" @click="handleDownload('windows')">
            <el-icon><Download /></el-icon>
            {{ $t('download.download') }}
          </button>
        </div>

        <div class="download-card macos">
          <div class="os-icon">
            <svg viewBox="0 0 24 24" width="64" height="64" class="svg-icon">
              <path fill="#000000" d="M17.34 22.042c-1.155 0-1.896-.79-3.26-.79-1.39 0-2.037.767-3.237.767-3.056 0-5.756-5.066-4.522-8.625.962-2.756 3.033-3.415 4.31-3.415 1.154 0 1.88.66 2.89.66 1.057 0 1.733-.703 3.012-.703 1.26 0 2.503.746 3.237 1.83-2.91 1.735-2.293 6.096.533 7.291-.703 1.756-1.732 3.472-2.964 2.984zM12.42 2.91c1.24-1.536 1.057-3.956-1.154-4.922-1.39.263-2.94 1.713-2.677 3.328.02.042 1.413 3.054 3.83 1.594z" transform="translate(4 4) scale(0.7)"/>
              <path fill="#000000" d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.02-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.79-1.31.02-2.3-1.28-3.14-2.49C3.12 15.29 4.41 9.4 7.7 9.35c1.3-.02 2.52.87 3.31.87.79 0 2.27-1.07 3.83-.91 1.3.05 2.49.53 3.19 1.55-2.8 1.4-2.33 5.48.51 6.64-.63 1.57-1.49 3.12-2.83 5zM13 5.3c.7-1.73 2.76-2.6 4.38-2.6.22 2.08-1.92 4.35-4.38 2.6z"/>
            </svg>
          </div>
          <h2>{{ $t('download.macos') }}</h2>
          <div class="version-info">
            <div class="info-row">
              <span class="label">{{ $t('download.version') }}</span>
              <span class="value">v1.0.0</span>
            </div>
            <div class="info-row">
              <span class="label">{{ $t('download.size') }}</span>
              <span class="value">52.8 MB</span>
            </div>
          </div>
          <div class="requirements">
            <p><strong>{{ $t('download.requirements') }}:</strong></p>
            <p>macOS 11.0+ (Intel / Apple Silicon)</p>
          </div>
          <button class="download-btn" @click="handleDownload('macos')">
            <el-icon><Download /></el-icon>
            {{ $t('download.download') }}
          </button>
        </div>

        <div class="download-card linux">
          <div class="os-icon">
            <svg viewBox="0 0 24 24" width="64" height="64" class="svg-icon">
              <path fill="#FCC624" d="M12 0c6.627 0 12 5.373 12 12s-5.373 12-12 12S0 18.627 0 12 5.373 0 12 0z"/>
              <path fill="#000" d="M15.5 15.5c-1 0-1.5.5-1.5 1s.5 1 1.5 1 1.5-.5 1.5-1-.5-1-1.5-1zm-7 0c-1 0-1.5.5-1.5 1s.5 1 1.5 1 1.5-.5 1.5-1-.5-1-1.5-1zM12 4.5c-3 0-5 2.5-5 6.5s2 6.5 5 6.5 5-2.5 5-6.5-2-6.5-5-6.5z"/>
            </svg>
          </div>
          <h2>{{ $t('download.linux') }}</h2>
          <div class="version-info">
            <div class="info-row">
              <span class="label">{{ $t('download.version') }}</span>
              <span class="value">v1.0.0</span>
            </div>
            <div class="info-row">
              <span class="label">{{ $t('download.size') }}</span>
              <span class="value">48.5 MB</span>
            </div>
          </div>
          <div class="requirements">
            <p><strong>{{ $t('download.requirements') }}:</strong></p>
            <p>Ubuntu 20.04+ / CentOS 7+</p>
          </div>
          <button class="download-btn" @click="handleDownload('linux')">
            <el-icon><Download /></el-icon>
            {{ $t('download.download') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const handleDownload = (os: string) => {
  ElMessage.info(`正在为您准备 ${os} 版本的下载...`)
  // 模拟下载延迟
  setTimeout(() => {
    ElMessage.success('开始下载')
  }, 1000)
}
</script>

<style scoped lang="scss">
.download-page {
  min-height: 100vh;
  background: #f8fafc;
  padding-top: 72px;
}

.page-header {
  background: #0f172a;
  color: white;
  padding: 80px 24px 120px;
  text-align: center;
  position: relative;
  overflow: hidden;

  .header-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 30% 30%, #1e293b 0%, #0f172a 100%);
    z-index: 1;
  }

  .header-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;

    h1 {
      font-size: 48px;
      font-weight: 800;
      margin-bottom: 16px;
    }

    p {
      font-size: 20px;
      color: #94a3b8;
    }
  }
}

.page-container {
  max-width: 1200px;
  margin: -80px auto 80px;
  padding: 0 24px;
  position: relative;
  z-index: 10;
}

.download-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
}

.download-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  }

  .os-icon {
    margin-bottom: 24px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .svg-icon {
      width: 64px;
      height: 64px;
    }
  }

  h2 {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 24px;
  }

  .version-info {
    background: #f8fafc;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 24px;

    .info-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      
      &:last-child {
        margin-bottom: 0;
      }

      .label {
        color: #64748b;
        font-size: 14px;
      }

      .value {
        color: #0f172a;
        font-weight: 600;
        font-family: monospace;
      }
    }
  }

  .requirements {
    margin-bottom: 32px;
    color: #64748b;
    font-size: 14px;
    
    strong {
      color: #334155;
    }
  }

  .download-btn {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    background: #2563eb;
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: background 0.2s;

    &:hover {
      background: #1d4ed8;
    }

    .el-icon {
      font-size: 18px;
    }
  }
  
  &.windows:hover { border-color: #0078d4; }
  &.macos:hover { border-color: #999999; }
  &.linux:hover { border-color: #fcc624; }
}
</style>
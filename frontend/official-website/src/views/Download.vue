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
              <!-- Tux Icon -->
              <path fill="#000" d="M12.14 3a2.6 2.6 0 0 0-2.56 2.65c0 1.14 0 3.06 1.48 4.28 0 0 2.22 1.51 2.69 4.41.06.33.2 1.6-1.55 1.76-1.74.16-1.63 1.77-.38 1.94 1.25.17 2.06-.54 2.24-.96.18-.42.92-2 .88-3.17-.03-.7-.34-3.41-1.66-4.63C12.18 8.16 12.14 7.6 12.14 3zM9.46 8.68c-.7.65-2.06 2.37-2.14 5.34-.02.73 1.94.88 1.94.88s.22 1.15-1.12 1.24c-1.34.09-1.92-.78-2.02-1.78-.1-1 .36-4.52 1.86-6.38.38-.47 1.1.13 1.48.7zm7.64 5.42c-.08-2.97-1.44-4.69-2.14-5.34.38-.57 1.1-1.17 1.48-.7 1.5 1.86 1.96 5.38 1.86 6.38-.1 1-1.38 1.68-2.02 1.78-1.34-.09-1.12-1.24-1.12-1.24s1.96-.15 1.94-.88z" transform="scale(1.5) translate(-4, -1)"/>
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

    <!-- Features Section -->
    <div class="client-features">
      <div class="container">
        <h2 class="section-title">为什么选择桌面客户端？</h2>
        <div class="features-grid">
          <div class="feature-item">
            <div class="icon-box">🚀</div>
            <h3>原生性能</h3>
            <p>深度适配系统硬件，支持 CUDA 与 Metal 加速，推理速度提升 300%。</p>
          </div>
          <div class="feature-item">
            <div class="icon-box">🔒</div>
            <h3>隐私安全</h3>
            <p>所有数据本地处理，无需上传云端，完全掌控您的数据主权。</p>
          </div>
          <div class="feature-item">
            <div class="icon-box">📂</div>
            <h3>批量处理</h3>
            <p>支持文件夹拖拽导入，一键处理万张图片，自动导出 CSV/Excel 报表。</p>
          </div>
          <div class="feature-item">
            <div class="icon-box">🔌</div>
            <h3>离线运行</h3>
            <p>无网络环境也能稳定运行，适合地下车库、偏远地区等场景。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Install Guide -->
    <div class="install-guide">
      <div class="container">
        <h2 class="section-title">安装说明</h2>
        <div class="guide-tabs">
          <div class="guide-card">
            <h3>Windows</h3>
            <ol>
              <li>下载 <code>.exe</code> 安装包</li>
              <li>双击运行安装程序</li>
              <li>按照提示完成安装</li>
              <li>首次运行需联网激活</li>
            </ol>
          </div>
          <div class="guide-card">
            <h3>macOS</h3>
            <ol>
              <li>下载 <code>.dmg</code> 镜像文件</li>
              <li>将 DarkVision 拖入 Applications</li>
              <li>首次打开若提示安全拦截，请在"系统设置 > 隐私与安全性"中允许运行</li>
            </ol>
          </div>
          <div class="guide-card">
            <h3>Linux</h3>
            <ol>
              <li>下载 <code>.AppImage</code> 文件</li>
              <li>赋予执行权限: <code>chmod +x DarkVision*.AppImage</code></li>
              <li>直接运行即可</li>
            </ol>
          </div>
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

.client-features {
  padding: 80px 0;
  background: white;

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
  }

  .section-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 60px;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 40px;

    .feature-item {
      text-align: center;
      
      .icon-box {
        width: 64px;
        height: 64px;
        background: #f8fafc;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        margin: 0 auto 20px;
        transition: transform 0.3s;

        &:hover {
          transform: scale(1.1);
          background: #eff6ff;
        }
      }

      h3 {
        font-size: 18px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 12px;
      }

      p {
        color: #64748b;
        font-size: 14px;
        line-height: 1.6;
      }
    }
  }
}

.install-guide {
  padding: 80px 0 100px;
  background: #f8fafc;
  
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 24px;
  }

  .section-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 60px;
  }

  .guide-tabs {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }

  .guide-card {
    background: white;
    padding: 32px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;

    h3 {
      font-size: 20px;
      font-weight: 600;
      color: #0f172a;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 8px;
      
      &::before {
        content: '';
        width: 4px;
        height: 16px;
        background: #2563eb;
        border-radius: 2px;
      }
    }

    ol {
      padding-left: 20px;
      color: #64748b;
      font-size: 14px;
      line-height: 1.8;

      li {
        margin-bottom: 8px;
      }
    }

    code {
      background: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      color: #0f172a;
      font-family: monospace;
      font-size: 12px;
    }
  }
}
</style>
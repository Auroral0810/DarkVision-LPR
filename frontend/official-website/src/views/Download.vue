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
        <div 
          v-for="item in downloads" 
          :key="item.id" 
          class="download-card" 
          :class="item.os"
        >
          <div class="os-icon">
            <img :src="getIconPath(item.os)" :alt="item.os" class="svg-icon" />
          </div>
          <h2>{{ formatOsName(item.os) }}</h2>
          <div class="version-info">
            <div class="info-row">
              <span class="label">{{ $t('download.version') }}</span>
              <span class="value">{{ item.version }}</span>
            </div>
            <div class="info-row">
              <span class="label">{{ $t('download.releaseDate') || '发布日期' }}</span>
              <span class="value">{{ item.release_date }}</span>
            </div>
          </div>
          <div class="requirements">
            <p><strong>{{ $t('download.requirements') }}:</strong></p>
            <p>{{ getRequirements(item.os) }}</p>
          </div>
          <button class="download-btn" @click="handleDownload(item)">
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
import { ref, onMounted } from 'vue'
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { ClientDownload } from '@/types/website'

// Import icons for dynamic use
import windowsIcon from '@/assets/icons/windows.svg'
import macosIcon from '@/assets/icons/macos.svg'
import linuxIcon from '@/assets/icons/linux.svg'

const downloads = ref<ClientDownload[]>([])

onMounted(() => {
  // Mock Data
  downloads.value = [
    {
      id: 1,
      os: 'windows',
      version: 'v1.0.0',
      download_url: 'https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/EasyRename_1.0.0_x64_zh%2DCN.msi',
      changelog: 'Initial release',
      release_date: '2026-01-01',
      is_latest: true
    },
    {
      id: 2,
      os: 'macos',
      version: 'v1.0.0',
      download_url: 'https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/EasyRename_1.0.0_aarch64.dmg',
      changelog: 'Initial release',
      release_date: '2026-01-01',
      is_latest: true
    },
    {
      id: 3,
      os: 'linux',
      version: 'v1.0.0',
      download_url: 'https://github.com/Auroral0810/EasyRename/releases/download/v1.0.0/easy%2Drename_1.0.0_amd64.deb',
      changelog: 'Initial release',
      release_date: '2026-01-01',
      is_latest: true
    }
  ]
})

const getIconPath = (os: string) => {
  switch (os) {
    case 'windows': return windowsIcon
    case 'macos': return macosIcon
    case 'linux': return linuxIcon
    default: return ''
  }
}

const formatOsName = (os: string) => {
  switch (os) {
    case 'windows': return 'Windows'
    case 'macos': return 'macOS'
    case 'linux': return 'Linux'
    default: return os
  }
}

const getRequirements = (os: string) => {
  // Could also be in DB or derived
  switch (os) {
    case 'windows': return 'Windows 10 / 11 (64-bit)'
    case 'macos': return 'macOS 11.0+ (Intel / Apple Silicon)'
    case 'linux': return 'Ubuntu 20.04+ / CentOS 7+'
    default: return ''
  }
}

const handleDownload = (item: ClientDownload) => {
  if (item.download_url) {
    window.open(item.download_url, '_blank')
    ElMessage.success(`正在跳转到 ${formatOsName(item.os)} 版本下载页面`)
  } else {
    ElMessage.error('未找到对应的下载链接')
  }
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
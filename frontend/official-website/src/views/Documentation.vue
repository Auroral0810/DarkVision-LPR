<template>
  <div class="documentation-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-bg">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">{{ $t('documentation.title') }}</h1>
        <p class="hero-subtitle">
          探索 DarkVision-LPR 的无限可能。<br>
          一站式开发者资源中心，为您提供最详尽的技术指引。
        </p>
        <div class="hero-actions">
          <a href="http://localhost:5173/" target="_blank" class="tech-docs-btn">
            <el-icon class="btn-icon"><Monitor /></el-icon>
            <span>官方技术文档</span>
            <el-icon class="arrow-icon"><Right /></el-icon>
          </a>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="page-container">
      <div class="docs-grid">
        <!-- Technical Architecture (Internal Summary, links to full docs) -->
        <div class="doc-card featured" @click="openExternalDocs">
          <div class="card-bg"></div>
          <div class="icon-box blue">
            <el-icon><Connection /></el-icon>
          </div>
          <div class="card-content">
            <h3>{{ $t('documentation.technical') }}</h3>
            <p>深入了解系统架构、部署方案与运维指南。完整技术细节请访问新版文档中心。</p>
            <span class="link-text">前往查阅 <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>

        <!-- API Reference -->
        <div class="doc-card" @click="handleDocClick('api')">
          <div class="icon-box purple">
            <el-icon><Cpu /></el-icon>
          </div>
          <div class="card-content">
            <h3>{{ $t('documentation.api') }}</h3>
            <p>完整的 RESTful API 参考手册、接口定义与错误码说明。</p>
            <span class="link-text">查看 API <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>

        <!-- Service Agreement -->
        <div class="doc-card" @click="handleDocClick('agreement')">
          <div class="icon-box orange">
            <el-icon><DocumentChecked /></el-icon>
          </div>
          <div class="card-content">
            <h3>{{ $t('documentation.agreement') }}</h3>
            <p>了解服务条款、SLA 保障标准与平台使用规范。</p>
            <span class="link-text">阅读协议 <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>

        <!-- Privacy Policy -->
        <div class="doc-card" @click="handleDocClick('privacy')">
          <div class="icon-box green">
            <el-icon><Lock /></el-icon>
          </div>
          <div class="card-content">
            <h3>{{ $t('documentation.privacy') }}</h3>
            <p>我们如何收集、使用与保护您的数据，保障您的隐私安全。</p>
            <span class="link-text">隐私政策 <el-icon><ArrowRight /></el-icon></span>
          </div>
        </div>
      </div>

      <!-- Content Placeholder / Detail View -->
      <div class="doc-detail-view" v-if="currentDocType" id="doc-detail">
        <div class="detail-container">
          <div class="detail-header">
            <div class="header-icon">
              <el-icon v-if="currentDocType === 'api'"><Cpu /></el-icon>
              <el-icon v-else-if="currentDocType === 'agreement'"><DocumentChecked /></el-icon>
              <el-icon v-else><Lock /></el-icon>
            </div>
            <h2>{{ currentDocTitle }}</h2>
            <el-button circle size="small" @click="closeDetail">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          
          <div class="detail-body">
            <div v-if="currentDocContent" class="markdown-body" v-html="currentDocContent.content"></div>
            <div v-else class="empty-state">
              <el-empty description="文档内容正在编写中，敬请期待..." />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { useWebsiteStore } from '@/store/website'
import { 
  Monitor, Right, Connection, ArrowRight, Cpu, DocumentChecked, Lock, Close 
} from '@element-plus/icons-vue'

const { t } = useI18n()
const websiteStore = useWebsiteStore()
const { documents } = storeToRefs(websiteStore)

const currentDocType = ref<string | null>(null)

const currentDocContent = computed(() => {
  if (!currentDocType.value) return null
  return documents.value.find(d => d.doc_type === currentDocType.value && d.is_current)
})

const currentDocTitle = computed(() => {
  if (!currentDocType.value) return ''
  return t(`documentation.${currentDocType.value}`)
})

const handleDocClick = (type: string) => {
  currentDocType.value = type
  setTimeout(() => {
    const el = document.getElementById('doc-detail')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 100)
}

const openExternalDocs = () => {
  window.open('http://localhost:5173/', '_blank')
}

const closeDetail = () => {
  currentDocType.value = null
}
</script>

<style scoped lang="scss">
.documentation-page {
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Hero Section */
.hero-section {
  position: relative;
  background: #0f172a;
  color: white;
  padding: 120px 24px 160px;
  text-align: center;
  overflow: hidden;

  .hero-bg {
    position: absolute;
    inset: 0;
    z-index: 1;
    
    .glow-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.6;
    }
    
    .orb-1 {
      width: 400px;
      height: 400px;
      background: #3b82f6;
      top: -100px;
      left: -100px;
      opacity: 0.4;
    }
    
    .orb-2 {
      width: 500px;
      height: 500px;
      background: #8b5cf6;
      bottom: -200px;
      right: -100px;
      opacity: 0.3;
    }
  }

  .hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
  }

  .hero-title {
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 24px;
    background: linear-gradient(to right, #ffffff, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 20px;
    line-height: 1.6;
    color: #94a3b8;
    margin-bottom: 48px;
  }

  .tech-docs-btn {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    padding: 16px 40px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    font-size: 18px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 15px 30px -5px rgba(37, 99, 235, 0.5);
      
      .arrow-icon {
        transform: translateX(4px);
      }
    }

    .arrow-icon {
      transition: transform 0.2s;
    }
  }
}

/* Page Container */
.page-container {
  max-width: 1200px;
  margin: -80px auto 80px;
  padding: 0 24px;
  position: relative;
  z-index: 10;
}

/* Docs Grid */
.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
  margin-bottom: 64px;
}

.doc-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(226, 232, 240, 0.8);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);

  &.featured {
    grid-column: span 2;
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border-color: #bfdbfe;
    
    @media (max-width: 768px) {
      grid-column: span 1;
    }
  }

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;

    .link-text {
      color: #2563eb;
      gap: 8px;
    }
  }

  .icon-box {
    width: 64px;
    height: 64px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin-bottom: 24px;
    
    &.blue { background: #eff6ff; color: #3b82f6; }
    &.purple { background: #f3e8ff; color: #9333ea; }
    &.orange { background: #fff7ed; color: #f97316; }
    &.green { background: #f0fdf4; color: #16a34a; }
  }

  .card-content {
    h3 {
      font-size: 22px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 12px;
    }

    p {
      color: #64748b;
      margin-bottom: 24px;
      line-height: 1.6;
      font-size: 15px;
    }

    .link-text {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-weight: 600;
      color: #475569;
      font-size: 15px;
      transition: all 0.2s;
    }
  }
}

/* Detail View */
.doc-detail-view {
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  animation: slideUp 0.4s ease-out;

  .detail-header {
    padding: 24px 32px;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8fafc;

    .header-icon {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: white;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;
      color: #3b82f6;
      border: 1px solid #e2e8f0;
    }

    h2 {
      flex: 1;
      margin: 0;
      font-size: 20px;
      color: #0f172a;
    }
  }

  .detail-body {
    padding: 40px;
    min-height: 300px;
  }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Markdown Styling (Basic) */
.markdown-body {
  color: #334155;
  line-height: 1.8;
  
  h1, h2, h3 { color: #0f172a; margin-top: 1.5em; margin-bottom: 0.8em; }
  p { margin-bottom: 1.2em; }
  ul { padding-left: 20px; margin-bottom: 1.2em; }
  code { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
}
</style>

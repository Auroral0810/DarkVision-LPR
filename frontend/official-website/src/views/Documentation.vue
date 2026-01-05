<template>
  <div class="documentation-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>{{ $t('documentation.title') }}</h1>
        <p>一站式开发者资源中心</p>
      </div>
    </div>

    <div class="page-container">
      <div class="docs-grid">
        <div class="doc-card" @click="handleDocClick('technical')">
          <div class="icon-wrapper blue">
            <span class="icon">📚</span>
          </div>
          <h3>{{ $t('documentation.technical') }}</h3>
          <p>深入了解系统架构、部署方案与运维指南。</p>
          <span class="link-text">阅读文档 →</span>
        </div>

        <div class="doc-card" @click="handleDocClick('api')">
          <div class="icon-wrapper purple">
            <span class="icon">🔌</span>
          </div>
          <h3>{{ $t('documentation.api') }}</h3>
          <p>完整的 RESTful API 参考手册与错误码说明。</p>
          <span class="link-text">查看 API →</span>
        </div>

        <div class="doc-card" @click="handleDocClick('agreement')">
          <div class="icon-wrapper orange">
            <span class="icon">📄</span>
          </div>
          <h3>{{ $t('documentation.agreement') }}</h3>
          <p>了解服务条款、SLA 保障与使用规范。</p>
          <span class="link-text">阅读协议 →</span>
        </div>

        <div class="doc-card" @click="handleDocClick('privacy')">
          <div class="icon-wrapper green">
            <span class="icon">🔒</span>
          </div>
          <h3>{{ $t('documentation.privacy') }}</h3>
          <p>我们如何收集、使用与保护您的数据。</p>
          <span class="link-text">隐私政策 →</span>
        </div>
      </div>

      <div class="doc-content-placeholder" v-if="currentDocType">
        <div class="placeholder-box">
          <el-icon :size="64" class="icon"><DocumentIcon /></el-icon>
          <h2>{{ currentDocTitle }}</h2>
          <div v-if="currentDocContent" class="doc-body">
            <!-- Render actual content if available (supports HTML if trusted, or markdown) -->
            {{ currentDocContent.content }}
          </div>
          <p v-else>文档内容正在编写中，敬请期待...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { Document as DocumentIcon } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'
import { useWebsiteStore } from '@/store/website'

const { t } = useI18n()
const currentDocType = ref<string | null>(null)
const websiteStore = useWebsiteStore()
const { documents } = storeToRefs(websiteStore)

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
  // 简单的滚动逻辑，实际可能需要更复杂的定位
  setTimeout(() => {
    const el = document.querySelector('.doc-content-placeholder')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' })
    }
  }, 100)
}
</script>

<style scoped lang="scss">
.documentation-page {
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
    background: radial-gradient(circle at 70% 50%, #1e293b 0%, #0f172a 100%);
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

.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  margin-bottom: 64px;
}

.doc-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;

    .link-text {
      color: #2563eb;
      transform: translateX(4px);
    }
  }

  .icon-wrapper {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    font-size: 24px;

    &.blue { background: #eff6ff; }
    &.purple { background: #f3e8ff; }
    &.orange { background: #fff7ed; }
    &.green { background: #f0fdf4; }
  }

  h3 {
    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 12px;
  }

  p {
    color: #64748b;
    margin-bottom: 24px;
    line-height: 1.6;
    flex: 1;
  }

  .link-text {
    font-size: 14px;
    font-weight: 600;
    color: #64748b;
    transition: all 0.2s;
  }
}

.doc-content-placeholder {
  background: white;
  border-radius: 24px;
  padding: 80px;
  text-align: center;
  border: 1px solid #e2e8f0;
  
  .placeholder-box {
    max-width: 400px;
    margin: 0 auto;
    
    .icon {
      color: #cbd5e1;
      margin-bottom: 24px;
    }
    
    h2 {
      color: #0f172a;
      margin-bottom: 16px;
    }
    
    p {
      color: #64748b;
    }
  }
}
</style>

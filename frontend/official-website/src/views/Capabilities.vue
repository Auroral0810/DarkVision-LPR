<template>
  <div class="capabilities-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>{{ $t('capabilities.title') }}</h1>
        <p>从数据采集到智能分析的全链路能力展示</p>
      </div>
    </div>

    <div class="page-container">
      <!-- Statistics -->
      <section class="statistics-bar">
        <div class="stat-item">
          <div class="stat-value">{{ totalRecognition.toLocaleString() }}</div>
          <div class="stat-label">累计识别车牌</div>
        </div>
        <div class="divider"></div>
        <div class="stat-item">
          <div class="stat-value">99.9%</div>
          <div class="stat-label">服务可用性</div>
        </div>
        <div class="divider"></div>
        <div class="stat-item">
          <div class="stat-value">500+</div>
          <div class="stat-label">企业客户</div>
        </div>
      </section>

      <!-- Steps -->
      <section class="section">
        <h2 class="section-title">{{ $t('capabilities.steps.title') }}</h2>
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-icon">1</div>
            <h3>{{ $t('capabilities.steps.step1') }}</h3>
            <p>支持本地上传或视频流接入，系统自动适配输入格式。</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step-card">
            <div class="step-icon">2</div>
            <h3>{{ $t('capabilities.steps.step2') }}</h3>
            <p>云端高性能集群进行实时增强与推理分析。</p>
          </div>
          <div class="step-arrow">→</div>
          <div class="step-card">
            <div class="step-icon">3</div>
            <h3>{{ $t('capabilities.steps.step3') }}</h3>
            <p>通过 Web 控制台或 API 获取结构化数据结果。</p>
          </div>
        </div>
      </section>

      <!-- Examples -->
      <section class="section">
        <h2 class="section-title">场景示例</h2>
        <div class="examples-grid">
          <div class="example-card">
            <div class="card-image dark">
              <div class="overlay-text">Low Light</div>
            </div>
            <div class="card-content">
              <h3>{{ $t('capabilities.examples.example1') }}</h3>
              <p>在不足 0.1 lux 的光照条件下，依然能清晰还原车牌号码与颜色。</p>
            </div>
          </div>
          
          <div class="example-card">
            <div class="card-image angle">
              <div class="overlay-text">Wide Angle</div>
            </div>
            <div class="card-content">
              <h3>{{ $t('capabilities.examples.example2') }}</h3>
              <p>支持水平/垂直方向 60° 以内的大角度倾斜识别，适应路侧停车场景。</p>
            </div>
          </div>
          
          <div class="example-card">
            <div class="card-image batch">
              <div class="overlay-text">Batch Process</div>
            </div>
            <div class="card-content">
              <h3>{{ $t('capabilities.examples.example3') }}</h3>
              <p>高并发处理能力，单节点支持每秒处理 100+ 张高清图片。</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { SystemConfig } from '@/types/website'
import request from '@/utils/request'

const totalRecognition = ref(125680)

onMounted(async () => {
  try {
    const { data } = await request.get('/website/content')
    if (data && data.configs) {
      const configs = data.configs as SystemConfig[]
      const config = configs.find(c => c.config_key === 'total_recognition_count')
      if (config) totalRecognition.value = parseInt(config.config_value)
    }
  } catch (error) {
    console.error('Failed to fetch configs:', error)
  }
})
</script>

<style scoped lang="scss">
.capabilities-page {
  min-height: 100vh;
  background: white;
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
    background: radial-gradient(circle at 20% 80%, #1e293b 0%, #0f172a 100%);
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
  margin: 0 auto;
  padding: 0 24px 100px;
}

.statistics-bar {
  background: white;
  border-radius: 16px;
  padding: 40px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
  margin-top: -60px;
  position: relative;
  z-index: 10;
  margin-bottom: 80px;

  .stat-item {
    text-align: center;
    
    .stat-value {
      font-size: 40px;
      font-weight: 800;
      color: #2563eb;
      line-height: 1;
      margin-bottom: 8px;
    }
    
    .stat-label {
      color: #64748b;
      font-weight: 500;
    }
  }

  .divider {
    width: 1px;
    height: 40px;
    background: #e2e8f0;
  }
}

.section {
  margin-bottom: 100px;

  .section-title {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
    text-align: center;
    margin-bottom: 64px;
  }
}

.steps-grid {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;

  .step-card {
    flex: 1;
    text-align: center;
    padding: 32px;
    background: #f8fafc;
    border-radius: 16px;
    transition: transform 0.3s;
    
    &:hover {
      transform: translateY(-5px);
    }
    
    .step-icon {
      width: 48px;
      height: 48px;
      background: #2563eb;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      font-weight: bold;
      margin: 0 auto 24px;
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

  .step-arrow {
    color: #cbd5e1;
    font-size: 24px;
    font-weight: bold;
  }
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;

  .example-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }

    .card-image {
      height: 200px;
      background: #0f172a;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.dark { background: #020617; }
      &.angle { background: #1e293b; }
      &.batch { background: #334155; }
      
      .overlay-text {
        color: rgba(255, 255, 255, 0.5);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }
    }

    .card-content {
      padding: 24px;

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

@media (max-width: 768px) {
  .statistics-bar {
    flex-direction: column;
    gap: 32px;
    padding: 32px;
    
    .divider { 
      width: 40px;
      height: 1px;
    }
  }

  .steps-grid {
    flex-direction: column;
    
    .step-arrow {
      transform: rotate(90deg);
    }
  }
}
</style>
<template>
  <div class="about-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>关于我们</h1>
        <p class="subtitle">用 AI 技术重塑智慧交通的未来</p>
      </div>
    </div>

    <div class="page-container">
      <!-- 公司简介 -->
      <section class="section intro">
        <div class="section-content">
          <h2>我们的故事</h2>
          <p>
            DarkVision LPR 始于对人工智能与计算机视觉技术的无限热爱。作为来自南京审计大学的创新团队，我们致力于将最前沿的深度学习算法应用于实际生活场景，解决智慧交通领域的核心痛点。
          </p>
          <p>
            从最初的一个校园创新项目，发展成为如今拥有高精度车牌识别能力的成熟系统，我们的每一步都凝聚了对技术的执着追求。我们的团队成员曾获得国家奖学金、数维杯数学建模竞赛全国一等奖等50余项荣誉，拥有多项软件著作权。我们不仅是代码的编写者，更是智慧生活的构建者。
          </p>
        </div>
        <div class="section-image">
          <div class="image-placeholder">
            <el-icon :size="64"><Monitor /></el-icon>
            <span>Innovation & Passion</span>
          </div>
        </div>
      </section>

      <!-- 核心价值 -->
      <section class="section values">
        <h2>核心价值</h2>
        <div class="values-grid">
          <div class="value-card">
            <div class="icon-box">
              <el-icon><Aim /></el-icon>
            </div>
            <h3>精准高效</h3>
            <p>追求极致的识别准确率与处理速度，确保每一次识别都值得信赖。</p>
          </div>
          <div class="value-card">
            <div class="icon-box">
              <el-icon><Connection /></el-icon>
            </div>
            <h3>开放共享</h3>
            <p>拥抱开源精神，致力于构建开放的技术生态，与开发者共同成长。</p>
          </div>
          <div class="value-card">
            <div class="icon-box">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <h3>持续创新</h3>
            <p>紧跟 AI 技术浪潮，不断探索 YOLO 系列模型的应用边界。</p>
          </div>
        </div>
      </section>

      <!-- 技术栈 -->
      <section class="section tech-stack">
        <h2>技术基因</h2>
        <p class="tech-desc">我们采用行业领先的技术栈构建高性能系统</p>
        <div class="tech-grid">
          <div class="tech-item">Python / FastAPI</div>
          <div class="tech-item">Vue.js / TypeScript</div>
          <div class="tech-item">PyTorch / YOLOv12</div>
          <div class="tech-item">Redis / MySQL</div>
          <div class="tech-item">Docker / K8s</div>
          <div class="tech-item">Spring Cloud</div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Monitor, Aim, Connection, TrendCharts } from '@element-plus/icons-vue'
</script>

<style scoped lang="scss">
.about-page {
  min-height: 100vh;
  background: #fff;
  padding-top: 72px;
}

.page-header {
  background: #0f172a;
  color: white;
  padding: 100px 24px;
  text-align: center;
  position: relative;
  overflow: hidden;

  .header-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 100%);
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
      margin-bottom: 24px;
      letter-spacing: -0.02em;
    }

    .subtitle {
      font-size: 24px;
      color: #94a3b8;
      font-weight: 300;
    }
  }
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 24px;
}

.section {
  margin-bottom: 120px;

  &:last-child {
    margin-bottom: 40px;
  }

  h2 {
    font-size: 36px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 48px;
    text-align: center;
  }
}

.intro {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }

  .section-content {
    h2 {
      text-align: left;
    }

    p {
      font-size: 18px;
      line-height: 1.8;
      color: #475569;
      margin-bottom: 24px;
      text-align: justify;
    }
  }

  .section-image {
    height: 400px;
    background: #f8fafc;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #e2e8f0;

    .image-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      color: #94a3b8;
      
      span {
        font-weight: 600;
        letter-spacing: 0.1em;
      }
    }
  }
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }

  .value-card {
    text-align: center;
    padding: 40px;
    background: #f8fafc;
    border-radius: 16px;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-8px);
      background: white;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    .icon-box {
      width: 64px;
      height: 64px;
      background: #eff6ff;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 24px;
      color: #2563eb;
      font-size: 32px;
    }

    h3 {
      font-size: 20px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 16px;
    }

    p {
      color: #64748b;
      line-height: 1.6;
    }
  }
}

.tech-stack {
  text-align: center;

  .tech-desc {
    font-size: 18px;
    color: #64748b;
    margin-bottom: 48px;
    margin-top: -32px;
  }

  .tech-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 16px;
    max-width: 800px;
    margin: 0 auto;

    .tech-item {
      padding: 12px 24px;
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 50px;
      font-weight: 600;
      color: #334155;
      font-size: 16px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      transition: all 0.2s;

      &:hover {
        border-color: #2563eb;
        color: #2563eb;
        transform: translateY(-2px);
      }
    }
  }
}
</style>

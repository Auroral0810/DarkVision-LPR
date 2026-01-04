<template>
  <div class="features-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>{{ $t('features.title') }}</h1>
        <p>探索下一代车牌识别技术的核心能力</p>
      </div>
    </div>

    <div class="page-container">
      <section class="features-list">
        <div class="feature-item">
          <div class="feature-visual">
            <div class="visual-card enhancement">
              <div class="before-after">
                <span>Before</span>
                <span>After</span>
              </div>
            </div>
          </div>
          <div class="feature-content">
            <div class="icon-box purple">
              <el-icon><MagicStick /></el-icon>
            </div>
            <h2>{{ $t('features.enhancement.title') }}</h2>
            <p>{{ $t('features.enhancement.desc') }}</p>
            <ul class="feature-points">
              <li>
                <strong>多尺度 Retinex 算法</strong>
                <span>动态调整图像对比度，在极低光照下还原细节。</span>
              </li>
              <li>
                <strong>自适应直方图均衡</strong>
                <span>智能平衡光照分布，消除阴影和过曝。</span>
              </li>
              <li>
                <strong>AI 降噪</strong>
                <span>深度学习去噪技术，保留边缘细节的同时去除噪点。</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="feature-item reverse">
          <div class="feature-visual">
            <div class="visual-card detection">
              <div class="scan-line"></div>
            </div>
          </div>
          <div class="feature-content">
            <div class="icon-box blue">
              <el-icon><Aim /></el-icon>
            </div>
            <h2>{{ $t('features.detection.title') }}</h2>
            <p>{{ $t('features.detection.desc') }}</p>
            <ul class="feature-points">
              <li>
                <strong>YOLOv12 架构</strong>
                <span>最新的目标检测模型，兼顾速度与精度。</span>
              </li>
              <li>
                <strong>全种类支持</strong>
                <span>支持蓝牌、黄牌、绿牌、黑牌及特种车牌。</span>
              </li>
              <li>
                <strong>毫秒级响应</strong>
                <span>端到端处理延迟低于 50ms，满足高速抓拍需求。</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="feature-item">
          <div class="feature-visual">
            <div class="visual-card scenarios">
              <div class="weather-icons">
                <span>☀️</span><span>🌧️</span><span>🌙</span><span>❄️</span>
              </div>
            </div>
          </div>
          <div class="feature-content">
            <div class="icon-box green">
              <el-icon><Monitor /></el-icon>
            </div>
            <h2>{{ $t('features.recognition.title') }}</h2>
            <p>{{ $t('features.recognition.desc') }}</p>
            <ul class="feature-points">
              <li>
                <strong>全天候适应</strong>
                <span>无论是正午强光还是深夜微光，表现始终如一。</span>
              </li>
              <li>
                <strong>复杂场景鲁棒性</strong>
                <span>针对倾斜、模糊、遮挡等常见干扰进行了专项优化。</span>
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MagicStick, Aim, Monitor } from '@element-plus/icons-vue'
</script>

<style scoped lang="scss">
.features-page {
  min-height: 100vh;
  background: white;
  padding-top: 72px;
}

.page-header {
  background: #0f172a;
  color: white;
  padding: 80px 24px 100px;
  text-align: center;
  position: relative;
  overflow: hidden;

  .header-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 80% 20%, #1e293b 0%, #0f172a 100%);
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

.features-list {
  display: flex;
  flex-direction: column;
  gap: 120px;
  margin-top: 80px;

  .feature-item {
    display: flex;
    align-items: center;
    gap: 80px;

    &.reverse {
      flex-direction: row-reverse;
    }

    .feature-visual {
      flex: 1;
      
      .visual-card {
        aspect-ratio: 4/3;
        background: #f1f5f9;
        border-radius: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
        
        &.enhancement {
          background: linear-gradient(90deg, #1e293b 50%, #e2e8f0 50%);
          
          .before-after {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            height: 60%;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(4px);
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            padding: 20px;
            color: white;
            font-weight: bold;
          }
        }
        
        &.detection {
          background: #0f172a;
          
          .scan-line {
            width: 100%;
            height: 2px;
            background: #22c55e;
            box-shadow: 0 0 10px #22c55e;
            position: absolute;
            top: 0;
            animation: scan 2s linear infinite;
          }
        }
        
        &.scenarios {
          background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          
          .weather-icons {
            font-size: 48px;
            display: flex;
            gap: 20px;
          }
        }
      }
    }

    .feature-content {
      flex: 1;

      .icon-box {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 24px;

        &.purple { background: #f3e8ff; color: #9333ea; }
        &.blue { background: #eff6ff; color: #2563eb; }
        &.green { background: #f0fdf4; color: #16a34a; }
      }

      h2 {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 16px;
      }

      p {
        font-size: 18px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 32px;
      }

      .feature-points {
        list-style: none;
        
        li {
          margin-bottom: 24px;
          
          strong {
            display: block;
            color: #0f172a;
            font-size: 16px;
            margin-bottom: 4px;
          }
          
          span {
            color: #64748b;
            font-size: 15px;
            line-height: 1.5;
          }
        }
      }
    }
  }
}

@keyframes scan {
  0% { top: 10%; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 90%; opacity: 0; }
}

@media (max-width: 768px) {
  .features-list {
    gap: 60px;
    
    .feature-item {
      flex-direction: column !important;
      gap: 32px;
    }
  }
}
</style>
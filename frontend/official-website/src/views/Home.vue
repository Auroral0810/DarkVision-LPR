<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg"></div>
      <div class="hero-container">
        <div class="hero-content">
          <div class="hero-badge">New Generation LPR</div>
          <h1 class="hero-title">
            智能感知，<span class="highlight">精准识别</span><br>
            让车牌识别更简单
          </h1>
          <p class="hero-description">
            {{ $t('home.description') }}<br>
            基于 YOLOv12 与 Retinex 图像增强技术，支持极端低光照场景，识别率高达 99.9%。
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary" @click="$router.push('/register')">
              {{ $t('home.getStarted') }}
              <el-icon class="icon"><Right /></el-icon>
            </button>
            <button class="btn btn-secondary" @click="$router.push('/contact')">
              {{ $t('home.consultation') }}
            </button>
          </div>
          
          <div class="hero-stats">
            <div class="stat-item">
              <span class="num">99.9%</span>
              <span class="label">识别准确率</span>
            </div>
            <div class="divider"></div>
            <div class="stat-item">
              <span class="num">&lt;50ms</span>
              <span class="label">响应速度</span>
            </div>
            <div class="divider"></div>
            <div class="stat-item">
              <span class="num">24/7</span>
              <span class="label">全天候支持</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Demo Section (Dashboard Preview) -->
    <section class="demo-section">
      <div class="container">
        <div class="demo-dashboard">
          <div class="dashboard-header">
            <div class="traffic-lights">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
            </div>
            <div class="address-bar">darkvision-lpr.com/demo</div>
          </div>
          <div class="dashboard-body">
            <div class="panel upload-panel">
              <div class="panel-title">
                <el-icon><Camera /></el-icon> 图像采集
              </div>
              <div class="image-preview">
                <!-- 模拟车辆图片 -->
                <div class="car-scene">
                  <div class="license-plate-overlay">
                    <span class="plate-text">京A·88888</span>
                    <div class="confidence-tag">99.8%</div>
                  </div>
                </div>
              </div>
              <div class="upload-actions">
                <div class="action-btn active"><el-icon><Picture /></el-icon> 上传图片</div>
                <div class="action-btn"><el-icon><VideoCamera /></el-icon> 视频流</div>
              </div>
            </div>
            <div class="panel result-panel">
              <div class="panel-title">
                <el-icon><DataAnalysis /></el-icon> 分析结果
              </div>
              <div class="result-list">
                <div class="result-row">
                  <span class="label">车牌号码</span>
                  <span class="value highlight">京A·88888</span>
                </div>
                <div class="result-row">
                  <span class="label">车牌颜色</span>
                  <span class="value">蓝色 <span class="color-dot blue"></span></span>
                </div>
                <div class="result-row">
                  <span class="label">置信度</span>
                  <span class="value">0.9982</span>
                </div>
                <div class="result-row">
                  <span class="label">车辆类型</span>
                  <span class="value">小型汽车</span>
                </div>
                
                <div class="json-preview">
<pre>{
  "plate": "京A·88888",
  "color": "blue",
  "confidence": 0.9982,
  "rect": [245, 380, 120, 45]
}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">{{ $t('home.features.title') }}</h2>
          <p class="section-subtitle">专为复杂场景打造的下一代车牌识别引擎</p>
        </div>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="icon-wrapper blue">
              <el-icon><Aim /></el-icon>
            </div>
            <h3>{{ $t('home.features.accurate') }}</h3>
            <p>基于最新的 YOLOv12 架构，我们在数百万张车牌数据上进行了微调，确保在各种角度下都能精准捕获。</p>
          </div>
          
          <div class="feature-card">
            <div class="icon-wrapper purple">
              <el-icon><Sunny /></el-icon>
            </div>
            <h3>{{ $t('home.features.lighting') }}</h3>
            <p>独有的 Retinex 图像增强算法，让系统在极低光照、逆光、强反光等恶劣光线下依然表现出色。</p>
          </div>
          
          <div class="feature-card">
            <div class="icon-wrapper green">
              <el-icon><Lightning /></el-icon>
            </div>
            <h3>高性能推理</h3>
            <p>深度优化的推理引擎，支持 TensorRT 加速，单张图片处理延迟低于 50ms，满足实时业务需求。</p>
          </div>

          <div class="feature-card">
            <div class="icon-wrapper orange">
              <el-icon><Monitor /></el-icon>
            </div>
            <h3>多端支持</h3>
            <p>提供 Web API、Windows/Linux SDK 以及移动端 SDK，轻松集成到您的现有业务系统中。</p>
          </div>

           <div class="feature-card">
            <div class="icon-wrapper red">
              <el-icon><Lock /></el-icon>
            </div>
            <h3>安全可靠</h3>
            <p>企业级数据加密传输，支持私有化部署，确保您的数据安全与隐私合规。</p>
          </div>

           <div class="feature-card">
            <div class="icon-wrapper cyan">
              <el-icon><DataLine /></el-icon>
            </div>
            <h3>数据洞察</h3>
            <p>内置强大的统计分析仪表盘，实时监控识别流量、成功率与业务趋势。</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-box">
          <div class="cta-content">
            <h2>准备好开始了吗？</h2>
            <p>立即注册体验免费额度，或联系我们获取企业级解决方案。</p>
          </div>
          <div class="cta-actions">
            <button class="btn btn-white" @click="$router.push('/register')">免费试用</button>
            <button class="btn btn-outline-white" @click="$router.push('/contact')">联系销售</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { Right, Camera, Picture, VideoCamera, DataAnalysis, Aim, Sunny, Lightning, Monitor, Lock, DataLine } from '@element-plus/icons-vue'
</script>

<style scoped lang="scss">
.home {
  width: 100%;
  overflow-x: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Buttons */
.btn {
  padding: 12px 28px;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  border: none;
  
  &.btn-primary {
    background: #2563eb;
    color: white;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);

    &:hover {
      background: #1d4ed8;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5);
    }
  }

  &.btn-secondary {
    background: white;
    color: #0f172a;
    border: 1px solid #e2e8f0;

    &:hover {
      border-color: #cbd5e1;
      background: #f8fafc;
      transform: translateY(-2px);
    }
  }

  &.btn-white {
    background: white;
    color: #2563eb;
    
    &:hover {
      background: #f1f5f9;
    }
  }

  &.btn-outline-white {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.6);
    }
  }
}

/* Hero Section */
.hero {
  position: relative;
  padding-top: 160px;
  padding-bottom: 180px;
  text-align: center;
  background: radial-gradient(circle at 50% 0%, #f1f5f9 0%, #ffffff 100%);
  overflow: hidden;

  .hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
      radial-gradient(circle at 15% 50%, rgba(37, 99, 235, 0.05) 0%, transparent 25%),
      radial-gradient(circle at 85% 30%, rgba(147, 51, 234, 0.05) 0%, transparent 25%);
    z-index: 0;
    pointer-events: none;
  }

  .hero-container {
    position: relative;
    z-index: 1;
    max-width: 800px;
    margin: 0 auto;
    padding: 0 24px;
  }

  .hero-badge {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(37, 99, 235, 0.1);
    color: #2563eb;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 24px;
    letter-spacing: 0.5px;
    border: 1px solid rgba(37, 99, 235, 0.2);
  }

  .hero-title {
    font-size: 56px;
    line-height: 1.1;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 24px;
    letter-spacing: -0.02em;

    .highlight {
      background: linear-gradient(135deg, #2563eb 0%, #9333ea 100%);
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }

  .hero-description {
    font-size: 20px;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 40px;
  }

  .hero-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 64px;
  }

  .hero-stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 32px;
    
    .divider {
      width: 1px;
      height: 24px;
      background: #e2e8f0;
    }

    .stat-item {
      display: flex;
      flex-direction: column;
      align-items: center;

      .num {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
      }
      .label {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
      }
    }
  }
}

/* Demo Section */
.demo-section {
  margin-top: -100px;
  position: relative;
  z-index: 10;
  padding-bottom: 80px;

  .demo-dashboard {
    background: #1e293b;
    border-radius: 16px;
    box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    max-width: 1000px;
    margin: 0 auto;

    .dashboard-header {
      background: #0f172a;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);

      .traffic-lights {
        display: flex;
        gap: 8px;
        margin-right: 20px;

        .dot {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          &.red { background: #ef4444; }
          &.yellow { background: #f59e0b; }
          &.green { background: #22c55e; }
        }
      }

      .address-bar {
        background: rgba(255, 255, 255, 0.05);
        color: #94a3b8;
        font-size: 13px;
        padding: 4px 16px;
        border-radius: 4px;
        flex: 1;
        text-align: center;
        font-family: monospace;
      }
    }

    .dashboard-body {
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      height: 500px;

      .panel {
        padding: 24px;
        
        .panel-title {
          color: #e2e8f0;
          font-weight: 600;
          margin-bottom: 16px;
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 15px;

          .el-icon {
            color: #3b82f6;
          }
        }
      }

      .upload-panel {
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;

        .image-preview {
          flex: 1;
          background: #0f172a;
          border-radius: 8px;
          margin-bottom: 20px;
          position: relative;
          overflow: hidden;
          background-image: url('https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80');
          background-size: cover;
          background-position: center;

          .car-scene {
            width: 100%;
            height: 100%;
            position: relative;
          }

          .license-plate-overlay {
            position: absolute;
            top: 60%;
            left: 50%;
            transform: translate(-50%, -50%);
            border: 2px solid #22c55e;
            padding: 4px 12px;
            background: rgba(34, 197, 94, 0.2);
            border-radius: 4px;
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);

            .confidence-tag {
              font-size: 10px;
              background: #22c55e;
              color: black;
              padding: 1px 4px;
              border-radius: 2px;
            }
          }
        }

        .upload-actions {
          display: flex;
          gap: 12px;

          .action-btn {
            background: rgba(255, 255, 255, 0.05);
            color: #94a3b8;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;

            &:hover {
              background: rgba(255, 255, 255, 0.1);
              color: white;
            }

            &.active {
              background: #2563eb;
              color: white;
            }
          }
        }
      }

      .result-panel {
        background: #0f172a;

        .result-list {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .result-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding-bottom: 12px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);

          .label {
            color: #94a3b8;
            font-size: 14px;
          }

          .value {
            color: #e2e8f0;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;

            &.highlight {
              color: #22c55e;
              font-size: 18px;
              font-weight: bold;
              font-family: monospace;
            }
          }

          .color-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            &.blue { background: #3b82f6; }
          }
        }

        .json-preview {
          margin-top: 20px;
          background: #1e293b;
          padding: 16px;
          border-radius: 8px;
          
          pre {
            color: #a5b4fc;
            font-family: monospace;
            font-size: 12px;
            margin: 0;
            white-space: pre-wrap;
          }
        }
      }
    }
  }
}

/* Features Section */
.features {
  padding: 100px 0;
  background: white;

  .section-header {
    text-align: center;
    max-width: 600px;
    margin: 0 auto 64px;

    .section-title {
      font-size: 36px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 16px;
    }

    .section-subtitle {
      font-size: 18px;
      color: #64748b;
    }
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 40px;
  }

  .feature-card {
    padding: 32px;
    border-radius: 16px;
    background: white;
    border: 1px solid #f1f5f9;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
      border-color: #e2e8f0;
    }

    .icon-wrapper {
      width: 56px;
      height: 56px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      margin-bottom: 24px;

      &.blue { background: #eff6ff; color: #2563eb; }
      &.purple { background: #f3e8ff; color: #9333ea; }
      &.green { background: #f0fdf4; color: #16a34a; }
      &.orange { background: #fff7ed; color: #ea580c; }
      &.red { background: #fef2f2; color: #dc2626; }
      &.cyan { background: #ecfeff; color: #0891b2; }
    }

    h3 {
      font-size: 20px;
      font-weight: 600;
      color: #0f172a;
      margin-bottom: 12px;
    }

    p {
      color: #64748b;
      line-height: 1.6;
    }
  }
}

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: white;

  .cta-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .cta-content {
      h2 {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 12px;
      }
      p {
        color: #94a3b8;
        font-size: 18px;
      }
    }

    .cta-actions {
      display: flex;
      gap: 16px;
    }
  }
}

@media (max-width: 1024px) {
  .hero {
    .hero-title {
      font-size: 42px;
    }
  }
  
  .demo-dashboard .dashboard-body {
    grid-template-columns: 1fr;
    height: auto;

    .upload-panel {
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      height: 400px;
    }
  }
}

@media (max-width: 768px) {
  .hero-stats {
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    
    .divider { display: none; }
    .stat-item { flex: 1 1 30%; }
  }

  .cta-box {
    flex-direction: column;
    text-align: center;
    gap: 32px;
    
    .cta-actions {
      width: 100%;
      flex-direction: column;
      
      .btn {
        width: 100%;
        justify-content: center;
      }
    }
  }
}
</style>
<template>
  <div class="careers-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>加入我们</h1>
        <p class="subtitle">与顶尖人才一起，探索 AI 的无限可能</p>
      </div>
    </div>

    <div class="page-container">
      <!-- 招聘理念 -->
      <section class="section culture">
        <h2>为什么选择 DarkVision？</h2>
        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="icon-box">💡</div>
            <h3>创新驱动</h3>
            <p>我们鼓励每一个疯狂的想法，这里是技术创新的试验田。</p>
          </div>
          <div class="benefit-card">
            <div class="icon-box">🚀</div>
            <h3>快速成长</h3>
            <p>扁平化管理，你将直接参与核心业务，获得指数级成长。</p>
          </div>
          <div class="benefit-card">
            <div class="icon-box">🌏</div>
            <h3>远程友好</h3>
            <p>我们支持灵活的工作方式，只看结果，不看打卡。</p>
          </div>
        </div>
      </section>

      <!-- 职位列表 (示例) -->
      <section class="section positions">
        <h2>开放职位</h2>
        <div class="position-list">
          <div class="position-card">
            <div class="pos-info">
              <h3>AI 算法工程师</h3>
              <span class="tag">全职 / 远程</span>
            </div>
            <p>负责 YOLO 系列模型的训练与优化，提升车牌识别在复杂场景下的准确率。</p>
            <button class="apply-btn" @click="scrollToContact">申请职位</button>
          </div>
          <div class="position-card">
            <div class="pos-info">
              <h3>全栈开发工程师</h3>
              <span class="tag">全职 / 南京</span>
            </div>
            <p>负责系统前后端开发（Vue3 + FastAPI），构建高可用、高性能的业务系统。</p>
            <button class="apply-btn" @click="scrollToContact">申请职位</button>
          </div>
          <div class="position-card">
            <div class="pos-info">
              <h3>开源社区运营</h3>
              <span class="tag">兼职 / 远程</span>
            </div>
            <p>负责 GitHub 社区维护，技术文档撰写，与开发者建立连接。</p>
            <button class="apply-btn" @click="scrollToContact">申请职位</button>
          </div>
        </div>
      </section>

      <!-- 联系方式 -->
      <section class="section contact" id="contact-section">
        <h2>联系我们</h2>
        <p class="contact-desc">无论是申请职位，还是商务合作，亦或是技术交流，我们随时欢迎您的联系。</p>
        
        <div class="contact-card">
          <div class="contact-grid">
            <!-- 电话 & 邮箱 -->
            <div class="contact-group">
              <div class="contact-item">
                <el-icon class="icon"><Iphone /></el-icon>
                <div class="info">
                  <span class="label">电话 / Phone</span>
                  <span class="value">15968588744</span>
                </div>
              </div>
              <div class="contact-item">
                <el-icon class="icon"><Message /></el-icon>
                <div class="info">
                  <span class="label">邮箱 / Email</span>
                  <a href="mailto:15968588744@163.com" class="value link">15968588744@163.com</a>
                </div>
              </div>
            </div>

            <!-- 社交媒体/链接 -->
            <div class="social-group">
              <a href="https://github.com/Auroral0810" target="_blank" class="social-btn github">
                <i class="fab fa-github"></i> GitHub 主页
              </a>
              <a href="http://fishblog.yyf040810.cn/" target="_blank" class="social-btn blog">
                <i class="fas fa-blog"></i> 个人博客
              </a>
            </div>

            <!-- 二维码展示 -->
            <div class="qr-grid">
              <div class="qr-item">
                <div class="qr-wrapper">
                  <img :src="wechatQr" alt="WeChat QR" />
                </div>
                <div class="qr-info">
                  <img :src="wechatIcon" class="platform-icon" />
                  <span class="id">Lucky_ff0810</span>
                </div>
              </div>
              
              <div class="qr-item">
                <div class="qr-wrapper">
                  <img :src="qqQr" alt="QQ QR" />
                </div>
                <div class="qr-info">
                  <img :src="qqIcon" class="platform-icon" />
                  <span class="id">1957689514</span>
                </div>
              </div>

              <div class="qr-item">
                <div class="qr-wrapper">
                  <img :src="csdnQr" alt="CSDN QR" />
                </div>
                <div class="qr-info">
                  <img :src="csdnIcon" class="platform-icon" />
                  <span class="id">Auroral0810</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Iphone, Message } from '@element-plus/icons-vue'

// 导入图片资源
import wechatIcon from '@/assets/images/wexin.png'
import wechatQr from '@/assets/images/wechat.jpg'
import qqIcon from '@/assets/images/qq.png'
import qqQr from '@/assets/images/QQ.jpg'
import csdnIcon from '@/assets/images/csdn博客.png'
import csdnQr from '@/assets/images/CSDN.png'

const scrollToContact = () => {
  document.getElementById('contact-section')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped lang="scss">
.careers-page {
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
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
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
  max-width: 1000px;
  margin: 0 auto;
  padding: 80px 24px;
}

.section {
  margin-bottom: 120px;

  h2 {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 48px;
    text-align: center;
  }
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }

  .benefit-card {
    background: #f8fafc;
    padding: 32px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #e2e8f0;

    .icon-box {
      font-size: 48px;
      margin-bottom: 24px;
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

.position-list {
  display: flex;
  flex-direction: column;
  gap: 24px;

  .position-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.2s;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);

    @media (max-width: 768px) {
      flex-direction: column;
      align-items: flex-start;
      gap: 24px;
    }

    &:hover {
      border-color: #2563eb;
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .pos-info {
      h3 {
        font-size: 20px;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 8px;
      }
      
      .tag {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb;
        font-size: 12px;
        padding: 4px 12px;
        border-radius: 50px;
        font-weight: 500;
      }
    }

    p {
      flex: 1;
      margin: 0 48px;
      color: #64748b;
      line-height: 1.6;

      @media (max-width: 768px) {
        margin: 0;
      }
    }

    .apply-btn {
      padding: 10px 24px;
      background: #0f172a;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;

      &:hover {
        background: #2563eb;
      }
    }
  }
}

.contact-desc {
  text-align: center;
  color: #64748b;
  font-size: 18px;
  max-width: 600px;
  margin: -32px auto 48px;
}

.contact-card {
  background: white;
  border-radius: 24px;
  padding: 48px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;

  .contact-grid {
    display: flex;
    flex-direction: column;
    gap: 48px;
  }

  .contact-group {
    display: flex;
    justify-content: center;
    gap: 64px;
    flex-wrap: wrap;

    .contact-item {
      display: flex;
      align-items: center;
      gap: 16px;

      .icon {
        width: 48px;
        height: 48px;
        background: #eff6ff;
        color: #2563eb;
        border-radius: 12px;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .info {
        display: flex;
        flex-direction: column;

        .label {
          font-size: 12px;
          color: #64748b;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin-bottom: 4px;
        }

        .value {
          font-size: 18px;
          font-weight: 600;
          color: #0f172a;

          &.link {
            color: #2563eb;
            text-decoration: none;
            
            &:hover {
              text-decoration: underline;
            }
          }
        }
      }
    }
  }

  .social-group {
    display: flex;
    justify-content: center;
    gap: 24px;

    .social-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 32px;
      border-radius: 50px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s;

      &.github {
        background: #24292e;
        color: white;

        &:hover {
          background: #000;
          transform: translateY(-2px);
        }
      }

      &.blog {
        background: #f59e0b;
        color: white;

        &:hover {
          background: #d97706;
          transform: translateY(-2px);
        }
      }
    }
  }

  .qr-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
    padding-top: 32px;
    border-top: 1px solid #e2e8f0;

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }

    .qr-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;

      .qr-wrapper {
        padding: 12px;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        
        img {
          width: 160px;
          height: 160px;
          display: block;
          border-radius: 4px;
        }
      }

      .qr-info {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .platform-icon {
          width: 20px;
          height: 20px;
          object-fit: contain;
        }

        .id {
          font-weight: 600;
          color: #475569;
        }
      }
    }
  }
}
</style>

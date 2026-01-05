<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="logo">
            <span class="brand">DarkVision</span>
            <span class="tag">LPR</span>
          </div>
          <p class="slogan">下一代智能车牌识别解决方案，为智慧交通、安防监控赋能。</p>
          <div class="social-links">
            <a href="#" class="social-link"><i class="icon">G</i></a>
            <a href="#" class="social-link"><i class="icon">T</i></a>
            <a href="#" class="social-link"><i class="icon">W</i></a>
          </div>
        </div>

        <div class="footer-nav">
          <div class="nav-group">
            <h3>产品</h3>
            <ul>
              <li><router-link to="/features">核心功能</router-link></li>
              <li><router-link to="/capabilities">系统能力</router-link></li>
              <li><router-link to="/pricing">价格方案</router-link></li>
              <li><router-link to="/download">下载中心</router-link></li>
            </ul>
          </div>
          <div class="nav-group">
            <h3>支持</h3>
            <ul>
              <li><router-link to="/documentation">技术文档</router-link></li>
              <li><router-link to="/contact">帮助中心</router-link></li>
              <li><router-link to="/contact">API 状态</router-link></li>
            </ul>
          </div>
          <div class="nav-group">
            <h3>公司</h3>
            <ul>
              <li><router-link to="/about">关于我们</router-link></li>
              <li><router-link to="/contact">联系我们</router-link></li>
              <li><router-link to="/careers">加入我们</router-link></li>
            </ul>
          </div>
          <div class="nav-group">
            <h3>法律</h3>
            <ul>
              <li><router-link to="/documentation?type=privacy">隐私政策</router-link></li>
              <li><router-link to="/documentation?type=agreement">服务条款</router-link></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <div class="copyright">
          © 2026 DarkVision LPR System. All Rights Reserved.
        </div>
        <div class="stats">
          <span class="label">累计服务请求:</span>
          <span class="value">{{ viewCount.toLocaleString() }}</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const viewCount = ref(0)

onMounted(() => {
  const stored = localStorage.getItem('viewCount')
  if (stored) {
    viewCount.value = parseInt(stored, 10)
  } else {
    viewCount.value = Math.floor(Math.random() * 10000) + 10000
    localStorage.setItem('viewCount', viewCount.value.toString())
  }
  
  viewCount.value++
  localStorage.setItem('viewCount', viewCount.value.toString())
})
</script>

<style scoped lang="scss">
.footer {
  background: #0f172a;
  color: #94a3b8;
  padding: 80px 0 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);

  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
  }

  .footer-grid {
    display: grid;
    grid-template-columns: 1.5fr 3fr;
    gap: 64px;
    margin-bottom: 64px;

    @media (max-width: 1024px) {
      grid-template-columns: 1fr;
    }
  }

  .footer-brand {
    .logo {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
      
      .footer-logo-img {
        width: 32px;
        height: 32px;
        object-fit: contain;
      }

      .brand-text {
        display: flex;
        align-items: baseline;
        gap: 8px;
      }
      
      .brand {
        font-size: 24px;
        font-weight: 700;
        color: white;
      }
      
      .tag {
        font-size: 12px;
        color: #64748b;
        letter-spacing: 0.1em;
      }
    }

    .slogan {
      line-height: 1.6;
      margin-bottom: 24px;
      max-width: 300px;
    }

    .social-links {
      display: flex;
      gap: 12px;
      
      .social-link {
        width: 36px;
        height: 36px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        transition: all 0.2s;
        font-style: normal;
        font-weight: bold;
        font-size: 14px;
        
        &:hover {
          background: #2563eb;
          transform: translateY(-2px);
        }
        
        .icon {
          font-style: normal;
        }
      }
    }
  }

  .footer-nav {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    
    @media (max-width: 768px) {
      grid-template-columns: repeat(2, 1fr);
    }

    .nav-group {
      h3 {
        color: white;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }

      ul {
        list-style: none;
        padding: 0;
        
        li {
          margin-bottom: 12px;
          
          a {
            color: #94a3b8;
            font-size: 14px;
            transition: color 0.2s;
            
            &:hover {
              color: white;
            }
          }
        }
      }
    }
  }

  .footer-bottom {
    padding-top: 32px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;

    @media (max-width: 640px) {
      flex-direction: column;
      gap: 16px;
    }
    
    .stats {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .value {
        color: #e2e8f0;
        font-family: monospace;
      }
    }
  }
}
</style>
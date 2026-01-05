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
            <div v-for="item in socialLinks" :key="item.name" class="social-item">
              <div class="social-link">
                <img :src="item.icon" :alt="item.name" class="social-icon-img" />
              </div>
              <div class="qr-popup">
                <img :src="item.qr" :alt="item.name + ' QR'" class="qr-img" />
              </div>
            </div>
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
              <li><a href="#" @click.prevent="openDoc('privacy')">隐私政策</a></li>
              <li><a href="#" @click.prevent="openDoc('agreement')">服务条款</a></li>
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

    <!-- 法律文档弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="docTitle"
      width="800px"
      class="legal-dialog"
      align-center
      destroy-on-close
    >
      <div class="legal-content">
        <el-scrollbar height="60vh">
          <component :is="currentDocComponent" />
        </el-scrollbar>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import PrivacyPolicy from '@/components/legal/PrivacyPolicy.vue'
import TermsOfService from '@/components/legal/TermsOfService.vue'

import wechatIcon from '@/assets/images/wexin.png'
import wechatQr from '@/assets/images/wechat.jpg'
import qqIcon from '@/assets/images/qq.png'
import qqQr from '@/assets/images/QQ.jpg'
import csdnIcon from '@/assets/images/csdn博客.png'
import csdnQr from '@/assets/images/CSDN.png'

const viewCount = ref(0)
const dialogVisible = ref(false)
const currentDocType = ref<'privacy' | 'agreement'>('privacy')

const socialLinks = [
  { name: 'WeChat', icon: wechatIcon, qr: wechatQr },
  { name: 'QQ', icon: qqIcon, qr: qqQr },
  { name: 'CSDN', icon: csdnIcon, qr: csdnQr }
]

const docTitle = computed(() => currentDocType.value === 'privacy' ? '隐私政策' : '服务条款')
const currentDocComponent = computed(() => currentDocType.value === 'privacy' ? PrivacyPolicy : TermsOfService)

const openDoc = (type: 'privacy' | 'agreement') => {
  currentDocType.value = type
  dialogVisible.value = true
}

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
      
      .social-item {
        position: relative;
        
        &:hover {
          .qr-popup {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(0);
          }
        }
      }
      
      .social-link {
        width: 36px;
        height: 36px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        
        &:hover {
          background: #2563eb;
          transform: translateY(-2px);
        }
        
        .social-icon-img {
          width: 20px;
          height: 20px;
          object-fit: contain;
          border-radius: 2px;
        }
      }

      .qr-popup {
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        margin-top: 12px;
        background: white;
        padding: 8px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 100;
        
        &::before {
            content: '';
            position: absolute;
            top: -6px;
            left: 50%;
            transform: translateX(-50%);
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-bottom: 6px solid white;
        }

        .qr-img {
          width: 120px;
          height: 120px;
          display: block;
          border-radius: 4px;
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

:deep(.legal-dialog) {
  border-radius: 12px;
  overflow: hidden;

  .el-dialog__header {
    margin: 0;
    padding: 20px 24px;
    border-bottom: 1px solid #f0f0f0;
    
    .el-dialog__title {
      font-size: 18px;
      font-weight: 600;
      color: #1f2937;
    }
  }

  .el-dialog__body {
    padding: 0;
  }

  .el-dialog__footer {
    padding: 16px 24px;
    border-top: 1px solid #f0f0f0;
  }
}

:deep(.legal-content) {
  padding: 24px;
}
</style>
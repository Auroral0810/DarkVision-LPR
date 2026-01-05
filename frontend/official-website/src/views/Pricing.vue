<template>
  <div class="pricing-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>{{ $t('pricing.title') }}</h1>
        <p>灵活的方案，满足不同规模的业务需求</p>
      </div>
    </div>

    <div class="page-container">
      <div class="pricing-cards">
        <!-- Free Plan -->
        <div class="pricing-card">
          <div class="card-header">
            <h2>{{ $t('pricing.free.name') }}</h2>
            <div class="price">
              <span class="currency">¥</span>
              <span class="amount">0</span>
              <span class="period">/月</span>
            </div>
            <p class="desc">{{ $t('pricing.free.desc') }}</p>
          </div>
          <div class="card-body">
            <ul class="features-list">
              <li><el-icon><Check /></el-icon>每日 20 次免费识别</li>
              <li><el-icon><Check /></el-icon>单张图片识别 (最大 5MB)</li>
              <li><el-icon><Check /></el-icon>历史记录保留 7 天</li>
              <li><el-icon><Check /></el-icon>基础准确率模型</li>
              <li><el-icon><Check /></el-icon>社区技术支持</li>
            </ul>
            <button class="plan-btn" @click="handleChoose('free')">
              {{ $t('pricing.choose') }}
            </button>
          </div>
        </div>

        <!-- VIP Plan -->
        <div class="pricing-card featured">
          <div class="featured-tag">MOST POPULAR</div>
          <div class="card-header">
            <h2>{{ $t('pricing.vip.name') }}</h2>
            <div class="price">
              <span class="currency">¥</span>
              <span class="amount">99</span>
              <span class="period">/月</span>
            </div>
            <p class="desc">{{ $t('pricing.vip.desc') }}</p>
          </div>
          <div class="card-body">
            <ul class="features-list">
              <li><el-icon><Check /></el-icon>每日 500 次识别 & 5000 次 API 调用</li>
              <li><el-icon><Check /></el-icon>批量图片识别 (50 张/次)</li>
              <li><el-icon><Check /></el-icon>视频文件识别 (10 个/月)</li>
              <li><el-icon><Check /></el-icon>高精度模式 (YOLOv12)</li>
              <li><el-icon><Check /></el-icon>永久历史记录 & 10GB 云存储</li>
            </ul>
            <button class="plan-btn primary" @click="handleChoose('vip')">
              {{ $t('pricing.choose') }}
            </button>
          </div>
        </div>

        <!-- Enterprise Plan -->
        <div class="pricing-card">
          <div class="card-header">
            <h2>{{ $t('pricing.enterprise.name') }}</h2>
            <div class="price">
              <span class="amount">定制</span>
            </div>
            <p class="desc">{{ $t('pricing.enterprise.desc') }}</p>
          </div>
          <div class="card-body">
            <ul class="features-list">
              <li><el-icon><Check /></el-icon>无限次识别 & API 调用</li>
              <li><el-icon><Check /></el-icon>私有化部署 & 定制化模型训练</li>
              <li><el-icon><Check /></el-icon>多账户管理 & 团队协作</li>
              <li><el-icon><Check /></el-icon>SLA 保障 & 专属客户经理</li>
              <li><el-icon><Check /></el-icon>企业级安全与审计日志</li>
            </ul>
            <button class="plan-btn" @click="handleChoose('enterprise')">
              {{ $t('pricing.choose') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能对比表格 -->
    <div class="comparison-section">
      <div class="section-container">
        <h2>详细功能对比</h2>
        <div class="table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>功能模块</th>
                <th>普通用户</th>
                <th class="highlight">VIP用户</th>
                <th>企业用户</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>单张图片识别</td>
                <td>20次/日</td>
                <td class="highlight">500次/日</td>
                <td>无限</td>
              </tr>
              <tr>
                <td>批量图片识别</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight">50张/次</td>
                <td>1000张/次</td>
              </tr>
              <tr>
                <td>视频识别</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight">10个/月</td>
                <td>无限</td>
              </tr>
              <tr>
                <td>实时摄像头识别</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight"><span class="check">✓</span></td>
                <td><span class="check">✓</span></td>
              </tr>
              <tr>
                <td>历史记录保留</td>
                <td>7天 (50条)</td>
                <td class="highlight">永久</td>
                <td>永久</td>
              </tr>
              <tr>
                <td>高精度模式 (YOLOv12)</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight"><span class="check">✓</span></td>
                <td><span class="check">✓</span></td>
              </tr>
              <tr>
                <td>API 调用</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight">5000次/日</td>
                <td>无限</td>
              </tr>
              <tr>
                <td>云端存储空间</td>
                <td>0 GB</td>
                <td class="highlight">10 GB</td>
                <td>无限</td>
              </tr>
              <tr>
                <td>多账户管理</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight"><span class="cross">✕</span></td>
                <td>50个子账户</td>
              </tr>
              <tr>
                <td>定制化模型</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight"><span class="cross">✕</span></td>
                <td><span class="check">✓</span></td>
              </tr>
              <tr>
                <td>私有化部署</td>
                <td><span class="cross">✕</span></td>
                <td class="highlight"><span class="cross">✕</span></td>
                <td>可选增值服务</td>
              </tr>
              <tr>
                <td>客服支持</td>
                <td>机器人</td>
                <td class="highlight">人工优先</td>
                <td>7×24 专属支持</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const { t } = useI18n()

const freeFeatures = computed(() => t('pricing.free.features', { returnObjects: true }) as string[])
const vipFeatures = computed(() => t('pricing.vip.features', { returnObjects: true }) as string[])
const enterpriseFeatures = computed(() => t('pricing.enterprise.features', { returnObjects: true }) as string[])

const handleChoose = (plan: string) => {
  if (plan === 'free') {
    router.push('/register')
  } else {
    router.push('/contact')
    ElMessage.info('请联系我们的销售团队获取更多信息')
  }
}
</script>

<style scoped lang="scss">
.pricing-page {
  min-height: 100vh;
  background: #f8fafc;
  padding-top: 72px; /* Header height */
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
      margin-bottom: 16px;
      letter-spacing: -0.02em;
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

.pricing-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  align-items: start;
}

.pricing-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  &.featured {
    border-color: #2563eb;
    box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.1), 0 10px 10px -5px rgba(37, 99, 235, 0.04);
    transform: scale(1.05);
    z-index: 2;

    @media (max-width: 1024px) {
      transform: none;
      z-index: 1;
    }

    &:hover {
      transform: scale(1.05) translateY(-8px);
      
      @media (max-width: 1024px) {
        transform: translateY(-8px);
      }
    }
  }

  .featured-tag {
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: #2563eb;
    color: white;
    padding: 4px 16px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.05em;
  }

  .card-header {
    text-align: center;
    margin-bottom: 32px;

    h2 {
      font-size: 20px;
      font-weight: 600;
      color: #0f172a;
      margin-bottom: 16px;
    }

    .price {
      display: flex;
      align-items: baseline;
      justify-content: center;
      color: #0f172a;
      
      .currency {
        font-size: 24px;
        font-weight: 500;
        margin-right: 4px;
      }

      .amount {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -0.02em;
      }

      .period {
        font-size: 16px;
        color: #64748b;
        margin-left: 4px;
      }
    }

    .desc {
      margin-top: 12px;
      font-size: 14px;
      color: #64748b;
    }
  }

  .features-list {
    list-style: none;
    margin-bottom: 32px;

    li {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
      color: #334155;
      font-size: 15px;

      .el-icon {
        color: #2563eb;
        flex-shrink: 0;
      }
    }
  }

  .plan-btn {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    background: white;
    border: 1px solid #e2e8f0;
    color: #0f172a;

    &:hover {
      background: #f8fafc;
      border-color: #cbd5e1;
    }

    &.primary {
      background: #2563eb;
      border-color: #2563eb;
      color: white;

      &:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
      }
    }
  }
}

.comparison-section {
  padding: 80px 0;
  background: white;

  .section-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 24px;

    h2 {
      text-align: center;
      font-size: 30px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 48px;
    }
  }

  .table-wrapper {
    overflow-x: auto;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    border: 1px solid #e2e8f0;
  }

  .comparison-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    
    th, td {
      padding: 16px 24px;
      text-align: center;
      border-bottom: 1px solid #e2e8f0;
      color: #334155;
      font-size: 15px;

      &:first-child {
        text-align: left;
        font-weight: 500;
        color: #0f172a;
        padding-left: 32px;
        width: 25%;
      }
    }

    thead {
      th {
        background: #f8fafc;
        font-weight: 600;
        color: #0f172a;
        font-size: 16px;
        padding-top: 20px;
        padding-bottom: 20px;
        
        &.highlight {
          color: #2563eb;
          background: #eff6ff;
        }
      }
    }

    tbody {
      tr:last-child td {
        border-bottom: none;
      }

      tr:hover td {
        background: #f8fafc;
      }
      
      .highlight {
        background: #eff6ff;
        font-weight: 500;
        color: #1e40af;
      }

      tr:hover .highlight {
        background: #dbeafe;
      }

      .check {
        color: #16a34a;
        font-weight: bold;
        font-size: 18px;
      }

      .cross {
        color: #cbd5e1;
        font-size: 18px;
      }
    }
  }
}
</style>
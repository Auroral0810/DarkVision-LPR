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
        <div 
          class="pricing-card" 
          v-for="pkg in packages" 
          :key="pkg.id"
          :class="{ featured: pkg.code.includes('vip') }"
        >
          <div class="featured-tag" v-if="pkg.code === 'vip_yearly'">推荐 (省33%)</div>
          <div class="card-header">
            <h2>{{ pkg.name }}</h2>
            <div class="price">
              <span class="currency">¥</span>
              <span class="amount">{{ pkg.price == 0 ? (pkg.code === 'enterprise_custom' ? '定制' : '0') : Number(pkg.price) }}</span>
              <span class="period" v-if="pkg.duration_months">/{{ pkg.duration_months === 12 ? '年' : '月' }}</span>
            </div>
            <p class="desc">{{ pkg.description }}</p>
          </div>
          <div class="card-body">
            <ul class="features-list">
              <!-- 根据关键特性展示，这里手动选取几个重要特性用于卡片展示 -->
              <li v-if="pkg.features.daily_limit">
                <el-icon><Check /></el-icon>
                每日 {{ pkg.features.daily_limit === '0' ? '无限' : pkg.features.daily_limit }} 次识别
              </li>
              <li v-if="pkg.features.api_access === 'true'">
                <el-icon><Check /></el-icon>
                API 调用支持
              </li>
              <li v-if="pkg.features.video_recognition_enabled === 'true'">
                <el-icon><Check /></el-icon>
                视频识别支持
              </li>
              <li v-if="pkg.features.model_version">
                 <el-icon><Check /></el-icon>
                 {{ pkg.features.model_version === 'base' ? '基础精度模型' : '高精度模型 (YOLOv12)' }}
              </li>
              <li v-if="pkg.features.cloud_storage_enabled === 'true'">
                <el-icon><Check /></el-icon>
                {{ pkg.features.cloud_storage_size_gb === '0' ? '云存储按需' : pkg.features.cloud_storage_size_gb + 'GB 云存储' }}
              </li>
            </ul>
            <button class="plan-btn" :class="{ primary: pkg.code.includes('vip') }" @click="handleChoose(pkg.code)">
              {{ $t('pricing.choose') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能对比表格 -->
    <div class="comparison-section" v-if="packages.length > 0">
      <div class="section-container">
        <h2>详细功能对比</h2>
        <div class="table-wrapper">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>功能模块</th>
                <th v-for="pkg in packages" :key="pkg.id" :class="{ highlight: pkg.code.includes('vip') }">
                  {{ pkg.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in comparisonRows" :key="row.label">
                <td>{{ row.label }}</td>
                <td v-for="pkg in packages" :key="pkg.id" :class="{ highlight: pkg.code.includes('vip') }">
                  <span v-html="formatFeatureValue(row, pkg)"></span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getPricingPlans } from '../api/website'

const router = useRouter()
const { t } = useI18n()

interface Package {
  id: number
  name: string
  code: string
  price: number
  duration_months: number | null
  description: string
  features: Record<string, string>
}

const packages = ref<Package[]>([])

const fetchPackages = async () => {
  try {
    const res = await getPricingPlans()
    if (res.code === 20000 && res.data) {
      packages.value = res.data
    }
  } catch (error) {
    console.error("Failed to fetch pricing plans", error)
  }
}

onMounted(() => {
  fetchPackages()
})

const handleChoose = (code: string) => {
  if (code === 'free') {
    router.push('/register')
  } else if (code === 'enterprise_custom') {
    router.push('/contact')
    ElMessage.info('请联系我们的销售团队获取更多信息')
  } else {
    // VIP scenarios
    router.push({ path: '/register', query: { plan: code } })
  }
}

// Comparison Table Logic
interface ComparisonRow {
  label: string
  key: string // Primary feature key
  format?: (pkg: Package) => string
}

const comparisonRows: ComparisonRow[] = [
  { label: '每日识别限额', key: 'daily_limit', format: (pkg) => pkg.features.daily_limit === '0' ? '无限' : `${pkg.features.daily_limit}次` },
  { label: 'API每日限额', key: 'api_daily_limit', format: (pkg) => pkg.features.api_daily_limit === '0' ? (pkg.code === 'free' ? '<span class="cross">✕</span>' : '无限') : `${pkg.features.api_daily_limit}次` },
  { label: '单张图片识别', key: 'single_image_enabled', format: (pkg) => pkg.features.single_image_enabled === 'true' ? '<span class="check">✓</span>' : '<span class="cross">✕</span>' },
  { label: '批量图片识别', key: 'batch_upload_enabled', format: (pkg) => pkg.features.batch_upload_enabled === 'true' ? `${pkg.features.batch_upload_max_count}张/次` : '<span class="cross">✕</span>' },
  { label: '视频识别', key: 'video_recognition_enabled', format: (pkg) => pkg.features.video_recognition_enabled === 'true' ? (pkg.features.video_monthly_limit === '0' ? '无限' : `${pkg.features.video_monthly_limit}个/月`) : '<span class="cross">✕</span>' },
  { label: '高精度模式 (YOLOv12)', key: 'high_precision_mode', format: (pkg) => pkg.features.high_precision_mode === 'true' ? '<span class="check">✓</span>' : '<span class="cross">✕</span>' },
  { label: 'API 访问权限', key: 'api_access', format: (pkg) => pkg.features.api_access === 'true' ? '<span class="check">✓</span>' : '<span class="cross">✕</span>' },
  { label: '云端存储', key: 'cloud_storage_enabled', format: (pkg) => pkg.features.cloud_storage_enabled === 'true' ? (pkg.features.cloud_storage_size_gb === '0' ? '按需' : `${pkg.features.cloud_storage_size_gb}GB`) : '0GB' },
  { label: '历史记录保留', key: 'history_retention_days', format: (pkg) => pkg.features.history_retention_days === '0' ? '永久' : `${pkg.features.history_retention_days}天` },
  { label: '多账户管理', key: 'sub_account_enabled', format: (pkg) => pkg.features.sub_account_enabled === 'true' ? `${pkg.features.sub_account_max_count}个` : '<span class="cross">✕</span>' },
  { label: '私有化部署', key: 'on_premise_deployment', format: (pkg) => pkg.features.on_premise_deployment === 'true' ? '支持' : '<span class="cross">✕</span>' },
  { label: '客服支持', key: 'priority_support', format: (pkg) => pkg.features.priority_support === 'true' ? (pkg.code.includes('enterprise') ? '7x24专属' : '优先支持') : '社区支持' },
]

const formatFeatureValue = (row: ComparisonRow, pkg: Package) => {
  if (row.format) {
    return row.format(pkg)
  }
  return pkg.features[row.key] || '-'
}
</script>

<style scoped lang="scss">
.pricing-page {
  min-height: 100vh;
  background: #f8fafc;
  padding-top: 60px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.page-header {
  background: #0f172a;
  color: white;
  padding: 100px 24px 160px;
  text-align: center;
  position: relative;
  overflow: hidden;

  .header-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 0%, #3b82f6 0%, #0f172a 60%);
    opacity: 0.4;
    z-index: 1;
  }

  .header-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;

    h1 {
      font-size: 56px;
      font-weight: 800;
      margin-bottom: 24px;
      letter-spacing: -0.03em;
      background: linear-gradient(to right, #ffffff, #93c5fd);
      background-clip: text;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    p {
      font-size: 20px;
      color: #cbd5e1;
      font-weight: 400;
      line-height: 1.6;
    }
  }
}

.page-container {
  max-width: 1280px;
  margin: -100px auto 80px;
  padding: 0 32px;
  position: relative;
  z-index: 10;
}

.pricing-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 24px;
}

.pricing-card {
  flex: 1;
  min-width: 280px;
  max-width: 320px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 40px 32px;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08); // Softer, deeper shadow
  border: 1px solid rgba(255, 255, 255, 0.5);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-12px);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.12);
  }

  &.featured {
    background: #ffffff;
    border: 2px solid #3b82f6; // Slightly more vibrant blue
    box-shadow: 0 20px 40px -10px rgba(59, 130, 246, 0.15);
    z-index: 2;
    transform: scale(1.05);

    @media (max-width: 1024px) {
      transform: none;
      border-width: 1px;
    }

    &:hover {
      transform: scale(1.05) translateY(-12px);
      box-shadow: 0 30px 60px -12px rgba(59, 130, 246, 0.25);

      @media (max-width: 1024px) {
        transform: translateY(-8px);
      }
    }
  }

  .featured-tag {
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    padding: 6px 20px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
  }

  .card-header {
    text-align: center;
    margin-bottom: 40px;

    h2 {
      font-size: 22px;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 16px;
    }

    .price {
      display: flex;
      align-items: baseline;
      justify-content: center;
      color: #0f172a;
      
      .currency {
        font-size: 24px;
        font-weight: 600;
        margin-right: 4px;
        color: #64748b;
      }

      .amount {
        font-size: 56px;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1;
      }

      .period {
        font-size: 16px;
        font-weight: 500;
        color: #64748b;
        margin-left: 6px;
      }
    }

    .desc {
      margin-top: 16px;
      font-size: 15px;
      color: #64748b;
      line-height: 1.5;
    }
  }

  .card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .features-list {
    flex: 1;
    list-style: none;
    margin-bottom: 40px;
    padding: 0;

    li {
      display: flex;
      align-items: start;
      gap: 12px;
      margin-bottom: 16px;
      color: #475569;
      font-size: 15px;
      line-height: 1.5;

      .el-icon {
        color: #3b82f6;
        font-size: 18px;
        margin-top: 2px;
        flex-shrink: 0;
        background: rgba(59, 130, 246, 0.1);
        padding: 2px;
        border-radius: 50%;
      }
    }
  }

  .plan-btn {
    width: 100%;
    padding: 16px;
    border-radius: 14px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    background: transparent;
    border: 2px solid #e2e8f0;
    color: #475569;

    &:hover {
      background: #f8fafc;
      border-color: #cbd5e1;
      color: #1e293b;
    }

    &.primary {
      background: #2563eb;
      border-color: #2563eb;
      color: white;
      box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.15);

      &:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.25);
        transform: translateY(-2px);
      }
      
      &:active {
        transform: translateY(0);
      }
    }
  }
}

.comparison-section {
  padding: 100px 0;
  background: white;

  .section-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 32px;

    h2 {
      text-align: center;
      font-size: 36px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 64px;
      letter-spacing: -0.02em;
    }
  }

  .table-wrapper {
    overflow-x: auto;
    border-radius: 24px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
    border: 1px solid #f1f5f9;
    background: white;
  }

  .comparison-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    
    th, td {
      padding: 20px 32px;
      text-align: center;
      border-bottom: 1px solid #f1f5f9;
      color: #475569;
      font-size: 15px;

      &:first-child {
        text-align: left;
        font-weight: 600;
        color: #1e293b;
        position: sticky;
        left: 0;
        background: inherit;
        z-index: 10;
        border-right: 1px solid #f1f5f9;
      }
      
      &:not(:first-child) {
        min-width: 160px;
      }
    }

    thead {
      th {
        background: #f8fafc;
        font-weight: 700;
        color: #0f172a;
        font-size: 18px;
        padding-top: 32px;
        padding-bottom: 32px;
        
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
        
        &.highlight {
           background: #dbeafe;
        }
      }
      
      .highlight {
        background: #eff6ff;
        font-weight: 500;
        color: #1e40af;
      }

      .check {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #dcfce7;
        color: #16a34a;
        font-size: 16px; 
        font-weight: bold;
      }

      .cross {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #f1f5f9;
        color: #94a3b8;
        font-size: 16px;
      }
    }
  }
}
</style>
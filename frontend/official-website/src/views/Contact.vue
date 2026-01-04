<template>
  <div class="contact-page">
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1>{{ $t('contact.title') }}</h1>
        <p>{{ $t('contact.consultation') }}</p>
      </div>
    </div>

    <div class="page-container">
      <div class="contact-wrapper">
        <div class="info-sidebar">
          <h2>联系方式</h2>
          <p class="desc">无论是技术咨询、商务合作还是产品建议，我们都乐于听到您的声音。</p>
          
          <div class="info-list">
            <div class="info-item">
              <div class="icon"><Message /></div>
              <div>
                <strong>邮箱</strong>
                <p>support@darkvision-lpr.com</p>
              </div>
            </div>
            <div class="info-item">
              <div class="icon"><Phone /></div>
              <div>
                <strong>电话</strong>
                <p>400-888-8888</p>
              </div>
            </div>
            <div class="info-item">
              <div class="icon"><Location /></div>
              <div>
                <strong>地址</strong>
                <p>北京市海淀区中关村大街1号</p>
              </div>
            </div>
          </div>
        </div>

        <div class="form-container">
          <h2>在线咨询</h2>
          <el-form :model="form" label-position="top" size="large">
            <div class="form-row">
              <el-form-item label="姓名" class="half">
                <el-input v-model="form.name" placeholder="您的姓名" />
              </el-form-item>
              <el-form-item label="邮箱" class="half">
                <el-input v-model="form.email" placeholder="您的邮箱" />
              </el-form-item>
            </div>
            <el-form-item label="问题或建议">
              <el-input
                v-model="form.message"
                type="textarea"
                :rows="6"
                :placeholder="$t('contact.placeholder')"
              />
            </el-form-item>
            <el-form-item>
              <button class="submit-btn" @click.prevent="handleSubmit">
                {{ $t('contact.send') }}
              </button>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <div class="faq-section">
        <h2 class="section-title">常见问题</h2>
        <div class="faq-grid">
          <div class="faq-item">
            <h3>如何开始使用系统？</h3>
            <p>注册账号后即可开始使用，普通用户每日有20次免费识别机会。您可以在控制台查看详细的使用指南。</p>
          </div>
          <div class="faq-item">
            <h3>支持哪些图片格式？</h3>
            <p>支持 JPG、PNG、BMP 等常见图片格式。单张图片建议在 5MB 以内，VIP 用户支持最大 10MB 的高清图片。</p>
          </div>
          <div class="faq-item">
            <h3>如何升级到 VIP？</h3>
            <p>在价格页面选择 VIP 方案，点击购买并完成支付后，您的账号将立即升级，享受更多权益。</p>
          </div>
          <div class="faq-item">
            <h3>是否提供 API 接口？</h3>
            <p>是的，VIP 用户和企业用户可以使用 RESTful API 接口。我们提供完善的 API 文档和多语言 SDK。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Message, Phone, Location } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const form = ref({
  name: '',
  email: '',
  message: ''
})

const handleSubmit = () => {
  if (!form.value.name || !form.value.email || !form.value.message) {
    ElMessage.warning('请填写完整信息')
    return
  }
  ElMessage.success('提交成功，我们会尽快回复您！')
  form.value = {
    name: '',
    email: '',
    message: ''
  }
}
</script>

<style scoped lang="scss">
.contact-page {
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
    background: radial-gradient(circle at 50% 100%, #1e293b 0%, #0f172a 100%);
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

.contact-wrapper {
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
  display: grid;
  grid-template-columns: 1fr 2fr;
  overflow: hidden;
  margin-top: -80px;
  position: relative;
  z-index: 10;
  margin-bottom: 80px;

  .info-sidebar {
    background: #1e293b;
    color: white;
    padding: 48px;

    h2 {
      font-size: 24px;
      margin-bottom: 16px;
    }

    .desc {
      color: #94a3b8;
      margin-bottom: 40px;
      line-height: 1.6;
    }

    .info-list {
      display: flex;
      flex-direction: column;
      gap: 32px;

      .info-item {
        display: flex;
        gap: 16px;

        .icon {
          width: 40px;
          height: 40px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #3b82f6;
        }

        strong {
          display: block;
          font-size: 14px;
          color: #94a3b8;
          margin-bottom: 4px;
        }

        p {
          font-size: 16px;
          color: white;
        }
      }
    }
  }

  .form-container {
    padding: 48px;

    h2 {
      font-size: 24px;
      color: #0f172a;
      margin-bottom: 32px;
    }

    .form-row {
      display: flex;
      gap: 24px;
      
      .half {
        flex: 1;
      }
    }

    .submit-btn {
      background: #2563eb;
      color: white;
      padding: 12px 32px;
      border-radius: 8px;
      border: none;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;

      &:hover {
        background: #1d4ed8;
      }
    }
  }
}

.faq-section {
  .section-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 48px;
  }

  .faq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 32px;

    .faq-item {
      background: white;
      padding: 32px;
      border-radius: 16px;
      border: 1px solid #e2e8f0;

      h3 {
        font-size: 18px;
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
}

@media (max-width: 768px) {
  .contact-wrapper {
    grid-template-columns: 1fr;
    
    .form-row {
      flex-direction: column;
      gap: 0;
    }
  }

  .faq-grid {
    grid-template-columns: 1fr;
  }
}
</style>
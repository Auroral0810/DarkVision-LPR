<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo">
            <span class="logo-icon">DV</span>
          </div>
          <h1>{{ $t('login.title') }}</h1>
          <p>欢迎回来，请登录您的账号</p>
        </div>

        <el-tabs v-model="loginType" class="login-tabs">
          <el-tab-pane label="手机号登录" name="phone">
            <el-form :model="phoneForm" :rules="phoneRules" ref="phoneFormRef" size="large">
              <el-form-item prop="phone">
                <el-input
                  v-model="phoneForm.phone"
                  placeholder="请输入手机号"
                >
                  <template #prefix>
                    <el-icon><Iphone /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item prop="code">
                <div class="code-input">
                  <el-input
                    v-model="phoneForm.code"
                    placeholder="请输入验证码"
                  >
                    <template #prefix>
                      <el-icon><Key /></el-icon>
                    </template>
                  </el-input>
                  <el-button
                    type="primary"
                    link
                    :disabled="codeDisabled"
                    @click="sendCode"
                    class="code-btn"
                  >
                    {{ codeButtonText }}
                  </el-button>
                </div>
              </el-form-item>
              <div class="form-options">
                <el-checkbox v-model="rememberMe">{{ $t('login.remember') }}</el-checkbox>
                <el-link type="primary" :underline="false" @click="$router.push('/forgot-password')">
                  {{ $t('login.forgot') }}
                </el-link>
              </div>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="loading"
                @click="handlePhoneLogin"
              >
                {{ $t('login.login') }}
              </el-button>
            </el-form>
          </el-tab-pane>

          <el-tab-pane label="邮箱登录" name="email">
            <el-form :model="emailForm" :rules="emailRules" ref="emailFormRef" size="large">
              <el-form-item prop="email">
                <el-input
                  v-model="emailForm.email"
                  placeholder="请输入邮箱"
                >
                  <template #prefix>
                    <el-icon><Message /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <el-form-item prop="password">
                <el-input
                  v-model="emailForm.password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
                >
                  <template #prefix>
                    <el-icon><Lock /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              <div class="form-options">
                <el-checkbox v-model="rememberMe">{{ $t('login.remember') }}</el-checkbox>
                <el-link type="primary" :underline="false" @click="$router.push('/forgot-password')">
                  {{ $t('login.forgot') }}
                </el-link>
              </div>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="loading"
                @click="handleEmailLogin"
              >
                {{ $t('login.login') }}
              </el-button>
            </el-form>
          </el-tab-pane>
        </el-tabs>

        <div class="divider">
          <span>{{ $t('login.thirdParty') }}</span>
        </div>

        <div class="third-party-buttons">
          <div class="icon-btn wechat" @click="handleThirdPartyLogin('wechat')">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="icon-btn qq" @click="handleThirdPartyLogin('qq')">
            <el-icon><User /></el-icon>
          </div>
          <div class="icon-btn github" @click="handleThirdPartyLogin('github')">
            <el-icon><Link /></el-icon>
          </div>
        </div>

        <div class="login-footer">
          <span>{{ $t('login.noAccount') }}</span>
          <el-link type="primary" :underline="false" @click="$router.push('/register')">
            {{ $t('login.register') }}
          </el-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { Iphone, Message, Lock, Key, ChatDotRound, User, Link } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const loginType = ref('phone')
const loading = ref(false)
const rememberMe = ref(false)
const codeDisabled = ref(false)
const countdown = ref(0)

const phoneFormRef = ref<FormInstance>()
const emailFormRef = ref<FormInstance>()

const phoneForm = ref({
  phone: '',
  code: ''
})

const emailForm = ref({
  email: '',
  password: ''
})

const phoneRules: FormRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ]
}

const emailRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const codeButtonText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}s` : '获取验证码'
})

const sendCode = async () => {
  if (!phoneForm.value.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  
  ElMessage.success('验证码已发送')
  codeDisabled.value = true
  countdown.value = 60
  
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      codeDisabled.value = false
    }
  }, 1000)
}

const handlePhoneLogin = async () => {
  if (!phoneFormRef.value) return
  
  await phoneFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      setTimeout(() => {
        userStore.login('mock-token', {
          phone: phoneForm.value.phone,
          nickname: '用户' + phoneForm.value.phone.slice(-4)
        })
        loading.value = false
        ElMessage.success('登录成功')
        router.push('/')
      }, 1000)
    }
  })
}

const handleEmailLogin = async () => {
  if (!emailFormRef.value) return
  
  await emailFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      setTimeout(() => {
        userStore.login('mock-token', {
          email: emailForm.value.email,
          nickname: '用户'
        })
        loading.value = false
        ElMessage.success('登录成功')
        router.push('/')
      }, 1000)
    }
  })
}

const handleThirdPartyLogin = (type: string) => {
  ElMessage.info(`${type}登录功能开发中...`)
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-container {
  width: 100%;
  max-width: 420px;
}

.login-card {
  background: white;
  border-radius: 24px;
  padding: 48px;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
  
  .login-header {
    text-align: center;
    margin-bottom: 40px;
    
    .logo {
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 24px;
      
      .logo-icon {
        color: white;
        font-weight: 800;
        font-size: 18px;
      }
    }
    
    h1 {
      font-size: 24px;
      font-weight: 700;
      color: #0f172a;
      margin-bottom: 8px;
    }
    
    p {
      color: #64748b;
      font-size: 14px;
    }
  }
  
  .login-tabs {
    margin-bottom: 24px;
    
    :deep(.el-tabs__nav-wrap::after) {
      height: 1px;
      background-color: #e2e8f0;
    }
    
    :deep(.el-tabs__item) {
      font-size: 15px;
      color: #64748b;
      
      &.is-active {
        color: #2563eb;
        font-weight: 600;
      }
    }
    
    :deep(.el-tabs__active-bar) {
      background-color: #2563eb;
    }
  }
  
  .code-input {
    position: relative;
    
    .code-btn {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      padding: 0;
      height: auto;
      font-weight: 600;
    }
  }
  
  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    :deep(.el-checkbox__label) {
      color: #64748b;
    }
  }
  
  .submit-btn {
    width: 100%;
    height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    background: #2563eb;
    border-color: #2563eb;
    
    &:hover {
      background: #1d4ed8;
      border-color: #1d4ed8;
    }
  }
  
  .divider {
    position: relative;
    text-align: center;
    margin: 32px 0 24px;
    
    &::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      height: 1px;
      background: #e2e8f0;
    }
    
    span {
      position: relative;
      background: white;
      padding: 0 16px;
      color: #94a3b8;
      font-size: 12px;
    }
  }
  
  .third-party-buttons {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-bottom: 32px;
    
    .icon-btn {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 20px;
      color: #64748b;
      
      &:hover {
        transform: translateY(-2px);
        background: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      }
      
      &.wechat:hover { color: #07c160; border-color: #07c160; }
      &.qq:hover { color: #12b7f5; border-color: #12b7f5; }
      &.github:hover { color: #24292e; border-color: #24292e; }
    }
  }
  
  .login-footer {
    text-align: center;
    color: #64748b;
    font-size: 14px;
    
    .el-link {
      margin-left: 8px;
      color: #2563eb;
      font-weight: 600;
      
      &:hover {
        color: #1d4ed8;
      }
    }
  }
}

:deep(.el-input__wrapper) {
  background-color: #f8fafc;
  box-shadow: none !important;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1px 15px;
  transition: all 0.2s;
  
  &:hover {
    border-color: #cbd5e1;
  }
  
  &.is-focus {
    background-color: white;
    border-color: #2563eb;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
  }
}

:deep(.el-input__inner) {
  height: 46px;
}
</style>
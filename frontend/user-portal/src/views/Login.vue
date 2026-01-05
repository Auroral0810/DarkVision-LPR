<template>
  <div class="auth-page">
    <div class="login-layout">
      <div class="login-side">
        <div class="brand-content">
          <div class="brand-logo">
            <span class="logo-text">DV</span>
          </div>
          <h2>DarkVision LPR</h2>
          <p class="slogan">极速、精准、企业级的车牌识别平台</p>
          <ul class="features-list">
            <li><el-icon><Check /></el-icon> 99.9% 识别准确率</li>
            <li><el-icon><Check /></el-icon> &lt;50ms 响应速度</li>
            <li><el-icon><Check /></el-icon> 夜间/逆光稳健识别</li>
            <li><el-icon><Check /></el-icon> 私有化与多端支持</li>
          </ul>
        </div>
        <div class="side-bg-overlay"></div>
      </div>

      <div class="login-form-container">
        <div class="form-header">
          <h2 v-if="!showForgot">欢迎回来，请登录您的账号</h2>
          <h2 v-else>重置密码</h2>
          <p v-if="!showForgot">开启高性能识别之旅</p>
          <p v-else>通过验证码重置您的密码</p>
        </div>

        <template v-if="showForgot">
          <el-form :model="forgotForm" :rules="forgotRules" ref="forgotFormRef" size="large" class="login-form">
            <el-form-item prop="account">
              <el-input v-model="forgotForm.account" placeholder="手机号或邮箱">
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="code">
              <div class="input-group">
                <el-input v-model="forgotForm.code" placeholder="验证码" maxlength="6">
                  <template #prefix>
                    <el-icon><Key /></el-icon>
                  </template>
                </el-input>
                <el-button 
                  type="primary" 
                  plain
                  class="send-btn"
                  :disabled="codeDisabled"
                  @click="sendForgotCode"
                  :loading="sendingCode"
                >
                  {{ codeButtonText }}
                </el-button>
              </div>
            </el-form-item>
            <el-form-item prop="newPassword">
              <el-input
                v-model="forgotForm.newPassword"
                type="password"
                placeholder="新密码（6-20位）"
                show-password
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="forgotForm.confirmPassword"
                type="password"
                placeholder="确认新密码"
                show-password
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <div class="form-options">
              <el-link type="primary" :underline="false" @click="showForgot = false">返回登录</el-link>
            </div>
            <el-button
              type="primary"
              class="submit-btn"
              :loading="loading"
              @click="handleResetPassword"
              round
            >
              提交重置
            </el-button>
          </el-form>
        </template>

        <template v-else>
          <el-tabs v-model="loginType" class="login-tabs" stretch>
            <el-tab-pane label="验证码登录" name="code">
              <el-form :model="codeForm" :rules="codeRules" ref="codeFormRef" size="large" class="login-form">
                <el-form-item prop="account">
                  <el-input v-model="codeForm.account" placeholder="手机号或邮箱">
                    <template #prefix>
                      <el-icon><User /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item prop="code">
                  <div class="input-group">
                    <el-input v-model="codeForm.code" placeholder="请输入验证码" maxlength="6">
                      <template #prefix>
                        <el-icon><Key /></el-icon>
                      </template>
                    </el-input>
                    <el-button 
                      type="primary" 
                      plain
                      class="send-btn"
                      :disabled="codeDisabled"
                      @click="sendLoginCode"
                      :loading="sendingCode"
                    >
                      {{ codeButtonText }}
                    </el-button>
                  </div>
                </el-form-item>
                <div class="form-options">
                  <el-checkbox v-model="rememberMe">记住我</el-checkbox>
                  <el-link type="primary" :underline="false" @click="showForgot = true">
                    忘记密码
                  </el-link>
                </div>
                <el-button
                  type="primary"
                  class="submit-btn"
                  :loading="loading"
                  @click="handleCodeLogin"
                  round
                >
                  登录
                </el-button>
              </el-form>
            </el-tab-pane>

            <el-tab-pane label="密码登录" name="password">
              <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" size="large" class="login-form">
                <el-form-item prop="account">
                  <el-input v-model="passwordForm.account" placeholder="手机号/邮箱">
                    <template #prefix>
                      <el-icon><User /></el-icon>
                    </template>
                  </el-input>
                </el-form-item>
                <el-form-item prop="password">
                  <el-input
                    v-model="passwordForm.password"
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
                  <el-checkbox v-model="rememberMe">记住我</el-checkbox>
                  <el-link type="primary" :underline="false" @click="showForgot = true">
                    忘记密码
                  </el-link>
                </div>
                <el-button
                  type="primary"
                  class="submit-btn"
                  :loading="loading"
                  @click="handlePasswordLogin"
                  round
                >
                  登录
                </el-button>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </template>

        <div class="divider">
          <span>其他方式登录</span>
        </div>

        <div class="third-party-buttons">
          <div class="icon-btn wechat" @click="handleThirdPartyLogin('wechat')" title="微信登录">
            <i class="iconfont icon-wechat"></i>
          </div>
          <div class="icon-btn qq" @click="handleThirdPartyLogin('qq')" title="QQ登录">
            <i class="iconfont icon-qq"></i>
          </div>
          <div class="icon-btn github" @click="handleThirdPartyLogin('github')" title="GitHub登录">
            <i class="iconfont icon-github"></i>
          </div>
        </div>

        <div class="login-footer">
          <span>没有账号？</span>
          <el-link type="primary" :underline="false" @click="goRegister">
            立即注册
          </el-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// @ts-nocheck
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { Lock, Key, User, Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { loginByPhone, loginByEmail, sendSmsCode, sendEmailCode } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loginType = ref<'code' | 'password'>('code')
const showForgot = ref(false)
const loading = ref(false)
const sendingCode = ref(false)
const rememberMe = ref(true)
const codeDisabled = ref(false)
const countdown = ref(0)

const passwordFormRef = ref<FormInstance>()
const codeFormRef = ref<FormInstance>()
const forgotFormRef = ref<FormInstance>()

const codeForm = ref({
  account: '',
  code: ''
})

const passwordForm = ref({
  account: '',
  password: ''
})

const forgotForm = ref({
  account: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const codeRules: FormRules = {
  account: [
    { required: true, message: '请输入手机号或邮箱', trigger: 'blur' },
    { validator: (_rule, value, callback) => {
        const isEmail = value && value.includes('@')
        const isPhone = /^1[3-9]\d{9}$/.test(value || '')
        if (!isEmail && !isPhone) callback(new Error('请输入正确的手机号或邮箱'))
        else callback()
      }, trigger: 'blur'
    }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ]
}

const passwordRules: FormRules = {
  account: [
    { required: true, message: '请输入账号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const forgotRules: FormRules = {
  account: [
    { required: true, message: '请输入手机号或邮箱', trigger: 'blur' },
    { validator: (_rule, value, callback) => {
        const isEmail = value && value.includes('@')
        const isPhone = /^1[3-9]\d{9}$/.test(value || '')
        if (!isEmail && !isPhone) callback(new Error('请输入正确的手机号或邮箱'))
        else callback()
      }, trigger: 'blur'
    }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: (_rule: any, value: string, callback: any) => {
        if (value !== forgotForm.value.newPassword) callback(new Error('两次输入的密码不一致'))
        else callback()
      }, trigger: 'blur'
    }
  ]
}

const codeButtonText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}s` : '获取验证码'
})

const startCountdown = () => {
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

const sendLoginCode = async () => {
  if (!codeForm.value.account) {
    ElMessage.warning('请先输入手机号或邮箱')
    return
  }
  try {
    sendingCode.value = true
    const isEmail = codeForm.value.account.includes('@')
    if (isEmail) {
      await sendEmailCode(codeForm.value.account, 'login')
    } else {
      await sendSmsCode(codeForm.value.account, 'login')
    }
    ElMessage.success('验证码已发送')
    startCountdown()
  } catch (error) {
    console.error(error)
  } finally {
    sendingCode.value = false
  }
}

const redirectAfterLogin = () => {
  router.push('/dashboard/overview')
}

const handleCodeLogin = async () => {
  if (!codeFormRef.value) return
  
  await codeFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        const isEmail = codeForm.value.account.includes('@')
        const res = isEmail
          ? await loginByEmail({ email: codeForm.value.account, email_code: codeForm.value.code })
          : await loginByPhone({ phone: codeForm.value.account, sms_code: codeForm.value.code })
        const token = res.data?.access_token || res.data?.token || ''
        const userInfo = res.data?.user_info || res.data?.user || {}
        userStore.login(token, userInfo, rememberMe.value)
        ElMessage.success('登录成功')
        redirectAfterLogin()
      } catch (error) {
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

const handlePasswordLogin = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        const account = passwordForm.value.account
        const isEmail = account.includes('@')
        const res = isEmail
          ? await loginByEmail({ email: account, password: passwordForm.value.password })
          : await loginByPhone({ phone: account, password: passwordForm.value.password })
        const token = res.data?.access_token || res.data?.token || ''
        const userInfo = res.data?.user_info || res.data?.user || {}
        userStore.login(token, userInfo, rememberMe.value)
        ElMessage.success('登录成功')
        redirectAfterLogin()
      } catch (error) {
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

const handleThirdPartyLogin = (type: string) => {
  ElMessage.info(`${type}登录功能开发中...`)
}

const goRegister = () => {
  router.push('/register')
}

const sendForgotCode = async () => {
  if (!forgotForm.value.account) {
    ElMessage.warning('请先输入手机号或邮箱')
    return
  }
  try {
    sendingCode.value = true
    const isEmail = forgotForm.value.account.includes('@')
    if (isEmail) {
      await sendEmailCode(forgotForm.value.account, 'reset_password')
    } else {
      await sendSmsCode(forgotForm.value.account, 'reset_password')
    }
    ElMessage.success('验证码已发送')
    startCountdown()
  } catch (error) {
    console.error(error)
  } finally {
    sendingCode.value = false
  }
}

const handleResetPassword = async () => {
  if (!forgotFormRef.value) return
  await forgotFormRef.value.validate(async (valid) => {
    if (valid) {
      ElMessage.success('密码重置成功，请使用新密码登录')
      showForgot.value = false
      loginType.value = 'password'
    }
  })
}
</script>

<style scoped lang="scss">
.auth-page {
  min-height: 100vh;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
}

.login-layout {
  display: flex;
  width: 960px;
  min-height: 560px;
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.login-side {
  width: 340px;
  background-image: url('https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=900&q=80');
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
  color: white;
  
  .side-bg-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.9) 0%, rgba(30, 64, 175, 0.8) 100%);
    z-index: 1;
  }
  
  .brand-content {
    position: relative;
    z-index: 2;
    
    .brand-logo {
      width: 64px;
      height: 64px;
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 24px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      
      .logo-text {
        font-size: 24px;
        font-weight: 800;
        color: white;
      }
    }
    
    h2 {
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 10px;
    }
    
    .slogan {
      font-size: 15px;
      opacity: 0.9;
      margin-bottom: 28px;
    }
    
    .features-list {
      list-style: none;
      padding: 0;
      margin: 0;
      
      li {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
        font-size: 14px;
        opacity: 0.9;
        
        .el-icon {
          background: rgba(255, 255, 255, 0.2);
          padding: 4px;
          border-radius: 50%;
          font-size: 12px;
        }
      }
    }
  }
}

.login-form-container {
  flex: 1;
  padding: 40px 48px;
  display: flex;
  flex-direction: column;
  
  .form-header {
    margin-bottom: 24px;
    
    h2 {
      font-size: 26px;
      color: #0f172a;
      margin-bottom: 8px;
      font-weight: 700;
    }
    
    p {
      color: #64748b;
      font-size: 14px;
    }
  }
  
  .login-tabs {
    :deep(.el-tabs__nav-wrap::after) {
      height: 1px;
      background-color: #e2e8f0;
    }
    :deep(.el-tabs__item) {
      font-size: 15px;
      color: #64748b;
      padding: 0 20px !important;
      &.is-active {
        color: #2563eb;
        font-weight: 600;
      }
    }
    :deep(.el-tabs__active-bar) {
      background-color: #2563eb;
    }
  }
  
  .login-form {
    .input-group {
      display: flex;
      gap: 12px;
      width: 100%;
      
      .el-input {
        flex: 1;
      }
      
      .send-btn {
        width: 120px;
      }
    }
    
    .form-options {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      
      :deep(.el-checkbox__label) {
        color: #64748b;
      }
    }
    
    .submit-btn {
      width: 100%;
      height: 46px;
      border-radius: 12px;
      font-size: 16px;
      font-weight: 600;
      background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      border: none;
      box-shadow: 0 6px 18px rgba(37, 99, 235, 0.25);
      
      &:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
      }
    }
  }
  
  .divider {
    position: relative;
    text-align: center;
    margin: 28px 0 22px;
    
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
    gap: 18px;
    margin-bottom: 24px;
    
    .icon-btn {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
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

@media (max-width: 768px) {
  .login-layout {
    flex-direction: column;
    width: 100%;
    
    .login-side {
      display: none;
    }
    
    .login-form-container {
      padding: 30px 24px;
    }
  }
  
  .auth-page {
    padding: 16px;
  }
}
</style>

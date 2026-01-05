<template>
  <div class="auth-page">
    <div class="return-home" @click="goHome">
      <el-icon><Back /></el-icon>
      <span>返回官网</span>
    </div>
    <div class="register-layout">
      <div class="register-side">
        <div class="brand-content">
          <div class="brand-logo">
            <img :src="logoIcon" alt="Logo" class="logo-img"/>
          </div>
          <h2>DarkVision LPR</h2>
          <p class="slogan">下一代智能车牌识别系统</p>
          <ul class="features-list">
            <li><el-icon><Check /></el-icon> 99.9% 识别准确率</li>
            <li><el-icon><Check /></el-icon> 毫秒级极速响应</li>
            <li><el-icon><Check /></el-icon> 支持极端光照环境</li>
            <li><el-icon><Check /></el-icon> 企业级数据安全</li>
          </ul>
        </div>
        <div class="side-bg-overlay"></div>
      </div>

      <div class="register-form-container">
        <div class="form-header">
          <h2>创建您的账号</h2>
          <p>开启智能识别之旅</p>
        </div>

        <div class="auth-tabs">
          <div 
            class="tab-item" 
            :class="{ active: registerMethod === 'phone' }"
            @click="switchMethod('phone')"
          >
            手机注册
          </div>
          <div 
            class="tab-item" 
            :class="{ active: registerMethod === 'email' }"
            @click="switchMethod('email')"
          >
            邮箱注册
          </div>
        </div>

        <el-form :model="form" :rules="rules" ref="formRef" size="large" class="register-form">
          <el-form-item prop="account">
            <el-input 
              v-model="form.account" 
              :placeholder="registerMethod === 'phone' ? '请输入手机号' : '请输入邮箱地址'"
            >
              <template #prefix>
                <el-icon v-if="registerMethod === 'phone'"><Iphone /></el-icon>
                <el-icon v-else><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="nickname">
            <el-input v-model="form.nickname" placeholder="设置昵称">
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="captcha">
            <div class="input-group">
              <el-input v-model="form.captcha" placeholder="请输入图形验证码" maxlength="4">
                <template #prefix>
                  <el-icon><Picture /></el-icon>
                </template>
              </el-input>
              <div 
                class="captcha-box" 
                @click="refreshCaptcha"
                :class="{ loading: captchaLoading }"
                title="点击刷新验证码"
              >
                <el-icon v-if="captchaLoading" class="is-loading"><Loading /></el-icon>
                <img 
                  v-else-if="captchaImage" 
                  :src="captchaImage" 
                  alt="验证码" 
                  class="captcha-img"
                />
                <span v-else class="captcha-placeholder">获取验证码</span>
              </div>
            </div>
          </el-form-item>

          <el-form-item prop="code">
            <div class="input-group">
              <el-input v-model="form.code" :placeholder="registerMethod === 'phone' ? '短信验证码' : '邮箱验证码'" maxlength="6">
                <template #prefix>
                  <el-icon><Key /></el-icon>
                </template>
              </el-input>
              <el-button 
                type="primary" 
                plain
                class="send-btn" 
                :disabled="codeDisabled || !isCaptchaFilled"
                @click="handleSendCode"
                :loading="sendingCode"
              >
                {{ codeButtonText }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="设置密码（6-20位）"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="确认密码"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="agreement" class="agreement-item">
            <el-checkbox v-model="form.agreement">
              我已阅读并同意 
              <el-link type="primary" :underline="false">服务协议</el-link> 
              和 
              <el-link type="primary" :underline="false">隐私政策</el-link>
            </el-checkbox>
          </el-form-item>

          <el-button
            type="primary"
            class="submit-btn"
            :loading="loading"
            @click="handleRegister"
            round
          >
            立即注册
          </el-button>

          <div class="form-footer">
            <span>已有账号？</span>
            <el-link type="primary" :underline="false" @click="goLogin">
              立即登录
            </el-link>
          </div>

          <div class="divider">
            <span>其他方式注册</span>
          </div>
          
          <div class="third-party-icons">
            <div class="icon-btn" title="微信注册">
              <img :src="wechatIcon" alt="WeChat" />
            </div>
            <div class="icon-btn" title="QQ注册">
              <img :src="qqIcon" alt="QQ" />
            </div>
            <div class="icon-btn" title="Google注册">
              <img :src="googleIcon" alt="Google" />
            </div>
            <div class="icon-btn" title="Github注册">
              <img :src="githubIcon" alt="GitHub" />
            </div>
            <div class="icon-btn" title="微博注册">
              <img :src="weiboIcon" alt="Weibo" />
            </div>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Iphone, User, Message, Lock, Key, Picture, 
  Loading, Check, Back 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getCaptcha, verifyCaptcha } from '@/api/captcha'
import { sendSmsCode, sendEmailCode, register } from '@/api/auth'
import wechatIcon from '@/assets/icons/微信.svg'
import qqIcon from '@/assets/icons/QQ.svg'
import githubIcon from '@/assets/icons/github.svg'
import googleIcon from '@/assets/icons/gogle.svg'
import weiboIcon from '@/assets/icons/微博.svg'
import logoIcon from '@/assets/icons/logo.svg'

const router = useRouter()

const formRef = ref<FormInstance>()
const loading = ref(false)
const registerMethod = ref<'phone' | 'email'>('phone')

const captchaImage = ref('')
const captchaId = ref('')
const captchaLoading = ref(false)

const codeDisabled = ref(false)
const countdown = ref(0)
const sendingCode = ref(false)

const form = reactive({
  account: '',
  nickname: '',
  captcha: '',
  code: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

const isCaptchaFilled = computed(() => form.captcha.length >= 4)

const codeButtonText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}s 后重新获取` : '获取验证码'
})

const validateAccount = (_rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error(registerMethod.value === 'phone' ? '请输入手机号' : '请输入邮箱'))
  } else {
    if (registerMethod.value === 'phone') {
      if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号'))
      } else {
        callback()
      }
    } else {
      if (!/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(value)) {
        callback(new Error('请输入正确的邮箱地址'))
      } else {
        callback()
      }
    }
  }
}

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = computed<FormRules>(() => ({
  account: [
    { validator: validateAccount, trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度为2-20个字符', trigger: 'blur' }
  ],
  captcha: [
    { required: true, message: '请输入图形验证码', trigger: 'blur' },
    { min: 4, message: '请输入4位验证码', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '请输入6位验证码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  agreement: [
    { 
      validator: (_rule, value, callback) => {
        if (!value) callback(new Error('请阅读并同意服务协议'))
        else callback()
      }, 
      trigger: 'change' 
    }
  ]
}))

const switchMethod = (method: 'phone' | 'email') => {
  registerMethod.value = method
  form.account = ''
  formRef.value?.clearValidate()
}

const refreshCaptcha = async () => {
  if (captchaLoading.value) return
  try {
    captchaLoading.value = true
    const res = await getCaptcha(captchaId.value)
    if (res.code === 20000) {
      captchaImage.value = res.data.image_base64
      captchaId.value = res.data.captcha_id
      form.captcha = ''
    }
  } catch (error) {
    console.error(error)
  } finally {
    captchaLoading.value = false
  }
}

const handleSendCode = async () => {
  formRef.value?.validateField('account', async (valid) => {
    if (valid) {
      if (!form.captcha) {
        ElMessage.warning('请先输入图形验证码')
        return
      }

      try {
        sendingCode.value = true
        await verifyCaptcha(captchaId.value, form.captcha)
        
        if (registerMethod.value === 'phone') {
          await sendSmsCode(form.account, 'register')
        } else {
          await sendEmailCode(form.account, 'register')
        }
        
        ElMessage.success('验证码发送成功')
        startCountdown()
        
      } catch (error: any) {
        console.error(error)
        refreshCaptcha()
      } finally {
        sendingCode.value = false
      }
    }
  })
}

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

const handleRegister = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        const payload: any = {
          nickname: form.nickname,
          password: form.password
        }
        
        if (registerMethod.value === 'phone') {
          payload.phone = form.account
          payload.sms_code = form.code
        } else {
          payload.email = form.account
          payload.email_code = form.code
        }

        await register(payload)
        ElMessage.success('注册成功')
        goLogin()
        
      } catch (error) {
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

const goLogin = () => {
  router.push('/login')
}

watch(
  () => true,
  () => {
    // init captcha on mount
    if (!captchaId.value) {
      refreshCaptcha()
    }
  },
  { immediate: true }
)

const goHome = () => {
  window.location.href = 'http://localhost:3000'
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
  position: relative;
}

.return-home {
  position: absolute;
  top: 32px;
  left: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #64748b;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s;
  z-index: 10;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.5);

  &:hover {
    color: #2563eb;
    transform: translateX(-4px);
    background: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
}

.register-layout {
  display: flex;
  width: 1000px;
  min-height: 620px;
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  
  .register-side {
    width: 360px;
    background-image: url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80');
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
      width: 80px;
      height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 24px;
      
      .logo-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }
      
      h2 {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 12px;
        line-height: 1.2;
      }
      
      .slogan {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 40px;
      }
      
      .features-list {
        list-style: none;
        padding: 0;
        margin: 0;
        
        li {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
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
  
  .register-form-container {
    flex: 1;
    padding: 40px 50px;
    display: flex;
    flex-direction: column;
    
    .form-header {
      margin-bottom: 32px;
      
      h2 {
        font-size: 28px;
        color: #0f172a;
        margin-bottom: 8px;
        font-weight: 700;
      }
      
      p {
        color: #64748b;
        font-size: 14px;
      }
    }
    
    .auth-tabs {
      display: flex;
      gap: 32px;
      margin-bottom: 24px;
      border-bottom: 1px solid #e2e8f0;
      
      .tab-item {
        padding-bottom: 12px;
        font-size: 16px;
        color: #64748b;
        cursor: pointer;
        position: relative;
        transition: all 0.3s;
        font-weight: 500;
        
        &.active {
          color: #2563eb;
          font-weight: 600;
          
          &::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 100%;
            height: 2px;
            background: #2563eb;
            border-radius: 2px;
          }
        }
        
        &:hover:not(.active) {
          color: #0f172a;
        }
      }
    }
    
    .register-form {
      .input-group {
        display: flex;
        gap: 12px;
        width: 100%;
        
        .el-input {
          flex: 1;
        }
        
        .captcha-box {
          width: 120px;
          height: 40px;
          border-radius: 4px;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #f8fafc;
          border: 1px solid #e2e8f0;
          overflow: hidden;
          flex-shrink: 0;
          
          .captcha-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
          }
          
          .captcha-placeholder {
            font-size: 12px;
            color: #64748b;
          }
          
          &:hover {
            border-color: #cbd5e1;
          }
        }
        
        .send-btn {
          width: 120px;
        }
      }
      
      .submit-btn {
        width: 100%;
        height: 44px;
        font-size: 16px;
        margin-top: 12px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        
        &:hover {
          transform: translateY(-1px);
          box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        }
      }
    }
    
    .form-footer {
      margin-top: 16px;
      text-align: center;
      font-size: 14px;
      color: #64748b;
    }
    
    .divider {
      margin: 32px 0 24px;
      position: relative;
      text-align: center;
      
      &::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 1px;
        background: #e2e8f0;
      }
      
      span {
        position: relative;
        background: white;
        padding: 0 12px;
        color: #94a3b8;
        font-size: 12px;
      }
    }
    
    .third-party-icons {
      display: flex;
      justify-content: center;
      gap: 24px;
      
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
      padding: 10px;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
      
      &:hover {
        transform: translateY(-2px);
        background: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      }
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
  .register-layout {
    flex-direction: column;
    width: 100%;
    
    .register-side {
      display: none;
    }
    
    .register-form-container {
      padding: 30px 20px;
    }
  }
  
  .auth-page {
    padding: 16px;
  }
}
</style>


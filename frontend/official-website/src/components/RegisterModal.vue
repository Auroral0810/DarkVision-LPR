<template>
  <el-dialog
    v-model="dialogVisible"
    title=""
    width="480px"
    class="register-modal"
    :append-to-body="true"
    destroy-on-close
    center
    align-center
  >
    <div class="register-container">
      <div class="register-header">
        <div class="logo">
          <span class="logo-icon">DV</span>
        </div>
        <h1>{{ $t('register.title') }}</h1>
        <p>创建您的账号，开始体验</p>
      </div>

      <el-form :model="form" :rules="rules" ref="formRef" size="large">
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="手机号（必填）">
            <template #prefix>
              <el-icon><Iphone /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="nickname">
          <el-input v-model="form.nickname" placeholder="昵称">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱（可选）">
            <template #prefix>
              <el-icon><Message /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="code">
          <div class="input-with-btn">
            <el-input v-model="form.code" placeholder="请输入验证码">
              <template #prefix>
                <el-icon><Key /></el-icon>
              </template>
            </el-input>
            <el-button
              type="primary"
              class="append-btn"
              :disabled="codeDisabled"
              @click="sendCode"
            >
              {{ codeButtonText }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item prop="captcha">
          <div class="input-with-btn">
            <el-input v-model="form.captcha" placeholder="请输入图形验证码">
              <template #prefix>
                <el-icon><Picture /></el-icon>
              </template>
            </el-input>
            <div class="captcha-box" @click="refreshCaptcha">
              <span v-if="!captchaImage">点击获取</span>
              <span v-else>1234</span>
            </div>
          </div>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="设置密码"
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
            {{ $t('register.agreement') }}
            <el-link type="primary" :underline="false" @click.stop>{{ $t('register.terms') }}</el-link>
            {{ $t('register.and') }}
            <el-link type="primary" :underline="false" @click.stop>{{ $t('register.privacy') }}</el-link>
          </el-checkbox>
        </el-form-item>

        <el-button
          type="primary"
          class="submit-btn"
          :loading="loading"
          @click="handleRegister"
        >
          {{ $t('register.register') }}
        </el-button>
      </el-form>

      <div class="register-footer">
        <span>{{ $t('register.hasAccount') }}</span>
        <el-link type="primary" :underline="false" @click="switchToLogin">
          {{ $t('register.login') }}
        </el-link>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { Iphone, User, Message, Lock, Key, Picture } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const emit = defineEmits(['switch-to-login'])
const dialogVisible = defineModel<boolean>('visible')

const userStore = useUserStore()

const formRef = ref<FormInstance>()
const loading = ref(false)
const codeDisabled = ref(false)
const countdown = ref(0)
const captchaImage = ref(false)

const form = ref({
  phone: '',
  nickname: '',
  email: '',
  code: '',
  captcha: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== form.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const validateAgreement = (_rule: any, value: boolean, callback: any) => {
  if (!value) {
    callback(new Error('请先阅读并同意服务协议和隐私政策'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度为2-20个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ],
  captcha: [
    { required: true, message: '请输入图形验证码', trigger: 'blur' }
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
    { validator: validateAgreement, trigger: 'change' }
  ]
}

const codeButtonText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}s` : '获取验证码'
})

const sendCode = async () => {
  if (!form.value.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  
  if (!form.value.captcha) {
    ElMessage.warning('请先输入图形验证码')
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

const refreshCaptcha = () => {
  captchaImage.value = true
  form.value.captcha = ''
}

const handleRegister = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      setTimeout(() => {
        userStore.login('mock-token', {
          phone: form.value.phone,
          nickname: form.value.nickname,
          email: form.value.email
        })
        loading.value = false
        ElMessage.success('注册成功')
        dialogVisible.value = false
      }, 1000)
    }
  })
}

const switchToLogin = () => {
  dialogVisible.value = false
  emit('switch-to-login')
}
</script>

<style scoped lang="scss">
.register-container {
  width: 100%;
  padding: 0 20px;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
  
  .logo {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    
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

.input-with-btn {
  display: flex;
  gap: 12px;
  width: 100%;
  
  .el-input {
    flex: 1;
  }
  
  .append-btn {
    padding: 0 4px;
    min-width: 90px;
    height: 46px;
    border-radius: 12px;
  }
  
  .captcha-box {
    min-width: 100px;
    height: 46px;
    background: #f1f5f9;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: #2563eb;
    font-size: 14px;
    border: 1px solid #e2e8f0;
    
    &:hover {
      background: #e2e8f0;
    }
  }
}

.agreement-item {
  margin-bottom: 32px;
  
  :deep(.el-checkbox__label) {
    color: #64748b;
    font-size: 13px;
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

.register-footer {
  text-align: center;
  margin-top: 24px;
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

:deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  
  .el-dialog__header {
    margin: 0;
    padding: 0;
  }
  
  .el-dialog__body {
    padding: 30px;
  }
}
</style>

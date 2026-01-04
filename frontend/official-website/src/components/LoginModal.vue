<template>
  <el-dialog
    v-model="dialogVisible"
    title=""
    width="420px"
    class="login-modal"
    :append-to-body="true"
    destroy-on-close
    center
    align-center
  >
    <div class="login-container">
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">DV</span>
        </div>
        <h1>{{ $t('login.title') }}</h1>
        <p>欢迎回来，请登录您的账号</p>
      </div>

      <el-tabs v-model="loginType" class="login-tabs" stretch>
        <el-tab-pane label="验证码登录" name="code">
          <el-form :model="phoneForm" :rules="phoneRules" ref="phoneFormRef" size="large">
            <el-form-item prop="phone">
              <el-input v-model="phoneForm.phone" placeholder="请输入手机号">
                <template #prefix>
                  <el-icon><Iphone /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="code">
              <div class="input-with-btn">
                <el-input v-model="phoneForm.code" placeholder="请输入验证码">
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

        <el-tab-pane label="密码登录" name="password">
          <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" size="large">
            <el-form-item prop="account">
              <el-input v-model="passwordForm.account" placeholder="手机号/邮箱/账号">
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
              <el-checkbox v-model="rememberMe">{{ $t('login.remember') }}</el-checkbox>
              <el-link type="primary" :underline="false" @click="$router.push('/forgot-password')">
                {{ $t('login.forgot') }}
              </el-link>
            </div>
            <el-button
              type="primary"
              class="submit-btn"
              :loading="loading"
              @click="handlePasswordLogin"
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
          <svg viewBox="0 0 28 28" width="20" height="20"><path d="M21.35 15.65c0-3.32-3.1-6-6.92-6-3.83 0-6.93 2.68-6.93 6 0 3.32 3.1 6 6.93 6 .82 0 1.6-.14 2.33-.38.71.53 2.5 1.76 2.5 1.76s-.5-1.46-.57-1.95c1.67-1.39 2.66-3.23 2.66-5.43zM10.84 8.78c-4.42 0-8 2.87-8 6.4 0 2.22 1.41 4.18 3.55 5.37-.09.68-.66 2.08-.66 2.08s2.07-.36 3.65-1.35c.46.08.93.13 1.43.13.06 0 .12 0 .18 0-.3-1.02-.45-2.09-.45-3.17 0-4.66 4.31-8.45 9.63-8.45.68 0 1.34.07 1.99.18-1.52-2.78-5.91-4.7-10.45-4.7V8.78c-.28-.01-.58-.02-.87 0z" fill="currentColor"/></svg>
        </div>
        <div class="icon-btn qq" @click="handleThirdPartyLogin('qq')">
          <svg viewBox="0 0 24 24" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.33 14.17c-.31.25-.66.44-1.03.55-.42.12-.86.19-1.3.19s-.87-.07-1.3-.19c-.37-.11-.72-.3-1.03-.55-.26-.21-.48-.46-.66-.74-.18-.28-.31-.59-.39-.91-.08-.32-.12-.65-.12-.99 0-.34.04-.67.12-.99.08-.32.21-.63.39-.91.18-.28.4-.53.66-.74.31-.25.66-.44 1.03-.55.42-.12.86-.19 1.3-.19s.87.07 1.3.19c.37.11.72.3 1.03.55.26.21.48.46.66.74.18.28.31.59.39.91.08.32.12.65.12.99 0 .34-.04.67-.12.99-.08.32-.21.63-.39.91-.18.28-.4.53-.66.74z" fill="currentColor"/></svg>
        </div>
        <div class="icon-btn github" @click="handleThirdPartyLogin('github')">
          <svg viewBox="0 0 24 24" width="20" height="20"><path d="M12 2C6.477 2 2 6.477 2 12c0 4.418 2.865 8.167 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.379.202 2.398.1 2.651.64.7 1.028 1.597 1.028 2.688 0 3.848-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.161 22 16.416 22 12c0-5.523-4.477-10-10-10z" fill="currentColor"/></svg>
        </div>
      </div>

      <div class="login-footer">
        <span>{{ $t('login.noAccount') }}</span>
        <el-link type="primary" :underline="false" @click="switchToRegister">
          {{ $t('login.register') }}
        </el-link>
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/store/user'
import { Iphone, Lock, Key, User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

const props = defineProps<{
  // modelValue is handled by defineModel in Vue 3.4+, but for safety in older setups we use standard props/emits or computed
}>()

const emit = defineEmits(['switch-to-register'])

// Using defineModel for two-way binding of visibility
const dialogVisible = defineModel<boolean>('visible')

const userStore = useUserStore()

const loginType = ref('phone')
const loading = ref(false)
const rememberMe = ref(false)
const codeDisabled = ref(false)
const countdown = ref(0)

const passwordFormRef = ref<FormInstance>()
const phoneFormRef = ref<FormInstance>()

const phoneForm = ref({
  phone: '',
  code: ''
})

const passwordForm = ref({
  account: '',
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

const passwordRules: FormRules = {
  account: [
    { required: true, message: '请输入账号', trigger: 'blur' }
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
        dialogVisible.value = false
      }, 1000)
    }
  })
}

const handlePasswordLogin = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      setTimeout(() => {
        userStore.login('mock-token', {
          nickname: '用户'
        })
        loading.value = false
        ElMessage.success('登录成功')
        dialogVisible.value = false
      }, 1000)
    }
  })
}

const handleThirdPartyLogin = (type: string) => {
  ElMessage.info(`${type}登录功能开发中...`)
}

const switchToRegister = () => {
  dialogVisible.value = false
  emit('switch-to-register')
}
</script>

<style scoped lang="scss">
.login-container {
  width: 100%;
  padding: 0 20px;
}

.login-header {
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

.login-tabs {
  margin-bottom: 24px;
  
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
  
  :deep(.el-tabs__nav) {
    width: 100%;
    display: flex;
    justify-content: center;
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
    padding: 0 4px; /* Reduced padding since text is short */
    min-width: 90px; /* Ensure minimum width */
    height: 46px; /* Match input height */
    border-radius: 12px;
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

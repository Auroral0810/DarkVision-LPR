<template>
  <header class="header" :class="{ 'is-scrolled': isScrolled }">
    <div class="header-container">
      <div class="logo" @click="$router.push('/')">
        <div class="logo-icon">DV</div>
        <div class="logo-text">
          <span class="brand">DarkVision</span>
          <span class="tag">LPR</span>
        </div>
      </div>
      
      <nav class="nav-menu">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="nav-item"
          active-class="active"
        >
          {{ $t(`nav.${item.key}`) }}
        </router-link>
      </nav>
      
      <div class="header-actions">
        <el-dropdown @command="handleLanguageChange" trigger="hover" popper-class="lang-dropdown">
          <span class="language-switcher">
            <span class="lang-icon" style="font-size: 16px; margin-right: 4px; opacity: 0.6;">🌐</span>
            {{ currentLanguageLabel }}
            <el-icon class="arrow-icon"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item 
                v-for="lang in languages" 
                :key="lang.value"
                :command="lang.value"
                :class="{ 'is-active': currentLocale.value === lang.value }"
              >
                {{ lang.label }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <div class="divider"></div>

        <template v-if="!isLoggedIn">
          <router-link to="/login" class="login-link">
            {{ $t('nav.login') }}
          </router-link>
          <button class="register-btn" @click="$router.push('/register')">
            {{ $t('nav.register') }}
          </button>
        </template>
        <template v-else>
          <el-dropdown @command="handleUserAction" trigger="click">
            <div class="user-profile">
              <el-avatar :size="32" class="user-avatar" :src="userInfo?.avatar">
                {{ userInfo?.nickname?.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userInfo?.nickname }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item divided command="logout" style="color: #ef4444;">{{ $t('common.logout') }}</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import { ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const { t, locale: currentLocale } = useI18n()
const userStore = useUserStore()
const appStore = useAppStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const userInfo = computed(() => userStore.userInfo)
const isScrolled = ref(false)

const navItems = [
  { path: '/', key: 'home' },
  { path: '/capabilities', key: 'capabilities' },
  { path: '/features', key: 'features' },
  { path: '/pricing', key: 'pricing' },
  { path: '/documentation', key: 'documentation' },
  { path: '/download', key: 'download' },
  { path: '/contact', key: 'contact' }
]

const languages = [
  { value: 'zh-CN', label: '简体中文' },
  { value: 'en-US', label: 'English' },
  { value: 'zh-TW', label: '繁體中文' },
  { value: 'ja-JP', label: '日本語' },
  { value: 'fr-FR', label: 'Français' },
  { value: 'ru-RU', label: 'Русский' }
]

const currentLanguageLabel = computed(() => {
  const lang = languages.find(l => l.value === currentLocale.value)
  return lang?.label || '中文'
})

const handleLanguageChange = (lang: string) => {
  currentLocale.value = lang
  appStore.setLocale(lang)
  ElMessage.success(t('common.success'))
}

const handleUserAction = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    router.push('/')
    ElMessage.success(t('common.success'))
  } else if (command === 'profile') {
    router.push('/user/profile')
  }
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped lang="scss">
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 72px;

  &.is-scrolled {
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  }

  .header-container {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 32px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;

  .logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    border-radius: 8px;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 14px;
    letter-spacing: -0.5px;
  }

  .logo-text {
    display: flex;
    flex-direction: column;
    line-height: 1;

    .brand {
      font-size: 18px;
      font-weight: 700;
      color: #0f172a;
      letter-spacing: -0.02em;
    }

    .tag {
      font-size: 11px;
      color: #64748b;
      font-weight: 500;
      letter-spacing: 0.1em;
    }
  }
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 32px;

  .nav-item {
    color: #475569;
    font-size: 14px;
    font-weight: 500;
    padding: 8px 0;
    position: relative;
    transition: color 0.2s;

    &:hover {
      color: #0f172a;
    }

    &.active {
      color: #2563eb;
      font-weight: 600;

      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: #2563eb;
        border-radius: 2px;
      }
    }
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;

  .language-switcher {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #64748b;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 6px;
    transition: background 0.2s;

    &:hover {
      background: rgba(0, 0, 0, 0.04);
      color: #0f172a;
    }

    .arrow-icon {
      font-size: 12px;
      opacity: 0.5;
    }
  }

  .divider {
    width: 1px;
    height: 24px;
    background: #e2e8f0;
  }

  .login-link {
    font-size: 14px;
    font-weight: 600;
    color: #475569;
    transition: color 0.2s;

    &:hover {
      color: #2563eb;
    }
  }

  .register-btn {
    background: #0f172a;
    color: white;
    padding: 8px 20px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    transition: all 0.2s;

    &:hover {
      background: #334155;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }

    &:active {
      transform: translateY(0);
    }
  }

  .user-profile {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    padding: 4px;
    border-radius: 50px;
    transition: background 0.2s;

    &:hover {
      background: rgba(0, 0, 0, 0.04);
    }

    .user-avatar {
      background: #2563eb;
      color: white;
      font-weight: 600;
      font-size: 14px;
    }

    .username {
      font-size: 14px;
      font-weight: 500;
      color: #334155;
      max-width: 100px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin-right: 8px;
    }
  }
}

@media (max-width: 1024px) {
  .nav-menu {
    display: none;
  }
}
</style>
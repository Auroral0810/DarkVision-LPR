import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const locale = ref<string>(localStorage.getItem('locale') || 'zh-CN')
  const theme = ref<string>(localStorage.getItem('theme') || 'light')

  // 切换语言
  const setLocale = (newLocale: string) => {
    locale.value = newLocale
    localStorage.setItem('locale', newLocale)
  }

  // 切换主题
  const setTheme = (newTheme: string) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
  }

  // 弹窗状态
  const loginModalVisible = ref(false)
  const registerModalVisible = ref(false)

  const showLoginModal = () => {
    loginModalVisible.value = true
    registerModalVisible.value = false
  }

  const showRegisterModal = () => {
    registerModalVisible.value = true
    loginModalVisible.value = false
  }

  const hideLoginModal = () => {
    loginModalVisible.value = false
  }

  const hideRegisterModal = () => {
    registerModalVisible.value = false
  }

  return {
    locale,
    theme,
    setLocale,
    setTheme,
    loginModalVisible,
    registerModalVisible,
    showLoginModal,
    showRegisterModal,
    hideLoginModal,
    hideRegisterModal
  }
})
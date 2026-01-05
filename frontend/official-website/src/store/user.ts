import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(
    sessionStorage.getItem('token') || localStorage.getItem('token') || ''
  )
  const userInfo = ref<any>(null)
  const isLoggedIn = ref<boolean>(!!token.value)

  // 登录
  const login = (newToken: string, user: any, rememberMe = true) => {
    token.value = newToken
    userInfo.value = user
    isLoggedIn.value = true
    // 记住我：存 localStorage；否则存 sessionStorage
    if (rememberMe) {
      localStorage.setItem('token', newToken)
      localStorage.setItem('userInfo', JSON.stringify(user))
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('userInfo')
    } else {
      sessionStorage.setItem('token', newToken)
      sessionStorage.setItem('userInfo', JSON.stringify(user))
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    userInfo.value = null
    isLoggedIn.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  // 初始化用户信息
  const initUserInfo = () => {
    // 优先 sessionStorage，其次 localStorage
    const savedToken = sessionStorage.getItem('token') || localStorage.getItem('token')
    const savedUserInfo =
      sessionStorage.getItem('userInfo') || localStorage.getItem('userInfo')
    if (savedToken) {
      token.value = savedToken
      isLoggedIn.value = true
    }
    if (savedUserInfo) {
      userInfo.value = JSON.parse(savedUserInfo)
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    logout,
    initUserInfo
  }
})
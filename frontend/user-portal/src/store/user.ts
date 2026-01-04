import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserRole = 'FREE' | 'VIP' | 'COMPANY'

export interface UserInfo {
  id: string
  avatar: string
  nickname: string
  email: string
  role: UserRole
  balance: number
}

// Mock initial state
const defaultUser: UserInfo = {
  id: '1',
  avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
  nickname: 'Guest User',
  email: 'guest@darkvision.com',
  role: 'FREE',
  balance: 0
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo>({ ...defaultUser })
  
  const isLoggedIn = computed(() => !!token.value)
  const isVIP = computed(() => userInfo.value.role === 'VIP' || userInfo.value.role === 'COMPANY')
  const isCompany = computed(() => userInfo.value.role === 'COMPANY')

  // Quotas based on role
  const quota = computed(() => {
    switch (userInfo.value.role) {
      case 'FREE':
        return { daily: 20, maxBatch: 1, video: 0 }
      case 'VIP':
        return { daily: 500, maxBatch: 50, video: 10 }
      case 'COMPANY':
        return { daily: Infinity, maxBatch: 1000, video: Infinity }
      default:
        return { daily: 0, maxBatch: 0, video: 0 }
    }
  })

  function login(role: UserRole = 'FREE') {
    token.value = 'mock-token-' + role.toLowerCase()
    localStorage.setItem('token', token.value)
    
    // Simulate fetching user info
    userInfo.value = {
      ...defaultUser,
      role,
      nickname: `${role} User`
    }
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
    userInfo.value = { ...defaultUser }
  }

  // Debug function to switch roles
  function switchRole(role: UserRole) {
    userInfo.value.role = role
    userInfo.value.nickname = `${role} User`
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isVIP,
    isCompany,
    quota,
    login,
    logout,
    switchRole
  }
})

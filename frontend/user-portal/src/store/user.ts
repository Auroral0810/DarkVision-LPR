import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserRole = 'FREE' | 'VIP' | 'COMPANY'
export type UserType = 'free' | 'vip' | 'enterprise' | 'admin'
export type MembershipType = 'free' | 'vip_monthly' | 'vip_yearly' | 'enterprise_custom'
export type Gender = 'male' | 'female' | 'unknown'
export type VerificationStatus = 'pending' | 'approved' | 'rejected'

export interface UserInfo {
  id: string
  phone: string
  nickname: string
  email: string | null
  avatar_url: string | null
  user_type: UserType
  role: UserRole
  status: 'active' | 'inactive' | 'banned'
  created_at: string
  last_login_at: string | null
}

export interface UserProfile {
  real_name: string | null
  id_card_number: string | null
  gender: Gender | null
  birthday: string | null
  address: string | null
}

export interface Membership {
  membership_type: MembershipType
  start_date: string
  expire_date: string | null
  is_active: boolean
}

export interface Verification {
  id_card_front: string | null
  id_card_back: string | null
  face_photo: string | null
  status: VerificationStatus
  reject_reason: string | null
}

export interface ThirdPartyLogin {
  provider: 'wechat' | 'qq' | 'github'
  open_id: string
  union_id: string | null
  bound: boolean
}

// Mock initial state
const defaultUser: UserInfo = {
  id: '1',
  phone: '13800138000',
  nickname: 'Guest User',
  email: 'guest@darkvision.com',
  avatar_url: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
  user_type: 'free',
  role: 'FREE',
  status: 'active',
  created_at: '2026-01-01 00:00:00',
  last_login_at: null
}

const defaultProfile: UserProfile = {
  real_name: null,
  id_card_number: null,
  gender: null,
  birthday: null,
  address: null
}

const defaultMembership: Membership = {
  membership_type: 'free',
  start_date: '2026-01-01 00:00:00',
  expire_date: null,
  is_active: true
}

const defaultVerification: Verification = {
  id_card_front: null,
  id_card_back: null,
  face_photo: null,
  status: 'pending',
  reject_reason: null
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo>({ ...defaultUser })
  const userProfile = ref<UserProfile>({ ...defaultProfile })
  const membership = ref<Membership>({ ...defaultMembership })
  const verification = ref<Verification>({ ...defaultVerification })
  const thirdPartyLogins = ref<ThirdPartyLogin[]>([
    { provider: 'wechat', open_id: '', union_id: null, bound: false },
    { provider: 'qq', open_id: '', union_id: null, bound: false },
    { provider: 'github', open_id: '', union_id: null, bound: false }
  ])
  
  const isLoggedIn = computed(() => !!token.value)
  const isVIP = computed(() => userInfo.value.role === 'VIP' || userInfo.value.role === 'COMPANY')
  const isCompany = computed(() => userInfo.value.role === 'COMPANY')
  const isVerified = computed(() => verification.value.status === 'approved')

  // Quotas based on role
  const quota = computed(() => {
    switch (userInfo.value.role) {
      case 'FREE':
        return { daily: 20, maxBatch: 1, video: 0, api: 0, storage: 0 }
      case 'VIP':
        return { daily: 500, maxBatch: 50, video: 10, api: 5000, storage: 10 }
      case 'COMPANY':
        return { daily: Infinity, maxBatch: 1000, video: Infinity, api: Infinity, storage: Infinity }
      default:
        return { daily: 0, maxBatch: 0, video: 0, api: 0, storage: 0 }
    }
  })

  // Membership info
  const membershipInfo = computed(() => {
    if (userInfo.value.role === 'FREE') {
      return {
        name: '免费版',
        features: ['单张图片识别', '每日20次识别', '7天历史记录', '基础客服支持']
      }
    } else if (userInfo.value.role === 'VIP') {
      return {
        name: membership.value.membership_type === 'vip_monthly' ? 'VIP 月付版' : 'VIP 年付版',
        features: [
          '单张图片识别',
          '批量识别（50张/次）',
          '视频识别（10个/月）',
          '每日500次识别',
          '无限历史记录',
          '数据分析报表',
          'API调用（5000次/日）',
          '10GB云端存储',
          '优先客服支持'
        ],
        expireDate: membership.value.expire_date
      }
    } else {
      return {
        name: '企业版',
        features: [
          '无限识别次数',
          '批量识别（1000张/次）',
          '无限视频识别',
          '多账户管理（50个）',
          '定制化模型',
          '无限API调用',
          '无限云端存储',
          '7×24专属客服',
          'SLA保障',
          '私有化部署（可选）'
        ]
      }
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
    
    if (role === 'VIP') {
      membership.value = {
        membership_type: 'vip_monthly',
        start_date: '2026-01-01 00:00:00',
        expire_date: '2026-02-01 00:00:00',
        is_active: true
      }
      verification.value.status = 'approved'
    } else if (role === 'COMPANY') {
      membership.value = {
        membership_type: 'enterprise_custom',
        start_date: '2026-01-01 00:00:00',
        expire_date: null,
        is_active: true
      }
      verification.value.status = 'approved'
    }
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
    userInfo.value = { ...defaultUser }
    userProfile.value = { ...defaultProfile }
    membership.value = { ...defaultMembership }
    verification.value = { ...defaultVerification }
  }

  // Debug function to switch roles
  function switchRole(role: UserRole) {
    userInfo.value.role = role
    userInfo.value.nickname = `${role} User`
    
    if (role === 'VIP') {
      userInfo.value.user_type = 'vip'
      membership.value = {
        membership_type: 'vip_monthly',
        start_date: '2026-01-01 00:00:00',
        expire_date: '2026-02-01 00:00:00',
        is_active: true
      }
      verification.value.status = 'approved'
    } else if (role === 'COMPANY') {
      userInfo.value.user_type = 'enterprise'
      membership.value = {
        membership_type: 'enterprise_custom',
        start_date: '2026-01-01 00:00:00',
        expire_date: null,
        is_active: true
      }
      verification.value.status = 'approved'
    } else {
      userInfo.value.user_type = 'free'
      membership.value = {
        membership_type: 'free',
        start_date: '2026-01-01 00:00:00',
        expire_date: null,
        is_active: true
      }
      verification.value.status = 'pending'
    }
  }

  return {
    token,
    userInfo,
    userProfile,
    membership,
    verification,
    thirdPartyLogins,
    isLoggedIn,
    isVIP,
    isCompany,
    isVerified,
    quota,
    membershipInfo,
    login,
    logout,
    switchRole
  }
})
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
// @ts-ignore
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
// @ts-ignore
import enLocale from 'element-plus/dist/locale/en.mjs'

export type UserRole = 'FREE' | 'VIP' | 'COMPANY'
export type UserType = 'free' | 'vip' | 'enterprise' | 'admin'
export type MembershipType = 'free' | 'vip_monthly' | 'vip_yearly' | 'enterprise_custom'
export type Gender = 'male' | 'female' | 'unknown'
export type VerificationStatus = 'unverified' | 'pending' | 'approved' | 'rejected'

export interface UserInfo {
  id: string | number
  phone: string | null
  nickname: string
  email: string | null
  avatar_url: string | null
  user_type: UserType
  role: UserRole
  status: 'active' | 'inactive' | 'banned'
  created_at: string
  last_login_at: string | null
  daily_quota: number
  used_quota_today: number
  remaining_quota_today: number
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
  real_name: string | null
  id_card_number: string | null
  id_card_front: string | null
  id_card_back: string | null
  face_photo: string | null
  status: VerificationStatus
  reject_reason: string | null
}

export interface RecentRecognitionRecord {
  id: number
  date: string
  plate: string
  type: string
  confidence: number
  image_url?: string
}

export interface RecognitionStats {
  success_rate_today: number
  success_rate_yesterday: number
  rate_change: number
}

export interface ThirdPartyLogin {
  provider: 'wechat' | 'qq' | 'github'
  open_id: string
  union_id: string | null
  bound: boolean
}

// Mock / fallback initial state
const defaultUser: UserInfo = {
  id: '1',
  phone: null,
  nickname: 'Guest User',
  email: 'guest@darkvision.com',
  avatar_url: null,
  user_type: 'free',
  role: 'FREE',
  status: 'active',
  created_at: '2026-01-01 00:00:00',
  last_login_at: null,
  daily_quota: 10,
  used_quota_today: 0,
  remaining_quota_today: 10
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
  real_name: null,
  id_card_number: null,
  id_card_front: null,
  id_card_back: null,
  face_photo: null,
  status: 'unverified',
  reject_reason: null
}

export const useUserStore = defineStore('user', () => {
  // 读取官网存储的 token / userInfo，官网与门户使用相同 key：token、userInfo
  const token = ref<string | null>(
    sessionStorage.getItem('token') || localStorage.getItem('token')
  )
  const userInfo = ref<UserInfo>({ ...defaultUser })
  const userProfile = ref<UserProfile>({ ...defaultProfile })
  const membership = ref<Membership>({ ...defaultMembership })
  const verification = ref<Verification>({ ...defaultVerification })
  const recentRecords = ref<RecentRecognitionRecord[]>([])
  const recognitionStats = ref<RecognitionStats | null>(null)
  const thirdPartyLogins = ref<ThirdPartyLogin[]>([
    { provider: 'wechat', open_id: '', union_id: null, bound: false },
    { provider: 'qq', open_id: '', union_id: null, bound: false },
    { provider: 'github', open_id: '', union_id: null, bound: false }
  ])
  
  const lang = ref(localStorage.getItem('lang') || 'zh-cn')
  const locale = computed(() => lang.value === 'zh-cn' ? zhCn : enLocale)

  function setLang(val: string) {
    lang.value = val
    localStorage.setItem('lang', val)
  }
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

  /**
   * 登录写入（从官网或本地登录流程）
   * @param rememberMe true 写入 localStorage；false 写入 sessionStorage
   */
  function login(newToken: string, payloadUser: any, rememberMe = true) {
    const storage = rememberMe ? localStorage : sessionStorage
    const otherStorage = rememberMe ? sessionStorage : localStorage

    token.value = newToken
    storage.setItem('token', newToken)
    otherStorage.removeItem('token')

    // 将 user_type 转换为 role
    const userType = payloadUser?.user_type || 'free'
    let normalizedRole: UserRole = 'FREE'
    if (userType === 'vip') {
      normalizedRole = 'VIP'
    } else if (userType === 'enterprise') {
      normalizedRole = 'COMPANY'
    } else {
      normalizedRole = 'FREE'
    }

    userInfo.value = {
      ...defaultUser,
      id: payloadUser?.id ?? defaultUser.id,
      phone: payloadUser?.phone ?? null,
      nickname: payloadUser?.nickname ?? defaultUser.nickname,
      email: payloadUser?.email ?? null,
      avatar_url: payloadUser?.avatar_url ?? null,
      user_type: userType as UserType,
      role: normalizedRole,
      status: (payloadUser?.status || 'active') as 'active' | 'inactive' | 'banned',
      created_at: payloadUser?.created_at || defaultUser.created_at,
      last_login_at: payloadUser?.last_login_at ?? null,
      daily_quota: payloadUser?.daily_quota ?? 10,
      used_quota_today: payloadUser?.used_quota_today ?? 0,
      remaining_quota_today: payloadUser?.remaining_quota_today ?? 10,
    }
    
    // 更新profile信息（如果有）
    if (payloadUser?.gender || payloadUser?.birthday || payloadUser?.address) {
      userProfile.value = {
        ...defaultProfile,
        gender: payloadUser?.gender ?? null,
        birthday: payloadUser?.birthday ?? null,
        address: payloadUser?.address ?? null,
        real_name: payloadUser?.real_name ?? null,
        id_card_number: null,
      }
    }

    storage.setItem('userInfo', JSON.stringify(userInfo.value))
    otherStorage.removeItem('userInfo')
  }
  
  /**
   * 更新用户信息（在获取到详细信息后调用）
   */
  async function updateUserInfo(fullUserInfo?: any) {
    // 如果没有传入数据，则从API获取
    if (!fullUserInfo) {
      try {
        const { getCurrentUserInfo } = await import('@/api/auth')
        const res = await getCurrentUserInfo()
        if (res.code === 20000 && res.data) {
          fullUserInfo = res.data
        } else {
          console.error('Failed to fetch user info:', res.message)
          return
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error)
        return
      }
    }
    
    if (!fullUserInfo) return
    
    const userType = fullUserInfo?.user_type || 'free'
    let normalizedRole: UserRole = 'FREE'
    if (userType === 'vip') {
      normalizedRole = 'VIP'
    } else if (userType === 'enterprise') {
      normalizedRole = 'COMPANY'
    } else {
      normalizedRole = 'FREE'
    }

    userInfo.value = {
      ...userInfo.value,
      ...fullUserInfo,
      role: normalizedRole,
      daily_quota: fullUserInfo?.daily_quota ?? userInfo.value.daily_quota,
      used_quota_today: fullUserInfo?.used_quota_today ?? userInfo.value.used_quota_today,
      remaining_quota_today: fullUserInfo?.remaining_quota_today ?? userInfo.value.remaining_quota_today,
    }
    
    // 更新profile信息
    if (fullUserInfo?.gender || fullUserInfo?.birthday || fullUserInfo?.address) {
      userProfile.value = {
        ...userProfile.value,
        gender: fullUserInfo?.gender ?? null,
        birthday: fullUserInfo?.birthday ?? null,
        address: fullUserInfo?.address ?? null,
        real_name: fullUserInfo?.real_name ?? null,
      }
    }
    
    // 更新membership信息
    if (fullUserInfo?.membership_type) {
      membership.value = {
        membership_type: fullUserInfo.membership_type as MembershipType,
        start_date: fullUserInfo.created_at || '2026-01-01 00:00:00',
        expire_date: fullUserInfo.membership_expire_date ?? null,
        is_active: fullUserInfo.is_membership_active ?? false,
      }
    }
    
    // 更新verification状态
    if (fullUserInfo?.is_verified !== undefined) {
      if (fullUserInfo.is_verified) {
        verification.value.status = 'approved'
      } else if (fullUserInfo.verification_status === 'pending') {
        verification.value.status = 'pending'
      } else if (fullUserInfo.verification_status === 'rejected') {
        verification.value.status = 'rejected'
      } else {
        verification.value.status = 'unverified'
      }
    }
    
    if (fullUserInfo?.real_name) {
      verification.value.real_name = fullUserInfo.real_name
    }
    if (fullUserInfo?.id_card_number) {
      verification.value.id_card_number = fullUserInfo.id_card_number
    }
    if (fullUserInfo?.id_card_front) {
      verification.value.id_card_front = fullUserInfo.id_card_front
    }
    if (fullUserInfo?.id_card_back) {
      verification.value.id_card_back = fullUserInfo.id_card_back
    }
    if (fullUserInfo?.face_photo) {
      verification.value.face_photo = fullUserInfo.face_photo
    }
    if (fullUserInfo?.reject_reason) {
      verification.value.reject_reason = fullUserInfo.reject_reason
    }
    
    // 更新识别记录
    if (fullUserInfo?.recent_records) {
      recentRecords.value = fullUserInfo.recent_records
    }
    
    // 更新识别统计
    if (fullUserInfo?.recognition_stats) {
      recognitionStats.value = fullUserInfo.recognition_stats
    }
    
    // 保存到storage
    const storage = localStorage.getItem('token') ? localStorage : sessionStorage
    storage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  async function logout() {
    try {
      const { logout: apiLogout } = await import('@/api/auth')
      await apiLogout()
    } catch (e) {
      console.error('Logout API failed:', e)
    }
    
    token.value = null
    localStorage.removeItem('token')
    sessionStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    sessionStorage.removeItem('userInfo')
    userInfo.value = { ...defaultUser }
    userProfile.value = { ...defaultProfile }
    membership.value = { ...defaultMembership }
    verification.value = { ...defaultVerification }
    recentRecords.value = []
    recognitionStats.value = null
  }

  function withdrawVerification() {
    verification.value.status = 'unverified'
    // Actually we should call an API here to notify the backend
    console.log('Verification withdrawn locally')
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

  // 初始化：若官网已登录则自动同步 token/userInfo
  ;(() => {
    const savedToken = sessionStorage.getItem('token') || localStorage.getItem('token')
    const savedUserInfo = sessionStorage.getItem('userInfo') || localStorage.getItem('userInfo')
    if (savedToken) token.value = savedToken
    if (savedUserInfo) {
      try {
        const parsed = JSON.parse(savedUserInfo)
        const normalizedRole = (parsed?.user_type || parsed?.role || 'free').toUpperCase()
        userInfo.value = {
          ...defaultUser,
          ...parsed,
          role: normalizedRole,
          user_type: parsed?.user_type || 'free',
        }
      } catch (e) {
        console.error('Failed to parse saved userInfo', e)
      }
    }
  })()

  return {
    token,
    userInfo,
    userProfile,
    membership,
    verification,
    recentRecords,
    recognitionStats,
    thirdPartyLogins,
    isLoggedIn,
    isVIP,
    isCompany,
    isVerified,
    quota,
    membershipInfo,
    login,
    updateUserInfo,
    logout,
    withdrawVerification,
    switchRole,
    lang,
    locale,
    setLang
  }
})
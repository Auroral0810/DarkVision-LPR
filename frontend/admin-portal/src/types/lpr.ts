/**
 * DarkVision-LPR TypeScript Type Definitions
 */

// ==================== User Types ====================

export type UserType = 'free' | 'vip' | 'enterprise' | 'admin'
export type UserStatus = 'active' | 'inactive' | 'banned'

export interface User {
  id: number
  phone: string | null
  nickname: string
  email: string | null
  avatar_url: string | null
  user_type: UserType
  status: UserStatus
  is_online?: boolean
  banned_reason: string | null
  banned_until: string | null
  last_login_at: string | null
  last_login_ip: string | null
  created_at: string
  updated_at: string
  // 额外增强字段
  is_admin?: boolean
  roles?: any[]
  parent_id?: number | null
  parent_nickname?: string | null
  sub_account_role?: string | null
  login_count?: number
  registration_ip?: string | null
  total_recognition_count?: number
  total_order_amount?: number
  order_count?: number
  last_recognition_at?: string | null
  is_verified?: boolean
  verification_status?: string | null
  id_card_front?: string | null
  id_card_back?: string | null
  face_photo?: string | null
  gender?: string | null
  birthday?: string | null
  address?: string | null
  real_name?: string | null
  is_deleted?: boolean
  reject_reason?: string | null
  is_enterprise_main?: boolean
  sub_account_count?: number
  // 会员相关
  membership_type?: string
  membership_expire_date?: string | null
  is_membership_active?: boolean
  // 配额
  daily_quota?: number
  used_quota_today?: number
  remaining_quota_today?: number
  // 详情数据
  recent_records?: any[]
  recognition_stats?: any | null
}

export interface UserProfile {
  user_id: number
  real_name: string | null
  id_card_number: string | null
  gender: 'male' | 'female' | 'unknown' | null
  birthday: string | null
  address: string | null
}

export interface UserMembership {
  id: number
  user_id: number
  membership_type: 'free' | 'vip_monthly' | 'vip_yearly' | 'enterprise_custom'
  start_date: string
  expire_date: string | null
  is_active: boolean
}

// ==================== Verification Types ====================

export type VerificationStatus = 'pending' | 'approved' | 'rejected'

export interface RealNameVerification {
  id: number
  user_id: number
  id_card_front: string
  id_card_back: string
  face_photo: string | null
  status: VerificationStatus
  reject_reason: string | null
  reviewed_by: number | null
  reviewed_at: string | null
  created_at: string
}

// ==================== Recognition Types ====================

export type TaskType = 'single' | 'batch' | 'video' | 'realtime'
export type TaskStatus = 'pending' | 'processing' | 'completed' | 'failed'

export interface RecognitionTask {
  id: number
  task_uuid: string
  user_id: number
  task_type: TaskType
  status: TaskStatus
  progress: number
  total_items: number | null
  success_count: number
  failed_count: number
  started_at: string | null
  finished_at: string | null
  created_at: string
}

export type PlateType = 'blue' | 'yellow' | 'green' | 'new_energy' | 'other'

export interface RecognitionResult {
  id: number
  task_id: number | null
  user_id: number
  original_image_url: string
  enhanced_image_url: string | null
  license_plate: string
  plate_type: PlateType
  confidence: number
  province: string | null
  enhanced_algorithm: string | null
  processing_time_ms: number
  is_correct: boolean | null
  created_at: string
}

// ==================== Role & Permission Types ====================

export interface Role {
  id: number
  name: string
  description: string | null
  is_system: boolean
  created_at: string
}

export interface Permission {
  id: number
  code: string
  name: string
  category: string | null
  created_at: string
}

// ==================== Order Types ====================

export type OrderStatus = 'pending' | 'paid' | 'cancelled' | 'refunded'
export type PaymentMethod = 'wechat' | 'alipay'  | 'bank_transfer'

export interface Order {
  id: number
  order_no: string
  user_id: number
  package_id: number
  original_price: number
  actual_price: number
  coupon_id: number | null
  status: OrderStatus
  payment_method: PaymentMethod | null
  paid_at: string | null
  created_at: string
}

// ==================== Statistics Types ====================

export interface DashboardStats {
  total_users: number
  today_registrations: number
  total_recognitions: number
  today_recognitions: number
  total_revenue: number
  today_revenue: number
  active_users_30d: number
}

export interface UserTrendData {
  date: string
  count: number
}

export interface RecognitionTrendData {
  date: string
  total: number
  success: number
  failed: number
}

// ==================== System Config Types ====================

export interface SystemConfig {
  key: string
  value: string
  value_type: 'string' | 'number' | 'boolean' | 'json'
  category: string
  description: string | null
  updated_at: string
}

// ==================== API Request/Response Types ====================

export interface PageParams {
  page: number
  pageSize: number
}

export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// User Management API Params
export interface UserListParams extends PageParams {
  keyword?: string
  user_type?: UserType
  status?: UserStatus
  start_date?: string
  end_date?: string
}

export interface BanUserParams {
  user_id: number
  reason: string
  banned_until?: string | null // null for permanent ban
}

// Recognition Management API Params
export interface RecognitionListParams extends PageParams {
  user_id?: number
  task_type?: TaskType
  start_date?: string
  end_date?: string
  keyword?: string
}

// Verification Review Params
export interface VerificationReviewParams {
  verification_id: number
  status: 'approved' | 'rejected'
  reject_reason?: string
}
// User Create/Update Params
export interface AdminUserCreate {
  phone: string
  nickname: string
  email?: string
  password: string
  user_type: UserType
  role_ids?: number[]
}

export interface AdminUserUpdate {
  phone?: string
  nickname?: string
  email?: string
  user_type?: string
  status?: string
  role_ids?: number[]
  password?: string // Although usually handled separately, sometimes convenient
}

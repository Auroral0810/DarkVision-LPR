import request from '@/utils/request'

// 统一响应结构
interface UnifiedResponse<T = any> {
  code: number
  message: string
  data: T
}

interface RegisterRequest {
  phone?: string
  sms_code?: string
  email?: string
  email_code?: string
  nickname: string
  password: string
}

interface LoginResponseData {
  access_token: string
  token_type: string
  user_info: any
}

export function register(data: RegisterRequest): Promise<UnifiedResponse<LoginResponseData>> {
  return request.post('/auth/register', data)
}

export function loginByPhone(data: { phone: string; password?: string; sms_code?: string }): Promise<UnifiedResponse<LoginResponseData>> {
  return request.post('/auth/login/phone', data)
}

export function loginByEmail(data: { email: string; password?: string; email_code?: string }): Promise<UnifiedResponse<LoginResponseData>> {
  return request.post('/auth/login/email', data)
}

export function sendSmsCode(phone: string, scene: string): Promise<UnifiedResponse<{ code: string; expire_seconds: number }>> {
  return request.post('/auth/sms/send', { phone, scene })
}

export function sendEmailCode(email: string, scene: string): Promise<UnifiedResponse<{ code: string; expire_seconds: number }>> {
  return request.post('/auth/email/send', { email, scene })
}

export function resetPassword(data: {
  account: string
  code: string
  new_password: string
  confirm_password: string
}): Promise<UnifiedResponse> {
  return request.post('/auth/password/reset', data)
}

// 用户信息更新
export interface UpdateProfileRequest {
  nickname?: string
  avatar_url?: string
  gender?: 'male' | 'female' | 'unknown'
  birthday?: string
  address?: string
}

export function updateProfile(data: UpdateProfileRequest): Promise<UnifiedResponse<any>> {
  return request.put('/users/profile', data)
}

export function changePassword(data: any): Promise<UnifiedResponse> {
  return request.put('/users/password', data)
}

// 获取当前用户详细信息
export function getCurrentUserInfo(): Promise<UnifiedResponse<any>> {
  return request.get('/auth/me')
}

export interface VerificationSubmitRequest {
  real_name: string
  id_card_number: string
  id_card_front: string
  id_card_back: string
  face_photo?: string
}

export function submitVerification(data: VerificationSubmitRequest): Promise<UnifiedResponse> {
  return request.post('/users/verify', data)
}

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

export function resetPassword(data: any): Promise<UnifiedResponse> {
  return request.post('/auth/password/reset', data)
}


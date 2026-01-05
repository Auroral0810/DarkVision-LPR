import request from '@/utils/request'

/**
 * Send SMS verification code
 */
export function sendSmsCode(phone: string, scene: string = 'register') {
  return request.post('/auth/sms/send', { phone, scene })
}

/**
 * Send Email verification code
 */
export function sendEmailCode(email: string, scene: string = 'register') {
  return request.post('/auth/email/send', { email, scene })
}

/**
 * Register user
 */
export function register(data: any) {
  return request.post('/auth/register', data)
}

/**
 * Login by phone
 */
export function loginByPhone(data: { phone: string; password?: string; sms_code?: string }) {
  return request.post('/auth/login/phone', data)
}

/**
 * Login by email
 */
export function loginByEmail(data: { email: string; password?: string; email_code?: string }) {
  return request.post('/auth/login/email', data)
}


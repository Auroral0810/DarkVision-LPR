import request from '@/utils/request'

/**
 * 验证码API响应接口
 */
export interface CaptchaResponse {
  captcha_id: string
  image_base64: string
  expire_seconds: number
}

/**
 * 获取图形验证码
 * @param captchaId 可选，刷新时传入旧的验证码ID
 * @returns 验证码数据
 */
export function getCaptcha(captchaId?: string) {
  return request.post<any, { code: number; data: CaptchaResponse; message: string }>(
    '/captcha/generate',
    captchaId ? { captcha_id: captchaId } : {}
  )
}

/**
 * 验证图形验证码（可选调用）
 * @param captchaId 验证码ID
 * @param code 用户输入的验证码
 */
export function verifyCaptcha(captchaId: string, code: string) {
  return request.post('/captcha/verify', {
    captcha_id: captchaId,
    code
  })
}


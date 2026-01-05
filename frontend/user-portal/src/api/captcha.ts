import request from '@/utils/request'

interface CaptchaGenerateResponse {
  captcha_id: string
  image_base64: string
  expire_seconds: number
}

interface CaptchaVerifyRequest {
  captcha_id: string
  code: string
}

interface UnifiedResponse<T = any> {
  code: number
  message: string
  data: T
}

export function getCaptcha(captchaId?: string): Promise<UnifiedResponse<CaptchaGenerateResponse>> {
  return request.get('/captcha/generate', { params: { captcha_id: captchaId } })
}

export function verifyCaptcha(captchaId: string, code: string): Promise<UnifiedResponse> {
  const payload: CaptchaVerifyRequest = { captcha_id: captchaId, code }
  return request.post('/captcha/verify', payload)
}


import request from '../utils/request'

export function getPricingPlans(): Promise<any> {
  return request.get('/website/pricing')
}

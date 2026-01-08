import request from '@/utils/request'
import type { PageResult } from '@/types/lpr'

export interface OperationLog {
  id: number
  admin_id: number
  module: string
  action: string
  description?: string
  method?: string
  path?: string
  ip_address?: string
  status: number
  duration?: number
  params?: string
  result?: string
  created_at: string
  admin_username?: string
}

export interface IpRule {
  id: number
  ip_address: string
  type: 'allow' | 'deny'
  remark?: string
  created_at: string
}

export interface SecurityConfig {
  login_fail_limit: number
  login_lock_duration: number
  api_rate_limit: number
  enable_ip_whitelist: boolean
}

export interface SystemLogData {
  content: string
  filename: string
  total_lines: number
}

const SYSTEM_BASE_URL = '/api/admin/system'

const SystemAPI = {
  getLogs(params: any) {
    return request({
      url: `${SYSTEM_BASE_URL}/logs`,
      method: 'get',
      params
    }) as Promise<PageResult<OperationLog>>
  },

  getSystemLogs(params: { log_type: 'app' | 'error'; lines?: number }) {
    return request({
      url: `${SYSTEM_BASE_URL}/logs/system`,
      method: 'get',
      params
    }) as Promise<SystemLogData>
  },

  getIpRules(rule_type?: string) {
    return request({
      url: `${SYSTEM_BASE_URL}/ip-rules`,
      method: 'get',
      params: { rule_type }
    }) as Promise<IpRule[]>
  },

  addIpRule(data: Partial<IpRule>) {
    return request({
      url: `${SYSTEM_BASE_URL}/ip-rules`,
      method: 'post',
      data
    }) as Promise<IpRule>
  },

  deleteIpRule(id: number) {
    return request({
      url: `${SYSTEM_BASE_URL}/ip-rules/${id}`,
      method: 'delete'
    })
  },

  getSecurityConfig() {
    return request({
      url: `${SYSTEM_BASE_URL}/security/config`,
      method: 'get'
    }) as Promise<SecurityConfig>
  },

  updateSecurityConfig(data: Partial<SecurityConfig>) {
    return request({
      url: `${SYSTEM_BASE_URL}/security/config`,
      method: 'put',
      data
    }) as Promise<SecurityConfig>
  }
}

export default SystemAPI

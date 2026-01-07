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
  created_at: string
  admin_username?: string
}

const SYSTEM_BASE_URL = '/api/admin/system'

const SystemAPI = {
  /**
   * 获取操作日志列表
   */
  getLogs(params: any) {
    return request({
      url: `${SYSTEM_BASE_URL}/logs`,
      method: 'get',
      params
    }) as Promise<PageResult<OperationLog>>
  }
}

export default SystemAPI

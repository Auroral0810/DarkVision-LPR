import request from '@/utils/request'

export const maintenanceApi = {
  // --- Cache Management ---
  getCacheStats() {
    return request({
      url: '/api/admin/maintenance/cache/stats',
      method: 'get'
    }) as Promise<any>
  },
  searchCacheKeys(params: { pattern: string; limit?: number }) {
    return request({
      url: '/api/admin/maintenance/cache/keys',
      method: 'get',
      params
    }) as Promise<any[]>
  },
  clearCache(data: { prefix?: string; keys?: string[] }) {
    return request({
      url: '/api/admin/maintenance/cache/clear',
      method: 'post',
      data
    }) as Promise<any>
  },

  // --- Task Scheduling ---
  getTasks() {
    return request({
      url: '/api/admin/maintenance/tasks',
      method: 'get'
    }) as Promise<any[]>
  },
  createTask(data: any) {
    return request({
      url: '/api/admin/maintenance/tasks',
      method: 'post',
      data
    }) as Promise<any>
  },
  updateTask(id: number, data: any) {
    return request({
      url: `/api/admin/maintenance/tasks/${id}`,
      method: 'put',
      data
    }) as Promise<any>
  },
  deleteTask(id: number) {
    return request({
      url: `/api/admin/maintenance/tasks/${id}`,
      method: 'delete'
    }) as Promise<any>
  },
  toggleTask(id: number) {
    return request({
      url: `/api/admin/maintenance/tasks/${id}/toggle`,
      method: 'post'
    }) as Promise<any>
  },
  runTask(id: number) {
    return request({
      url: `/api/admin/maintenance/tasks/${id}/run`,
      method: 'post'
    }) as Promise<any>
  },

  // --- Version Update ---
  getVersions(params: { page: number; page_size: number; type?: string }) {
    return request({
      url: '/api/admin/maintenance/versions',
      method: 'get',
      params
    }) as Promise<{ list: any[]; total: number }>
  },
  createVersion(data: any) {
    return request({
      url: '/api/admin/maintenance/versions',
      method: 'post',
      data
    }) as Promise<any>
  },
  updateVersion(id: number, data: any) {
    return request({
      url: `/api/admin/maintenance/versions/${id}`,
      method: 'put',
      data
    }) as Promise<any>
  },
  deleteVersion(id: number) {
    return request({
      url: `/api/admin/maintenance/versions/${id}`,
      method: 'delete'
    }) as Promise<any>
  }
}

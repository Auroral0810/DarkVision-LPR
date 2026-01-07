import request from '@/utils/request'

export interface Permission {
  id: number
  name: string
  code: string
  description?: string
  type: string
  parent_id?: number
  path?: string
  component?: string
  icon?: string
  sort_order: number
  children?: Permission[]
  created_at: string
}

export interface Role {
  id: number
  name: string
  description?: string
  created_at: string
  permission_ids?: number[]
  permissions?: Permission[]
}

export interface RoleForm {
  name: string
  description?: string
  permission_ids: number[]
}

class PermAPI {
  /** 获取权限列表(树形) */
  static getPermissions() {
    return request({
      url: '/api/admin/permissions',
      method: 'get'
    }) as Promise<Permission[]>
  }

  /** 创建权限 */
  static createPermission(data: Partial<Permission>) {
    return request({
      url: '/api/admin/permissions',
      method: 'post',
      data
    }) as Promise<Permission>
  }

  /** 更新权限 */
  static updatePermission(id: number, data: Partial<Permission>) {
    return request({
      url: `/api/admin/permissions/${id}`,
      method: 'put',
      data
    }) as Promise<Permission>
  }

  /** 删除权限 */
  static deletePermission(id: number) {
    return request({
      url: `/api/admin/permissions/${id}`,
      method: 'delete'
    })
  }

  /** 获取角色列表 */
  static getRoles(params?: any) {
    return request({
      url: '/api/admin/roles',
      method: 'get',
      params
    }) as Promise<{ list: Role[], total: number }>
  }

  /** 获取所有角色 */
  static getAllRoles() {
    return request({
      url: '/api/admin/roles/all',
      method: 'get'
    }) as Promise<Role[]>
  }

  /** 创建角色 */
  static createRole(data: RoleForm) {
    return request({
      url: '/api/admin/roles',
      method: 'post',
      data
    }) as Promise<Role>
  }

  /** 更新角色 */
  static updateRole(id: number, data: Partial<RoleForm>) {
    return request({
      url: `/api/admin/roles/${id}`,
      method: 'put',
      data
    }) as Promise<Role>
  }

  /** 删除角色 */
  static deleteRole(id: number) {
    return request({
      url: `/api/admin/roles/${id}`,
      method: 'delete'
    })
  }
}

export default PermAPI

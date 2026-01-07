import request from '@/utils/request'
import type {
  User,
  UserListParams,
  BanUserParams,
  PageResult,
  AdminUserCreate,
  AdminUserUpdate
} from '@/types/lpr'

const USER_BASE_URL = '/api/admin/users'

/**
 * 用户管理 API
 */
const UserAPI = {
  /**
   * 获取用户列表（支持分页、搜索、筛选）
   */
  getUserList(params: UserListParams) {
    return request({
      url: USER_BASE_URL,
      method: 'get',
      params
    }) as Promise<PageResult<User>>
  },

  /**
   * 获取用户详情
   */
  getUserDetail(userId: number) {
    return request({
      url: `${USER_BASE_URL}/${userId}`,
      method: 'get'
    }) as Promise<User>
  },

  /**
   * 封禁用户
   */
  banUser(data: BanUserParams) {
    return request({
      url: `${USER_BASE_URL}/ban`,
      method: 'post',
      data
    })
  },

  /**
   * 解封用户
   */
  unbanUser(userId: number) {
    return request({
      url: `${USER_BASE_URL}/${userId}/unban`,
      method: 'post'
    })
  },

  /**
   * 重置用户密码
   */
  resetUserPassword(userId: number) {
    return request({
      url: `${USER_BASE_URL}/${userId}/reset-password`,
      method: 'post'
    }) as Promise<{ new_password: string }>
  },

  /**
   * 强制用户下线
   */
  forceLogout(userId: number) {
    return request({
      url: `${USER_BASE_URL}/${userId}/force-logout`,
      method: 'post'
    })
  },

  /**
   * 修改用户类型
   */
  updateUserType(userId: number, userType: 'free' | 'vip' | 'enterprise') {
    return request({
      url: `${USER_BASE_URL}/${userId}/type`,
      method: 'put',
      data: { user_type: userType }
    })
  },

  /**
   * 批量删除用户
   */
  batchDeleteUsers(userIds: number[]) {
    return request({
      url: `${USER_BASE_URL}/batch-delete`,
      method: 'post',
      data: { user_ids: userIds }
    })
  },

  /**
   * 导出用户数据到Excel
   */
  exportUsers(params: UserListParams) {
    return request({
      url: `${USER_BASE_URL}/export`,
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  /**
   * 创建用户
   */
  createUser(data: AdminUserCreate) {
    return request({
      url: USER_BASE_URL,
      method: 'post',
      data
    }) as Promise<User>
  },

  /**
   * 更新用户
   */
  updateUser(userId: number, data: AdminUserUpdate) {
    return request({
      url: `${USER_BASE_URL}/${userId}`,
      method: 'put',
      data
    }) as Promise<User>
  },

  /**
   * 删除用户
   */
  deleteUser(userId: number) {
     return this.batchDeleteUsers([userId])
  }
}

export default UserAPI

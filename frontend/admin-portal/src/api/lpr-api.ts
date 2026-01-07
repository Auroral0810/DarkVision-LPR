import request from '@/utils/request'
import type {
  User,
  UserListParams,
  BanUserParams,
  RealNameVerification,
  VerificationReviewParams,
  RecognitionTask,
  RecognitionResult,
  RecognitionListParams,
  Order,
  DashboardStats,
  UserTrendData,
  RecognitionTrendData,
  PageResult,
  ApiResponse
} from '@/types/lpr'

const LPR_BASE_URL = '/api/admin'

/**
 * LPR Admin API
 */
const LprAPI = {
  // ==================== User Management ====================
  
  /**
   * Get user list with pagination and filters
   */
  getUserList(params: UserListParams) {
    return request<any, PageResult<User>>({
      url: `${LPR_BASE_URL}/users`,
      method: 'get',
      params
    })
  },

  /**
   * Create user (Admin)
   */
  createUser(data: any) {
    return request({
      url: `${LPR_BASE_URL}/users`,
      method: 'post',
      data
    })
  },

  /**
   * Update user info (Admin)
   */
  updateUser(userId: number, data: any) {
    return request({
      url: `${LPR_BASE_URL}/users/${userId}`,
      method: 'put',
      data
    })
  },

  /**
   * Get user detail by ID
   */
  getUserDetail(userId: number) {
    return request<any, User>({
      url: `${LPR_BASE_URL}/users/${userId}`,
      method: 'get'
    })
  },

  /**
   * Ban user
   */
  banUser(data: BanUserParams) {
    return request({
      url: `${LPR_BASE_URL}/users/ban`,
      method: 'post',
      data
    })
  },

  /**
   * Unban user
   */
  unbanUser(userId: number) {
    return request({
      url: `${LPR_BASE_URL}/users/${userId}/unban`,
      method: 'post'
    })
  },

  /**
   * Reset user password
   */
  resetUserPassword(userId: number) {
    return request<any, { new_password: string }>({
      url: `${LPR_BASE_URL}/users/${userId}/reset-password`,
      method: 'post'
    })
  },

  /**
   * Force user logout
   */
  forceLogout(userId: number) {
    return request({
      url: `${LPR_BASE_URL}/users/${userId}/force-logout`,
      method: 'post'
    })
  },

  /**
   * Update user type
   */
  updateUserType(userId: number, userType: 'free' | 'vip' | 'enterprise') {
    return request({
      url: `${LPR_BASE_URL}/users/${userId}/type`,
      method: 'put',
      data: { user_type: userType }
    })
  },

  /**
   * Batch delete users
   */
  batchDeleteUsers(userIds: number[]) {
    return request({
      url: `${LPR_BASE_URL}/users/batch-delete`,
      method: 'post',
      data: { user_ids: userIds }
    })
  },

  /**
   * Export users to Excel
   */
  exportUsers(params: UserListParams) {
    return request({
      url: `${LPR_BASE_URL}/users/export`,
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  // ==================== Verification Management ====================

  /**
   * Get verification review list
   */
  getVerificationList(params: { status?: string; page: number; pageSize: number }) {
    return request<any, PageResult<RealNameVerification>>({
      url: `${LPR_BASE_URL}/verifications`,
      method: 'get',
      params
    })
  },

  /**
   * Review verification
   */
  reviewVerification(data: VerificationReviewParams) {
    return request({
      url: `${LPR_BASE_URL}/verifications/review`,
      method: 'post',
      data
    })
  },

  // ==================== Recognition Management ====================

  /**
   * Get recognition task list
   */
  getTaskList(params: RecognitionListParams) {
    return request<any, PageResult<RecognitionTask>>({
      url: `${LPR_BASE_URL}/recognition/tasks`,
      method: 'get',
      params
    })
  },

  /**
   * Get active tasks (real-time monitoring)
   */
  getActiveTasks() {
    return request<any, RecognitionTask[]>({
      url: `${LPR_BASE_URL}/recognition/tasks/active`,
      method: 'get'
    })
  },

  /**
   * Retry failed task
   */
  retryTask(taskId: number) {
    return request({
      url: `${LPR_BASE_URL}/recognition/tasks/${taskId}/retry`,
      method: 'post'
    })
  },

  /**
   * Get recognition results list
   */
  getRecognitionList(params: RecognitionListParams) {
    return request<any, PageResult<RecognitionResult>>({
      url: `${LPR_BASE_URL}/recognition/results`,
      method: 'get',
      params
    })
  },

  /**
   * Mark recognition result as correct/incorrect
   */
  auditRecognition(resultId: number, isCorrect: boolean) {
    return request({
      url: `${LPR_BASE_URL}/recognition/results/${resultId}/audit`,
      method: 'post',
      data: { is_correct: isCorrect }
    })
  },

  /**
   * Batch delete recognition results
   */
  batchDeleteRecognitions(resultIds: number[]) {
    return request({
      url: `${LPR_BASE_URL}/recognition/results/batch-delete`,
      method: 'post',
      data: { result_ids: resultIds }
    })
  },

  /**
   * Export recognition results
   */
  exportRecognitions(params: RecognitionListParams) {
    return request({
      url: `${LPR_BASE_URL}/recognition/results/export`,
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  // ==================== Model Management ====================

  /**
   * Get model list
   */
  getModelList() {
    return request<any, any[]>({
      url: `${LPR_BASE_URL}/models`,
      method: 'get'
    })
  },

  /**
   * Switch active model
   */
  switchModel(modelId: number) {
    return request({
      url: `${LPR_BASE_URL}/models/${modelId}/activate`,
      method: 'post'
    })
  },

  // ==================== Order Management ====================

  /**
   * Get order list
   */
  getOrderList(params: any) {
    return request<any, PageResult<Order>>({
      url: `${LPR_BASE_URL}/orders`,
      method: 'get',
      params
    })
  },

  /**
   * Refund order
   */
  refundOrder(orderId: number, reason: string) {
    return request({
      url: `${LPR_BASE_URL}/orders/${orderId}/refund`,
      method: 'post',
      data: { reason }
    })
  },

  // ==================== Statistics & Analytics ====================

  /**
   * Get dashboard statistics
   */
  getDashboardStats() {
    return request<any, DashboardStats>({
      url: `${LPR_BASE_URL}/stats/dashboard`,
      method: 'get'
    })
  },

  /**
   * Get user registration trend
   */
  getUserTrend(params: { start_date: string; end_date: string }) {
    return request<any, UserTrendData[]>({
      url: `${LPR_BASE_URL}/stats/user-trend`,
      method: 'get',
      params
    })
  },

  /**
   * Get recognition volume trend
   */
  getRecognitionTrend(params: { start_date: string; end_date: string }) {
    return request<any, RecognitionTrendData[]>({
      url: `${LPR_BASE_URL}/stats/recognition-trend`,
      method: 'get',
      params
    })
  },

  /**
   * Get user type distribution
   */
  getUserTypeDistribution() {
    return request<any, { type: string; count: number }[]>({
      url: `${LPR_BASE_URL}/stats/user-distribution`,
      method: 'get'
    })
  },

  /**
   * Get plate type distribution
   */
  getPlateTypeDistribution() {
    return request<any, { plate_type: string; count: number }[]>({
      url: `${LPR_BASE_URL}/stats/plate-distribution`,
      method: 'get'
    })
  }
}

export default LprAPI

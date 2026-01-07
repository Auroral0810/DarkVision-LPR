import request from '@/utils/request'
import request from '@/utils/request'

const LPR_BASE_URL = '/api/admin'

export interface VerificationUser {
  id: number
  nickname: string
  phone: string | null
  email: string | null
  avatar_url: string | null
}

export interface VerificationItem {
  id: number
  user_id: number
  user: VerificationUser
  real_name: string | null
  id_card_number: string | null
  id_card_front: string
  id_card_back: string
  face_photo: string | null
  status: 'pending' | 'approved' | 'rejected'
  reject_reason: string | null
  created_at: string
  reviewed_at: string | null
  reviewer_id: number | null
}

export interface VerificationListParams {
  page: number
  pageSize: number
  status?: string
  keyword?: string
}

export default {
  /**
   * Get verification list
   */
  getVerifications(params: VerificationListParams) {
    return request({
      url: `${LPR_BASE_URL}/verifications`,
      method: 'get',
      params: {
        page: params.page,
        page_size: params.pageSize,
        status: params.status,
        keyword: params.keyword
      }
    })
  },

  /**
   * Audit verification
   */
  auditVerification(id: number, data: { action: 'approve' | 'reject', reject_reason?: string }) {
    return request({
      url: `${LPR_BASE_URL}/verifications/${id}/audit`,
      method: 'post',
      data
    })
  }
}

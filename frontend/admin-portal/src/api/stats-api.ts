import request from '@/utils/request'
import type {
  DashboardStats,
  UserTrendData,
  RecognitionTrendData
} from '@/types/lpr'

const STATS_BASE_URL = '/api/v1/admin/stats'

/**
 * 统计分析 API
 */
const StatsAPI = {
  /**
   * 获取仪表板统计数据
   */
  getDashboardStats() {
    return request<any, DashboardStats>({
      url: `${STATS_BASE_URL}/dashboard`,
      method: 'get'
    })
  },

  /**
   * 获取用户注册趋势
   */
  getUserTrend(params: { start_date: string; end_date: string }) {
    return request<any, UserTrendData[]>({
      url: `${STATS_BASE_URL}/user-trend`,
      method: 'get',
      params
    })
  },

  /**
   * 获取识别量趋势
   */
  getRecognitionTrend(params: { start_date: string; end_date: string }) {
    return request<any, RecognitionTrendData[]>({
      url: `${STATS_BASE_URL}/recognition-trend`,
      method: 'get',
      params
    })
  },

  /**
   * 获取用户类型分布
   */
  getUserTypeDistribution() {
    return request<any, { type: string; count: number }[]>({
      url: `${STATS_BASE_URL}/user-distribution`,
      method: 'get'
    })
  },

  /**
   * 获取车牌类型分布
   */
  getPlateTypeDistribution() {
    return request<any, { plate_type: string; count: number }[]>({
      url: `${STATS_BASE_URL}/plate-distribution`,
      method: 'get'
    })
  },

  /**
   * 获取在线用户数
   */
  getOnlineUserCount() {
    return request<any, { count: number }>({
      url: '/api/v1/tracking/online-count',
      method: 'get'
    })
  }
}

export default StatsAPI

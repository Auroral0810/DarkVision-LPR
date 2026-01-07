import request from '@/utils/request'
import type {
  Order,
  PageResult
} from '@/types/lpr'

const ORDER_BASE_URL = '/api/v1/admin/orders'

/**
 * 订单管理 API
 */
const OrderAPI = {
  /**
   * 获取订单列表
   */
  getOrderList(params: any) {
    return request<any, PageResult<Order>>({
      url: ORDER_BASE_URL,
      method: 'get',
      params
    })
  },

  /**
   * 退款订单
   */
  refundOrder(orderId: number, reason: string) {
    return request({
      url: `${ORDER_BASE_URL}/${orderId}/refund`,
      method: 'post',
      data: { reason }
    })
  }
}

export default OrderAPI

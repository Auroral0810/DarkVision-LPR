import request from '@/utils/request'

/**
 * 获取识别历史记录
 */
export function getRecognitionHistory(params: any) {
  return request({
    url: '/history',
    method: 'get',
    params
  })
}

/**
 * 删除识别记录
 */
export function deleteRecognitionRecord(id: number | string) {
  return request({
    url: `/history/${id}`,
    method: 'delete'
  })
}

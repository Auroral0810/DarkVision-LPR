import request from '@/utils/request'

export interface AnalysisParams {
  time_range: 'week' | 'month' | 'year'
}

export function getAnalysisData(params: AnalysisParams) {
  return request({
    url: '/analysis/dashboard',
    method: 'get',
    params
  })
}

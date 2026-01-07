import request from '@/utils/request'
import type {
  RecognitionTask,
  RecognitionResult,
  RecognitionListParams,
  PageResult
} from '@/types/lpr'

const RECOGNITION_BASE_URL = '/api/v1/admin/recognition'

/**
 * 识别管理 API
 */
const RecognitionAPI = {
  /**
   * 获取识别任务列表
   */
  getTaskList(params: RecognitionListParams) {
    return request<any, PageResult<RecognitionTask>>({
      url: `${RECOGNITION_BASE_URL}/tasks`,
      method: 'get',
      params
    })
  },

  /**
   * 获取活动任务 (实时监控)
   */
  getActiveTasks() {
    return request<any, RecognitionTask[]>({
      url: `${RECOGNITION_BASE_URL}/tasks/active`,
      method: 'get'
    })
  },

  /**
   * 重试失败任务
   */
  retryTask(taskId: number) {
    return request({
      url: `${RECOGNITION_BASE_URL}/tasks/${taskId}/retry`,
      method: 'post'
    })
  },

  /**
   * 获取识别结果列表
   */
  getRecognitionList(params: RecognitionListParams) {
    return request<any, PageResult<RecognitionResult>>({
      url: `${RECOGNITION_BASE_URL}/results`,
      method: 'get',
      params
    })
  },

  /**
   * 标记识别结果正确性（质量审核）
   */
  auditRecognition(resultId: number, isCorrect: boolean) {
    return request({
      url: `${RECOGNITION_BASE_URL}/results/${resultId}/audit`,
      method: 'post',
      data: { is_correct: isCorrect }
    })
  },

  /**
   * 批量删除识别结果
   */
  batchDeleteRecognitions(resultIds: number[]) {
    return request({
      url: `${RECOGNITION_BASE_URL}/results/batch-delete`,
      method: 'post',
      data: { result_ids: resultIds }
    })
  },

  /**
   * 导出识别结果
   */
  exportRecognitions(params: RecognitionListParams) {
    return request({
      url: `${RECOGNITION_BASE_URL}/results/export`,
      method: 'get',
      params,
      responseType: 'blob'
    })
  },

  /**
   * 获取模型列表
   */
  getModelList() {
    return request<any, any[]>({
      url: `${RECOGNITION_BASE_URL}/models`,
      method: 'get'
    })
  },

  /**
   * 切换活动模型
   */
  switchModel(modelId: number) {
    return request({
      url: `${RECOGNITION_BASE_URL}/models/${modelId}/activate`,
      method: 'post'
    })
  }
}

export default RecognitionAPI

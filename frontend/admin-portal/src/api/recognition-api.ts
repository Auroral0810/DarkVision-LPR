import request from '@/utils/request'

export interface RecognitionTask {
  id: number
  task_uuid: string
  user_id: number
  task_type: string
  status: string
  progress: number
  total_items: number
  success_count: number
  failed_count: number
  started_at: string
  finished_at: string
  created_at: string
}

export interface RecognitionRecord {
  id: number
  task_id?: number
  user_id: number
  original_image_url: string
  enhanced_image_url?: string
  license_plate: string
  plate_type?: string
  confidence: number
  bbox?: any
  enhance_algorithm?: string
  model_version?: string
  processing_time?: number
  processed_at: string
  created_at: string
}

export interface RecognitionModel {
  id: number
  version: string
  name: string
  is_active: boolean
  accuracy?: number
  description?: string
  file_path?: string
  created_at: string
}

const BASE_URL = '/api/admin/recognition'

// --- Tasks ---
export function getTasks(params: any) {
  return request({
    url: `${BASE_URL}/tasks`,
    method: 'get',
    params
  })
}

export function deleteTask(id: number) {
  return request({
    url: `${BASE_URL}/tasks/${id}`,
    method: 'delete'
  })
}

// --- Records ---
export function getRecords(params: any) {
  return request({
    url: `${BASE_URL}/records`,
    method: 'get',
    params
  })
}

export function deleteRecord(id: number) {
  return request({
    url: `${BASE_URL}/records/${id}`,
    method: 'delete'
  })
}

// --- Models ---
export function getModels() {
  return request({
    url: `${BASE_URL}/models`,
    method: 'get'
  })
}

export function createModel(data: any) {
  return request({
    url: `${BASE_URL}/models`,
    method: 'post',
    data
  })
}

export function updateModel(id: number, data: any) {
  return request({
    url: `${BASE_URL}/models/${id}`,
    method: 'put',
    data
  })
}

export function deleteModel(id: number) {
  return request({
    url: `${BASE_URL}/models/${id}`,
    method: 'delete'
  })
}

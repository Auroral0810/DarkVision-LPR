import request from '@/utils/request'

/**
 * 上传图片到OSS
 * @param file 图片文件
 * @returns Promise<{url: string, filename: string, size: number, content_type: string}>
 */
export const uploadImage = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return request.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 通过OSS URL进行车牌识别 (同步返回)
 * @param imageUrl OSS图片URL
 * @returns Promise<识别结果>
 */
export const recognizePlateByUrl = (imageUrl: string) => {
  return request.post('/recognition/by-url', {
    image_url: imageUrl
  })
}

/**
 * 开始识别任务 (WebSocket模式)
 * @param imageUrl OSS图片URL
 * @returns Promise<{task_uuid: string}>
 */
export const startRecognitionTask = (imageUrl: string) => {
  return request.post('/recognition/start-single', {
    image_url: imageUrl
  })
}

import request from '@/utils/request'

/**
 * 上报页面访问数据
 * @param path 页面路径
 * @param fullPath 完整路径（包含查询参数）
 * @param title 页面标题
 */
export function trackPageView(path: string, fullPath: string, title: string) {
  // PageTypeEnum.WEBSITE = 'website'
  return request.post('/tracking/page-view', {
    page_type: 'website',
    page_path: path,
    full_path: fullPath,
    page_title: title,
    referrer: document.referrer || ''
  })
}

/**
 * 获取在线用户数
 */
export function getOnlineUserCount() {
  return request.get('/tracking/online-count')
}

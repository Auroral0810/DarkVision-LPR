import { Layout } from './index'
import { RouteRecordRaw } from 'vue-router'

/**
 * LPR Admin Routes
 */
export const lprRoutes: RouteRecordRaw[] = [
  {
    path: '/lpr',
    component: Layout,
    redirect: '/lpr/analytics',
    meta: { title: 'LPR管理', icon: 'monitoring' },
    children: [
      // Analytics
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('@/views/analytics/Overview.vue'),
        meta: { title: '数据分析', icon: 'data-analysis' }
      },

      // User Management
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('@/views/user-mgmt/UserList.vue'),
        meta: { title: '用户管理', icon: 'user' }
      },
      {
        path: 'verification',
        name: 'VerificationReview',
        component: () => import('@/views/user-mgmt/VerificationReview.vue'),
        meta: { title: '实名审核', icon: 'postcard' }
      },

      // Recognition Service
      {
        path: 'tasks',
        name: 'TaskMonitor',
        component: () => import('@/views/recognition/TaskMonitor.vue'),
        meta: { title: '任务监控', icon: 'monitor' }
      },
      {
        path: 'records',
        name: 'RecordManagement',
        component: () => import('@/views/recognition/RecordManagement.vue'),
        meta: { title: '识别记录', icon: 'document' }
      },
      {
        path: 'models',
        name: 'ModelManagement',
        component: () => import('@/views/recognition/ModelManagement.vue'),
        meta: { title: '模型管理', icon: 'cpu' }
      }
    ]
  }
]

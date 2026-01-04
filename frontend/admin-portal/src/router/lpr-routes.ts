import { Layout } from './index'
import { RouteRecordRaw } from 'vue-router'

const Placeholder = () => import('@/views/error/Placeholder.vue')

/**
 * DarkVision-LPR Admin Routes - 10 Core Modules
 */
export const lprRoutes: RouteRecordRaw[] = [
  // 1. 仪表盘 (Dashboard)
  {
    path: '/dashboard',
    component: Layout,
    redirect: '/dashboard/overview',
    meta: { title: '仪表盘', icon: 'homepage', alwaysShow: true },
    children: [
      {
        path: 'overview',
        component: () => import('@/views/dashboard/index.vue'),
        name: 'Overview',
        meta: { title: '概览', icon: 'el-icon-House', affix: true }
      }
    ]
  },

  // 2. 用户管理 (User Management)
  {
    path: '/user',
    component: Layout,
    redirect: '/user/list',
    meta: { title: '用户管理', icon: 'user', alwaysShow: true },
    children: [
      {
        path: 'list',
        component: () => import('@/views/user-mgmt/UserList.vue'),
        name: 'UserList',
        meta: { title: '用户列表', icon: 'el-icon-User' }
      },
      {
        path: 'status',
        component: Placeholder,
        name: 'UserStatus',
        meta: { title: '账户状态', icon: 'el-icon-Warning' }
      },
      {
        path: 'verification',
        component: () => import('@/views/user-mgmt/VerificationReview.vue'),
        name: 'Verification',
        meta: { title: '实名认证审核', icon: 'el-icon-Checked' }
      }
    ]
  },

  // 3. 权限管理 (Permission)
  {
    path: '/permission',
    component: Layout,
    redirect: '/permission/role',
    meta: { title: '权限管理', icon: 'el-icon-Lock', alwaysShow: true },
    children: [
      {
        path: 'role',
        component: () => import('@/views/perm/RoleList.vue'),
        name: 'RoleList',
        meta: { title: '角色管理', icon: 'role' }
      },
      {
        path: 'management',
        component: Placeholder,
        name: 'PermissionMgmt',
        meta: { title: '权限管理', icon: 'el-icon-Key' }
      },
      {
        path: 'admin',
        component: () => import('@/views/perm/AdminList.vue'),
        name: 'AdminList',
        meta: { title: '管理员账户', icon: 'el-icon-Setting' }
      }
    ]
  },

  // 4. 识别服务 (Recognition Service)
  {
    path: '/recognition',
    component: Layout,
    redirect: '/recognition/tasks',
    meta: { title: '识别服务', icon: 'monitor', alwaysShow: true },
    children: [
      {
        path: 'tasks',
        component: () => import('@/views/recognition/TaskMonitor.vue'),
        name: 'TaskMonitor',
        meta: { title: '任务监控', icon: 'el-icon-VideoPlay' }
      },
      {
        path: 'records',
        component: () => import('@/views/recognition/RecordManagement.vue'),
        name: 'RecordMgmt',
        meta: { title: '识别记录', icon: 'document' }
      },
      {
        path: 'models',
        component: () => import('@/views/recognition/ModelManagement.vue'),
        name: 'ModelMgmt',
        meta: { title: '模型管理', icon: 'el-icon-Cpu' }
      }
    ]
  },

  // 5. 内容管理 (Content)
  {
    path: '/content',
    component: Layout,
    redirect: '/content/site',
    meta: { title: '内容管理', icon: 'document', alwaysShow: true },
    children: [
      {
        path: 'site',
        component: () => import('@/views/content/ContentMgmt.vue'),
        name: 'SiteContent',
        meta: { title: '官网内容', icon: 'el-icon-Monitor' }
      },
      {
        path: 'docs',
        component: Placeholder,
        name: 'DocMgmt',
        meta: { title: '文档管理', icon: 'el-icon-Notebook' }
      },
      {
        path: 'announcement',
        component: Placeholder,
        name: 'AnnounceMgmt',
        meta: { title: '公告管理', icon: 'el-icon-Bell' }
      },
      {
        path: 'faq',
        component: Placeholder,
        name: 'FaqMgmt',
        meta: { title: 'FAQ管理', icon: 'el-icon-QuestionFilled' }
      }
    ]
  },

  // 6. 订单财务 (Finance)
  {
    path: '/finance',
    component: Layout,
    redirect: '/finance/orders',
    meta: { title: '订单财务', icon: 'el-icon-Money', alwaysShow: true },
    children: [
      {
        path: 'orders',
        component: () => import('@/views/finance/FinanceMgmt.vue'),
        name: 'OrderMgmt',
        meta: { title: '订单管理', icon: 'el-icon-Wallet' }
      },
      {
        path: 'packages',
        component: Placeholder,
        name: 'PackageMgmt',
        meta: { title: '套餐管理', icon: 'el-icon-Present' }
      },
      {
        path: 'reports',
        component: Placeholder,
        name: 'FinanceReport',
        meta: { title: '财务报表', icon: 'el-icon-DataAnalysis' }
      }
    ]
  },

  // 7. 数据统计 (Statistics)
  {
    path: '/statistics',
    component: Layout,
    redirect: '/statistics/user',
    meta: { title: '数据统计', icon: 'el-icon-DataAnalysis', alwaysShow: true },
    children: [
      {
        path: 'user',
        component: () => import('@/views/analytics/UserStats.vue'),
        name: 'UserStats',
        meta: { title: '用户统计', icon: 'user' }
      },
      {
        path: 'recognition',
        component: () => import('@/views/analytics/RecognitionStats.vue'),
        name: 'RecogStats',
        meta: { title: '识别统计', icon: 'el-icon-Search' }
      },
      {
        path: 'system',
        component: () => import('@/views/analytics/SystemMonitor.vue'),
        name: 'SystemMonitor',
        meta: { title: '系统性能', icon: 'el-icon-Odometer' }
      },
      {
        path: 'board',
        component: () => import('@/views/analytics/Overview.vue'),
        name: 'BusinessBoard',
        meta: { title: '业务看板', icon: 'homepage' }
      }
    ]
  },

  // 8. 日志安全 (Log & Security)
  {
    path: '/log',
    component: Layout,
    redirect: '/log/operation',
    meta: { title: '日志安全', icon: 'el-icon-Warning', alwaysShow: true },
    children: [
      {
        path: 'operation',
        component: Placeholder,
        name: 'OpLog',
        meta: { title: '操作日志', icon: 'el-icon-Document' }
      },
      {
        path: 'system',
        component: Placeholder,
        name: 'SysLog',
        meta: { title: '系统日志', icon: 'el-icon-Warning' }
      },
      {
        path: 'security',
        component: () => import('@/views/security/SecurityMgmt.vue'),
        name: 'SecurityMgmt',
        meta: { title: '安全管理', icon: 'lock' }
      }
    ]
  },

  // 9. 消息通知 (Messaging)
  {
    path: '/message',
    component: Layout,
    redirect: '/message/push',
    meta: { title: '消息通知', icon: 'message', alwaysShow: true },
    children: [
      {
        path: 'push',
        component: () => import('@/views/messaging/Messaging.vue'),
        name: 'MsgPush',
        meta: { title: '消息推送', icon: 'el-icon-ChatDotRound' }
      },
      {
        path: 'service',
        component: Placeholder,
        name: 'ServiceMgmt',
        meta: { title: '客服管理', icon: 'el-icon-Service' }
      }
    ]
  },

  // 10. 系统设置 (Settings)
  {
    path: '/setting',
    component: Layout,
    redirect: '/setting/base',
    meta: { title: '系统设置', icon: 'setting', alwaysShow: true },
    children: [
      {
        path: 'base',
        component: () => import('@/views/config/SystemConfig.vue'),
        name: 'BaseConfig',
        meta: { title: '基础配置', icon: 'setting' }
      },
      {
        path: 'params',
        component: Placeholder,
        name: 'RecogParams',
        meta: { title: '识别参数', icon: 'el-icon-Operation' }
      },
      {
        path: 'quotas',
        component: Placeholder,
        name: 'UserQuotas',
        meta: { title: '用户限额', icon: 'el-icon-Histogram' }
      },
      {
        path: 'email-sms',
        component: Placeholder,
        name: 'EmailSms',
        meta: { title: '邮件短信', icon: 'el-icon-Postcard' }
      },
      {
        path: 'external',
        component: () => import('@/views/external/ExternalService.vue'),
        name: 'ExternalService',
        meta: { title: '第三方服务', icon: 'connection' }
      },
      {
        path: 'backup',
        component: () => import('@/views/maintenance/Maintenance.vue'),
        name: 'BackupRecover',
        meta: { title: '备份恢复', icon: 'el-icon-Collection' }
      },
      {
        path: 'maintenance',
        component: Placeholder,
        name: 'SysMaintenance',
        meta: { title: '系统维护', icon: 'cpu' }
      }
    ]
  }
]

import { RouteRecordRaw } from 'vue-router'

const Layout = () => import("@/layouts/index.vue");
const Placeholder = () => import('@/views/error/Placeholder.vue')

/**
 * DarkVision-LPR Admin Routes - 基于角色权限动态配置的路由
 * 
 * 角色映射:
 * - super_admin: 超级管理员 (所有权限)
 * - user_manager: 用户管理管理员 (用户+认证)
 * - finance_manager: 财务管理员 (订单+套餐+报表)
 * - ops_manager: 运营管理员 (内容+公告+活动+用户统计)
 * - ai_manager: 算法/识别管理员 (监控+记录+模型+识别统计)
 * - security_admin: 安全/运维管理员 (日志+安全+备份+监控)
 */
export const lprRoutes: RouteRecordRaw[] = [
  // 1. Dashboard
  {
    path: '/dashboard',
    component: Layout,
    redirect: '/dashboard/overview',
    meta: { 
      title: 'Dashboard', 
      icon: 'homepage', 
      alwaysShow: true 
    },
    children: [
      {
        path: 'overview',
        component: () => import('@/views/dashboard/index.vue'),
        name: 'Overview',
        meta: { title: '控制台首页', icon: 'el-icon-House', affix: true }
      }
    ]
  },

  // 2. 用户管理
  {
    path: '/user',
    component: Layout,
    redirect: '/user/list',
    meta: { 
      title: '用户管理', 
      icon: 'user', 
      alwaysShow: true,
      roles: ['super_admin', 'user_manager']
    },
    children: [
      {
        path: 'list',
        component: () => import('@/views/user-mgmt/UserList.vue'),
        name: 'UserList',
        meta: { title: '用户列表', icon: 'el-icon-User', roles: ['super_admin', 'user_manager'] }
      },
      {
        path: 'verification',
        component: () => import('@/views/verification/VerificationList.vue'),
        name: 'Verification',
        meta: { title: '实名认证审核', icon: 'el-icon-Checked', roles: ['super_admin', 'user_manager'] }
      },
      {
        path: 'tags',
        component: Placeholder,
        name: 'UserTags',
        meta: { title: '用户标签管理', icon: 'el-icon-CollectionTag', roles: ['super_admin', 'user_manager'] }
      }
    ]
  },

  // 3. 权限与管理员
  {
    path: '/permission',
    component: Layout,
    redirect: '/permission/role',
    meta: { 
      title: '权限与管理员', 
      icon: 'el-icon-Lock', 
      alwaysShow: true,
      roles: ['super_admin']
    },
    children: [
      {
        path: 'role',
        component: () => import('@/views/perm/RoleList.vue'),
        name: 'RoleList',
        meta: { title: '角色管理', icon: 'role' }
      },
      {
        path: 'management',
        component: () => import('@/views/perm/PermissionList.vue'),
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

  // 4. 识别服务
  {
    path: '/recognition',
    component: Layout,
    redirect: '/recognition/tasks',
    meta: { 
      title: '识别服务', 
      icon: 'monitor', 
      alwaysShow: true,
      roles: ['super_admin', 'ai_manager']
    },
    children: [
      {
        path: 'tasks',
        component: () => import('@/views/recognition/task/TaskMonitor.vue'),
        name: 'TaskMonitor',
        meta: { title: '任务监控', icon: 'el-icon-VideoPlay' }
      },
      {
        path: 'records',
        component: () => import('@/views/recognition/record/RecordList.vue'),
        name: 'RecordMgmt',
        meta: { title: '识别记录', icon: 'el-icon-Document' }
      },
      {
        path: 'models',
        component: () => import('@/views/recognition/model/ModelList.vue'),
        name: 'ModelMgmt',
        meta: { title: '模型管理', icon: 'el-icon-Cpu' }
      }
    ]
  },

  // 5. 内容运营
  {
    path: '/content',
    component: Layout,
    redirect: '/content/site',
    meta: { 
      title: '内容运营', 
      icon: 'document', 
      alwaysShow: true,
      roles: ['super_admin', 'ops_manager']
    },
    children: [
      {
        path: 'site',
        component: () => import('@/views/content/ContentMgmt.vue'),
        name: 'SiteContent',
        meta: { title: '官网内容', icon: 'el-icon-Monitor' }
      },
      {
        path: 'docs',
        component: () => import('@/views/content/DocMgmt.vue'),
        name: 'DocMgmt',
        meta: { title: '文档管理', icon: 'el-icon-Notebook' }
      },
      {
        path: 'announcement',
        component: () => import('@/views/content/AnnounceMgmt.vue'),
        name: 'AnnounceMgmt',
        meta: { title: '公告管理', icon: 'el-icon-Bell' }
      },
      {
        path: 'faq',
        component: () => import('@/views/content/FaqMgmt.vue'),
        name: 'FaqMgmt',
        meta: { title: 'FAQ 管理', icon: 'el-icon-QuestionFilled' }
      }
    ]
  },

  // 6. 订单与财务
  {
    path: '/finance',
    component: Layout,
    redirect: '/finance/orders',
    meta: { 
      title: '订单与财务', 
      icon: 'el-icon-Money', 
      alwaysShow: true,
      roles: ['super_admin', 'finance_manager']
    },
    children: [
      {
        path: 'orders',
        component: () => import('@/views/finance/OrderMgmt.vue'),
        name: 'OrderMgmt',
        meta: { title: '订单管理', icon: 'el-icon-Wallet' }
      },
      {
        path: 'packages',
        component: () => import('@/views/finance/PackageMgmt.vue'),
        name: 'PackageMgmt',
        meta: { title: '套餐管理', icon: 'el-icon-Present' }
      },
      {
        path: 'reports',
        component: () => import('@/views/finance/FinanceReport.vue'),
        name: 'FinanceReport',
        meta: { title: '财务报表', icon: 'el-icon-DataAnalysis' }
      }
    ]
  },

  // 7. 统计分析
  {
    path: '/statistics',
    component: Layout,
    redirect: '/statistics/user',
    meta: { 
      title: '统计分析', 
      icon: 'el-icon-DataAnalysis', 
      alwaysShow: true,
      roles: ['super_admin', 'ops_manager', 'ai_manager', 'finance_manager']
    },
    children: [
      {
        path: 'user',
        component: () => import('@/views/analytics/UserStats.vue'),
        name: 'UserStats',
        meta: { title: '用户统计', icon: 'user', roles: ['super_admin', 'ops_manager'] }
      },
      {
        path: 'recognition',
        component: () => import('@/views/analytics/RecognitionStats.vue'),
        name: 'RecogStats',
        meta: { title: '识别统计', icon: 'el-icon-Search', roles: ['super_admin', 'ai_manager'] }
      },
      {
        path: 'board',
        component: () => import('@/views/analytics/Overview.vue'),
        name: 'BusinessBoard',
        meta: { title: '业务看板', icon: 'homepage', roles: ['super_admin', 'finance_manager'] }
      }
    ]
  },

  // 8. 日志与安全
  {
    path: '/log',
    component: Layout,
    redirect: '/log/operation',
    meta: { 
      title: '日志与安全', 
      icon: 'el-icon-Warning', 
      alwaysShow: true,
      roles: ['super_admin', 'security_admin']
    },
    children: [
      {
        path: 'operation',
        component: () => import('@/views/system/log/OpLog.vue'),
        name: 'OpLog',
        meta: { title: '操作日志', icon: 'el-icon-Document' }
      },
      {
        path: 'system',
        component: () => import('@/views/system/log/SysLog.vue'),
        name: 'SysLog',
        meta: { title: '系统日志', icon: 'el-icon-Warning' }
      },
      {
        path: 'security',
        component: () => import('@/views/security/SecurityMgmt.vue'),
        name: 'SecurityMgmt',
        meta: { title: '安全配置', icon: 'el-icon-Lock' }
      }
    ]
  },

  // 9. 系统配置
  {
    path: '/setting',
    component: Layout,
    redirect: '/setting/base',
    meta: { 
      title: '系统配置', 
      icon: 'el-icon-Setting', 
      alwaysShow: true,
      roles: ['super_admin']
    },
    children: [
      {
        path: 'base',
        component: () => import('@/views/config/SystemConfig.vue'),
        name: 'BaseConfig',
        meta: { title: '基础配置', icon: 'setting' }
      },
      {
        path: 'params',
        component: () => import('@/views/config/SystemConfig.vue'),
        name: 'RecogParams',
        meta: { title: '识别参数', icon: 'el-icon-Operation' },
        beforeEnter: (to, from, next) => {
          if (!to.query.tab) {
            to.query.tab = 'recognition'
          }
          next()
        }
      },
      {
        path: 'quotas',
        component: () => import('@/views/config/SystemConfig.vue'),
        name: 'UserQuotas',
        meta: { title: '限额配置', icon: 'el-icon-Histogram' },
        beforeEnter: (to, from, next) => {
          if (!to.query.tab) {
            to.query.tab = 'quota'
          }
          next()
        }
      },
      {
        path: 'email-sms',
        component: () => import('@/views/config/SystemConfig.vue'),
        name: 'EmailSms',
        meta: { title: '邮件 & 短信', icon: 'el-icon-Postcard' },
        beforeEnter: (to, from, next) => {
          if (!to.query.tab) {
            to.query.tab = 'notice'
          }
          next()
        }
      }
    ]
  },

  // 10. 第三方服务
  {
    path: '/external',
    component: Layout,
    redirect: '/external/storage',
    meta: { 
      title: '第三方服务', 
      icon: 'el-icon-Connection', 
      alwaysShow: true,
      roles: ['super_admin']
    },
    children: [
      {
        path: 'storage',
        component: () => import('@/views/external/ExternalService.vue'),
        name: 'StorageConfig',
        meta: { title: '存储配置', icon: 'el-icon-Files' }
      },
      {
        path: 'payment',
        component: Placeholder,
        name: 'PaymentConfig',
        meta: { title: '支付配置', icon: 'el-icon-CreditCard' }
      },
      {
        path: 'login',
        component: Placeholder,
        name: 'ThirdLoginConfig',
        meta: { title: '第三方登录', icon: 'el-icon-UserFilled' }
      }
    ]
  },

  // 11. 系统维护
  {
    path: '/maintenance',
    component: Layout,
    redirect: '/maintenance/cache',
    meta: { 
      title: '系统维护', 
      icon: 'el-icon-Cpu', 
      alwaysShow: true,
      roles: ['super_admin']
    },
    children: [
      {
        path: 'cache',
        component: Placeholder,
        name: 'CacheMgmt',
        meta: { title: '缓存管理', icon: 'el-icon-Refresh' }
      },
      {
        path: 'tasks',
        component: Placeholder,
        name: 'TaskScheduler',
        meta: { title: '任务调度', icon: 'el-icon-Timer' }
      },
      {
        path: 'version',
        component: Placeholder,
        name: 'VersionMgmt',
        meta: { title: '版本更新', icon: 'el-icon-Upload' }
      }
    ]
  },

  // 12. 备份与恢复
  {
    path: '/backup',
    component: Layout,
    redirect: '/backup/data',
    meta: { 
      title: '备份与恢复', 
      icon: 'el-icon-Collection', 
      alwaysShow: true,
      roles: ['super_admin', 'security_admin']
    },
    children: [
      {
        path: 'data',
        component: () => import('@/views/maintenance/Maintenance.vue'),
        name: 'DataBackup',
        meta: { title: '数据备份', icon: 'el-icon-DocumentCopy' }
      },
      {
        path: 'recover',
        component: Placeholder, // 如果复用组件，需注意区分路由参数
        name: 'DataRecover',
        meta: { title: '数据恢复', icon: 'el-icon-RefreshLeft' }
      }
    ]
  }
]

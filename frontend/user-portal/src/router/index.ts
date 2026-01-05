import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import { useUserStore } from '@/store/user'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/dashboard',
    component: DashboardLayout,
    redirect: '/dashboard/overview',
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: () => import('@/views/dashboard/Overview.vue'),
        meta: { title: 'Dashboard' }
      },
      {
        path: 'recognition',
        name: 'Recognition',
        component: () => import('@/views/dashboard/Recognition.vue'),
        meta: { title: 'Recognition' }
      },
      {
        path: 'history',
        name: 'History',
        component: () => import('@/views/dashboard/History.vue'),
        meta: { title: 'History' }
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('@/views/dashboard/Analysis.vue'),
        meta: { title: 'Analysis', roles: ['VIP', 'COMPANY'] }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/dashboard/Settings.vue'),
        meta: { title: 'Settings' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：无 token 强制到 /login
const whiteList = ['/login', '/register']
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  const hasToken = userStore.token
  if (whiteList.includes(to.path)) {
    if (hasToken) {
      next('/dashboard/overview')
    } else {
      next()
    }
    return
  }
  if (!hasToken) {
    next('/login')
  } else {
    next()
  }
})

export default router

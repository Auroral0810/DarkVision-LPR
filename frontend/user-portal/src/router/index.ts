import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
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

export default router

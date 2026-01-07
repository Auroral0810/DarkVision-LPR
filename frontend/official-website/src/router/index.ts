import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/capabilities',
    name: 'Capabilities',
    component: () => import('@/views/Capabilities.vue'),
    meta: { title: '系统能力' }
  },
  {
    path: '/features',
    name: 'Features',
    component: () => import('@/views/Features.vue'),
    meta: { title: '功能介绍' }
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('@/views/Pricing.vue'),
    meta: { title: '价格方案' }
  },
  {
    path: '/documentation',
    name: 'Documentation',
    component: () => import('@/views/Documentation.vue'),
    meta: { title: '文档中心' }
  },
  {
    path: '/download',
    name: 'Download',
    component: () => import('@/views/Download.vue'),
    meta: { title: '客户端下载' }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/About.vue'),
    meta: { title: '关于我们' }
  },
  {
    path: '/careers',
    name: 'Careers',
    component: () => import('@/views/Careers.vue'),
    meta: { title: '加入我们' }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/Contact.vue'),
    meta: { title: '联系我们' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫


// 全局后置钩子：上报访问统计
import { trackPageView } from '@/api/tracking'

router.afterEach((to) => {
  // 延迟执行，确保 document.title 已更新（虽然上面 beforeEach 更新了，但为了稳健）
  setTimeout(() => {
    trackPageView(
      to.path,
      to.fullPath,
      (to.meta.title as string) || document.title
    ).catch(err => {
      console.error('Failed to track page view:', err)
    })
  }, 0)
})


router.beforeEach((to, _from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - 暗视车牌识别系统` || '暗视车牌识别系统'
  next()
})


export default router
import { defineConfig } from 'vitepress'

export default defineConfig({
  // 站点基础配置
  title: '我的系统技术文档',
  description: 'DarkVision-LPR 系统技术说明',
  base: '/',

  // 语言配置（只保留中文）
  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN'
    }
  },

  // 主题配置
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/zh/guide/quick-start' }
    ],
    sidebar: {
      '/zh/guide/': [
        {
          text: '基础指南',
          items: [
            { text: '快速开始', link: '/zh/guide/quick-start' }
          ]
        }
      ]
    },
    // 可选：开启搜索
    search: {
      provider: 'local'
    }
  }
})

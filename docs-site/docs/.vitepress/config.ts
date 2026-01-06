import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'DarkVision-LPR',
  description: 'Low-Light License Plate Recognition System',
  base: '/',
  lastUpdated: true,

  locales: {
    // Root landing page (redirect or minimal config)
    root: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/', // Since root serves content at /, but main zh content is at /zh/, we guide links to /zh/
      // Effectively this makes the "Language Switcher" go to /zh/ when targeting Chinese.
    },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/zh/',
      description: '低光照车牌识别系统官方技术文档',
      themeConfig: {
        nav: [
          { 
            text: '指南', 
            items: [
              { text: '介绍', link: '/zh/guide/intro' },
              { text: '快速上手', link: '/zh/guide/quick-start' },
              { text: '系统配置', link: '/zh/usage/configuration' }
            ]
          },
          { 
            text: '参考', 
            items: [
               { text: '架构设计', link: '/zh/architecture/overview' },
               { text: 'API 参考', link: '/zh/usage/api' },
               { text: 'FAQ', link: '/zh/faq/index' }
            ]
          },
          { text: '了解更多', link: '/zh/about/index' },
          { text: 'v2.0.0', items: [
            { text: '更新日志', link: 'https://github.com/Auroral0810/DarkVision-LPR/releases' }
          ]}
        ],
        sidebar: {
          '/zh/guide/': [
            {
              text: '基础指南',
              items: [
                { text: '项目介绍', link: '/zh/guide/intro' },
                { text: '快速开始', link: '/zh/guide/quick-start' },
              ]
            }
          ],
          '/zh/architecture/': [
            {
              text: '系统架构',
              items: [
                { text: '架构总览', link: '/zh/architecture/overview' },
                { text: '前端设计', link: '/zh/architecture/frontend' },
                { text: '后端设计', link: '/zh/architecture/backend' },
                { text: '数据库设计', link: '/zh/architecture/database' },
                { text: '深度学习模型', link: '/zh/architecture/model' },
              ]
            }
          ],
          '/zh/usage/': [
              {
                text: '使用手册',
                items: [
                  { text: '系统配置', link: '/zh/usage/configuration' },
                  { text: '功能介绍', link: '/zh/usage/features' },
                  { text: '付费套餐', link: '/zh/usage/pricing' },
                  { text: 'API 接口', link: '/zh/usage/api' },
                ]
              }
          ],
          '/zh/faq/': [
             {
               text: '常见问题',
               items: [
                 { text: '常见问题 (FAQ)', link: '/zh/faq/index' },
               ]
             }
          ],
          '/zh/about/': [
            {
              text: '关于',
              items: [
                 { text: '关于我们', link: '/zh/about/index' }
              ]
            }
          ], 
           '/zh/': [
            {
                text: '指南',
                items: [
                    { text: '项目介绍', link: '/zh/guide/intro' },
                    { text: '快速开始', link: '/zh/guide/quick-start' },
                ]
            },
            {
                text: '参考',
                 items: [
                  { text: '架构总览', link: '/zh/architecture/overview' },
                   { text: 'API 接口', link: '/zh/usage/api' },
                   { text: '付费套餐', link: '/zh/usage/pricing' },
                ]
            }
           ]
        },
        docFooter: {
          prev: '上一页',
          next: '下一页'
        },
        outline: {
           level: 'deep',
           label: '当前页大纲'
        },
        search: {
          provider: 'local',
          options: {
            locales: {
              zh: {
                translations: {
                  button: {
                    buttonText: '搜索文档',
                    buttonAriaLabel: '搜索文档'
                  },
                  modal: {
                    noResultsText: '无法找到相关结果',
                    resetButtonTitle: '清除查询条件',
                    footer: {
                      selectText: '选择',
                      navigateText: '切换',
                      closeText: '关闭'
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    en: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      description: 'Official Technical Documentation for Low-Light LPR System',
      themeConfig: {
        nav: [
          { text: 'Guide', items: [
              { text: 'Introduction', link: '/en/guide/intro' },
              { text: 'Quick Start', link: '/en/guide/quick-start' }
          ] },
          { text: 'Reference', items: [
             { text: 'Architecture', link: '/en/architecture/overview' },
             { text: 'API', link: '/en/usage/api' }
          ]},
          { text: 'v2.0.0', items: [
            { text: 'Changelog', link: 'https://github.com/Auroral0810/DarkVision-LPR/releases' }
          ]}
        ],
        sidebar: {
            '/en/guide/': [
              {
                text: 'Guide',
                items: [
                  { text: 'Introduction', link: '/en/guide/intro' },
                  { text: 'Quick Start', link: '/en/guide/quick-start' },
                ]
              }
            ],
             '/en/architecture/': [
              {
                text: 'Architecture',
                 items: [
                  { text: 'Overview', link: '/en/architecture/overview' },
                  { text: 'Frontend', link: '/en/architecture/frontend' },
                  { text: 'Backend', link: '/en/architecture/backend' },
                  { text: 'Database', link: '/en/architecture/database' },
                  { text: 'Model', link: '/en/architecture/model' },
                ]
              }
             ],
            '/en/usage/': [
               {
                 text: 'Usage',
                 items: [
                   { text: 'Configuration', link: '/en/usage/configuration' },
                   { text: 'Features', link: '/en/usage/features' },
                   { text: 'Pricing', link: '/en/usage/pricing' },
                   { text: 'API', link: '/en/usage/api' },
                 ]
               }
            ],
             '/en/faq/': [
               {
                 text: 'FAQ',
                 items: [
                   { text: 'FAQ', link: '/en/faq/index' },
                 ]
               }
             ],
             '/en/about/': [
               {
                 text: 'About',
                 items: [
                   { text: 'About Us', link: '/en/about/index' },
                 ]
               }
             ],
            '/en/': [
              {
                text: 'Guide',
                items: [
                  { text: 'Introduction', link: '/en/guide/intro' },
                  { text: 'Quick Start', link: '/en/guide/quick-start' },
                ]
              }
            ]
        },
        docFooter: {
          prev: 'Previous',
          next: 'Next'
        },
        outline: {
          level: 'deep',
          label: 'On this page'
        }
      }
    }
  },

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'DarkVision-LPR',
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Auroral0810/DarkVision-LPR' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 DarkVision-LPR Team'
    },

    search: {
      provider: 'local'
    }
  }
})

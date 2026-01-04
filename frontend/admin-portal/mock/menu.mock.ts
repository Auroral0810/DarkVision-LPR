import { defineMock } from "./base";

export default defineMock([
  // 1. 获取菜单路由
  {
    url: "menus/routes",
    method: ["GET"],
    body: {
      code: "00000",
      data: [
        {
          path: "/dashboard",
          component: "Layout",
          redirect: "/dashboard/overview",
          name: "Dashboard",
          meta: { title: "仪表盘", icon: "homepage", hidden: false, alwaysShow: true },
          children: [
            { path: "overview", component: "dashboard/index", name: "Overview", meta: { title: "概览", icon: "el-icon-House" } },
          ],
        },
        {
          path: "/user",
          component: "Layout",
          redirect: "/user/list",
          name: "UserMgmt",
          meta: { title: "用户管理", icon: "user", hidden: false, alwaysShow: true },
          children: [
            { path: "list", component: "user-mgmt/UserList", name: "UserList", meta: { title: "用户列表", icon: "el-icon-User" } },
            { path: "status", component: "error/Placeholder", name: "UserStatus", meta: { title: "账户状态", icon: "el-icon-Warning" } },
            { path: "verification", component: "user-mgmt/VerificationReview", name: "Verification", meta: { title: "实名认证审核", icon: "el-icon-Checked" } },
          ],
        },
        {
          path: "/permission",
          component: "Layout",
          redirect: "/permission/role",
          name: "PermMgmt",
          meta: { title: "权限管理", icon: "el-icon-Lock", hidden: false, alwaysShow: true },
          children: [
            { path: "role", component: "perm/RoleList", name: "RoleList", meta: { title: "角色管理", icon: "role" } },
            { path: "management", component: "error/Placeholder", name: "PermissionMgmt", meta: { title: "权限管理", icon: "el-icon-Key" } },
            { path: "admin", component: "perm/AdminList", name: "AdminList", meta: { title: "管理员账户", icon: "el-icon-Setting" } },
          ],
        },
        {
          path: "/recognition",
          component: "Layout",
          redirect: "/recognition/tasks",
          name: "Recognition",
          meta: { title: "识别服务", icon: "monitor", hidden: false, alwaysShow: true },
          children: [
            { path: "tasks", component: "recognition/TaskMonitor", name: "TaskMonitor", meta: { title: "任务监控", icon: "el-icon-VideoPlay" } },
            { path: "records", component: "recognition/RecordManagement", name: "RecordMgmt", meta: { title: "识别记录", icon: "document" } },
            { path: "models", component: "recognition/ModelManagement", name: "ModelMgmt", meta: { title: "模型管理", icon: "el-icon-Cpu" } },
          ],
        },
        {
          path: "/content",
          component: "Layout",
          redirect: "/content/site",
          name: "Content",
          meta: { title: "内容管理", icon: "document", hidden: false, alwaysShow: true },
          children: [
            { path: "site", component: "content/ContentMgmt", name: "SiteContent", meta: { title: "官网内容", icon: "el-icon-Monitor" } },
            { path: "docs", component: "error/Placeholder", name: "DocMgmt", meta: { title: "文档管理", icon: "el-icon-Notebook" } },
            { path: "announcement", component: "error/Placeholder", name: "AnnounceMgmt", meta: { title: "公告管理", icon: "el-icon-Bell" } },
            { path: "faq", component: "error/Placeholder", name: "FaqMgmt", meta: { title: "FAQ管理", icon: "el-icon-QuestionFilled" } },
          ],
        },
        {
          path: "/finance",
          component: "Layout",
          redirect: "/finance/orders",
          name: "Finance",
          meta: { title: "订单财务", icon: "el-icon-Money", hidden: false, alwaysShow: true },
          children: [
            { path: "orders", component: "finance/FinanceMgmt", name: "OrderMgmt", meta: { title: "订单管理", icon: "el-icon-Wallet" } },
            { path: "packages", component: "error/Placeholder", name: "PackageMgmt", meta: { title: "套餐管理", icon: "el-icon-Present" } },
            { path: "reports", component: "error/Placeholder", name: "FinanceReport", meta: { title: "财务报表", icon: "el-icon-DataAnalysis" } },
          ],
        },
        {
          path: "/statistics",
          component: "Layout",
          redirect: "/statistics/user",
          name: "Statistics",
          meta: { title: "数据统计", icon: "el-icon-DataAnalysis", hidden: false, alwaysShow: true },
          children: [
            { path: "user", component: "analytics/UserStats", name: "UserStats", meta: { title: "用户统计", icon: "user" } },
            { path: "recognition", component: "analytics/RecognitionStats", name: "RecogStats", meta: { title: "识别统计", icon: "el-icon-Search" } },
            { path: "system", component: "analytics/SystemMonitor", name: "SystemMonitor", meta: { title: "系统性能", icon: "el-icon-Odometer" } },
            { path: "board", component: "analytics/Overview", name: "BusinessBoard", meta: { title: "业务看板", icon: "homepage" } },
          ],
        },
        {
          path: "/log",
          component: "Layout",
          redirect: "/log/operation",
          name: "LogMgmt",
          meta: { title: "日志安全", icon: "el-icon-Warning", hidden: false, alwaysShow: true },
          children: [
            { path: "operation", component: "error/Placeholder", name: "OpLog", meta: { title: "操作日志", icon: "el-icon-Document" } },
            { path: "system", component: "error/Placeholder", name: "SysLog", meta: { title: "系统日志", icon: "el-icon-Warning" } },
            { path: "security", component: "security/SecurityMgmt", name: "SecurityMgmt", meta: { title: "安全管理", icon: "lock" } },
          ],
        },
        {
          path: "/message",
          component: "Layout",
          redirect: "/message/push",
          name: "Message",
          meta: { title: "消息通知", icon: "message", hidden: false, alwaysShow: true },
          children: [
            { path: "push", component: "messaging/Messaging", name: "MsgPush", meta: { title: "消息推送", icon: "el-icon-ChatDotRound" } },
            { path: "service", component: "error/Placeholder", name: "ServiceMgmt", meta: { title: "客服管理", icon: "el-icon-Service" } },
          ],
        },
        {
          path: "/setting",
          component: "Layout",
          redirect: "/setting/base",
          name: "Setting",
          meta: { title: "系统设置", icon: "setting", hidden: false, alwaysShow: true },
          children: [
            { path: "base", component: "config/SystemConfig", name: "BaseConfig", meta: { title: "基础配置", icon: "setting" } },
            { path: "params", component: "error/Placeholder", name: "RecogParams", meta: { title: "识别参数", icon: "el-icon-Operation" } },
            { path: "quotas", component: "error/Placeholder", name: "UserQuotas", meta: { title: "用户限额", icon: "el-icon-Histogram" } },
            { path: "email-sms", component: "error/Placeholder", name: "EmailSms", meta: { title: "邮件短信", icon: "el-icon-Postcard" } },
            { path: "external", component: "external/ExternalService", name: "ExternalService", meta: { title: "第三方服务", icon: "connection" } },
            { path: "backup", component: "maintenance/Maintenance", name: "BackupRecover", meta: { title: "备份恢复", icon: "el-icon-Collection" } },
            { path: "maintenance", component: "error/Placeholder", name: "SysMaintenance", meta: { title: "系统维护", icon: "cpu" } },
          ],
        },
      ],
      msg: "一切ok",
    },
  },

  // 2. 获取菜单树
  {
    url: "menus",
    method: ["GET"],
    body: {
      code: "00000",
      data: [
        { id: 1, parentId: 0, name: "仪表盘", type: "CATALOG", routeName: "Dashboard", routePath: "/dashboard", component: "Layout", sort: 1, visible: 1, icon: "homepage", children: [
          { id: 11, parentId: 1, name: "概览", type: "MENU", routeName: "Overview", routePath: "overview", component: "dashboard/index", sort: 1, visible: 1, icon: "el-icon-House" }
        ]},
        { id: 2, parentId: 0, name: "用户管理", type: "CATALOG", routeName: "UserMgmt", routePath: "/user", component: "Layout", sort: 2, visible: 1, icon: "user", children: [
          { id: 21, parentId: 2, name: "用户列表", type: "MENU", routeName: "UserList", routePath: "list", component: "user-mgmt/UserList", sort: 1, visible: 1, icon: "el-icon-User" },
          { id: 22, parentId: 2, name: "账户状态", type: "MENU", routeName: "UserStatus", routePath: "status", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Warning" },
          { id: 23, parentId: 2, name: "实名认证审核", type: "MENU", routeName: "Verification", routePath: "verification", component: "user-mgmt/VerificationReview", sort: 3, visible: 1, icon: "el-icon-Checked" }
        ]},
        { id: 3, parentId: 0, name: "权限管理", type: "CATALOG", routeName: "PermMgmt", routePath: "/permission", component: "Layout", sort: 3, visible: 1, icon: "lock", children: [
          { id: 31, parentId: 3, name: "角色管理", type: "MENU", routeName: "RoleList", routePath: "role", component: "perm/RoleList", sort: 1, visible: 1, icon: "role" },
          { id: 32, parentId: 3, name: "权限管理", type: "MENU", routeName: "PermissionMgmt", routePath: "management", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Key" },
          { id: 33, parentId: 3, name: "管理员账户", type: "MENU", routeName: "AdminList", routePath: "admin", component: "perm/AdminList", sort: 3, visible: 1, icon: "el-icon-Setting" }
        ]},
        { id: 4, parentId: 0, name: "识别服务", type: "CATALOG", routeName: "Recognition", routePath: "/recognition", component: "Layout", sort: 4, visible: 1, icon: "monitor", children: [
          { id: 41, parentId: 4, name: "任务监控", type: "MENU", routeName: "TaskMonitor", routePath: "tasks", component: "recognition/TaskMonitor", sort: 1, visible: 1, icon: "el-icon-VideoPlay" },
          { id: 42, parentId: 4, name: "识别记录", type: "MENU", routeName: "RecordMgmt", routePath: "records", component: "recognition/RecordManagement", sort: 2, visible: 1, icon: "document" },
          { id: 43, parentId: 4, name: "模型管理", type: "MENU", routeName: "ModelMgmt", routePath: "models", component: "recognition/ModelManagement", sort: 3, visible: 1, icon: "el-icon-Cpu" }
        ]},
        { id: 5, parentId: 0, name: "内容管理", type: "CATALOG", routeName: "Content", routePath: "/content", component: "Layout", sort: 5, visible: 1, icon: "document", children: [
          { id: 51, parentId: 5, name: "官网内容", type: "MENU", routeName: "SiteContent", routePath: "site", component: "content/ContentMgmt", sort: 1, visible: 1, icon: "el-icon-Monitor" },
          { id: 52, parentId: 5, name: "文档管理", type: "MENU", routeName: "DocMgmt", routePath: "docs", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Notebook" },
          { id: 53, parentId: 5, name: "公告管理", type: "MENU", routeName: "AnnounceMgmt", routePath: "announcement", component: "error/Placeholder", sort: 3, visible: 1, icon: "el-icon-Bell" },
          { id: 54, parentId: 5, name: "FAQ管理", type: "MENU", routeName: "FaqMgmt", routePath: "faq", component: "error/Placeholder", sort: 4, visible: 1, icon: "el-icon-QuestionFilled" }
        ]},
        { id: 6, parentId: 0, name: "订单财务", type: "CATALOG", routeName: "Finance", routePath: "/finance", component: "Layout", sort: 6, visible: 1, icon: "money", children: [
          { id: 61, parentId: 6, name: "订单管理", type: "MENU", routeName: "OrderMgmt", routePath: "orders", component: "finance/FinanceMgmt", sort: 1, visible: 1, icon: "el-icon-Wallet" },
          { id: 62, parentId: 6, name: "套餐管理", type: "MENU", routeName: "PackageMgmt", routePath: "packages", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Present" },
          { id: 63, parentId: 6, name: "财务报表", type: "MENU", routeName: "FinanceReport", routePath: "reports", component: "error/Placeholder", sort: 3, visible: 1, icon: "el-icon-DataAnalysis" }
        ]},
        { id: 7, parentId: 0, name: "数据统计", type: "CATALOG", routeName: "Statistics", routePath: "/statistics", component: "Layout", sort: 7, visible: 1, icon: "data-analysis", children: [
          { id: 71, parentId: 7, name: "用户统计", type: "MENU", routeName: "UserStats", routePath: "user", component: "analytics/UserStats", sort: 1, visible: 1, icon: "user" },
          { id: 72, parentId: 7, name: "识别统计", type: "MENU", routeName: "RecogStats", routePath: "recognition", component: "analytics/RecognitionStats", sort: 2, visible: 1, icon: "el-icon-Search" },
          { id: 73, parentId: 7, name: "系统性能", type: "MENU", routeName: "SystemMonitor", routePath: "system", component: "analytics/SystemMonitor", sort: 3, visible: 1, icon: "el-icon-Odometer" },
          { id: 74, parentId: 7, name: "业务看板", type: "MENU", routeName: "BusinessBoard", routePath: "board", component: "analytics/Overview", sort: 4, visible: 1, icon: "homepage" }
        ]},
        { id: 8, parentId: 0, name: "日志安全", type: "CATALOG", routeName: "LogMgmt", routePath: "/log", component: "Layout", sort: 8, visible: 1, icon: "warning", children: [
          { id: 81, parentId: 8, name: "操作日志", type: "MENU", routeName: "OpLog", routePath: "operation", component: "error/Placeholder", sort: 1, visible: 1, icon: "el-icon-Document" },
          { id: 82, parentId: 8, name: "系统日志", type: "MENU", routeName: "SysLog", routePath: "system", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Warning" },
          { id: 83, parentId: 8, name: "安全管理", type: "MENU", routeName: "SecurityMgmt", routePath: "security", component: "security/SecurityMgmt", sort: 3, visible: 1, icon: "lock" }
        ]},
        { id: 9, parentId: 0, name: "消息通知", type: "CATALOG", routeName: "Message", routePath: "/message", component: "Layout", sort: 9, visible: 1, icon: "message", children: [
          { id: 91, parentId: 9, name: "消息推送", type: "MENU", routeName: "MsgPush", routePath: "push", component: "messaging/Messaging", sort: 1, visible: 1, icon: "el-icon-ChatDotRound" },
          { id: 92, parentId: 9, name: "客服管理", type: "MENU", routeName: "ServiceMgmt", routePath: "service", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Service" }
        ]},
        { id: 10, parentId: 0, name: "系统设置", type: "CATALOG", routeName: "Setting", routePath: "/setting", component: "Layout", sort: 10, visible: 1, icon: "setting", children: [
          { id: 101, parentId: 10, name: "基础配置", type: "MENU", routeName: "BaseConfig", routePath: "base", component: "config/SystemConfig", sort: 1, visible: 1, icon: "setting" },
          { id: 102, parentId: 10, name: "识别参数", type: "MENU", routeName: "RecogParams", routePath: "params", component: "error/Placeholder", sort: 2, visible: 1, icon: "el-icon-Operation" },
          { id: 103, parentId: 10, name: "用户限额", type: "MENU", routeName: "UserQuotas", routePath: "quotas", component: "error/Placeholder", sort: 3, visible: 1, icon: "el-icon-Histogram" },
          { id: 104, parentId: 10, name: "邮件短信", type: "MENU", routeName: "EmailSms", routePath: "email-sms", component: "error/Placeholder", sort: 4, visible: 1, icon: "el-icon-Postcard" },
          { id: 105, parentId: 10, name: "第三方服务", type: "MENU", routeName: "ExternalService", routePath: "external", component: "external/ExternalService", sort: 5, visible: 1, icon: "connection" },
          { id: 106, parentId: 10, name: "备份恢复", type: "MENU", routeName: "BackupRecover", routePath: "backup", component: "maintenance/Maintenance", sort: 6, visible: 1, icon: "el-icon-Collection" },
          { id: 107, parentId: 10, name: "系统维护", type: "MENU", routeName: "SysMaintenance", routePath: "maintenance", component: "error/Placeholder", sort: 7, visible: 1, icon: "cpu" }
        ]}
      ],
      msg: "OK"
    }
  },

  // 3. 获取菜单下拉选项
  {
    url: "menus/options",
    method: ["GET"],
    body: {
      code: "00000",
      data: [
        { value: 1, label: "仪表盘" },
        { value: 2, label: "用户管理" },
        { value: 3, label: "权限管理" },
        { value: 4, label: "识别服务" },
        { value: 5, label: "内容管理" },
        { value: 6, label: "订单财务" },
        { value: 7, label: "数据统计" },
        { value: 8, label: "日志安全" },
        { value: 9, label: "消息通知" },
        { value: 10, label: "系统设置" },
      ],
      msg: "OK"
    }
  },

  // 4. CRUD 占位 (为了不破坏 API 稳定性)
  { url: "menus", method: ["POST"], body: { code: "00000", data: null, msg: "新增成功" } },
  { url: "menus/:id/form", method: ["GET"], body: { code: "00000", data: {}, msg: "OK" } },
  { url: "menus/:id", method: ["PUT"], body: { code: "00000", data: null, msg: "修改成功" } },
  { url: "menus/:id", method: ["DELETE"], body: { code: "00000", data: null, msg: "删除成功" } }
]);

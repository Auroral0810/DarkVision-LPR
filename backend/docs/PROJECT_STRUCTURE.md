# DarkVision-LPR 后端项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI 应用入口
│   ├── config.py                    # 配置文件
│   │
│   ├── core/                        # 核心模块
│   │   ├── __init__.py
│   │   ├── cache.py                 # Redis 缓存
│   │   ├── codes.py                 # ✨ 状态码定义
│   │   ├── database.py              # 数据库连接
│   │   ├── exceptions.py            # ✨ 自定义异常
│   │   ├── logger.py                # 日志配置
│   │   ├── response.py              # ✨ 响应工具
│   │   └── security.py              # 安全工具（JWT、密码）
│   │
│   ├── models/                      # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py                  # 用户模型
│   │   ├── order.py                 # 订单模型
│   │   ├── recognition.py           # 识别记录模型
│   │   ├── content.py               # 内容模型
│   │   ├── permission.py            # 权限模型
│   │   ├── system.py                # 系统配置模型
│   │   └── team.py                  # 团队模型
│   │
│   ├── schemas/                     # Pydantic 数据验证
│   │   ├── __init__.py
│   │   ├── user.py                  # 用户 Schema
│   │   ├── order.py                 # 订单 Schema
│   │   ├── recognition.py           # 识别 Schema
│   │   ├── response.py              # 响应 Schema
│   │   └── team.py                  # 团队 Schema
│   │
│   ├── services/                    # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth.py                  # ✨ 认证服务（已更新）
│   │   ├── user.py                  # 用户服务
│   │   ├── order.py                 # 订单服务
│   │   ├── recognition.py           # 识别服务
│   │   ├── email.py                 # 邮件服务
│   │   ├── sms.py                   # 短信服务
│   │   └── storage.py               # 存储服务
│   │
│   ├── api/                         # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py                  # 依赖注入
│   │   ├── v1/                      # API v1 版本
│   │   │   ├── __init__.py
│   │   │   ├── router.py            # 路由聚合
│   │   │   ├── auth.py              # ✨ 认证接口（已更新）
│   │   │   ├── user.py              # 用户接口
│   │   │   ├── recognition.py       # 识别接口
│   │   │   ├── order.py             # 订单接口
│   │   │   ├── upload.py            # 上传接口
│   │   │   ├── team.py              # 团队接口
│   │   │   └── dashboard.py         # 仪表板接口
│   │   │
│   │   └── admin/                   # 管理后台 API
│   │       ├── __init__.py
│   │       ├── users.py             # 用户管理
│   │       ├── content.py           # 内容管理
│   │       ├── finance.py           # 财务管理
│   │       ├── permissions.py       # 权限管理
│   │       ├── recognition.py       # 识别管理
│   │       ├── statistics.py        # 统计分析
│   │       └── system.py            # 系统设置
│   │
│   ├── middleware/                  # 中间件
│   │   ├── __init__.py
│   │   ├── auth.py                  # 认证中间件
│   │   ├── error_handler.py         # ✨ 异常处理（新增）
│   │   ├── logging.py               # 日志中间件
│   │   └── rate_limit.py            # 限流中间件
│   │
│   └── utils/                       # 工具函数
│       ├── __init__.py
│       ├── decorators.py            # 装饰器
│       ├── helpers.py               # 辅助函数
│       └── validators.py            # 验证器
│
├── scripts/                         # 脚本工具
│   ├── create_admin.py              # 创建管理员
│   ├── init_db.py                   # 初始化数据库
│   └── migrate_data.py              # 数据迁移
│
├── tests/                           # 测试
│   ├── __init__.py
│   ├── conftest.py                  # pytest 配置
│   ├── test_api/                    # API 测试
│   ├── test_services/               # 服务测试
│   └── test_utils/                  # 工具测试
│
├── alembic/                         # 数据库迁移
│   ├── versions/                    # 迁移版本
│   └── env.py                       # 迁移环境
│
├── docs/                            # ✨ 文档（新增）
│   ├── STATUS_CODE_GUIDE.md         # 状态码完整指南
│   ├── CODE_CHEATSHEET.md           # 状态码速查表
│   ├── STATUS_CODE_SUMMARY.md       # 系统总结
│   └── PROJECT_STRUCTURE.md         # 项目结构（本文件）
│
├── .env                             # 环境变量（需创建）
├── .gitignore                       # ✨ Git 忽略（新增）
├── alembic.ini                      # Alembic 配置
├── requirements.txt                 # 依赖包
├── requirements-dev.txt             # 开发依赖
│
├── start.sh                         # ✨ 启动脚本（新增）
├── export_openapi.py                # ✨ 导出 API 规范（新增）
├── export_api.sh                    # ✨ 导出脚本（新增）
│
├── CHANGELOG.md                     # ✨ 更新日志（新增）
├── README_STARTUP.md                # ✨ 启动指南（新增）
└── APIFOX_IMPORT_GUIDE.md          # ✨ Apifox 导入指南（新增）
```

---

## 文件说明

### ✨ 新增文件（本次更新）

#### 核心模块
- **app/core/codes.py** - 统一状态码定义（40+ 个业务状态码）
- **app/core/response.py** - 响应工具函数
- **app/core/exceptions.py** - 自定义异常类（40+ 个）
- **app/middleware/error_handler.py** - 全局异常处理器

#### 文档
- **docs/STATUS_CODE_GUIDE.md** - 状态码完整使用指南
- **docs/CODE_CHEATSHEET.md** - 快速参考卡片
- **docs/STATUS_CODE_SUMMARY.md** - 系统总结
- **docs/PROJECT_STRUCTURE.md** - 项目结构（本文件）

#### 工具脚本
- **start.sh** - 快速启动服务器
- **export_openapi.py** - 导出 OpenAPI 规范（JSON/YAML）
- **export_api.sh** - 导出脚本（支持多种方式）
- **.gitignore** - Git 忽略文件

#### 说明文档
- **CHANGELOG.md** - 更新日志
- **README_STARTUP.md** - 启动和使用指南
- **APIFOX_IMPORT_GUIDE.md** - Apifox 导入指南

### ✏️ 已更新文件

- **app/main.py** - 注册全局异常处理器
- **app/services/auth.py** - 使用新的异常系统
- **app/api/v1/auth.py** - 使用统一响应格式

---

## 目录职责

| 目录 | 职责 | 说明 |
|------|------|------|
| **core/** | 核心功能 | 数据库、缓存、安全、状态码、异常 |
| **models/** | 数据模型 | SQLAlchemy ORM 模型 |
| **schemas/** | 数据验证 | Pydantic 模型，用于请求/响应 |
| **services/** | 业务逻辑 | 具体的业务实现 |
| **api/** | API 路由 | FastAPI 路由和端点 |
| **middleware/** | 中间件 | 请求/响应拦截处理 |
| **utils/** | 工具函数 | 通用辅助函数 |
| **scripts/** | 脚本工具 | 数据库初始化、管理员创建等 |
| **tests/** | 测试代码 | 单元测试、集成测试 |
| **docs/** | 项目文档 | 使用指南、API 文档 |

---

## 分层架构

```
┌─────────────────────────────────────┐
│         API Layer (api/)            │  ← FastAPI 路由和端点
│  - 参数验证                         │
│  - 权限检查                         │
│  - 返回响应                         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      Service Layer (services/)      │  ← 业务逻辑
│  - 业务规则                         │
│  - 数据处理                         │
│  - 抛出异常                         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│       Model Layer (models/)         │  ← 数据持久化
│  - ORM 模型                         │
│  - 数据库操作                       │
└─────────────────────────────────────┘

          ↕ (middleware/)              ← 中间件拦截

┌─────────────────────────────────────┐
│         Core (core/)                │  ← 核心功能
│  - 数据库连接                       │
│  - Redis 缓存                       │
│  - JWT 认证                         │
│  - 状态码系统                       │
│  - 异常处理                         │
└─────────────────────────────────────┘
```

---

## 数据流向

### 请求处理流程

```
1. 客户端请求
   ↓
2. Middleware (日志、限流、认证)
   ↓
3. API Layer (路由匹配、参数验证)
   ↓
4. Service Layer (业务逻辑、数据处理)
   ↓
5. Model Layer (数据库操作)
   ↓
6. Service Layer (返回结果或抛出异常)
   ↓
7. API Layer (返回统一响应)
   ↓
8. Exception Handler (捕获异常，返回错误响应)
   ↓
9. 客户端响应
```

### 示例：用户注册

```
POST /api/v1/auth/register
    ↓
AuthMiddleware (跳过，注册不需要认证)
    ↓
auth.register() [API Layer]
    ↓
register_user() [Service Layer]
    ├─ 检查手机号 → PhoneExistedException? → 返回 40202
    ├─ 检查昵称 → NicknameExistedException? → 返回 40204
    ├─ 创建用户 [Model Layer]
    └─ 返回 User 对象
    ↓
success_created() [Response Tool]
    ↓
返回 {"code": 20001, "message": "注册成功", "data": {...}}
```

---

## 状态码系统集成位置

```
core/
├── codes.py           ← 定义所有状态码
├── exceptions.py      ← 定义异常类
└── response.py        ← 响应工具函数

middleware/
└── error_handler.py   ← 全局异常捕获

services/
└── *.py              ← 抛出异常

api/
└── *.py              ← 使用响应工具
```

---

## 快速导航

- 📖 [启动指南](README_STARTUP.md)
- 📋 [状态码指南](docs/STATUS_CODE_GUIDE.md)
- 🚀 [Apifox 导入](APIFOX_IMPORT_GUIDE.md)
- 📝 [更新日志](CHANGELOG.md)

---

**最后更新**: 2026-01-05


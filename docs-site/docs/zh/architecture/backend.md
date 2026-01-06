# 后端架构

后端服务基于 **Python** 生态构建，充分利用其在 AI 领域的优势，实现业务逻辑与模型推理的无缝衔接。

## 技术选型

| 技术 | 选型 | 作用 |
| :--- | :--- | :--- |
| **Web 框架** | FastAPI | 高性能异步 ASGI 框架，自动生成文档 |
| **语言版本** | Python 3.10+ | 利用最新的异步特性与类型提示 |
| **服务器** | Uvicorn | 生产级 ASGI 服务器实现 |
| **ORM** | SQLAlchemy 2.0 | 现代化的异步数据库映射工具 |
| **数据验证** | Pydantic 2.0 | 强大的数据解析与验证库 |
| **认证** | PyJWT (OAuth2) | 标准化的无状态身份验证 |
| **数据库迁移** | Alembic | 版本化的数据库结构变更管理 |
| **任务队列** | Celery / Redis Queue | 处理耗时任务（如视频分析） |

## 核心模块

### 1. API 接口模块 (app/api)
遵循 RESTful 规范，提供版本化的接口服务（`/api/v1/...`）。
- **Deps**: 统一的依赖注入系统（数据库会话、当前用户、权限校验）。

### 2. 业务服务层 (app/services)
封装具体业务逻辑，避免 Controller 层过于臃肿。
- `RecognitionService`: 处理识别流程，调用推理引擎。
- `AuthService`: 处理登录、注册、令牌刷新。
- `AnalysisService`: 处理数据报表聚合计算。

### 3. 实时通信
利用 FastAPI 的 **WebSocket** 支持，实现识别进度的实时全双工推送。
- 状态流转：`Uploading` -> `Detecting` -> `Enhancing` -> `Recognizing` -> `Completed`

## 性能优化
- **异步 I/O**: 全程使用 `async/await` 处理 I/O 密集型操作（数据库、网络请求）。
- **连接池**: 数据库与 Redis 均配置连接池，复用连接资源。
- **缓存策略**: 对高频读取且不常变更的数据（如配置、用户信息）使用 Redis 缓存。

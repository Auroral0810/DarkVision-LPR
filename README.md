<div align="center">
  <h1>🌙 暗视 · 低光照车牌识别系统</h1>
  <h3>DarkVision-LPR</h3>
  <p>基于 YOLOv12 与 Retinex 图像增强的低光照条件下车牌识别系统</p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
  [![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)
</div>

---

## 📋 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [功能模块](#功能模块)
- [部署指南](#部署指南)
- [开发文档](#开发文档)
- [贡献指南](#贡献指南)
- [许可证](#许可证)
- [联系我们](#联系我们)

---

## 🎯 项目简介

**DarkVision-LPR** 是一个专为低光照环境设计的智能车牌识别系统。通过结合先进的深度学习技术和图像增强算法，系统能够在夜间、隧道、地下停车场等极端低光照场景下实现高精度的车牌检测与识别。

### 论文标题
**基于YOLOv12与Retinex图像增强的低光照条件下车牌识别系统设计与优化**

### 应用场景
- 🚗 智能停车场管理
- 🛣️ 高速公路收费系统
- 🏙️ 城市交通监控
- 🔒 小区安防系统
- 🚓 公安交警执法

---

## ✨ 核心特性

### 🎨 图像增强
- ✅ **Multi-Scale Retinex (MSR)** - 多尺度图像增强
- ✅ **CLAHE** - 自适应直方图均衡化
- ✅ **动态参数调整** - 根据光照条件自动优化
- ✅ **实时处理** - 毫秒级响应速度

### 🎯 车牌识别
- ✅ **YOLOv12 目标检测** - 最新版本的 YOLO 架构
- ✅ **高精度识别** - 准确率 > 95%
- ✅ **多车牌类型** - 支持蓝牌、黄牌、绿牌等
- ✅ **批量处理** - 支持图片/视频批量识别

### 🌐 多端支持
- ✅ **Web 端** - 跨平台浏览器访问
- ✅ **桌面端** - Windows/macOS/Linux 客户端
- ✅ **移动端** - iOS/Android App（开发中）
- ✅ **小程序** - 微信小程序（规划中）

### 🔐 安全可靠
- ✅ **JWT 身份认证** - 安全的用户认证机制
- ✅ **RBAC 权限控制** - 细粒度权限管理
- ✅ **数据加密** - 传输与存储双重加密
- ✅ **操作审计** - 完整的操作日志记录

### 📊 数据分析
- ✅ **实时统计** - 识别数据实时展示
- ✅ **可视化报表** - 多维度数据分析
- ✅ **趋势分析** - 识别效果趋势预测
- ✅ **异常检测** - 智能异常车牌识别

---

## 🏗️ 技术架构

### 整体架构
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  前端展示层  │────▶│  后端业务层  │────▶│ AI推理服务层 │────▶│  数据存储层  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### 技术栈

#### 前端技术
| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.x | 前端框架 |
| TypeScript | 5.x | 类型系统 |
| Vite | 5.x | 构建工具 |
| Element Plus | 2.x | UI 组件库 |
| Pinia | 2.x | 状态管理 |
| Vue Router | 4.x | 路由管理 |
| Axios | 1.x | HTTP 客户端 |
| Vue I18n | 9.x | 国际化 |
| ECharts | 5.x | 数据可视化 |

#### 后端技术
| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.9+ | 编程语言 |
| FastAPI | 0.100+ | Web 框架 |
| Uvicorn | 0.23+ | ASGI 服务器 |
| SQLAlchemy | 2.0+ | ORM 框架 |
| Alembic | 1.12+ | 数据库迁移 |
| Pydantic | 2.0+ | 数据验证 |
| PyJWT | 2.8+ | JWT 认证 |
| Loguru | 0.7+ | 日志系统 |

#### AI 服务
| 技术 | 版本 | 用途 |
|------|------|------|
| PyTorch | 2.0+ | 深度学习框架 |
| YOLOv12 | Latest | 目标检测模型 |
| OpenCV | 4.8+ | 图像处理 |
| NumPy | 1.24+ | 数值计算 |
| Pillow | 10.0+ | 图像处理 |

#### 数据库
| 技术 | 版本 | 用途 |
|------|------|------|
| MySQL | 8.0+ | 关系型数据库 |
| Redis | 7.0+ | 缓存数据库 |
| MinIO | Latest | 对象存储 |
| 阿里云 OSS | - | 云端存储 |

#### 部署运维
| 技术 | 版本 | 用途 |
|------|------|------|
| Docker | Latest | 容器化 |
| Docker Compose | Latest | 容器编排 |
| Nginx | 1.24+ | 反向代理 |
| Kubernetes | 1.27+ | 容器编排（可选）|

---

## 🚀 快速开始

### 前置要求

确保你的开发环境满足以下要求：

- **Node.js**: >= 18.x (推荐 20.x)
- **Python**: >= 3.9
- **pnpm**: >= 8.x
- **MySQL**: >= 8.0
- **Redis**: >= 7.0
- **CUDA**: >= 11.8 (如需 GPU 加速)

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/your-username/DarkVision-LPR.git
cd DarkVision-LPR
```

#### 2. 安装前端依赖
```bash
# 官网前端
cd frontend/official-website
pnpm install
pnpm dev

# 用户端前端
cd ../user-portal
pnpm install
pnpm dev

# 管理员端前端
cd ../admin-portal
pnpm install
pnpm dev
```

#### 3. 安装后端依赖
```bash
cd ../../backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 创建管理员账户
python scripts/create_admin.py

# 启动后端服务
uvicorn app.main:app --reload --port 8000
```

#### 4. 安装 AI 推理服务
```bash
cd ../ai-service

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 下载预训练模型（根据文档说明）
# 放置模型文件到 models/yolov12/weights/

# 启动 AI 服务
uvicorn main:app --reload --port 8001
```

#### 5. 配置数据库
```bash
# 创建 MySQL 数据库
mysql -u root -p
CREATE DATABASE darkvision_lpr CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 启动 Redis
redis-server
```

#### 6. 配置环境变量
```bash
# 后端配置
cd backend
cp .env.example .env
# 编辑 .env 文件，填入数据库连接信息等

# 前端配置已在各项目中包含 .env.development
```

#### 7. 访问系统

- 官网: http://localhost:3000
- 用户端: http://localhost:3001
- 管理员端: http://localhost:3002
- 后端 API: http://localhost:8000/docs
- AI 服务 API: http://localhost:8001/docs

---

## 📁 项目结构
```
DarkVision-LPR/
├── frontend/                    # 前端项目
│   ├── official-website/       # 官网
│   ├── user-portal/            # 用户端
│   └── admin-portal/           # 管理员端
├── backend/                     # 后端服务
│   ├── app/                    # 应用主目录
│   │   ├── api/               # API 路由
│   │   ├── models/            # 数据模型
│   │   ├── schemas/           # Pydantic 模型
│   │   ├── services/          # 业务逻辑
│   │   └── core/              # 核心功能
│   └── alembic/               # 数据库迁移
├── ai-service/                  # AI 推理服务
│   ├── models/                 # 模型文件
│   ├── services/               # AI 服务
│   └── api/                    # API 接口
├── desktop-client/              # 桌面客户端 (Tauri)
├── mobile-app/                  # 移动端 (uni-app)
├── nginx/                       # Nginx 配置
├── deployment/                  # 部署配置
│   ├── docker/                 # Docker 文件
│   └── kubernetes/             # K8s 配置
└── docs/                        # 项目文档
```

详细的目录结构说明请参考 [项目结构文档](docs/architecture/project-structure.md)

---

## 🎮 功能模块

### 用户端功能

#### 普通用户 (FREE)
- ✅ 单张图片识别（20次/日）
- ✅ 识别历史记录（最近7天）
- ✅ 账户管理
- ✅ 实名认证（可选）

#### VIP 用户
- ✅ 批量图片识别（500次/日）
- ✅ 视频识别（10个/月）
- ✅ 实时摄像头识别
- ✅ 高精度模式
- ✅ API 调用（5000次/日）
- ✅ 数据分析报表
- ✅ 无限历史记录

#### 企业用户
- ✅ 无限识别次数
- ✅ 多账户管理（50个子账户）
- ✅ 团队协作
- ✅ 定制化模型训练
- ✅ 无限 API 调用
- ✅ 私有化部署
- ✅ 7×24 专属技术支持

### 管理员端功能

- 👥 **用户管理**: 用户信息、权限、实名认证审核
- 🔐 **权限管理**: 角色管理、权限分配、管理员账户
- 🎯 **识别服务**: 任务监控、识别记录、模型管理
- ⚙️ **系统配置**: 基础配置、识别参数、用户限额
- 📝 **内容管理**: 官网内容、文档、公告、FAQ
- 💰 **订单财务**: 订单管理、套餐配置、财务报表
- 📊 **统计分析**: 用户统计、识别统计、性能监控
- 📋 **日志安全**: 操作日志、系统日志、安全管理
- 💬 **消息通知**: 消息推送、客服管理
- 🔧 **系统维护**: 数据备份、缓存管理、任务调度

---

## 🐳 部署指南

### Docker 部署（推荐）
```bash
# 使用 Docker Compose 一键部署
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 手动部署

详细的部署步骤请参考：
- [生产环境部署指南](docs/deployment/production.md)
- [Docker 部署指南](docs/deployment/docker.md)
- [Kubernetes 部署指南](docs/deployment/kubernetes.md)

---

## 📚 开发文档

### API 文档
- [后端 API 文档](http://localhost:8000/docs)
- [AI 服务 API 文档](http://localhost:8001/docs)

### 技术文档
- [架构设计](docs/architecture/design.md)
- [数据库设计](docs/architecture/database.md)
- [前端开发指南](docs/development/frontend.md)
- [后端开发指南](docs/development/backend.md)
- [AI 模型训练](docs/development/ai-training.md)

### 用户文档
- [快速入门](docs/user-guide/quickstart.md)
- [功能使用手册](docs/user-guide/features.md)
- [常见问题 FAQ](docs/user-guide/faq.md)

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- **Python**: 遵循 PEP 8 规范
- **TypeScript/JavaScript**: 遵循 Airbnb 规范
- **Git Commit**: 遵循 Conventional Commits 规范

### 提交规范示例
```
feat: 添加视频批量识别功能
fix: 修复低光照下识别准确率问题
docs: 更新部署文档
style: 格式化代码
refactor: 重构图像增强模块
test: 添加单元测试
chore: 更新依赖版本
```

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 📞 联系我们

### 开发团队
- **项目负责人**: [Your Name]
- **技术支持**: support@darkvision-lpr.com
- **商务合作**: business@darkvision-lpr.com

### 社交媒体
- 🌐 官网: https://darkvision-lpr.com
- 📧 邮箱: contact@darkvision-lpr.com
- 💬 微信: DarkVision-LPR
- 🐦 Twitter: @DarkVisionLPR
- 📱 GitHub: https://github.com/your-org/DarkVision-LPR

### 问题反馈
- [GitHub Issues](https://github.com/your-org/DarkVision-LPR/issues)
- [讨论区](https://github.com/your-org/DarkVision-LPR/discussions)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=your-org/DarkVision-LPR&type=Date)](https://star-history.com/#your-org/DarkVision-LPR&Date)

---

## 📈 项目统计

![GitHub stars](https://img.shields.io/github/stars/your-org/DarkVision-LPR?style=social)
![GitHub forks](https://img.shields.io/github/forks/your-org/DarkVision-LPR?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/your-org/DarkVision-LPR?style=social)
![GitHub issues](https://img.shields.io/github/issues/your-org/DarkVision-LPR)
![GitHub pull requests](https://img.shields.io/github/issues-pr/your-org/DarkVision-LPR)
![GitHub last commit](https://img.shields.io/github/last-commit/your-org/DarkVision-LPR)

---

<div align="center">
  <p>Made with ❤️ by DarkVision-LPR Team</p>
  <p>© 2026 DarkVision-LPR. All rights reserved.</p>
</div>
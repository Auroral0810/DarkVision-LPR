# 快速上手

::: tip 提示
DarkVision-LPR 目前处于 v2.0 稳定版阶段。我们推荐使用 **Docker** 部署以获得最佳体验。
:::

## 在线试一试

你可以通过 [Demo 站点](http://demo.darkvision.com) (账号: `demo`, 密码: `demo`) 直接体验 DarkVision-LPR 的功能。

## 安装

### 依赖环境

- **Node.js v18.0+**
- **Python 3.10+** (推荐使用 Conda 管理环境)
- **MySQL 8.0+**

::: warning 注意
如果您计划使用 GPU 加速推理，请务必安装 CUDA 11.8+ 和对应版本的 PyTorch。
:::

### 创建项目

可以通过 Git 克隆代码库开始：

::: code-group
```bash [HTTPS]
git clone https://github.com/Auroral0810/DarkVision-LPR.git
```
```bash [SSH]
git clone git@github.com:Auroral0810/DarkVision-LPR.git
```
:::

## 开始使用

### 1. 启动数据库与 Redis

```bash
docker-compose up -d mysql redis
```

### 2. 启动后端服务

进入 `backend` 目录并在虚拟环境中安装依赖：

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. 启动前端服务

进入 `frontend/user-portal` 目录启动用户端：

```bash
cd frontend/user-portal
pnpm install
pnpm dev
```

恭喜！您已成功运行了 DarkVision-LPR。
- 深入了解 [系统架构](/architecture/overview)
- 查看 [API 文档](/usage/api)

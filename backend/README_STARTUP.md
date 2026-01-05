# DarkVision-LPR 后端启动指南

## 环境要求

- Python 3.10+
- MySQL 数据库
- Redis 服务器
- Conda 环境：DarkVision

## 快速启动

### 方式一：使用启动脚本（推荐）

```bash
cd backend
./start.sh
```

### 方式二：手动启动

```bash
cd backend
conda activate DarkVision
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 方式三：使用 conda run

```bash
cd backend
conda run -n DarkVision uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 访问地址

启动成功后，你可以访问：

- **API 文档 (Swagger UI)**: http://localhost:8000/docs
- **API 文档 (ReDoc)**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health
- **根路径**: http://localhost:8000/

## API 端点

### 认证相关

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户信息

## 测试 API

### 1. 注册用户

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "nickname": "testuser",
    "password": "123456",
    "email": "test@example.com"
  }'
```

### 2. 登录

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "password": "123456"
  }'
```

返回示例：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. 获取当前用户信息

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 环境配置

确保 `backend/.env` 文件包含正确的配置：

```env
SECRET_KEY=your-secret-key-change-in-production
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=darkvision_lpr
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 常见问题

### 1. ModuleNotFoundError

确保已安装所有依赖：
```bash
conda activate DarkVision
pip install -r requirements.txt
```

### 2. 数据库连接失败

- 检查 MySQL 服务是否启动
- 检查 `.env` 文件中的数据库配置
- 确保数据库 `darkvision_lpr` 已创建

### 3. Redis 连接失败

- 检查 Redis 服务是否启动：`redis-cli ping`
- 检查 `.env` 文件中的 Redis 配置

### 4. 端口被占用

如果 8000 端口被占用，可以更改端口：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 日志输出

启动时会看到类似的输出：

```
INFO:     Will watch for changes in these directories: ['/Users/.../backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 开发建议

1. 使用 `--reload` 参数自动重载代码更改
2. 开发时使用 Swagger UI 测试 API
3. 查看 `app/main.py` 中的路由注册
4. 错误会在终端中显示详细的 traceback

## 下一步

- 前往 http://localhost:8000/docs 查看完整的 API 文档
- 使用前端项目连接后端 API
- 根据需要添加更多的 API 端点


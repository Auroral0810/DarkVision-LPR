# Apifox 导入指南

## 🎯 三种导入方式

### 方式一：URL 导入（最简单，推荐）

1. **启动后端服务**
   ```bash
   cd backend
   ./start.sh
   ```

2. **在 Apifox 中导入**
   - 打开 Apifox
   - 点击「导入」→「导入数据」
   - 选择「URL 导入」
   - 输入 URL: `http://localhost:8000/openapi.json`
   - 点击「下一步」→「确认导入」

3. **优点**
   - 实时同步：每次导入都是最新的 API
   - 无需手动导出文件
   - 支持增量更新

---

### 方式二：文件导入（离线使用）

#### 步骤 1: 导出 OpenAPI 文件

**方法 A - 使用导出脚本（推荐）**
```bash
cd backend
./export_api.sh
```

**方法 B - 使用 Python 脚本**
```bash
cd backend
conda activate DarkVision
python export_openapi.py
```

**方法 C - 使用 curl（需要服务运行）**
```bash
# 确保服务正在运行
curl http://localhost:8000/openapi.json -o openapi.json
```

#### 步骤 2: 在 Apifox 中导入

1. 打开 Apifox
2. 点击「导入」→「导入数据」
3. 选择「OpenAPI/Swagger」格式
4. 选择「上传文件」
5. 选择 `openapi.json` 或 `openapi.yaml`
6. 点击「确认导入」

---

### 方式三：浏览器直接下载

1. 启动服务后访问: http://localhost:8000/openapi.json
2. 浏览器会显示 JSON 内容
3. 右键→「另存为」保存到本地
4. 在 Apifox 中导入该文件

---

## 📋 当前可用的 API 接口

### 认证模块 (Auth)

| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|---------|
| POST | `/api/v1/auth/register` | 用户注册 | ❌ |
| POST | `/api/v1/auth/login` | 用户登录 | ❌ |
| GET | `/api/v1/auth/me` | 获取当前用户信息 | ✅ |

---

## 🔧 Apifox 使用技巧

### 1. 设置环境变量

在 Apifox 中创建环境：

**本地开发环境**
```
baseUrl = http://localhost:8000
token = (登录后自动填充)
```

**测试环境**
```
baseUrl = http://test.darkvision.com
token = (登录后自动填充)
```

### 2. 配置认证

导入后，对于需要认证的接口：

1. 在接口详情中找到「认证」标签
2. 选择「Bearer Token」
3. Token 值使用环境变量: `{{token}}`
4. 或手动填入登录获取的 token

### 3. 自动刷新 Token

创建「前置操作」脚本（登录接口）：
```javascript
// 自动保存登录返回的 token
const response = pm.response.json();
if (response.access_token) {
    pm.environment.set("token", response.access_token);
    console.log("Token 已保存到环境变量");
}
```

### 4. 测试工作流

#### 注册 → 登录 → 获取用户信息

1. **注册用户**
   ```json
   POST /api/v1/auth/register
   {
     "phone": "13800138000",
     "nickname": "测试用户",
     "password": "123456",
     "email": "test@example.com"
   }
   ```

2. **登录**
   ```json
   POST /api/v1/auth/login
   {
     "phone": "13800138000",
     "password": "123456"
   }
   ```
   响应中的 `access_token` 会自动保存到环境变量

3. **获取用户信息**
   ```
   GET /api/v1/auth/me
   Authorization: Bearer {{token}}
   ```

---

## 🔄 更新 API 文档

当后端添加新接口时，重新导入即可：

### 增量更新（推荐）
1. 在 Apifox 中选择之前导入的项目
2. 点击「导入」→「导入数据」
3. 选择「覆盖模式」或「智能合并」
4. 导入最新的 OpenAPI 文件

### 完全重新导入
1. 删除旧的接口集合
2. 重新执行导入流程

---

## 📝 示例请求

### 1. 注册用户

```bash
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "phone": "13900139000",
  "nickname": "张三",
  "password": "password123",
  "email": "zhangsan@example.com"
}
```

### 2. 登录

```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "phone": "13900139000",
  "password": "password123"
}
```

响应：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. 获取当前用户

```bash
GET http://localhost:8000/api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

响应：
```json
{
  "id": 1,
  "phone": "13900139000",
  "nickname": "张三",
  "email": "zhangsan@example.com",
  "avatar_url": null,
  "user_type": "free",
  "status": "active",
  "created_at": "2026-01-05T10:30:00"
}
```

---

## ❓ 常见问题

### Q: 导入后看不到接口？
A: 检查导入设置，确保选择了「导入所有接口」，而不是「仅导入文档」。

### Q: 如何处理认证？
A: 
1. 先调用登录接口获取 token
2. 在 Apifox 环境变量中设置 token
3. 其他接口的 Header 中使用 `Authorization: Bearer {{token}}`

### Q: 更新接口后如何同步？
A: 重新运行导出脚本，然后在 Apifox 中重新导入，选择「智能合并」模式。

### Q: 支持哪些格式？
A: Apifox 支持：
- OpenAPI 3.0 (推荐，FastAPI 默认使用)
- Swagger 2.0
- Postman Collection
- HAR 格式

---

## 🎨 Apifox 高级功能

### 1. 自动化测试

创建测试用例，验证：
- 状态码是否正确
- 响应时间是否合理
- 返回数据格式是否正确
- 业务逻辑是否正确

### 2. Mock 数据

使用 Apifox 的 Mock 功能，在后端未完成时：
- 前端可以先进行开发
- 返回符合规范的假数据
- 加速前后端并行开发

### 3. 团队协作

- 共享 API 文档
- 在线查看和调试
- 版本控制
- 权限管理

---

## 📚 参考资源

- [Apifox 官方文档](https://www.apifox.cn/help/)
- [OpenAPI 规范](https://swagger.io/specification/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)

---

## 🔗 相关文件

- `export_openapi.py` - Python 导出脚本
- `export_api.sh` - Shell 导出脚本
- `README_STARTUP.md` - 后端启动指南


# 环境配置说明

## ✅ 问题已修复

### SQLAlchemy Enum 问题
**错误**: `LookupError: 'free' is not among the defined enum values`

**原因**: SQLAlchemy 的 Enum 默认期望枚举名（大写），但数据库存储的是枚举值（小写）

**解决方案**: 在 `app/models/user.py` 中配置 Enum 使用值而不是名称：
```python
Column(Enum(UserType, native_enum=False, values_callable=lambda obj: [e.value for e in obj]))
```

---

## 📝 配置文件说明

### 1. 创建 .env 文件

在 `backend/` 目录下创建 `.env` 文件（已在 `.gitignore` 中，不会提交到 Git）：

```env
# 项目配置
PROJECT_NAME=DarkVision-LPR
API_V1_PREFIX=/api/v1
SECRET_KEY=Lucky_ff0810
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=darkvision_lpr

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# CORS配置（根据你的README，前端端口为3000/3001/3002）
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:5173

# 邮件配置（使用你的163邮箱配置）
MAIL_HOST=smtp.163.com
MAIL_PORT=465
MAIL_USERNAME=15968588744@163.com
MAIL_PASSWORD=QSwPWYUaYmh32ggs
MAIL_FROM=15968588744@163.com
MAIL_FROM_NAME=DarkVision-LPR

# 短信配置（腾讯云 - 可选）
# SMS_SECRET_ID=your_secret_id
# SMS_SECRET_KEY=your_secret_key
# SMS_SDK_APP_ID=your_sdk_app_id
# SMS_SIGN_NAME=your_sign_name
# SMS_TEMPLATE_ID=your_template_id

# OSS配置（阿里云 - 可选）
# OSS_ENDPOINT=https://oss-cn-beijing.aliyuncs.com
# OSS_ACCESS_KEY_ID=LTAI5tCJAKHv96E4hYuhUEG4
# OSS_ACCESS_KEY_SECRET=RRxg1dBcF4rqB7uvKxyZm7L1kcdpbl
# OSS_BUCKET_NAME=big-event20040810

# 开发模式配置
DEBUG=true
RETURN_VERIFICATION_CODE=true
```

---

## 📧 邮件配置

### 已集成的邮件功能

1. ✅ **验证码邮件** - 精美的HTML模板
2. ✅ **欢迎邮件** - 注册成功自动发送
3. ✅ **密码重置邮件** - 带重置链接

### 邮件服务配置

使用你Java项目中的163邮箱配置：
- **SMTP服务器**: smtp.163.com
- **端口**: 465 (SSL)
- **用户名**: 15968588744@163.com
- **授权码**: QSwPWYUaYmh32ggs

**注意**: 
- 密码是授权码，不是邮箱登录密码
- 163邮箱需要开启SMTP服务并获取授权码

### 邮件模板

已创建三种精美的HTML邮件模板：

1. **验证码邮件** - 大号验证码，醒目提示
2. **欢迎邮件** - 介绍功能，引导使用
3. **密码重置邮件** - 安全提示，重置按钮

---

## 🔧 配置项说明

### 必需配置

| 配置项 | 说明 | 示例 |
|-------|------|------|
| MYSQL_* | 数据库配置 | 见上方 |
| REDIS_* | Redis配置 | 见上方 |
| SECRET_KEY | JWT密钥 | Lucky_ff0810 |

### 邮件配置（已配置）

| 配置项 | 说明 | 值 |
|-------|------|-----|
| MAIL_HOST | SMTP服务器 | smtp.163.com |
| MAIL_PORT | SMTP端口 | 465 |
| MAIL_USERNAME | 邮箱账号 | 15968588744@163.com |
| MAIL_PASSWORD | 邮箱授权码 | QSwPWYUaYmh32ggs |
| MAIL_FROM | 发件人邮箱 | 15968588744@163.com |
| MAIL_FROM_NAME | 发件人名称 | DarkVision-LPR |

### 可选配置

#### 短信服务（腾讯云）
如果需要真实短信验证码，配置以下项：
- `SMS_SECRET_ID`
- `SMS_SECRET_KEY`
- `SMS_SDK_APP_ID`
- `SMS_SIGN_NAME`
- `SMS_TEMPLATE_ID`

#### OSS存储（阿里云）
如果需要文件上传功能，配置以下项：
- `OSS_ENDPOINT`
- `OSS_ACCESS_KEY_ID`
- `OSS_ACCESS_KEY_SECRET`
- `OSS_BUCKET_NAME`

---

## 🚀 启动说明

### 1. 确保服务运行

```bash
# 启动 MySQL
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql

# 启动 Redis
# macOS: brew services start redis
# Linux: sudo systemctl start redis
```

### 2. 创建 .env 文件

复制上方完整的 `.env` 配置到 `backend/.env`

### 3. 启动后端

```bash
cd backend
./start.sh

# 或手动启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 测试登录

现在可以正常登录了！

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/phone" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "password": "password"
  }'
```

**注意**: 数据库中现有用户的密码哈希需要知道原始密码。常见的测试密码：
- `password`
- `123456`
- `secret`

---

## 📊 前端端口配置

根据你的 README.md：

| 服务 | 端口 | 说明 |
|-----|------|------|
| 官网 | 3000 | 官方网站 |
| 用户端 | 3001 | 用户门户 |
| 管理端 | 3002 | 管理后台 |
| 后端API | 8000 | FastAPI服务 |
| AI服务 | 8001 | AI识别服务 |

CORS已配置允许这些端口访问。

---

## ✅ 已完成的功能

1. ✅ 修复 SQLAlchemy Enum 问题
2. ✅ 配置邮件服务（163邮箱）
3. ✅ 创建精美的邮件模板
4. ✅ 集成邮件验证码发送
5. ✅ 更新 CORS 配置（支持3个前端端口）
6. ✅ 添加开发模式配置

---

## 🧪 测试邮件功能

### 1. 发送邮箱验证码

```bash
curl -X POST "http://localhost:8000/api/v1/auth/email/send" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "scene": "login"
  }'
```

**开发环境**: 会在响应中返回验证码（同时也会发送邮件）

**生产环境**: 只发送邮件，不返回验证码

### 2. 使用邮箱验证码登录

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/email" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user001@example.com",
    "email_code": "123456"
  }'
```

---

## 🔒 安全建议

### 生产环境配置

1. **更改 SECRET_KEY**
   ```env
   SECRET_KEY=your-production-secret-key-change-this
   ```

2. **关闭调试模式**
   ```env
   DEBUG=false
   RETURN_VERIFICATION_CODE=false
   ```

3. **使用环境变量**
   - 不要将 `.env` 文件提交到 Git
   - 在生产服务器上配置真实的环境变量

4. **HTTPS**
   - 生产环境必须使用 HTTPS
   - 更新 CORS 配置为生产域名

---

## 📚 相关文档

- [AUTH_GUIDE.md](./AUTH_GUIDE.md) - 完整的认证系统指南
- [STATUS_CODE_GUIDE.md](./docs/STATUS_CODE_GUIDE.md) - 状态码文档
- [README_STARTUP.md](./README_STARTUP.md) - 启动指南

---

**配置完成！现在可以正常使用登录功能和邮件服务了！** 🎉


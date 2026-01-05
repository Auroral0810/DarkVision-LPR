# 登录认证系统 - 完整文档

## 🎯 功能概览

### ✅ 已实现功能

1. **用户注册**
   - 手机号+密码+昵称
   - 可选邮箱
   - 自动创建为FREE用户

2. **多种登录方式**
   - 手机号+密码
   - 手机号+验证码
   - 邮箱+密码
   - 邮箱+验证码

3. **验证码系统**
   - 短信验证码
   - 邮箱验证码
   - Redis 缓存
   - 发送频率限制（1分钟）
   - 有效期5分钟

4. **用户信息**
   - 完整的用户详情
   - 会员状态
   - 每日识别额度
   - 实名认证状态
   - 企业子账户信息

5. **缓存优化**
   - 用户详情 Redis 缓存
   - Token Redis 存储
   - 验证码 Redis 存储

---

## 📋 API 端点

### 1. 用户注册

**POST** `/api/v1/auth/register`

**请求体**:
```json
{
  "phone": "13800138001",
  "nickname": "新用户",
  "password": "123456",
  "email": "newuser@example.com"  // 可选
}
```

**响应**:
```json
{
  "code": 20001,
  "message": "注册成功",
  "data": {
    "id": 2,
    "phone": "13800138001",
    "nickname": "新用户",
    "email": "newuser@example.com",
    "avatar_url": null,
    "user_type": "free",
    "status": "active",
    "membership_type": "free",
    "daily_quota": 10,
    "used_quota_today": 0,
    "remaining_quota_today": 10,
    ...
  }
}
```

---

### 2. 手机号登录

**POST** `/api/v1/auth/login/phone`

#### 方式一：手机号+密码

**请求体**:
```json
{
  "phone": "13800138000",
  "password": "password"
}
```

#### 方式二：手机号+验证码

**请求体**:
```json
{
  "phone": "13800138000",
  "sms_code": "123456"
}
```

**响应**:
```json
{
  "code": 20000,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_info": {
      "id": 1,
      "phone": "13800138000",
      "nickname": "普通用户001",
      "email": "user001@example.com",
      "avatar_url": "https://oss.example.com/avatars/user001.jpg",
      "user_type": "free",
      "status": "active",
      "membership_type": "free",
      "membership_expire_date": null,
      "is_membership_active": true,
      "daily_quota": 10,
      "used_quota_today": 0,
      "remaining_quota_today": 10,
      "is_verified": false,
      "real_name": null,
      "is_enterprise_main": false,
      "sub_account_count": 0,
      "created_at": "2026-01-05T23:50:11",
      "last_login_at": "2026-01-06T00:15:30"
    }
  }
}
```

---

### 3. 邮箱登录

**POST** `/api/v1/auth/login/email`

#### 方式一：邮箱+密码

**请求体**:
```json
{
  "email": "user001@example.com",
  "password": "password"
}
```

#### 方式二：邮箱+验证码

**请求体**:
```json
{
  "email": "user001@example.com",
  "email_code": "123456"
}
```

**响应**: 同手机号登录

---

### 4. 发送短信验证码

**POST** `/api/v1/auth/sms/send`

**请求体**:
```json
{
  "phone": "13800138000",
  "scene": "login"  // login/register/reset_password
}
```

**响应**:
```json
{
  "code": 20000,
  "message": "验证码已发送",
  "data": {
    "code": "123456",  // 开发环境返回，生产环境删除
    "expire_seconds": 300
  }
}
```

**限制**:
- 同一手机号1分钟内只能发送一次
- 验证码有效期5分钟

---

### 5. 发送邮箱验证码

**POST** `/api/v1/auth/email/send`

**请求体**:
```json
{
  "email": "user@example.com",
  "scene": "login"  // login/register/reset_password
}
```

**响应**: 同短信验证码

---

### 6. 获取当前用户信息

**GET** `/api/v1/auth/me`

**请求头**:
```
Authorization: Bearer <your_token>
```

**响应**:
```json
{
  "code": 20000,
  "message": "获取成功",
  "data": {
    // 完整的用户详情
  }
}
```

**说明**:
- 优先从 Redis 缓存读取
- 缓存有效期5分钟
- 包含会员状态、额度、认证信息等

---

### 7. 用户登出

**POST** `/api/v1/auth/logout`

**请求头**:
```
Authorization: Bearer <your_token>
```

**响应**:
```json
{
  "code": 20000,
  "message": "登出成功",
  "data": null
}
```

**说明**:
- 清除 Redis 中的 token
- 清除用户详情缓存

---

## 🔧 数据库字段说明

### users 表（主要字段）
```sql
- id: 用户ID
- phone: 手机号（唯一）
- nickname: 昵称（唯一）
- email: 邮箱（可选，唯一）
- password_hash: 密码哈希（bcrypt，最多72字节）
- avatar_url: 头像URL
- user_type: 用户类型（free/vip/enterprise/admin）
- status: 状态（active/inactive/banned）
- last_login_at: 最后登录时间
- last_login_ip: 最后登录IP
- created_at: 注册时间
- updated_at: 更新时间
```

### user_memberships 表
```sql
- user_id: 用户ID
- membership_type: 会员类型（free/vip_monthly/vip_yearly/enterprise_custom）
- start_date: 开始日期
- expire_date: 到期日期（NULL表示永久）
- is_active: 是否激活
```

---

## 💾 Redis 缓存设计

### 1. 验证码缓存
```
Key: verification_code:{scene}:{target}
Value: 验证码
TTL: 300秒（5分钟）

示例:
verification_code:login:13800138000 = "123456"
```

### 2. 发送频率限制
```
Key: code_rate_limit:{target}
Value: "1"
TTL: 60秒（1分钟）

示例:
code_rate_limit:13800138000 = "1"
```

### 3. 用户Token
```
Key: user_token:{user_id}
Value: JWT token
TTL: 604800秒（7天）

示例:
user_token:1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 4. 用户详情缓存
```
Key: user_detail:{user_id}
Value: JSON格式的用户详细信息
TTL: 300秒（5分钟）

示例:
user_detail:1 = '{"id":1,"phone":"13800138000",...}'
```

---

## 🧪 测试步骤

### 1. 测试注册

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13900139000",
    "nickname": "测试用户",
    "password": "test123",
    "email": "test@example.com"
  }'
```

### 2. 测试登录（密码方式）

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/phone" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "password": "password"
  }'
```

**注意**: 数据库中现有用户的密码是 bcrypt($2a$10$...) 格式，需要确认原始密码是什么。

### 3. 测试发送验证码

```bash
curl -X POST "http://localhost:8000/api/v1/auth/sms/send" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "scene": "login"
  }'
```

### 4. 测试验证码登录

```bash
# 先获取验证码（从上一步返回）
CODE="123456"

curl -X POST "http://localhost:8000/api/v1/auth/login/phone" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "sms_code": "'$CODE'"
  }'
```

### 5. 测试获取用户信息

```bash
# 从登录响应中获取 token
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. 测试登出

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🚀 前端对接示例

### 1. API 封装

```typescript
// api/auth.ts
import request from '@/utils/request'

// 注册
export function register(data: {
  phone: string
  nickname: string
  password: string
  email?: string
}) {
  return request.post('/api/v1/auth/register', data)
}

// 手机号登录（密码）
export function loginByPhonePassword(phone: string, password: string) {
  return request.post('/api/v1/auth/login/phone', { phone, password })
}

// 手机号登录（验证码）
export function loginByPhoneSMS(phone: string, sms_code: string) {
  return request.post('/api/v1/auth/login/phone', { phone, sms_code })
}

// 邮箱登录（密码）
export function loginByEmailPassword(email: string, password: string) {
  return request.post('/api/v1/auth/login/email', { email, password })
}

// 发送短信验证码
export function sendSMSCode(phone: string, scene: string) {
  return request.post('/api/v1/auth/sms/send', { phone, scene })
}

// 获取当前用户
export function getCurrentUser() {
  return request.get('/api/v1/auth/me')
}

// 登出
export function logout() {
  return request.post('/api/v1/auth/logout')
}
```

### 2. 登录组件示例

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { loginByPhonePassword, sendSMSCode } from '@/api/auth'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginType = ref('password') // 'password' 或 'sms'
const phone = ref('')
const password = ref('')
const smsCode = ref('')
const countdown = ref(0)

// 发送验证码
const handleSendCode = async () => {
  if (!phone.value) {
    ElMessage.error('请输入手机号')
    return
  }
  
  try {
    const res = await sendSMSCode(phone.value, 'login')
    ElMessage.success('验证码已发送')
    
    // 开发环境：自动填充验证码
    if (res.code) {
      smsCode.value = res.code
    }
    
    // 倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    console.error(error)
  }
}

// 登录
const handleLogin = async () => {
  try {
    let res
    if (loginType.value === 'password') {
      res = await loginByPhonePassword(phone.value, password.value)
    } else {
      res = await loginByPhoneSMS(phone.value, smsCode.value)
    }
    
    // 保存 token 和用户信息
    localStorage.setItem('token', res.access_token)
    localStorage.setItem('userInfo', JSON.stringify(res.user_info))
    
    ElMessage.success('登录成功')
    
    // 根据用户类型跳转
    if (res.user_info.user_type === 'admin') {
      router.push('/admin')
    } else {
      router.push('/dashboard')
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <div class="login-page">
    <el-form>
      <el-tabs v-model="loginType">
        <el-tab-pane label="密码登录" name="password"></el-tab-pane>
        <el-tab-pane label="验证码登录" name="sms"></el-tab-pane>
      </el-tabs>
      
      <el-form-item>
        <el-input v-model="phone" placeholder="手机号" />
      </el-form-item>
      
      <el-form-item v-if="loginType === 'password'">
        <el-input v-model="password" type="password" placeholder="密码" />
      </el-form-item>
      
      <el-form-item v-else>
        <el-input v-model="smsCode" placeholder="验证码">
          <template #append>
            <el-button 
              @click="handleSendCode" 
              :disabled="countdown > 0"
            >
              {{ countdown > 0 ? `${countdown}s` : '发送验证码' }}
            </el-button>
          </template>
        </el-input>
      </el-form-item>
      
      <el-button type="primary" @click="handleLogin">登录</el-button>
    </el-form>
  </div>
</template>
```

---

## 📊 用户类型和权限

| 用户类型 | 每日额度 | 说明 |
|---------|---------|------|
| free | 10次 | 免费用户 |
| vip | 100次 | VIP会员 |
| enterprise | 1000次 | 企业用户 |
| admin | 无限制 | 管理员 |

---

## ⚠️ 注意事项

### 1. 密码处理
- bcrypt 限制最多 72 字节
- 已在 `security.py` 中自动截断

### 2. 现有用户登录
数据库中现有用户的密码哈希是:
```
$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi
```

这个哈希对应的原始密码可能是 `"password"` 或其他，需要确认。

### 3. 验证码（开发环境）
开发环境会在响应中返回验证码，便于测试。
**生产环境务必删除返回验证码的代码！**

### 4. Redis 依赖
- 验证码功能依赖 Redis
- 用户信息缓存依赖 Redis
- 如果 Redis 不可用，会降级为直接查询数据库

---

## 🔄 完整登录流程

```
1. 用户选择登录方式
   ↓
2a. 密码登录              2b. 验证码登录
   - 输入手机号/邮箱           - 输入手机号/邮箱
   - 输入密码                  - 点击发送验证码
   ↓                          - 输入验证码
3. 提交登录请求              ↓
   ↓                       3. 提交登录请求
4. 后端验证                  ↓
   - 检查用户存在            4. 后端验证
   - 验证密码                 - 检查用户存在
   ↓                          - 验证验证码（Redis）
5. 检查用户状态              ↓
   - active/banned          5. 检查用户状态
   ↓                          ↓
6. 生成 JWT Token          6. 生成 JWT Token
   - 存入 Redis              - 存入 Redis
   ↓                          ↓
7. 获取用户详情            7. 获取用户详情
   - 优先读取缓存            - 优先读取缓存
   ↓                          ↓
8. 返回 token + 用户信息    8. 返回 token + 用户信息
   ↓                          ↓
9. 前端保存 token          9. 前端保存 token
   - localStorage            - localStorage
   - Vuex/Pinia             - Vuex/Pinia
   ↓                          ↓
10. 根据用户类型跳转页面    10. 根据用户类型跳转页面
```

---

完整实现已完成！🎉


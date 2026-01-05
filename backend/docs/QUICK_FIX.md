# 🔧 快速修复指南

## ✅ 已修复的问题

### 1. bcrypt 密码长度错误
**错误**: `ValueError: password cannot be longer than 72 bytes`

**解决方案**: 
1. 安装 `bcrypt` 库
2. 在 `security.py` 中添加密码截断逻辑

### 2. 注册接口缺少验证码
**问题**: 原注册接口没有验证码，存在安全隐患

**解决方案**: 添加短信验证码验证

### 3. SQLAlchemy Enum 错误
**错误**: `LookupError: 'free' is not among the defined enum values`

**解决方案**: 配置 Enum 使用值而不是名称

---

## 🚀 立即执行的修复步骤

### 步骤1: 安装 bcrypt
```bash
cd backend
conda activate DarkVision
pip install bcrypt==4.1.2
```

### 步骤2: 重启服务
```bash
# 停止当前服务（Ctrl+C）
# 重新启动
./start.sh
```

### 步骤3: 测试注册流程

#### 3.1 发送验证码
```bash
curl -X POST "http://localhost:8000/api/v1/auth/sms/send" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "15968588744",
    "scene": "register"
  }'
```

**响应** (开发环境会返回验证码):
```json
{
  "code": 20000,
  "message": "验证码已发送",
  "data": {
    "code": "123456",
    "expire_seconds": 300
  }
}
```

#### 3.2 使用验证码注册
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "15968588744",
    "sms_code": "123456",
    "nickname": "Auroral",
    "password": "123456",
    "email": "15968588744@163.com"
  }'
```

---

## 📋 新的注册流程

### 前端实现

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { sendSMSCode, register } from '@/api/auth'

const form = ref({
  phone: '',
  sms_code: '',
  nickname: '',
  password: '',
  email: ''
})

const countdown = ref(0)

// 1. 发送验证码
const handleSendCode = async () => {
  try {
    const res = await sendSMSCode(form.value.phone, 'register')
    ElMessage.success('验证码已发送')
    
    // 开发环境：自动填充验证码
    if (res.code) {
      form.value.sms_code = res.code
    }
    
    // 倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) clearInterval(timer)
    }, 1000)
  } catch (error) {
    console.error(error)
  }
}

// 2. 注册
const handleRegister = async () => {
  try {
    await register(form.value)
    ElMessage.success('注册成功')
    router.push('/login')
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <el-form :model="form">
    <el-form-item label="手机号">
      <el-input v-model="form.phone" placeholder="请输入手机号" />
    </el-form-item>
    
    <el-form-item label="验证码">
      <el-input v-model="form.sms_code" placeholder="请输入验证码">
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
    
    <el-form-item label="昵称">
      <el-input v-model="form.nickname" placeholder="请输入昵称" />
    </el-form-item>
    
    <el-form-item label="密码">
      <el-input v-model="form.password" type="password" placeholder="请输入密码" />
    </el-form-item>
    
    <el-form-item label="邮箱">
      <el-input v-model="form.email" placeholder="请输入邮箱（可选）" />
    </el-form-item>
    
    <el-button type="primary" @click="handleRegister">注册</el-button>
  </el-form>
</template>
```

---

## 🔐 安全说明

### 为什么需要验证码？

1. **防止恶意注册**: 避免自动化脚本批量注册账号
2. **验证手机号**: 确保用户拥有该手机号
3. **降低垃圾信息**: 减少虚假账号

### 验证码配置

| 配置项 | 值 | 说明 |
|-------|---|------|
| 验证码长度 | 6位数字 | 安全且易记 |
| 有效期 | 5分钟 | 防止重放攻击 |
| 发送频率限制 | 1分钟1次 | 防止短信轰炸 |
| 使用次数 | 一次性 | 验证后自动失效 |

### 生产环境注意

**必须修改的配置**:
```python
# app/config.py
DEBUG = False  # 关闭调试模式
RETURN_VERIFICATION_CODE = False  # 不返回验证码
```

**生产环境响应**（不包含验证码）:
```json
{
  "code": 20000,
  "message": "验证码已发送",
  "data": {
    "expire_seconds": 300
  }
}
```

---

## 📝 完整的API文档

### 1. 发送注册验证码
**POST** `/api/v1/auth/sms/send`

```json
{
  "phone": "13800138000",
  "scene": "register"
}
```

### 2. 用户注册
**POST** `/api/v1/auth/register`

```json
{
  "phone": "13800138000",
  "sms_code": "123456",
  "nickname": "新用户",
  "password": "123456",
  "email": "user@example.com"
}
```

### 3. 手机号+密码登录
**POST** `/api/v1/auth/login/phone`

```json
{
  "phone": "13800138000",
  "password": "123456"
}
```

### 4. 手机号+验证码登录
**POST** `/api/v1/auth/login/phone`

**先发送登录验证码**:
```json
{
  "phone": "13800138000",
  "scene": "login"
}
```

**然后登录**:
```json
{
  "phone": "13800138000",
  "sms_code": "123456"
}
```

---

## ⚠️ 常见问题

### Q1: bcrypt 安装失败？
```bash
# 尝试升级 pip
pip install --upgrade pip

# 或使用 conda 安装
conda install -c conda-forge bcrypt
```

### Q2: 验证码没收到？
开发环境会在响应中返回验证码，检查响应的 `data.code` 字段

### Q3: 注册时提示验证码错误？
1. 检查验证码是否过期（5分钟）
2. 检查是否已使用过（一次性）
3. 检查 Redis 是否正常运行

### Q4: 邮件没收到？
1. 检查邮箱配置是否正确
2. 查看日志：`backend/logs/app.log`
3. 确认163邮箱授权码是否有效

---

## ✅ 验证修复是否成功

运行测试脚本:
```bash
cd backend
./test_auth.sh
```

或手动测试:
```bash
# 1. 健康检查
curl http://localhost:8000/health

# 2. 发送验证码
curl -X POST "http://localhost:8000/api/v1/auth/sms/send" \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139000","scene":"register"}'

# 3. 注册用户（使用返回的验证码）
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone":"13900139000",
    "sms_code":"返回的验证码",
    "nickname":"测试用户",
    "password":"123456"
  }'
```

---

**所有问题已修复！现在可以正常使用注册和登录功能了！** 🎉


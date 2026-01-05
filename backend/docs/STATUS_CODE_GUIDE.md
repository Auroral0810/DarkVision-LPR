# 统一状态码系统使用指南

## 📚 目录

1. [系统概述](#系统概述)
2. [状态码体系](#状态码体系)
3. [使用方法](#使用方法)
4. [完整示例](#完整示例)
5. [前端对接](#前端对接)

---

## 系统概述

本系统采用 **HTTP 状态码 + 业务状态码** 的双重体系：

- **HTTP 状态码**: 遵循标准HTTP协议（200、400、401、403、500等）
- **业务状态码**: 自定义5位数字，精确标识业务错误类型

### 响应格式

所有API统一返回以下格式：

```json
{
  "code": 20000,
  "message": "操作成功",
  "data": {
    // 实际数据
  }
}
```

---

## 状态码体系

### 成功类 (20000-20999)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 20000 | 操作成功 | 200 |
| 20001 | 创建成功 | 200 |
| 20002 | 更新成功 | 200 |
| 20003 | 删除成功 | 200 |

### 客户端错误类 (40000-49999)

#### 通用错误 (40000-40099)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 40000 | 请求参数错误 | 400 |
| 40001 | 数据验证失败 | 400 |
| 40002 | 缺少必要参数 | 400 |
| 40003 | 参数格式错误 | 400 |

#### 认证授权错误 (40100-40199)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 40100 | 未登录/token失效 | 401 |
| 40101 | token过期 | 401 |
| 40102 | token无效 | 401 |
| 40103 | 无权限访问 | 403 |
| 40104 | 需要登录 | 401 |
| 40105 | 权限不足 | 403 |

#### 用户相关错误 (40200-40299)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 40200 | 用户不存在 | 400 |
| 40201 | 用户已存在 | 400 |
| 40202 | 手机号已注册 | 400 |
| 40203 | 邮箱已注册 | 400 |
| 40204 | 昵称已被使用 | 400 |
| 40205 | 密码错误 | 400 |
| 40206 | 用户已被封禁 | 400 |
| 40207 | 用户未激活 | 400 |

#### 识别服务错误 (40400-40499)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 40400 | 识别失败 | 400 |
| 40401 | 图片格式错误 | 400 |
| 40402 | 图片大小超限 | 400 |
| 40403 | 额度已用完 | 400 |
| 40404 | 未检测到车牌 | 400 |

#### 订单支付错误 (40500-40599)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 40500 | 订单不存在 | 400 |
| 40501 | 订单已支付 | 400 |
| 40502 | 订单已过期 | 400 |
| 40503 | 支付失败 | 400 |
| 40504 | 退款失败 | 400 |

### 服务器错误类 (50000-59999)

| 状态码 | 说明 | HTTP状态码 |
|--------|------|-----------|
| 50000 | 服务器内部错误 | 500 |
| 50001 | 数据库错误 | 500 |
| 50002 | Redis错误 | 500 |
| 50003 | 第三方服务错误 | 500 |
| 50004 | 文件上传失败 | 500 |
| 50005 | AI服务错误 | 500 |

---

## 使用方法

### 1. 在 Service 层使用异常

```python
from app.core.exceptions import (
    PhoneExistedException,
    WrongPasswordException,
    UserNotFoundException
)

def register_user(db: Session, user_data: UserRegister):
    # 检查手机号是否存在
    if existing_user:
        raise PhoneExistedException()  # 自动返回 40202
    
    # 检查密码
    if not verify_password(password, hash):
        raise WrongPasswordException()  # 自动返回 40205
    
    # 正常返回
    return new_user
```

### 2. 在 API 层使用响应工具

```python
from app.core.response import success, success_created, error
from app.core.codes import ResponseCode

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    
    # 方式一：使用快捷方法
    return success_created(
        data={"id": user.id, "nickname": user.nickname},
        message="注册成功"
    )
    
    # 方式二：使用通用方法
    return success(
        data=user_data,
        message="注册成功",
        code=ResponseCode.CREATED
    )
```

### 3. 手动返回错误

```python
from app.core.response import error
from app.core.codes import ResponseCode

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return error(
            code=ResponseCode.USER_NOT_FOUND,
            message="找不到该用户"
        )
    
    return success(data=user)
```

---

## 完整示例

### 示例1: 用户注册

```python
# app/api/v1/auth.py
from app.core.response import success_created
from app.core.exceptions import PhoneExistedException

@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册
    
    成功响应:
    {
      "code": 20001,
      "message": "注册成功",
      "data": {"id": 1, "nickname": "张三"}
    }
    
    失败响应:
    {
      "code": 40202,
      "message": "手机号已注册",
      "data": null
    }
    """
    user = register_user(db, user_data)
    return success_created(
        data={"id": user.id, "nickname": user.nickname},
        message="注册成功"
    )
```

### 示例2: 用户登录

```python
# app/services/auth.py
from app.core.exceptions import WrongPasswordException, UserBannedException

def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.phone == login_data.phone).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise WrongPasswordException()  # 40205
    
    if user.status == UserStatus.BANNED:
        raise UserBannedException()  # 40206
    
    return user


# app/api/v1/auth.py
@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data)
    token = create_user_token(user)
    
    return success(
        data={
            "access_token": token,
            "user_info": {"id": user.id, "user_type": user.user_type}
        },
        message="登录成功"
    )
```

### 示例3: 参数验证错误

FastAPI 的 Pydantic 验证错误会被自动捕获：

```python
# 请求
POST /api/v1/auth/register
{
  "phone": "123",  # 格式错误
  "password": "123"  # 太短
}

# 响应
{
  "code": 40001,
  "message": "phone: 手机号格式不正确; password: 密码长度不足",
  "data": [...]  # 详细的验证错误
}
```

---

## 前端对接

### 1. Axios 拦截器配置

```typescript
// request.ts
import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

// 响应拦截器
request.interceptors.response.use(
  response => {
    const { code, message, data } = response.data
    
    // 成功 (20000-20999)
    if (code >= 20000 && code < 21000) {
      return data  // 直接返回数据
    }
    
    // 业务错误
    ElMessage.error(message)
    return Promise.reject(new Error(message))
  },
  error => {
    // 网络错误或服务器错误
    const { code, message } = error.response?.data || {}
    
    // 根据业务状态码处理
    switch (code) {
      case 40100:  // 未登录
      case 40101:  // token过期
        ElMessage.error('登录已过期，请重新登录')
        // 跳转到登录页
        router.push('/login')
        break
      
      case 40103:  // 无权限
        ElMessage.error('无权限访问')
        break
      
      case 40202:  // 手机号已注册
        ElMessage.error('手机号已被注册')
        break
      
      default:
        ElMessage.error(message || '请求失败')
    }
    
    return Promise.reject(error)
  }
)

export default request
```

### 2. API 调用示例

```typescript
// api/auth.ts
import request from '@/utils/request'

// 用户注册
export function register(data: {
  phone: string
  nickname: string
  password: string
  email?: string
}) {
  return request({
    url: '/api/v1/auth/register',
    method: 'post',
    data
  })
}

// 用户登录
export function login(data: { phone: string; password: string }) {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

// 获取当前用户
export function getCurrentUser() {
  return request({
    url: '/api/v1/auth/me',
    method: 'get'
  })
}
```

### 3. 在组件中使用

```vue
<script setup lang="ts">
import { register, login } from '@/api/auth'
import { ElMessage } from 'element-plus'

// 注册
const handleRegister = async () => {
  try {
    const userData = await register({
      phone: '13800138000',
      nickname: '张三',
      password: '123456'
    })
    
    // 成功：拦截器已处理，直接得到 data
    ElMessage.success('注册成功')
    console.log(userData)  // { id: 1, nickname: '张三', ... }
    
  } catch (error) {
    // 失败：拦截器已提示错误消息
    console.error(error)
  }
}

// 登录
const handleLogin = async () => {
  try {
    const { access_token, user_info } = await login({
      phone: '13800138000',
      password: '123456'
    })
    
    // 保存 token
    localStorage.setItem('token', access_token)
    
    // 根据用户类型跳转
    if (user_info.user_type === 'admin') {
      router.push('/admin')
    } else {
      router.push('/dashboard')
    }
    
  } catch (error) {
    // 错误处理
  }
}
</script>
```

### 4. 状态码常量定义（前端）

```typescript
// constants/code.ts
export const ResponseCode = {
  // 成功
  SUCCESS: 20000,
  CREATED: 20001,
  
  // 认证错误
  UNAUTHORIZED: 40100,
  TOKEN_EXPIRED: 40101,
  FORBIDDEN: 40103,
  
  // 用户错误
  USER_NOT_FOUND: 40200,
  PHONE_EXISTED: 40202,
  WRONG_PASSWORD: 40205,
  USER_BANNED: 40206,
  
  // 识别服务
  QUOTA_EXCEEDED: 40403,
  
  // 服务器错误
  INTERNAL_ERROR: 50000
} as const

// 使用示例
if (code === ResponseCode.TOKEN_EXPIRED) {
  // 跳转登录页
}
```

---

## 最佳实践

### 1. Service 层抛出异常

```python
# ✅ 好的做法
def get_user(user_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise UserNotFoundException()  # 让全局异常处理器处理
    return user

# ❌ 不好的做法
def get_user(user_id: int):
    user = db.query(User).get(user_id)
    if not user:
        return None  # API层需要手动判断
    return user
```

### 2. API 层返回统一格式

```python
# ✅ 好的做法
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(user_id)  # 异常会被自动处理
    return success(data=user)

# ❌ 不好的做法
@router.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user": user}  # 没有统一格式
```

### 3. 错误消息要友好

```python
# ✅ 好的做法
raise UserNotFoundException("该用户不存在或已被删除")

# ❌ 不好的做法
raise Exception("User not found")
```

---

## 文件结构

```
backend/app/
├── core/
│   ├── codes.py           # 状态码定义
│   ├── response.py        # 响应工具
│   └── exceptions.py      # 自定义异常
├── middleware/
│   └── error_handler.py   # 全局异常处理
└── api/
    └── v1/
        └── auth.py        # 使用状态码的示例
```

---

## 总结

- ✅ 统一的状态码便于前后端协作
- ✅ 细分的错误类型便于问题定位
- ✅ 自动的异常处理减少重复代码
- ✅ 友好的错误提示提升用户体验


# 统一状态码系统 - 总结

## 📦 已创建的文件

### 核心文件
1. **app/core/codes.py** - 状态码定义
   - `ResponseCode`: 枚举类，定义所有业务状态码
   - `ResponseMessage`: 状态码消息映射
   - `get_http_status()`: 业务码转HTTP码

2. **app/core/response.py** - 响应工具
   - `UnifiedResponse`: 统一响应模型
   - `success()`: 成功响应
   - `error()`: 错误响应
   - `success_created()`, `success_updated()` 等快捷方法

3. **app/core/exceptions.py** - 自定义异常
   - `BusinessException`: 业务异常基类
   - `APIException`: API异常基类
   - 各种具体异常类（40+个）

4. **app/middleware/error_handler.py** - 全局异常处理
   - 自动捕获并处理所有异常
   - 返回统一格式的错误响应
   - 记录日志

### 文档文件
5. **docs/STATUS_CODE_GUIDE.md** - 完整使用指南（5.7KB）
   - 状态码体系说明
   - 详细使用示例
   - 前端对接方案

6. **docs/CODE_CHEATSHEET.md** - 快速参考卡片（1KB）
   - 常用状态码速查
   - 快速使用方法

### 已更新的文件
7. **app/main.py** - 注册异常处理器
8. **app/services/auth.py** - 使用新异常
9. **app/api/v1/auth.py** - 使用统一响应

---

## 🎯 状态码体系

### 编码规则
- **20000-20999**: 成功类
- **40000-40099**: 通用客户端错误
- **40100-40199**: 认证授权错误
- **40200-40299**: 用户相关错误
- **40300-40399**: 资源相关错误
- **40400-40499**: 识别服务错误
- **40500-40599**: 订单支付错误
- **40600-40699**: 实名认证错误
- **40700-40799**: 频率限制错误
- **50000-59999**: 服务器错误
- **60000-69999**: 业务错误

---

## ✨ 核心特性

### 1. 自动异常处理
Service 层只需抛出异常，全局处理器自动转换为统一格式：

```python
# Service 层
def register_user(db: Session, user_data: UserRegister):
    if phone_exists:
        raise PhoneExistedException()  # 👈 只需抛出
    return new_user

# 自动返回
{
  "code": 40202,
  "message": "手机号已注册",
  "data": null
}
```

### 2. 统一响应格式
API 层使用响应工具，格式自动统一：

```python
# API 层
@router.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return success_created(data=user)  # 👈 统一格式
```

### 3. 精确的错误定位
40+ 种预定义异常，精确标识错误类型：

```python
PhoneExistedException()     # 40202 - 手机号已注册
WrongPasswordException()    # 40205 - 密码错误
TokenExpiredException()     # 40101 - Token过期
QuotaExceededException()    # 40403 - 额度已用完
```

### 4. 前端友好
状态码区间设计便于前端统一处理：

```typescript
// 根据区间判断错误类型
if (code >= 40100 && code < 40200) {
  // 认证错误 -> 跳转登录
} else if (code >= 40200 && code < 40300) {
  // 用户错误 -> 提示用户
}
```

---

## 📝 使用示例

### 后端 - 抛出异常

```python
from app.core.exceptions import (
    PhoneExistedException,
    WrongPasswordException,
    QuotaExceededException
)

# 示例1: 注册检查
if db.query(User).filter(User.phone == phone).first():
    raise PhoneExistedException()

# 示例2: 登录验证
if not verify_password(password, user.password_hash):
    raise WrongPasswordException()

# 示例3: 额度检查
if user_quota >= daily_limit:
    raise QuotaExceededException("今日识别次数已用完")
```

### 后端 - 返回响应

```python
from app.core.response import success, success_created, error

# 成功响应
return success(data={"id": 1, "name": "张三"})

# 创建成功
return success_created(data=new_user, message="注册成功")

# 手动错误响应（少用，优先用异常）
return error(code=ResponseCode.USER_NOT_FOUND)
```

### 前端 - Axios 拦截器

```typescript
axios.interceptors.response.use(
  response => {
    const { code, data, message } = response.data
    
    if (code >= 20000 && code < 21000) {
      return data  // 成功，返回数据
    }
    
    ElMessage.error(message)
    return Promise.reject(new Error(message))
  },
  error => {
    const { code, message } = error.response?.data || {}
    
    // 根据状态码特殊处理
    if (code === 40100 || code === 40101) {
      router.push('/login')  // 跳转登录
    }
    
    ElMessage.error(message || '请求失败')
    return Promise.reject(error)
  }
)
```

---

## 🚀 当前已实现的功能

### 认证模块 (/api/v1/auth)
1. ✅ **POST /register** - 用户注册
   - 返回码: 20001 (成功) / 40202 (手机号已注册)
   
2. ✅ **POST /login** - 用户登录
   - 返回码: 20000 (成功) / 40205 (密码错误) / 40206 (用户封禁)
   
3. ✅ **GET /me** - 获取当前用户
   - 返回码: 20000 (成功) / 40100 (未登录) / 40102 (Token无效)

4. ✅ **POST /logout** - 用户登出
   - 返回码: 20000 (成功)

---

## 📖 响应示例

### 注册成功
```json
{
  "code": 20001,
  "message": "注册成功",
  "data": {
    "id": 1,
    "phone": "13800138000",
    "nickname": "张三",
    "user_type": "free",
    "status": "active"
  }
}
```

### 登录成功
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
      "user_type": "free"
    }
  }
}
```

### 手机号已注册
```json
{
  "code": 40202,
  "message": "手机号已注册",
  "data": null
}
```

### 密码错误
```json
{
  "code": 40205,
  "message": "手机号或密码错误",
  "data": null
}
```

### Token过期
```json
{
  "code": 40101,
  "message": "登录已过期,请重新登录",
  "data": null
}
```

---

## 🔧 配置说明

### 1. 全局异常处理已自动注册
在 `app/main.py` 中已经添加：

```python
from app.middleware.error_handler import register_exception_handlers
register_exception_handlers(app)
```

### 2. 所有异常自动处理
以下异常会被自动捕获并返回统一格式：
- ✅ BusinessException (业务异常)
- ✅ APIException (API异常)
- ✅ HTTPException (HTTP异常)
- ✅ RequestValidationError (参数验证错误)
- ✅ SQLAlchemyError (数据库错误)
- ✅ RedisError (Redis错误)
- ✅ Exception (其他未知错误)

---

## 📚 快速链接

- **完整文档**: `backend/docs/STATUS_CODE_GUIDE.md`
- **快速参考**: `backend/docs/CODE_CHEATSHEET.md`
- **状态码定义**: `backend/app/core/codes.py`
- **异常类定义**: `backend/app/core/exceptions.py`
- **响应工具**: `backend/app/core/response.py`

---

## 🎓 下一步建议

1. **测试登录注册功能**
   ```bash
   # 启动服务
   cd backend && ./start.sh
   
   # 访问 API 文档
   http://localhost:8000/docs
   ```

2. **导出 API 到 Apifox**
   ```bash
   cd backend
   ./export_api.sh
   # 或直接在 Apifox 中导入 URL:
   # http://localhost:8000/openapi.json
   ```

3. **前端对接**
   - 参考 `STATUS_CODE_GUIDE.md` 中的前端示例
   - 配置 Axios 拦截器
   - 根据状态码处理不同场景

4. **扩展新功能**
   - 在 `app/core/codes.py` 中添加新状态码
   - 在 `app/core/exceptions.py` 中添加新异常类
   - 在 Service 层抛出异常
   - 在 API 层使用响应工具

---

## ✅ 优势总结

| 特性 | 说明 | 好处 |
|-----|------|------|
| **统一格式** | 所有响应格式一致 | 前端处理简单 |
| **精确定位** | 40+种状态码 | 快速定位问题 |
| **自动处理** | 全局异常捕获 | 减少重复代码 |
| **类型安全** | 使用枚举定义 | IDE智能提示 |
| **易于扩展** | 模块化设计 | 添加新码简单 |
| **前后端协作** | 状态码文档化 | 沟通成本低 |

---

**系统已完全配置，可以开始使用！** 🎉


# 状态码快速参考

## 常用状态码速查表

### ✅ 成功类
```
20000 - 操作成功
20001 - 创建成功
20002 - 更新成功
20003 - 删除成功
```

### 🔐 认证类
```
40100 - 未登录
40101 - Token过期
40102 - Token无效
40103 - 无权限
40205 - 密码错误
```

### 👤 用户类
```
40200 - 用户不存在
40202 - 手机号已注册
40203 - 邮箱已注册
40206 - 用户已封禁
```

### 🖼️ 识别类
```
40400 - 识别失败
40403 - 额度已用完
40404 - 未检测到车牌
```

### 💰 订单类
```
40500 - 订单不存在
40501 - 订单已支付
40503 - 支付失败
```

### 💥 服务器类
```
50000 - 服务器错误
50001 - 数据库错误
50005 - AI服务错误
```

---

## 快速使用

### 1. 抛出异常
```python
from app.core.exceptions import PhoneExistedException
raise PhoneExistedException()
```

### 2. 返回成功
```python
from app.core.response import success
return success(data=result, message="操作成功")
```

### 3. 返回错误
```python
from app.core.response import error
from app.core.codes import ResponseCode
return error(code=ResponseCode.USER_NOT_FOUND)
```

---

## 前端处理
```typescript
// 根据 code 判断
if (code === 20000) {
  // 成功
} else if (code >= 40100 && code < 40200) {
  // 认证错误 -> 跳转登录
} else {
  // 其他错误 -> 提示用户
}
```


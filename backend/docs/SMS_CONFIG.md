# 短信服务配置说明

## 短信宝配置

本项目使用短信宝（smsbao.com）作为短信服务提供商。

### 配置步骤

1. **注册短信宝账号**
   - 访问 https://www.smsbao.com/
   - 注册账号并充值

2. **配置环境变量**

在 `backend/.env` 文件中添加以下配置：

```env
# 短信配置（短信宝）
SMS_PROVIDER=smsbao
SMS_API_URL=http://api.smsbao.com/sms
SMS_USER=你的短信宝账号
SMS_PASSWORD=你的短信宝密码
SMS_SIGN_NAME=DarkVision-LPR
```

### 配置说明

- `SMS_PROVIDER`: 短信服务商标识，固定为 `smsbao`
- `SMS_API_URL`: 短信宝API地址，固定为 `http://api.smsbao.com/sms`
- `SMS_USER`: 你的短信宝账号用户名
- `SMS_PASSWORD`: 你的短信宝账号密码（原始密码，系统会自动MD5加密）
- `SMS_SIGN_NAME`: 短信签名，需在短信宝后台申请

### 开发环境配置

开发环境下，如果未配置短信服务或余额不足，验证码仍会返回在接口响应中，方便测试：

```env
DEBUG=True
RETURN_VERIFICATION_CODE=True
```

生产环境请设置：

```env
DEBUG=False
RETURN_VERIFICATION_CODE=False
```

### 短信发送接口

验证码短信会通过以下方式发送：

```
【DarkVision-LPR】您的{场景}验证码是{code}。如非本人操作，请忽略本短信
```

支持的场景：
- `login`: 登录验证码
- `register`: 注册验证码
- `reset_password`: 重置密码验证码

### API 调用示例

发送注册短信验证码：

```bash
curl -X POST "http://localhost:8000/api/v1/auth/sms/send" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "scene": "register"
  }'
```

响应示例（开发环境）：

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

### 短信宝状态码说明

| 状态码 | 说明 |
|--------|------|
| 0 | 短信发送成功 |
| -1 | 参数不全 |
| -2 | 服务器不支持 |
| 30 | 密码错误 |
| 40 | 账号不存在 |
| 41 | 余额不足 |
| 42 | 账户已过期 |
| 43 | IP地址限制 |
| 50 | 内容含有敏感词 |

### 注意事项

1. **频率限制**: 同一手机号60秒内只能发送一次验证码
2. **有效期**: 验证码5分钟内有效
3. **签名申请**: 需要在短信宝后台申请短信签名
4. **余额监控**: 建议定期检查账户余额
5. **内容规范**: 避免使用敏感词汇

### 自定义短信

如需发送自定义短信内容，可使用 `sms_service.send_custom_message()` 方法：

```python
from app.services.sms import sms_service

# 发送自定义短信（需包含签名）
sms_service.send_custom_message(
    phone="13800138000",
    content="【DarkVision-LPR】您的订单已发货，快递单号：SF1234567890"
)
```

### 故障排查

1. **短信发送失败**
   - 检查账号密码是否正确
   - 检查账户余额是否充足
   - 检查短信签名是否已审核通过
   - 查看日志文件 `backend/logs/app.log`

2. **验证码无效**
   - 检查 Redis 是否正常运行
   - 验证码是否已过期（5分钟）
   - 是否已使用过（验证成功后会删除）

3. **接口报错**
   - 查看错误日志 `backend/logs/error.log`
   - 检查网络连接是否正常
   - 确认短信宝 API 服务是否可用


# 系统配置指南

DarkVision-LPR 提供了丰富的配置项，允许管理员根据部署环境和业务需求进行灵活调整。

## 环境变量配置 (.env)

在后端根目录下创建 `.env` 文件，用于管理敏感信息与核心参数。

```ini
# --- 数据库 ---
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=secret
MYSQL_DATABASE=darkvision_lpr

# --- Redis ---
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# --- 安全 ---
SECRET_KEY=your-super-secret-key-change-it-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # Token 有效期 (分钟)

# --- 阿里云 OSS (可选) ---
OSS_ACCESS_KEY_ID=LTAI...
OSS_ACCESS_KEY_SECRET=xyz...
OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com
OSS_BUCKET_NAME=darkvision-bucket
OSS_URL_PREFIX=https://darkvision-bucket.oss-cn-shanghai.aliyuncs.com

# --- 邮件服务 (可选) ---
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=no-reply@darkvision.com
MAIL_PORT=465
MAIL_SERVER=smtp.example.com
```

## 应用级配置

大部分业务配置可以在**管理后台**的「系统设置」中进行热更新，无需重启服务。

| 配置项 | 说明 | 默认值 |
| :--- | :--- | :--- |
| **识别阈值** | 低于该置信度的结果将被标记为不可信 | `0.75` |
| **每日免费额度** | 普通用户每日可识别的图片数量 | `20` |
| **上传限制** | 单张图片最大允许体积 (MB) | `5` |
| **维护模式** | 开启后，普通用户无法访问系统，仅管理员可用 | `关闭` |

## 日志配置

使用 `Loguru` 进行日志管理，配置文件位于 `app/core/logging.py`。
- **Console**: 输出 INFO 及以上级别。
- **File**: 每日轮转，保留 7 天，记录 ERROR 及以上级别。

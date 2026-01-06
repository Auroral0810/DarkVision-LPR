# API 接口参考

DarkVision-LPR 提供了标准的 RESTful API，方便开发者进行二次开发。

::: tip 提示
所有 API 请求需在 Header 中携带 `Authorization: Bearer <your_token>`。
:::

## 认证 (Auth)

### 登录获取 Token
- **Endpoint**: `POST /api/v1/login/access-token`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Params**: `username`, `password`

## 识别 (Recognition)

### 上传单张图片识别
- **Endpoint**: `POST /api/v1/recognition/single`
- **Content-Type**: `multipart/form-data`
- **Params**: `file` (Image)
- **Response**:
```json
{
  "code": 200,
  "data": {
    "license_plate": "皖AD18989",
    "confidence": 0.98,
    "color": "green",
    "processing_time": "45ms",
    "image_url": "https://oss..."
  }
}
```

### 获取识别历史
- **Endpoint**: `GET /api/v1/recognition/history`
- **Query**: `page=1`, `size=20`, `start_date=2024-01-01`

## 用户 (User)

### 获取个人信息
- **Endpoint**: `GET /api/v1/users/me`

### 申请实名认证
- **Endpoint**: `POST /api/v1/users/verification`
- **Body**: `{ "real_name": "张三", "id_card": "..." }`

> 详细的接口定义请参考系统集成的 Swagger UI 文档 (通常位于 `/docs`)。

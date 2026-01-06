# System Configuration

DarkVision-LPR supports configuration via environment variables to adapt to different runtime environments (Dev, Staging, Prod).

## Environment Variables (.env)

Create a `.env` file in the `backend/` directory.

### Core Configuration
```ini
# Application Mode: development / production
APP_ENV=development
# Secret Key for JWT
SECRET_KEY=your-super-secret-key-change-it
# Algorithm for JWT
ALGORITHM=HS256
# Access Token Expire Minutes
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Configuration
```ini
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=darkvision_lpr
```

### Redis Configuration
```ini
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

### Aliyun OSS (Optional)
Required for storing original images of recognition records.
```ini
ALIYUN_ACCESS_KEY_ID=your_access_key
ALIYUN_ACCESS_KEY_SECRET=your_secret_key
ALIYUN_OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com
ALIYUN_OSS_BUCKET=your-bucket-name
```

## Model Configuration

The model weights are located in the `backend/weights/` directory. You can modify `backend/app/core/config.py` to change the paths:

```python
class Settings(BaseSettings):
    YOLO_MODEL_PATH: str = "weights/best.pt"
    LPRNET_MODEL_PATH: str = "weights/Final_LPRNet_model.pth"
```

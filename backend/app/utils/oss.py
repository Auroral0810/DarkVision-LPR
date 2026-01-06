import oss2
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class OSSUploader:
    def __init__(self):
        self.enabled = all([
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET,
            settings.OSS_ENDPOINT,
            settings.OSS_BUCKET_NAME
        ])
        
        if self.enabled:
            self.auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
            # Ensure endpoint doesn't have bucket name if it's region endpoint
            # Prompt says endpoint: https://oss-cn-beijing.aliyuncs.com
            self.bucket = oss2.Bucket(self.auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET_NAME)
            self.url_prefix = settings.OSS_URL or f"{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT.replace('https://', '').replace('http://', '')}"
        else:
            logger.warning("Aliyun OSS is not fully configured.")

    def upload_file(self, file_data, filename):
        if not self.enabled:
            raise Exception("OSS is not configured")
            
        try:
            # put_object accepts bytes or file-like object
            result = self.bucket.put_object(filename, file_data)
            if result.status == 200:
                # Construct URL
                # If OSS_URL is provided (e.g. custom domain or bucket domain)
                if settings.OSS_URL:
                    # If OSS_URL doesn't start with http/https, assume https
                    base_url = settings.OSS_URL
                    if not base_url.startswith("http"):
                        base_url = f"https://{base_url}"
                    
                    # Ensure no double slashes
                    if base_url.endswith("/"):
                        base_url = base_url[:-1]
                    if filename.startswith("/"):
                        filename = filename[1:]
                        
                    return f"{base_url}/{filename}"
                else:
                    return f"https://{self.url_prefix}/{filename}"
            else:
                logger.error(f"OSS Upload failed with status: {result.status}")
                raise Exception(f"OSS Upload failed with status: {result.status}")
        except Exception as e:
            logger.error(f"OSS Upload Exception: {e}")
            raise e

    def get_file_content(self, object_key: str) -> bytes:
        """
        获取文件内容
        :param object_key: OSS Object Key
        :return: bytes
        """
        if not self.enabled:
            raise Exception("OSS is not configured")
            
        try:
            result = self.bucket.get_object(object_key)
            return result.read()
        except Exception as e:
            logger.error(f"OSS Download Exception: {e}")
            raise e

    def generate_presigned_url(self, object_key: str, expires: int = 3600) -> str:
        """
        生成带签名的临时访问URL
        :param object_key: OSS Object Key
        :param expires: 过期时间(秒)，默认1小时
        :return: 签名URL
        """
        if not self.enabled:
            raise Exception("OSS is not configured")
            
        try:
            url = self.bucket.sign_url('GET', object_key, expires)
            return url
        except Exception as e:
            logger.error(f"OSS Generate Presigned URL Exception: {e}")
            raise e

oss_uploader = OSSUploader()

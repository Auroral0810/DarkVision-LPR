import re
from typing import Optional
from urllib.parse import unquote
from app.config import settings
from app.utils.oss import oss_uploader
from app.core.logger import logger

def get_image_url(url: Optional[str]) -> Optional[str]:
    """
    统一处理图片URL：
    1. 如果是 OSS 链接且属于本项目桶，生成带签名的临时访问 URL
    2. 如果是本地相对路径 (static/uploads/...)，加上后端 HOST 前缀
    3. 否则原样返回
    """
    if not url:
        return url
    
    # 修复可能存在的双重编码问题
    if '%252F' in url:
        url = url.replace('%252F', '/')
        
    # 检查是否是 OSS 链接（带或不带签名）
    is_oss_url = 'aliyuncs.com' in url or (settings.OSS_URL and settings.OSS_URL in url)
    
    if not is_oss_url:
        # 处理本地相对路径
        if url.startswith('static/') or url.startswith('uploads/'):
            if url.startswith('uploads/'):
                return f"/static/{url}"
            return f"/{url}"
        return url
    
    # 处理 OSS 链接
    # 提取 object_key（去除域名和查询参数）
    object_key = None
    
    if 'aliyuncs.com' in url:
        # 匹配 aliyuncs.com/object_key 或 aliyuncs.com/object_key?params
        match = re.search(r'aliyuncs\.com/([^?]+)', url)
        if match:
            object_key = match.group(1)
    elif settings.OSS_URL and settings.OSS_URL in url:
        # 从自定义域名提取
        prefix = settings.OSS_URL.replace('http://', '').replace('https://', '')
        match = re.search(rf'{re.escape(prefix)}/([^?]+)', url)
        if match:
            object_key = match.group(1)
    
    if not object_key:
        logger.warning(f"Failed to extract object_key from OSS URL: {url}")
        return url
    
    # 解码 object_key（oss2 会自动处理编码）
    object_key = unquote(object_key)
    
    # 如果 URL 已经带签名，检查是否过期
    if 'Signature=' in url:
        from time import time
        expires_match = re.search(r'Expires=(\d+)', url)
        if expires_match:
            expires_timestamp = int(expires_match.group(1))
            current_timestamp = int(time())
            # 如果签名还有超过1小时的有效期，直接返回
            if expires_timestamp > current_timestamp + 3600:
                return url
            # 否则重新生成签名
    
    # 生成新的签名URL
    if oss_uploader.enabled:
        try:
            return oss_uploader.generate_presigned_url(object_key, expires=86400)
        except Exception as e:
            logger.warning(f"Failed to generate presigned URL for {object_key}: {e}")
            return url
    
    return url

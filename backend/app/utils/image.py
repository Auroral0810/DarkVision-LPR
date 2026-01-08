import re
from typing import Optional
from urllib.parse import unquote
from app.config import settings
from app.utils.oss import oss_uploader
from app.core.logger import logger

def get_image_url(url: Optional[str]) -> Optional[str]:
    """
    统一处理图片URL：
    1. 如果是 OSS 链接且属于本项目桶，直接返回其公网 URL
    2. 如果是本地相对路径 (static/uploads/...)，加上后端 HOST 前缀
    3. 否则原样返回
    """
    if not url:
        return url
    
    # 修复可能存在的双重编码问题
    if '%252F' in url:
        url = url.replace('%252F', '/')
        
    # 检查是否是 OSS 链接
    is_oss_url = 'aliyuncs.com' in url or (settings.OSS_URL and settings.OSS_URL in url)
    
    if is_oss_url:
        # 如果是 OSS 链接，且已经带签名，则去除签名部分，只保留基础路径
        if '?' in url and ('Signature=' in url or 'OSSAccessKeyId=' in url):
            return url.split('?')[0]
        return url
        
    # 处理本地相对路径
    if url.startswith('static/') or url.startswith('uploads/'):
        if url.startswith('uploads/'):
            return f"/static/{url}"
        return f"/{url}"
        
    return url

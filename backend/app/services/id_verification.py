import urllib3
import urllib.parse
import json
from typing import Dict, Any, Optional
from app.config import settings
from app.core.logger import logger

class IdVerificationService:
    """实名认证服务（调用阿里云市场接口）"""
    
    def __init__(self):
        self.host = 'https://tscheck2.market.alicloudapi.com'
        self.path = '/idcard'
        self.appcode = settings.ALIYUN_MARKET_APPCODE
        self.http = urllib3.PoolManager()

    def verify_id_card(self, name: str, id_card: str) -> Dict[str, Any]:
        """
        调用阿里云接口核验身份证和姓名是否一致
        
        Args:
            name: 真实姓名
            id_card: 身份证号
            
        Returns:
            Dict: 接口返回的数据
            {
                "success": bool,
                "res": str,  # "1" 一致；"2" 不一致；"3" 无记录
                "description": str,
                "data": dict (原始返回数据)
            }
        """
        if not self.appcode:
            logger.warning("ALIYUN_MARKET_APPCODE not configured, skipping real-name verification")
            return {
                "success": True, 
                "res": "1", 
                "description": "AppCode未配置，默认跳过验证",
                "data": {}
            }

        try:
            # 构造请求URL
            encoded_name = urllib.parse.quote(name)
            querys = f"name={encoded_name}&idcard={id_card}"
            url = f"{self.host}{self.path}?{querys}"
            
            headers = {
                'Authorization': f'APPCODE {self.appcode}'
            }
            
            logger.info(f"Calling Aliyun ID Verification API for {name}")
            response = self.http.request('GET', url, headers=headers)
            
            if response.status != 200:
                logger.error(f"Aliyun ID Verification API failed with status {response.status}: {response.data.decode('utf-8')}")
                return {
                    "success": False,
                    "res": "0",
                    "description": f"接口请求失败 (Status: {response.status})",
                    "data": {}
                }
            
            content = response.data.decode('utf-8')
            res_json = json.loads(content)
            
            # 解析结果
            # {
            #     "code": 1,
            #     "msg": "操作成功",
            #     "data": {
            #         "res": "1",  //核验结果状态码，1 一致；2 不一致；3 无记录
            #         "description": "一致",
            #         ...
            #     }
            # }
            if res_json.get("code") == 1 and "data" in res_json:
                data = res_json["data"]
                verify_res = data.get("res")
                return {
                    "success": verify_res == "1",
                    "res": verify_res,
                    "description": data.get("description", "Unknown"),
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "res": "0",
                    "description": res_json.get("msg", "Unknown error"),
                    "data": res_json
                }
                
        except Exception as e:
            logger.error(f"Error in ID verification: {e}")
            return {
                "success": False,
                "res": "0",
                "description": str(e),
                "data": {}
            }

id_verification_service = IdVerificationService()

# -*- coding: utf-8 -*-
"""
微信小店客服消息API
根据文档：https://developers.weixin.qq.com/doc/store/shop/API/kf/api_sendmsg.html
"""
import httpx
import time
import logging
from config import config

logger = logging.getLogger(__name__)


class WeixinMessage:
    """微信小店客服消息客户端"""

    def __init__(self):
        self.app_id = config.WEIXIN_APP_ID
        self.app_secret = config.WEIXIN_APP_SECRET
        self.access_token = None
        self.token_expire_time = 0
        self.base_url = "https://api.weixin.qq.com"

    def _get_access_token(self):
        """
        获取access_token（微信小店使用公众号的access_token）

        Returns:
            str: access_token
        """
        # 检查是否需要刷新token
        current_time = int(time.time())
        if self.access_token and current_time < self.token_expire_time:
            return self.access_token

        # 获取新的access_token
        url = f"{self.base_url}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }

        try:
            response = httpx.get(url, params=params, timeout=10)
            data = response.json()

            if "access_token" in data:
                self.access_token = data["access_token"]
                # 提前5分钟过期
                self.token_expire_time = current_time + data["expires_in"] - 300
                logger.info(f"获取access_token成功，过期时间: {self.token_expire_time}")
                return self.access_token
            else:
                logger.error(f"获取access_token失败: {data}")
                return None

        except Exception as e:
            logger.error(f"获取access_token异常: {e}")
            return None

    def send_text(self, to_user: str, text: str) -> bool:
        """
        发送文本客服消息（微信小店API）

        Args:
            to_user: 接收用户的openid
            text: 文本内容

        Returns:
            bool: 发送是否成功
        """
        access_token = self._get_access_token()
        if not access_token:
            logger.error("无法获取access_token")
            return False

        # 使用微信小店客服消息API
        url = f"{self.base_url}/shop/kf/message/send?access_token={access_token}"

        data = {
            "touser": to_user,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }

        try:
            response = httpx.post(url, json=data, timeout=10)
            result = response.json()

            if result.get("errcode") == 0:
                logger.info(f"发送客服消息成功: to_user={to_user}, text={text[:50]}...")
                return True
            else:
                logger.error(f"发送客服消息失败: {result}")
                return False

        except Exception as e:
            logger.error(f"发送客服消息异常: {e}")
            return False


# 全局实例
weixin_message = WeixinMessage()

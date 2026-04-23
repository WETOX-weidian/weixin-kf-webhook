"""
扣子API客户端
"""
import httpx
import os
from typing import Dict, Any, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CozeClient:
    """扣子API客户端（Bot Chat API）"""

    def __init__(self):
        """初始化"""
        self.api_url = os.getenv("COZE_API_URL", "https://api.coze.cn/v3/chat")
        self.api_key = os.getenv("COZE_API_KEY", "")
        self.bot_id = os.getenv("COZE_BOT_ID", "")
        self.timeout = 15  # 15秒超时

        if not all([self.api_url, self.api_key, self.bot_id]):
            logger.warning("⚠️  扣子API配置不完整")

    async def call_chat(
        self,
        user_input: str,
        user_id: str,
        additional_messages: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        调用扣子 Bot Chat API

        Args:
            user_input: 用户输入
            user_id: 用户ID
            additional_messages: 额外的历史消息

        Returns:
            响应结果
        """
        if not all([self.api_url, self.api_key, self.bot_id]):
            raise ValueError("扣子API配置不完整")

        # 构建消息列表
        messages = []

        # 添加历史消息（如果有）
        if additional_messages:
            messages.extend(additional_messages)

        # 添加当前消息
        messages.append({
            "content": user_input,
            "content_type": "text",
            "role": "user",
            "type": "question"
        })

        # 构建请求参数
        payload = {
            "bot_id": self.bot_id,
            "user_id": user_id,
            "stream": False,  # 非流式响应
            "additional_messages": messages
        }

        # 发送请求
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                result = response.json()

                logger.info(f"✅ 扣子API调用成功: conversation_id={result.get('conversation_id')}")

                return result

            except httpx.HTTPError as e:
                logger.error(f"❌ 扣子API调用失败: {e}")
                raise

            except Exception as e:
                logger.error(f"❌ 扣子API处理失败: {e}")
                raise


# 全局单例
coze_client = CozeClient()

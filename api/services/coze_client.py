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
        self.timeout = 30  # 30秒超时

        if not all([self.api_url, self.api_key, self.bot_id]):
            logger.warning("⚠️  扣子API配置不完整")

    def call_chat(
        self,
        user_input: str,
        user_id: str,
        additional_messages: Optional[list] = None
    ) -> str:
        """
        调用扣子 Bot Chat API（同步方法）

        Args:
            user_input: 用户输入
            user_id: 用户ID
            additional_messages: 额外的历史消息

        Returns:
            str: AI回复内容
        """
        if not all([self.api_url, self.api_key, self.bot_id]):
            logger.error("扣子API配置不完整")
            return "抱歉，服务配置错误"

        # 构建请求参数
        payload = {
            "bot_id": self.bot_id,
            "user_id": user_id,
            "stream": False,  # 非流式响应
            "additional_messages": [
                {
                    "content": user_input,
                    "content_type": "text",
                    "role": "user",
                    "type": "question"
                }
            ]
        }

        # 如果有历史消息，添加到前面
        if additional_messages:
            payload["additional_messages"] = additional_messages + payload["additional_messages"]

        # 发送请求
        try:
            with httpx.Client(timeout=self.timeout) as client:
                # 使用不同的Authorization header格式
                response = client.post(
                    self.api_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    }
                )
                result = response.json()

                logger.info(f"✅ 扣子API调用响应: {result}")

                # 检查是否有错误
                if result.get("code") != 0:
                    error_msg = result.get("msg", "未知错误")
                    logger.error(f"❌ 扣子API返回错误: code={result.get('code')}, msg={error_msg}")
                    return f"抱歉，AI服务错误: {error_msg}"

                # 解析响应，提取AI回复内容
                data = result.get("data", {})
                if data and "answer" in data:
                    return data["answer"]

                # 尝试其他可能的字段
                if "messages" in result:
                    messages = result["messages"]
                    for msg in reversed(messages):
                        if msg.get("role") == "assistant" and msg.get("content"):
                            return msg.get("content")

                logger.warning(f"扣子API返回格式异常: {result}")
                return "抱歉，AI回复格式错误"

        except httpx.HTTPError as e:
            logger.error(f"❌ 扣子API调用失败: {e}")
            return f"抱歉，调用AI服务失败: {str(e)}"

        except Exception as e:
            logger.error(f"❌ 扣子API处理失败: {e}")
            return f"抱歉，服务异常: {str(e)}"


# 全局单例
coze_client = CozeClient()

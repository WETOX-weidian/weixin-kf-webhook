"""
扣子API客户端（临时简化版）
"""
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CozeClient:
    """扣子API客户端（临时使用规则回复）"""

    def __init__(self):
        """初始化"""
        logger.warning("⚠️  当前使用规则回复系统，未连接到AI")

    def call_chat(
        self,
        user_input: str,
        user_id: str,
        additional_messages: Optional[list] = None
    ) -> str:
        """
        调用客服AI（临时使用规则回复）

        Args:
            user_input: 用户输入
            user_id: 用户ID
            additional_messages: 额外的历史消息

        Returns:
            str: AI回复内容
        """
        logger.info(f"用户消息: {user_input}")

        # 简单的规则回复系统
        responses = {
            "你好": "您好！我是智能客服，很高兴为您服务！有什么我可以帮助您的吗？",
            "在吗": "我在的！请问有什么可以帮您的吗？",
            "价格": "关于价格问题，请告诉我您想了解哪个产品，我会为您详细介绍。",
            "购买": "您可以通过我们的小程序直接购买，或者联系我们的销售团队了解更多详情。",
            "售后": "关于售后问题，我们提供7天无理由退换货和1年质保服务。有任何问题都可以联系我们的售后团队。",
            "订单": "关于订单查询，请提供您的订单号，我会帮您查询订单状态。"
        }

        # 查找匹配的关键词
        for keyword, response in responses.items():
            if keyword in user_input:
                logger.info(f"匹配关键词: {keyword}")
                return response

        # 默认回复
        default_response = "感谢您的咨询！我已收到您的消息，稍后会有专员为您详细解答。或者您可以尝试询问关于价格、购买、售后、订单等问题。"
        logger.info(f"使用默认回复")
        return default_response


# 全局单例
coze_client = CozeClient()

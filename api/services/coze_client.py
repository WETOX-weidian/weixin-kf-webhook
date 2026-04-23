"""
扣子工作流API客户端
"""
import json
import httpx
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_sse_response(response_text: str) -> str:
    """
    解析SSE流式响应，提取完整的AI回复

    Args:
        response_text: SSE响应文本

    Returns:
        str: 完整的AI回复
    """
    full_answer = ""
    lines = response_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('data: '):
            json_str = line[6:]  # 去掉 "data: " 前缀
            try:
                data = json.loads(json_str)
                if data.get('type') == 'answer':
                    answer = data.get('content', {}).get('answer')
                    if answer:
                        full_answer += answer
            except json.JSONDecodeError:
                continue

    return full_answer


class CozeClient:
    """扣子工作流API客户端"""

    def __init__(self, workflow_url: str, jwt_token: str):
        """
        初始化

        Args:
            workflow_url: 工作流API URL
            jwt_token: JWT认证Token
        """
        self.workflow_url = workflow_url
        self.jwt_token = jwt_token
        logger.info("✅ 扣子工作流API客户端初始化成功")

    def call_chat(
        self,
        user_input: str,
        user_id: str,
        additional_messages: Optional[list] = None
    ) -> str:
        """
        调用工作流API获取AI回复

        Args:
            user_input: 用户输入
            user_id: 用户ID
            additional_messages: 额外的历史消息（暂不支持）

        Returns:
            str: AI回复内容
        """
        logger.info(f"用户[{user_id}]消息: {user_input}")

        try:
            # 调用工作流API（使用httpx）
            with httpx.Client(timeout=60) as client:
                response = client.post(
                    self.workflow_url,
                    json={
                        "input": user_input,
                        "stream": False
                    },
                    headers={
                        "Authorization": f"Bearer {self.jwt_token}",
                        "Content-Type": "application/json"
                    }
                )

            if response.status_code != 200:
                logger.error(f"工作流API调用失败: {response.status_code} - {response.text}")
                return "抱歉，AI服务暂时不可用，请稍后再试。"

            # 解析SSE响应
            full_answer = parse_sse_response(response.text)

            if not full_answer:
                logger.warning("工作流API返回空回复")
                return "抱歉，我暂时无法理解您的问题，请换个方式提问。"

            logger.info(f"AI回复: {full_answer[:100]}...")
            return full_answer

        except httpx.TimeoutException:
            logger.error("工作流API调用超时")
            return "抱歉，服务响应超时，请稍后再试。"
        except Exception as e:
            logger.error(f"工作流API调用异常: {e}")
            return "抱歉，AI服务出现异常，请稍后再试。"


# 全局单例（延迟初始化）
coze_client: Optional[CozeClient] = None


def init_coze_client(workflow_url: str, jwt_token: str) -> CozeClient:
    """
    初始化全局CozeClient单例

    Args:
        workflow_url: 工作流API URL
        jwt_token: JWT认证Token

    Returns:
        CozeClient: 客户端实例
    """
    global coze_client
    coze_client = CozeClient(workflow_url, jwt_token)
    return coze_client

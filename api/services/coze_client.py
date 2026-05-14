#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唯电宝客服API客户端
使用本地知识库实现问答，不再依赖外部工作流API
"""

import logging
from typing import Optional
from .wetox_knowledge import WetoXKnowledgeBase

logger = logging.getLogger(__name__)


class WetoXCozeClient:
    """唯电宝客服客户端"""
    
    def __init__(self):
        """初始化知识库"""
        self.knowledge = WetoXKnowledgeBase()
        logger.info("唯电宝知识库初始化完成")
    
    def call_chat(self, user_input: str, user_id: str, additional_messages=None) -> str:
        """
        调用对话
        
        Args:
            user_input: 用户输入
            user_id: 用户ID（用于上下文）
            additional_messages: 额外的消息历史（可选）
        
        Returns:
            str: AI回复内容
        """
        logger.info(f"用户[{user_id}]消息: {user_input}")
        
        try:
            # 从additional_messages获取上下文
            context = {}
            if additional_messages:
                for msg in additional_messages[-6:]:  # 取最近3轮对话
                    content = msg.get("content", "")
                    if isinstance(content, str):
                        # 尝试从历史中提取产品信息
                        if "2mini" in content:
                            context["product"] = "2mini"
                        elif "2代" in content or "唯电宝2代" in content:
                            context["product"] = "2"
                        elif "AC" in content or "交流" in content:
                            context["product"] = "AC"
            
            # 生成回复
            result = self.knowledge.generate_response(user_input, context)
            
            response = result["response"]
            logger.info(f"AI回复: {response}")
            
            if result.get("need_product"):
                logger.info("回复需要产品信息")
            
            if result.get("need_car"):
                logger.info("回复需要车型信息")
            
            return response
            
        except Exception as e:
            logger.error(f"知识库调用异常: {str(e)}")
            return "亲，抱歉，AI服务出现异常，请稍后再试呢～"
    
    def init_client(self) -> bool:
        """初始化客户端"""
        try:
            logger.info("唯电宝客服客户端初始化")
            return True
        except Exception as e:
            logger.error(f"初始化失败: {str(e)}")
            return False


# 全局实例
_client = None


def init_coze_client():
    """初始化并返回客户端实例"""
    global _client
    if _client is None:
        _client = WetoXCozeClient()
        _client.init_client()
    return _client


def get_coze_client():
    """获取客户端实例"""
    global _client
    if _client is None:
        return init_coze_client()
    return _client

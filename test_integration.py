#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Flask应用和扣子工作流API
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from config import config
from services.coze_client import init_coze_client

print("="*60)
print("测试扣子工作流API集成")
print("="*60)

# 验证配置
if not config.validate():
    print("❌ 配置验证失败")
    sys.exit(1)

print("✅ 配置验证成功")

# 初始化扣子客户端
coze = init_coze_client(
    workflow_url=config.COZE_WORKFLOW_URL,
    jwt_token=config.COZE_JWT_TOKEN
)

# 测试调用
print("\n测试问题1: '你好'")
response = coze.call_chat("你好", "test_user_001")
print(f"回复: {response}")

print("\n测试问题2: '什么是人工智能'")
response = coze.call_chat("什么是人工智能", "test_user_001")
print(f"回复: {response}")

print("\n测试问题3: '怎么购买'")
response = coze.call_chat("怎么购买", "test_user_001")
print(f"回复: {response}")

print("\n✅ 所有测试完成！")

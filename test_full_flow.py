#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信客服消息完整流程
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from config import config
from services.coze_client import init_coze_client
from services.weixin_message import weixin_message

print("="*60)
print("微信客服消息完整流程测试")
print("="*60)

# 验证配置
print("\n【步骤1】验证配置")
if not config.validate():
    print("❌ 配置验证失败")
    sys.exit(1)
print("✅ 配置验证成功")

# 初始化扣子客户端
print("\n【步骤2】初始化扣子客户端")
coze = init_coze_client(
    workflow_url=config.COZE_WORKFLOW_URL,
    jwt_token=config.COZE_JWT_TOKEN
)
print("✅ 扣子客户端初始化成功")

# 测试AI调用
print("\n【步骤3】测试AI调用")
test_message = "你好"
print(f"发送测试消息: {test_message}")

ai_response = coze.call_chat(test_message, "test_user")
print(f"AI回复: {ai_response}")

if not ai_response:
    print("❌ AI调用失败")
    sys.exit(1)
print("✅ AI调用成功")

# 测试客服消息发送
print("\n【步骤4】测试客服消息发送")
print("注意：这需要有效的微信用户openid")
print("从之前的日志中获取的openid: ooFOb4tyiiL600BUj-VsqreyodGE")

test_openid = "ooFOb4tyiiL600BUj-VsqreyodGE"
print(f"\n尝试发送客服消息到: {test_openid}")
print(f"消息内容: {ai_response[:50]}...")

success = weixin_message.send_text(test_openid, ai_response)

if success:
    print("\n✅✅✅ 客服消息发送成功！")
    print("请检查微信是否收到消息")
else:
    print("\n❌ 客服消息发送失败")
    print("\n可能的原因：")
    print("1. 微信小店自研客服配置未生效（需要等待几分钟）")
    print("2. 需要额外的店铺ID或客服账号参数")
    print("3. API端点或参数格式需要调整")
    print("\n请查看上面的错误日志获取详细信息")

print("\n" + "="*60)
print("测试完成")
print("="*60)

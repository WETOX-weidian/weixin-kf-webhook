#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据微信小店文档分析回调机制
"""
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

ctx = new_context(method='search.web')
client = SearchClient(ctx=ctx)

print("="*60)
print("分析微信小店客服消息回调机制")
print("="*60)

# 搜索1：微信小店客服消息回调
print("\n搜索1：微信小店客服消息回调机制")
response = client.web_search(
    query='site:developers.weixin.qq.com 微信小店 客服消息 被动回复',
    count=3,
    need_summary=True
)

print(f"AI Summary: {response.summary}\n")
for i, item in enumerate(response.web_items[:2], 1):
    print(f"{i}. {item.title}")
    print(f"   {item.snippet[:200]}...\n")

# 搜索2：微信小店API发送消息
print("搜索2：微信小店客服消息API发送")
response = client.web_search(
    query='微信小店 /shop/kf/message/send 被动回复 无法收到消息',
    count=3,
    need_summary=True
)

print(f"AI Summary: {response.summary}\n")
for i, item in enumerate(response.web_items[:2], 1):
    print(f"{i}. {item.title}")
    print(f"   {item.snippet[:200]}...\n")

# 搜索3：微信小店客服消息必须返回success
print("搜索3：微信小店客服消息 必须返回success")
response = client.web_search(
    query='微信小店客服消息 5秒内返回success 被动回复',
    count=3,
    need_summary=True
)

print(f"AI Summary: {response.summary}\n")
for i, item in enumerate(response.web_items[:2], 1):
    print(f"{i}. {item.title}")
    print(f"   {item.snippet[:200]}...\n")

print("="*60)
print("关键发现：")
print("="*60)
print("根据搜索结果和文档分析：")
print("1. 微信小店的客服消息回调可能需要5秒内返回success")
print("2. 微信小店可能不支持被动回复，必须使用API主动发送")
print("3. 需要在返回success后，异步调用客服消息API发送回复")
print("="*60)

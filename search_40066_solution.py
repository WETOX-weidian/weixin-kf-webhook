#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索微信小店客服消息API 40066 错误的解决方案
"""
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context

ctx = new_context(method='search.web')
client = SearchClient(ctx=ctx)

print("="*60)
print("搜索微信小店客服消息API 40066 错误解决方案")
print("="*60)

# 搜索1：40066错误的具体含义
print("\n搜索1：微信API 40066 invalid url 错误码含义")
response = client.web_search(
    query='微信API 40066 invalid url 错误码 含义 解决方案',
    count=3,
    need_summary=True
)

print(f"AI Summary: {response.summary}\n")
for i, item in enumerate(response.web_items[:2], 1):
    print(f"{i}. {item.title}")
    print(f"   {item.snippet[:300]}...\n")

# 搜索2：微信小店客服消息API的正确调用方式
print("搜索2：微信小店客服消息API 如何正确调用")
response = client.web_search(
    query='微信小店 客服消息 API shopid 店铺ID 正确调用方式',
    count=3,
    need_summary=True
)

print(f"AI Summary: {response.summary}\n")
for i, item in enumerate(response.web_items[:2], 1):
    print(f"{i}. {item.title}")
    print(f"   {item.snippet[:300]}...\n")

# 搜索3：微信小程序客服消息的替代方案
print("搜索3：微信小程序 客服消息 替代方案 订阅消息")
response = client.web_search(
    query='微信小程序 客服消息 40066 使用订阅消息替代',
    count=3,
    need_summary=True
)

print(f"AI Summary: {response.summary}\n")
for i, item in enumerate(response.web_items[:2], 1):
    print(f"{i}. {item.title}")
    print(f"   {item.snippet[:300]}...\n")

print("="*60)
print("结论：")
print("="*60)
print("根据搜索结果，40066错误可能的原因：")
print("1. API端点不正确或已废弃")
print("2. 需要特殊的店铺ID或客服账号ID")
print("3. 需要在微信小店后台开启特殊权限")
print("4. 客服消息API可能不适用于所有场景")
print("\n建议：")
print("- 在微信小店后台查找API配置说明")
print("- 联系微信官方客服获取正确调用方式")
print("- 考虑使用订阅消息作为替代方案")
print("="*60)

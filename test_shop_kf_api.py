#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信小店自研客服消息的正确调用方式
根据实际文档和社区经验
"""
import httpx
import json

# 微信配置
app_id = "wx6d76fe7674ec5657"
app_secret = "e0ed88e6b89e4e1319dc220223b3096b"

# 获取access_token
token_url = f"https://api.weixin.qq.com/cgi-bin/token"
params = {
    "grant_type": "client_credential",
    "appid": app_id,
    "secret": app_secret
}

response = httpx.get(token_url, params=params, timeout=10)
token_data = response.json()

if "access_token" not in token_data:
    print(f"❌ 获取access_token失败: {token_data}")
    exit(1)

access_token = token_data["access_token"]
print(f"✅ access_token: {access_token[:20]}...")

test_openid = "ooFOb4tyiiL600BUj-VsqreyodGE"

# 根据微信小店文档，可能需要不同的参数
print("\n" + "="*60)
print("测试微信小店自研客服消息")
print("="*60)

# 尝试1: 使用完整的shop kf message/send（可能需要shopid）
print("\n尝试1: 添加shopid参数")
url = f"https://api.weixin.qq.com/shop/kf/message/send?access_token={access_token}"

# 尝试获取店铺ID（可能需要从配置中获取）
# 这里先尝试一些可能的shopid格式
data = {
    "shopid": "default",  # 可能的默认值
    "touser": test_openid,
    "msgtype": "text",
    "text": {
        "content": "测试消息1"
    }
}

response = httpx.post(url, json=data, timeout=10)
print(f"响应: {response.json()}")

# 尝试2: 使用wxa/business/kf/send（小程序客服）
print("\n尝试2: 使用小程序客服API")
url = f"https://api.weixin.qq.com/wxa/business/kf/send?access_token={access_token}"

data = {
    "touser": test_openid,
    "msgtype": "text",
    "text": {
        "content": "测试消息2"
    }
}

response = httpx.post(url, json=data, timeout=10)
print(f"响应: {response.json()}")

# 尝试3: 查看微信小店是否有特殊的端点
print("\n尝试3: 尝试其他可能的端点")
endpoints_to_try = [
    "https://api.weixin.qq.com/shop/kf/account/send",  # 可能是客服账号相关
    "https://api.weixin.qq.com/shop/kf/sendmsg",       # 可能是sendmsg
]

for endpoint in endpoints_to_try:
    print(f"\n测试端点: {endpoint}")
    url = f"{endpoint}?access_token={access_token}"
    data = {
        "touser": test_openid,
        "msgtype": "text",
        "text": {
            "content": "测试消息"
        }
    }
    try:
        response = httpx.post(url, json=data, timeout=10)
        result = response.json()
        print(f"errcode: {result.get('errcode')}, errmsg: {result.get('errmsg')}")

        if result.get("errcode") == 0:
            print(f"✅✅✅ 成功！正确的端点: {endpoint}")
            break
    except Exception as e:
        print(f"异常: {e}")

print("\n" + "="*60)
print("如果所有尝试都失败，说明：")
print("1. 微信小店客服消息API可能需要特殊的授权流程")
print("2. 可能需要使用不同的认证方式（不是access_token）")
print("3. 可能需要在微信小店后台获取额外的API密钥")
print("\n建议：")
print("- 查看微信小店管理后台的'自研客服'配置页面")
print("- 查找是否有'API密钥'或'授权码'等配置")
print("- 联系微信客服获取正确的调用方式")
print("="*60)

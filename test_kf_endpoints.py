#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据微信小店文档测试客服消息API
"""
import httpx
import json

# 微信配置
app_id = "wx6d76fe7674ec5657"
app_secret = "e0ed88e6b89e4e1319dc220223b3096b"

# 测试不同的API端点
endpoints = [
    # 1. 公众号客服消息（之前使用的）
    "https://api.weixin.qq.com/cgi-bin/message/custom/send",
    # 2. 微信小店客服消息（当前使用的）
    "https://api.weixin.qq.com/shop/kf/message/send",
    # 3. 可能的其他端点
    "https://api.weixin.qq.com/cgi-bin/message/custom/send",
    "https://api.weixin.qq.com/shop/kf/send",
    "https://api.weixin.qq.com/wxa/business/kf/send",
]

# 先获取access_token
print("="*60)
print("获取 access_token")
print("="*60)

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
print(f"✅ 获取access_token成功: {access_token[:20]}...")
print()

# 测试不同端点
print("="*60)
print("测试不同的客服消息API端点")
print("="*60)

test_openid = "ooFOb4tyiiL600BUj-VsqreyodGE"  # 从日志中获取的openid
test_message = "这是一条测试消息"

for i, base_url in enumerate(endpoints, 1):
    print(f"\n测试端点 {i}: {base_url}")
    print("-" * 60)

    url = f"{base_url}?access_token={access_token}"
    data = {
        "touser": test_openid,
        "msgtype": "text",
        "text": {
            "content": test_message
        }
    }

    try:
        response = httpx.post(url, json=data, timeout=10)
        result = response.json()

        errcode = result.get("errcode", "N/A")
        errmsg = result.get("errmsg", "N/A")

        print(f"errcode: {errcode}")
        print(f"errmsg: {errmsg}")

        if errcode == 0:
            print(f"✅✅✅ 端点 {i} 成功！")
            print(f"正确的端点: {base_url}")
            break
        else:
            print(f"❌ 端点 {i} 失败")

    except Exception as e:
        print(f"❌ 请求异常: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)

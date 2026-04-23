#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用微信小店 AppSecret 调用客服消息API
"""
import httpx
import json

# 微信小店配置（新提供的）
app_id = "wx6d76fe7674ec5657"
app_secret = "b54b2e7b1411ce20e858dfc44f1d7761"

# 获取access_token
print("="*60)
print("使用微信小店 AppSecret 测试客服消息API")
print("="*60)

token_url = f"https://api.weixin.qq.com/cgi-bin/token"
params = {
    "grant_type": "client_credential",
    "appid": app_id,
    "secret": app_secret
}

response = httpx.get(token_url, params=params, timeout=10)
token_data = response.json()

print(f"\n获取 access_token 响应:")
print(json.dumps(token_data, ensure_ascii=False, indent=2))

if "access_token" not in token_data:
    print(f"\n❌ 获取access_token失败")
    print(f"错误: {token_data}")
    exit(1)

access_token = token_data["access_token"]
print(f"\n✅ access_token 获取成功: {access_token[:20]}...")

# 测试客服消息发送
test_openid = "ooFOb4tyiiL600BUj-VsqreyodGE"

print("\n" + "="*60)
print("测试客服消息API")
print("="*60)

# 尝试不同的端点
endpoints = [
    "https://api.weixin.qq.com/shop/kf/message/send",
    "https://api.weixin.qq.com/cgi-bin/message/custom/send",
    "https://api.weixin.qq.com/wxa/business/kf/send",
]

for i, base_url in enumerate(endpoints, 1):
    print(f"\n测试端点 {i}: {base_url}")
    print("-" * 60)

    url = f"{base_url}?access_token={access_token}"
    data = {
        "touser": test_openid,
        "msgtype": "text",
        "text": {
            "content": "测试消息（使用微信小店AppSecret）"
        }
    }

    try:
        response = httpx.post(url, json=data, timeout=10)
        result = response.json()

        errcode = result.get("errcode")
        errmsg = result.get("errmsg")

        print(f"errcode: {errcode}")
        print(f"errmsg: {errmsg}")
        print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if errcode == 0:
            print(f"\n✅✅✅ 成功！正确的端点和配置：")
            print(f"   AppID: {app_id}")
            print(f"   AppSecret: {app_secret}")
            print(f"   API端点: {base_url}")
            print(f"\n请检查微信是否收到测试消息！")
            break
        else:
            print(f"❌ 端点 {i} 失败")

    except Exception as e:
        print(f"❌ 请求异常: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)

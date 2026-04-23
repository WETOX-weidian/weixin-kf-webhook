#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信小店自研客服API的正确参数格式
根据文档：https://developers.weixin.qq.com/doc/store/shop/API/kf/api_sendmsg.html
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

# 测试不同的请求格式
print("\n" + "="*60)
print("测试不同的请求格式")
print("="*60)

# 格式1: 标准格式（当前使用的）
print("\n格式1: 标准格式")
url = f"https://api.weixin.qq.com/shop/kf/message/send?access_token={access_token}"
data1 = {
    "touser": test_openid,
    "msgtype": "text",
    "text": {
        "content": "测试消息1"
    }
}
response = httpx.post(url, json=data1, timeout=10)
print(f"响应: {response.json()}")

# 格式2: 添加KfAccount字段（可能需要）
print("\n格式2: 添加KfAccount字段")
data2 = {
    "touser": test_openid,
    "kf_account": "kf001@gh_7ebcb1d52687",  # 可能需要客服账号
    "msgtype": "text",
    "text": {
        "content": "测试消息2"
    }
}
response = httpx.post(url, json=data2, timeout=10)
print(f"响应: {response.json()}")

# 格式3: 尝试JSON字符串（某些API要求）
print("\n格式3: JSON字符串格式")
import json
data3 = json.dumps({
    "touser": test_openid,
    "msgtype": "text",
    "text": {
        "content": "测试消息3"
    }
})
response = httpx.post(url, data=data3, headers={"Content-Type": "application/json"}, timeout=10)
print(f"响应: {response.json()}")

# 格式4: 检查是否需要其他必需参数（如shopid）
print("\n格式4: 添加shopid参数（可能需要）")
data4 = {
    "shopid": "shop_12345678",  # 可能需要店铺ID
    "touser": test_openid,
    "msgtype": "text",
    "text": {
        "content": "测试消息4"
    }
}
response = httpx.post(url, json=data4, timeout=10)
print(f"响应: {response.json()}")

print("\n" + "="*60)
print("如果所有格式都失败，可能的原因：")
print("1. 微信小店未开启'自研客服'功能")
print("2. 需要在微信小店后台配置客服权限")
print("3. API端点或参数格式与文档不符")
print("4. 需要特殊的认证方式或权限")
print("="*60)

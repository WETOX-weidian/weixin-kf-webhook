import requests
import json

# OAuth2 凭证
client_id = "14551257602322566430629311570220.app.coze"
client_secret = "iqXx6ftNWLVBsqFgGwD8k9tiW5xDE3hNNPZ3kyF3AbtUb6yc"

# 尝试不同的OAuth2端点
endpoints = [
    "https://api.coze.cn/api/open-auth/oauth2/access_token",
    "https://api.coze.cn/open_api/v2/oauth/token",
    "https://api.coze.cn/v1/auth/oauth2/access_token",
    "https://api.coze.cn/oauth/token",
    "https://api.coze.cn/open_api/oauth2/access_token"
]

for endpoint in endpoints:
    print(f"\n尝试端点: {endpoint}")

    # 方法1: POST JSON
    try:
        response = requests.post(
            endpoint,
            json={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"  响应: {response.text[:500]}")
            data = response.json()
            if "access_token" in data:
                print(f"\n✅ 找到正确的端点!")
                print(f"Access Token: {data['access_token']}")
                break
        elif response.status_code != 404:
            print(f"  响应: {response.text[:200]}")
    except Exception as e:
        print(f"  错误: {e}")

    # 方法2: POST Form URL Encoded
    try:
        response = requests.post(
            endpoint,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        print(f"  状态码 (form): {response.status_code}")
        if response.status_code == 200:
            print(f"  响应: {response.text[:500]}")
            data = response.json()
            if "access_token" in data:
                print(f"\n✅ 找到正确的端点!")
                print(f"Access Token: {data['access_token']}")
                break
    except Exception as e:
        print(f"  错误 (form): {e}")

print("\n完成")

import requests
import json
import base64

# OAuth2 凭证
client_id = "14551257602322566430629311570220.app.coze"
client_secret = "iqXx6ftNWLVBsqFgGwD8k9tiW5xDE3hNNPZ3kyF3AbtUb6yc"

# 尝试不同的IAM OAuth端点
endpoints = [
    ("IAM OAuth", "https://api.coze.cn/api/iam/oauth/token"),
    ("Open Auth", "https://api.coze.cn/open_api/v2/oauth/token"),
    ("Auth OAuth2", "https://api.coze.cn/api/open-auth/oauth2/access_token")
]

for name, endpoint in endpoints:
    print(f"\n{'='*60}")
    print(f"尝试: {name}")
    print(f"端点: {endpoint}")
    print(f"{'='*60}")

    # 方法1: Basic Auth
    auth_string = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()

    try:
        response = requests.post(
            endpoint,
            json={"grant_type": "client_credentials"},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {b64_auth}"
            },
            timeout=10
        )
        print(f"✓ Basic Auth - 状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  响应: {json.dumps(data, ensure_ascii=False, indent=2)[:300]}")
            if "access_token" in data:
                print(f"\n✅✅✅ 成功获取Token! ✅✅✅")
                print(f"Access Token: {data['access_token']}")
                print(f"Token类型: {data.get('token_type', 'Bearer')}")
                print(f"过期时间: {data.get('expires_in', 'N/A')}秒")
                break
        elif response.status_code != 404:
            print(f"  错误: {response.text[:200]}")
    except Exception as e:
        print(f"✗ Basic Auth - 错误: {e}")

    # 方法2: Form with credentials in body
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
        print(f"✓ Form Body - 状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  响应: {json.dumps(data, ensure_ascii=False, indent=2)[:300]}")
            if "access_token" in data:
                print(f"\n✅✅✅ 成功获取Token! ✅✅✅")
                print(f"Access Token: {data['access_token']}")
                print(f"Token类型: {data.get('token_type', 'Bearer')}")
                print(f"过期时间: {data.get('expires_in', 'N/A')}秒")
                break
        elif response.status_code != 404:
            print(f"  错误: {response.text[:200]}")
    except Exception as e:
        print(f"✗ Form Body - 错误: {e}")

print("\n" + "="*60)
print("测试完成")
print("="*60)

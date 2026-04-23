import requests
import json
import base64

# OAuth2 凭证
client_id = "14551257602322566430629311570220.app.coze"
client_secret = "iqXx6ftNWLVBsqFgGwD8k9tiW5xDE3hNNPZ3kyF3AbtUb6yc"

print("="*60)
print("测试OAuth2应用是否已激活")
print("="*60)
print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret[:20]}...\n")

# 编码Basic Auth
auth_string = f"{client_id}:{client_secret}"
b64_auth = base64.b64encode(auth_string.encode()).decode()

# 尝试获取Access Token
endpoint = "https://api.coze.cn/api/iam/oauth/token"

print("尝试获取Access Token...")
print(f"端点: {endpoint}")
print(f"认证: Basic {b64_auth[:20]}...\n")

response = requests.post(
    endpoint,
    json={"grant_type": "client_credentials"},
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Basic {b64_auth}"
    },
    timeout=30
)

print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

if response.status_code == 200:
    data = response.json()
    if "access_token" in data:
        print(f"\n✅✅✅ 成功获取Access Token! ✅✅✅")
        print(f"Access Token: {data['access_token']}")
        print(f"Token类型: {data.get('token_type', 'Bearer')}")
        print(f"过期时间: {data.get('expires_in', 'N/A')}秒")

        # 立即测试使用这个Token调用Bot Chat API
        print(f"\n{'='*60}")
        print("测试使用OAuth2 Access Token调用Bot Chat API")
        print(f"{'='*60}")

        access_token = data['access_token']
        bot_id = "7631814381948420148"

        response2 = requests.post(
            "https://api.coze.cn/v3/chat",
            json={
                "bot_id": bot_id,
                "user_id": "test_oauth_user",
                "stream": False,
                "additional_messages": [
                    {
                        "role": "user",
                        "content": "你好，测试OAuth2认证",
                        "content_type": "text"
                    }
                ]
            },
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        print(f"\n状态码: {response2.status_code}")
        result = response2.json()
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

        if result.get("code") == 0:
            print(f"\n🎉🎉🎉 成功! AI回复: {result.get('data', {}).get('answer', 'N/A')[:100]}")
        else:
            print(f"\n❌ 失败: code={result.get('code')}, msg={result.get('msg')}")
else:
    print(f"\n❌ OAuth2应用可能未激活或配置错误")

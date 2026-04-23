import requests
import base64

# OAuth2 凭证
client_id = "14551257602322566430629311570220.app.coze"
client_secret = "iqXx6ftNWLVBsqFgGwD8k9tiW5xDE3hNNPZ3kyF3AbtUb6yc"

# 编码 Basic Auth
auth_string = f"{client_id}:{client_secret}"
b64_auth = base64.b64encode(auth_string.encode()).decode()

endpoint = "https://api.coze.cn/api/open-auth/oauth2/access_token"

# 尝试不同的请求格式

# 方法1: Basic Auth + JSON
print("方法1: Basic Auth + JSON")
response = requests.post(
    endpoint,
    json={"grant_type": "client_credentials"},
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Basic {b64_auth}"
    },
    timeout=10
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

if response.status_code == 200:
    data = response.json()
    if "access_token" in data:
        print(f"✅ Access Token: {data['access_token']}")

# 方法2: Basic Auth + Form URL Encoded
print("方法2: Basic Auth + Form")
response = requests.post(
    endpoint,
    data={"grant_type": "client_credentials"},
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_auth}"
    },
    timeout=10
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

if response.status_code == 200:
    data = response.json()
    if "access_token" in data:
        print(f"✅ Access Token: {data['access_token']}")

# 方法3: 将凭证放在body中
print("方法3: 凭证在body + Form")
response = requests.post(
    endpoint,
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    },
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    },
    timeout=10
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

if response.status_code == 200:
    data = response.json()
    if "access_token" in data:
        print(f"✅ Access Token: {data['access_token']}")

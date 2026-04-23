import requests
import json

# JWT Token
jwt_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRhODQyODA2LWQwZGYtNDlmYS05ZDAxLWNhM2MyNDJkMWUyNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkNWWk1Fdkc4OXY3d2gzMlhNaWxhVlZLd3ZGQjVhZEhMIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2OTQ1NDY2LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI4NjA4Mzk2MDEwMTkyOTIyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjMxOTIyNjYzOTM3NTQwMTIyIn0.mFSK0hO0eD2uSDPjS94BYoW6NpWNOXlr1oXgQ8nw5ph4y6TPCkn1oQjNiIoPgNzTTAUyf72mTVn3oWzqRHys4umjHm2QuNIgsVAdlYBUTWARJutHaJsTl8rHxZmFMHwqkv8vz7R5Kjo-SdpdLSSKZVwvMtOFTARkw9jxYOKPTtMBE9MR8k_TXdWUx73RwrO_DKUXbtO74RL1pBTHw-ZtttxAuK9G11huSAZn2E0ry-Bi6AI21_lV_HJhEJwYp870fdzdL2nPILdamM7Ye18bL-ZOUBOPQSI7lJmINmDjztyONP9F2n2629fk7pL8mEmw0WWqBp3XXnVE3292EKt-5Q"

# 工作流端点
workflow_url = "https://z2f493xmnp.coze.site/stream_run"

print("="*60)
print("测试使用JWT Token调用工作流API")
print("="*60)
print(f"Token: {jwt_token[:50]}...")
print(f"端点: {workflow_url}\n")

# 尝试不同的请求格式

# 方法1: POST with JSON body
print("方法1: POST with JSON body")
response = requests.post(
    workflow_url,
    json={
        "input": "你好",
        "stream": False
    },
    headers={
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)[:500]}")

if response.status_code == 200:
    data = response.json()
    if "data" in data:
        print(f"\n✅✅✅ 成功! 回复: {str(data['data'])[:200]}")

# 方法2: POST with query string
print("\n" + "="*60)
print("方法2: POST with query string")
response = requests.post(
    f"{workflow_url}?input=你好&stream=false",
    headers={
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

# 方法3: GET request
print("\n" + "="*60)
print("方法3: GET request")
response = requests.get(
    f"{workflow_url}?input=你好",
    headers={
        "Authorization": f"Bearer {jwt_token}"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

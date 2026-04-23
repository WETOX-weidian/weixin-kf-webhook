import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

# Bot ID
bot_id = "7631814381948420148"

# API端点
endpoint = "https://api.coze.cn/v3/chat"

# 尝试不同的Authorization格式

# 方法1: Bearer PAT
print("方法1: Bearer PAT")
response = requests.post(
    endpoint,
    json={
        "bot_id": bot_id,
        "user_id": "test_user",
        "stream": False,
        "additional_messages": [
            {
                "content": "你好",
                "content_type": "text",
                "role": "user",
                "type": "question"
            }
        ]
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat_token}"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

# 方法2: PAT without Bearer
print("方法2: PAT without Bearer")
response = requests.post(
    endpoint,
    json={
        "bot_id": bot_id,
        "user_id": "test_user",
        "stream": False,
        "additional_messages": [
            {
                "content": "你好",
                "content_type": "text",
                "role": "user",
                "type": "question"
            }
        ]
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": pat_token
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

# 方法3: 使用不同的API端点（v2）
endpoint_v2 = "https://api.coze.cn/v2/chat"
print("方法3: V2 API with Bearer PAT")
response = requests.post(
    endpoint_v2,
    json={
        "bot_id": bot_id,
        "user_id": "test_user",
        "query": "你好"
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat_token}"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

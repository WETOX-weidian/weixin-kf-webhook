import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

# Bot ID
bot_id = "7631814381948420148"

# 尝试不同的API格式

# 方法1: 使用对话ID而不是user_id
print("方法1: 使用conversation_id")
response = requests.post(
    "https://api.coze.cn/open_api/v1/chat",
    json={
        "bot_id": bot_id,
        "user": "test_user",
        "query": "你好",
        "stream": False
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat_token}"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

# 方法2: 使用不同的消息格式
print("方法2: 不同的消息格式")
response = requests.post(
    "https://api.coze.cn/open_api/v1/chat",
    json={
        "bot_id": bot_id,
        "user": "test_user",
        "additional_messages": [
            {
                "role": "user",
                "content": "你好",
                "content_type": "text"
            }
        ],
        "stream": False
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pat_token}"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

# 方法3: 尝试不带Bearer
print("方法3: 不带Bearer")
response = requests.post(
    "https://api.coze.cn/open_api/v1/chat",
    json={
        "bot_id": bot_id,
        "user": "test_user",
        "query": "你好"
    },
    headers={
        "Content-Type": "application/json",
        "Authorization": pat_token
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}\n")

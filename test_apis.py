import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

# Bot ID
bot_id = "7631814381948420148"

# 尝试不同的API端点

endpoints = [
    ("Workflow API", "https://api.coze.cn/open_api/v2/chat", {
        "conversation_id": "test",
        "bot_id": bot_id,
        "user": "test_user",
        "query": "你好",
        "stream": False
    }),
    ("Chat API V2", "https://api.coze.cn/v2/chat", {
        "bot_id": bot_id,
        "user_id": "test_user",
        "query": "你好"
    }),
    ("Stream Chat", "https://api.coze.cn/open_api/v1/chat", {
        "bot_id": bot_id,
        "user": "test_user",
        "query": "你好"
    })
]

for name, endpoint, payload in endpoints:
    print(f"\n尝试: {name}")
    print(f"端点: {endpoint}")

    response = requests.post(
        endpoint,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {pat_token}"
        },
        timeout=30
    )

    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")

        # 检查是否有answer字段
        if "data" in data and "answer" in data["data"]:
            print(f"\n✅ 成功! AI回复: {data['data']['answer'][:100]}")
            break
    else:
        print(f"错误响应: {response.text[:300]}")

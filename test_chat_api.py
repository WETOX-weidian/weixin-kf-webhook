import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

print("="*60)
print("测试扣子对话API（非Bot Chat）")
print("="*60)
print(f"PAT Token: {pat_token}\n")

# 尝试不同的对话API端点

# 方法1: 对话API
print("方法1: 对话API /chat")
response = requests.post(
    "https://api.coze.cn/v1/chat",
    json={
        "query": "你好",
        "conversation_id": "test_conversation_123"
    },
    headers={
        "Authorization": f"Bearer {pat_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)[:500]}")

if response.status_code == 200:
    data = response.json()
    if "answer" in data:
        print(f"\n✅✅✅ 成功! 回复: {data['answer'][:100]}")
        exit(0)

# 方法2: 开放API /open_api/v1/chat
print("\n" + "="*60)
print("方法2: 开放API /open_api/v1/chat")
response = requests.post(
    "https://api.coze.cn/open_api/v1/chat",
    json={
        "bot_id": "7631814381948420148",
        "user": "test_user",
        "query": "你好",
        "stream": False
    },
    headers={
        "Authorization": f"Bearer {pat_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)[:500]}")

if response.status_code == 200:
    data = response.json()
    if "data" in data and "answer" in data["data"]:
        print(f"\n✅✅✅ 成功! 回复: {data['data']['answer'][:100]}")

# 方法3: 尝试使用不同的模型参数
print("\n" + "="*60)
print("方法3: 开放API with model参数")
response = requests.post(
    "https://api.coze.cn/open_api/v1/chat",
    json={
        "model": "doubao-seed-1-6-251015",
        "user": "test_user",
        "query": "你好"
    },
    headers={
        "Authorization": f"Bearer {pat_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)[:500]}")

if response.status_code == 200:
    data = response.json()
    if "data" in data and "answer" in data["data"]:
        print(f"\n✅✅✅ 成功! 回复: {data['data']['answer'][:100]}")

# 方法4: 查看API文档中可用的端点列表
print("\n" + "="*60)
print("尝试获取API端点列表")
response = requests.get(
    "https://api.coze.cn/docs/developer_guides/api_overview",
    headers={
        "Authorization": f"Bearer {pat_token}"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
if response.status_code == 200:
    print(f"✅ 文档页面可访问")
    print(f"内容长度: {len(response.text)}")
else:
    print(f"响应: {response.text[:300]}")

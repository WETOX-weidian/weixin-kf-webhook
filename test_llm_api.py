import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

print("="*60)
print("测试直接调用扣子LLM模型API")
print("="*60)
print(f"PAT Token: {pat_token}\n")

# 尝试不同的LLM API端点

# 方法1: OpenAI兼容的端点
print("方法1: OpenAI兼容端点")
response = requests.post(
    "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    json={
        "model": "doubao-seed-1-6-251015",
        "messages": [
            {"role": "user", "content": "你好"}
        ]
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
    if "choices" in data and len(data["choices"]) > 0:
        print(f"\n✅✅✅ 成功! 回复: {data['choices'][0]['message']['content'][:100]}")
        exit(0)

# 方法2: 扣子LLM API
print("\n" + "="*60)
print("方法2: 扣子LLM API")
response = requests.post(
    "https://api.coze.cn/v1/chat/completions",
    json={
        "model": "doubao-seed-1-6-251015",
        "messages": [
            {"role": "user", "content": "你好"}
        ]
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
    if "choices" in data and len(data["choices"]) > 0:
        print(f"\n✅✅✅ 成功! 回复: {data['choices'][0]['message']['content'][:100]}")

# 方法3: 扣子V2 LLM API
print("\n" + "="*60)
print("方法3: 扣子V2 LLM API")
response = requests.post(
    "https://api.coze.cn/v2/chat/completions",
    json={
        "model": "doubao-seed-1-6-251015",
        "messages": [
            {"role": "user", "content": "你好"}
        ]
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
    if "choices" in data and len(data["choices"]) > 0:
        print(f"\n✅✅✅ 成功! 回复: {data['choices'][0]['message']['content'][:100]}")

# 方法4: 扣子V3 LLM API
print("\n" + "="*60)
print("方法4: 扣子V3 LLM API")
response = requests.post(
    "https://api.coze.cn/v3/chat/completions",
    json={
        "model": "doubao-seed-1-6-251015",
        "messages": [
            {"role": "user", "content": "你好"}
        ]
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
    if "choices" in data and len(data["choices"]) > 0:
        print(f"\n✅✅✅ 成功! 回复: {data['choices'][0]['message']['content'][:100]}")

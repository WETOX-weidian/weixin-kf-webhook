import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

# Workflow ID（需要从扣子平台获取）
# 先尝试用Bot ID
workflow_id = "7631814381948420148"

# 尝试Workflow API
print("="*60)
print("测试Workflow API")
print("="*60)

# 方法1: 使用Bot ID作为workflow_id
print("\n方法1: 使用Bot ID作为workflow_id")
response = requests.post(
    "https://api.coze.cn/v1/workflow/run",
    json={
        "workflow_id": workflow_id,
        "parameters": {
            "input": "你好"
        },
        "stream": False
    },
    headers={
        "Authorization": f"Bearer {pat_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

if response.status_code == 200:
    data = response.json()
    print(f"完整响应: {json.dumps(data, ensure_ascii=False, indent=2)[:1000]}")
    if "data" in data:
        print(f"\n✅ 成功! 数据: {data['data']}")
else:
    print(f"错误: {response.text[:300]}")

# 方法2: 尝试不同的参数格式
print("\n" + "="*60)
print("方法2: 不同的参数格式")
print("="*60)

response = requests.post(
    "https://api.coze.cn/v1/workflow/run",
    json={
        "workflow_id": workflow_id,
        "input": "你好",  # 直接使用input而不是parameters
        "stream": False
    },
    headers={
        "Authorization": f"Bearer {pat_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

# 方法3: 尝试v2 API
print("\n" + "="*60)
print("方法3: Workflow API V2")
print("="*60)

response = requests.post(
    "https://api.coze.cn/v2/workflow/run",
    json={
        "workflow_id": workflow_id,
        "input": "你好"
    },
    headers={
        "Authorization": f"Bearer {pat_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

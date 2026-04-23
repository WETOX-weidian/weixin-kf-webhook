import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"

# Bot ID
bot_id = "7631814381948420148"

print("="*60)
print("确认Bot Chat API的正确调用格式")
print("="*60)
print(f"PAT Token: {pat_token}")
print(f"Bot ID: {bot_id}")

# 标准格式（来自扣子文档）
response = requests.post(
    "https://api.coze.cn/v3/chat",
    json={
        "bot_id": bot_id,
        "user_id": "test_user_123",
        "stream": False,
        "additional_messages": [
            {
                "role": "user",
                "content": "你好",
                "content_type": "text"
            }
        ]
    },
    headers={
        "Authorization": f"Bearer {pat_token}",  # Bearer + 空格 + token
        "Content-Type": "application/json"
    },
    timeout=30
)

print(f"\n状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

if response.status_code == 200:
    print("\n✅ 调用成功!")
elif response.status_code == 401:
    print(f"\n❌ 认证失败 (401)")
    print(f"   错误码: {response.json().get('code')}")
    print(f"   错误信息: {response.json().get('msg')}")
    print(f"\n根据AI的建议，可能的原因：")
    print(f"   1. Bot未发布到'API'渠道")
    print(f"   2. Bot所在的团队空间不允许API调用")
    print(f"   3. PAT Token没有Bot Chat API的权限")

import requests
import json

# 你的PAT Token
pat_token = "sat_nrzdj4hNjQZeG7xA4ukFp0hQQtIqb1qnyPJY9hpz8LXVJltxQhQQDsqfUubbVOGv"
bot_id = "7631814381948420148"

print("="*60)
print("尝试不同的认证头格式")
print("="*60)

auth_formats = [
    ("Bearer + Token", f"Bearer {pat_token}"),
    ("Token without Bearer", pat_token),
    ("PAT prefix", f"pat {pat_token}"),
    ("Bot prefix", f"bot {pat_token}"),
    ("API-Key header", None),
]

for name, auth_value in auth_formats:
    print(f"\n{name}:")
    headers = {"Content-Type": "application/json"}

    if auth_value:
        headers["Authorization"] = auth_value

    if name == "API-Key header":
        headers["X-API-Key"] = pat_token

    try:
        response = requests.post(
            "https://api.coze.cn/v3/chat",
            json={
                "bot_id": bot_id,
                "user_id": "test_user",
                "stream": False,
                "additional_messages": [
                    {
                        "role": "user",
                        "content": "你好",
                        "content_type": "text"
                    }
                ]
            },
            headers=headers,
            timeout=30
        )

        print(f"  状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            code = data.get("code")
            if code == 0:
                print(f"  ✅✅✅ 成功！")
                print(f"  回复: {data.get('data', {}).get('answer', 'N/A')[:100]}")
                break
            else:
                print(f"  错误码: {code}")
                print(f"  错误信息: {data.get('msg', 'N/A')[:100]}")
        else:
            print(f"  HTTP错误: {response.text[:100]}")

    except Exception as e:
        print(f"  异常: {str(e)[:100]}")

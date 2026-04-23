import requests
import json
import re

# JWT Token
jwt_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRhODQyODA2LWQwZGYtNDlmYS05ZDAxLWNhM2MyNDJkMWUyNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkNWWk1Fdkc4OXY3d2gzMlhNaWxhVlZLd3ZGQjVhZEhMIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2OTQ1NDY2LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI4NjA4Mzk2MDEwMTkyOTIyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjMxOTIyNjYzOTM3NTQwMTIyIn0.mFSK0hO0eD2uSDPjS94BYoW6NpWNOXlr1oXgQ8nw5ph4y6TPCkn1oQjNiIoPgNzTTAUyf72mTVn3oWzqRHys4umjHm2QuNIgsVAdlYBUTWARJutHaJsTl8rHxZmFMHwqkv8vz7R5Kjo-SdpdLSSKZVwvMtOFTARkw9jxYOKPTtMBE9MR8k_TXdWUx73RwrO_DKUXbtO74RL1pBTHw-ZtttxAuK9G11huSAZn2E0ry-Bi6AI21_lV_HJhEJwYp870fdzdL2nPILdamM7Ye18bL-ZOUBOPQSI7lJmINmDjztyONP9F2n2629fk7pL8mEmw0WWqBp3XXnVE3292EKt-5Q"

def parse_sse_response(response_text):
    """解析SSE流式响应，提取完整的AI回复"""
    full_answer = ""
    lines = response_text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('data: '):
            json_str = line[6:]  # 去掉 "data: " 前缀
            try:
                data = json.loads(json_str)
                if data.get('type') == 'answer':
                    answer = data.get('content', {}).get('answer')
                    if answer:
                        full_answer += answer
            except json.JSONDecodeError:
                continue

    return full_answer

print("="*60)
print("测试SSE响应解析")
print("="*60)

response = requests.post(
    "https://z2f493xmnp.coze.site/stream_run",
    json={
        "input": "你好",
        "stream": False  # 虽然请求false，但响应仍是流式
    },
    headers={
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    },
    timeout=30
)

print(f"\n状态码: {response.status_code}")

if response.status_code == 200:
    full_answer = parse_sse_response(response.text)
    print(f"\n✅✅✅ AI完整回复:")
    print("="*60)
    print(full_answer)
    print("="*60)
    print(f"\n回复长度: {len(full_answer)} 字符")

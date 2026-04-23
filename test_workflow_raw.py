import requests
import json

# JWT Token
jwt_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRhODQyODA2LWQwZGYtNDlmYS05ZDAxLWNhM2MyNDJkMWUyNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkNWWk1Fdkc4OXY3d2gzMlhNaWxhVlZLd3ZGQjVhZEhMIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2OTQ1NDY2LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI4NjA4Mzk2MDEwMTkyOTIyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjMxOTIyNjYzOTM3NTQwMTIyIn0.mFSK0hO0eD2uSDPjS94BYoW6NpWNOXlr1oXgQ8nw5ph4y6TPCkn1oQjNiIoPgNzTTAUyf72mTVn3oWzqRHys4umjHm2QuNIgsVAdlYBUTWARJutHaJsTl8rHxZmFMHwqkv8vz7R5Kjo-SdpdLSSKZVwvMtOFTARkw9jxYOKPTtMBE9MR8k_TXdWUx73RwrO_DKUXbtO74RL1pBTHw-ZtttxAuK9G11huSAZn2E0ry-Bi6AI21_lV_HJhEJwYp870fdzdL2nPILdamM7Ye18bL-ZOUBOPQSI7lJmINmDjztyONP9F2n2629fk7pL8mEmw0WWqBp3XXnVE3292EKt-5Q"

# 工作流端点
workflow_url = "https://z2f493xmnp.coze.site/stream_run"

print("="*60)
print("测试工作流API（查看原始响应）")
print("="*60)

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

print(f"\n状态码: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
print(f"\n原始响应（前500字符）:")
print(response.text[:500])
print(f"\n原始响应（后500字符）:")
print(response.text[-500:])
print(f"\n完整长度: {len(response.text)} 字符")

# 保存响应
with open('/tmp/workflow_response.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)
print(f"\n✅ 完整响应已保存到 /tmp/workflow_response.txt")

import jwt
import json

# 用户提供的JWT Token
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRhODQyODA2LWQwZGYtNDlmYS05ZDAxLWNhM2MyNDJkMWUyNiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIkNWWk1Fdkc4OXY3d2gzMlhNaWxhVlZLd3ZGQjVhZEhMIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2OTQ1NDY2LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI4NjA4Mzk2MDEwMTkyOTIyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjMxOTIyNjYzOTM3NTQwMTIyIn0.mFSK0hO0eD2uSDPjS94BYoW6NpWNOXlr1oXgQ8nw5ph4y6TPCkn1oQjNiIoPgNzTTAUyf72mTVn3oWzqRHys4umjHm2QuNIgsVAdlYBUTWARJutHaJsTl8rHxZmFMHwqkv8vz7R5Kjo-SdpdLSSKZVwvMtOFTARkw9jxYOKPTtMBE9MR8k_TXdWUx73RwrO_DKUXbtO74RL1pBTHw-ZtttxAuK9G11huSAZn2E0ry-Bi6AI21_lV_HJhEJwYp870fdzdL2nPILdamM7Ye18bL-ZOUBOPQSI7lJmINmDjztyONP9F2n2629fk7pL8mEmw0WWqBp3XXnVE3292EKt-5Q"

print("="*60)
print("解码JWT Token")
print("="*60)

try:
    # 解码JWT（不验证签名）
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("\n✅ JWT解码成功!")
    print(f"\n完整信息:\n{json.dumps(decoded, ensure_ascii=False, indent=2)}")

    # 提取关键信息
    print("\n" + "="*60)
    print("关键信息提取:")
    print("="*60)
    print(f"签发者 (iss): {decoded.get('iss')}")
    print(f"接收者 (aud): {decoded.get('aud')}")
    print(f"过期时间 (exp): {decoded.get('exp')}")
    print(f"签发时间 (iat): {decoded.get('iat')}")
    print(f"主题 (sub): {decoded.get('sub')}")
    print(f"来源 (src): {decoded.get('src')}")

except Exception as e:
    print(f"\n❌ JWT解码失败: {e}")

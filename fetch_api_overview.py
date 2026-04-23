import requests
import json

url = "https://www.coze.cn/open/docs/developer_guides/coze_api_overview"

print("="*60)
print("获取扣子API概览文档")
print("="*60)
print(f"URL: {url}\n")

response = requests.get(url, timeout=30)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    print(f"内容长度: {len(response.text)} 字符")

    # 保存原始HTML
    with open('/tmp/coze_api_overview.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"✅ HTML已保存到 /tmp/coze_api_overview.html")

    # 查找关键词
    keywords = [
        'authentication',
        'token',
        'api key',
        'authorization',
        'bearer',
        'bot_id',
        'v3/chat'
    ]

    print(f"\n关键词搜索:")
    text_lower = response.text.lower()
    for keyword in keywords:
        count = text_lower.count(keyword)
        print(f"  '{keyword}': {count} 次")

    # 查找可能的API端点
    import re
    api_urls = re.findall(r'https://api\.coze\.cn/[^"\s<]+', response.text)
    if api_urls:
        print(f"\n找到的API端点:")
        for api_url in set(api_urls):
            print(f"  - {api_url}")

    # 查找curl命令
    curl_commands = re.findall(r'curl[^\n]{0,200}', response.text)
    if curl_commands:
        print(f"\n找到 {len(curl_commands)} 个curl命令示例:")
        for i, cmd in enumerate(curl_commands[:3]):
            print(f"\n--- 命令 {i+1} ---")
            print(cmd[:300])

else:
    print(f"❌ 获取失败: {response.status_code}")
    print(f"错误: {response.text[:200]}")

import requests

# 尝试不同的扣子API文档URL
urls = [
    "https://www.coze.cn/open/docs/coz_api",
    "https://www.coze.cn/open/docs/developer_guides/authentication",
    "https://www.coze.cn/open/docs/bot_chat_api",
    "https://www.coze.cn/open/docs/bot_chat_token",
    "https://www.coze.cn/docs/developer_guides/bot_authentication"
]

for url in urls:
    print(f"\n尝试: {url}")
    response = requests.get(url, timeout=10)
    print(f"  状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"  内容长度: {len(response.text)}")
        # 保存内容
        filename = url.split('/')[-1] or 'index'
        with open(f'/tmp/doc_{filename}.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"  ✅ 已保存到 /tmp/doc_{filename}.html")

import requests
from bs4 import BeautifulSoup
import json

# 获取扣子API文档
url = "https://www.coze.cn/open/docs/developer_guides"

print("正在获取扣子API文档...")
print(f"URL: {url}\n")

response = requests.get(url, timeout=30)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 尝试找到API认证相关的部分
    print("\n" + "="*60)
    print("页面标题:", soup.title.string if soup.title else "N/A")
    print("="*60)

    # 查找包含认证、API、token等关键词的内容
    keywords = ['认证', 'Authentication', 'API', 'Token', 'Bearer']

    for keyword in keywords:
        print(f"\n搜索关键词: {keyword}")
        elements = soup.find_all(string=lambda text: text and keyword in text.lower())
        for elem in elements[:5]:  # 只显示前5个匹配
            print(f"  - {elem.strip()[:100]}")

    # 保存HTML内容以便分析
    with open('/tmp/coze_docs.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\n✅ HTML内容已保存到 /tmp/coze_docs.html")

else:
    print(f"❌ 获取文档失败: {response.status_code}")

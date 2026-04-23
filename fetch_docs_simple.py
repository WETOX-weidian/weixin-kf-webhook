import requests

# 获取扣子API文档
url = "https://www.coze.cn/open/docs/developer_guides"

print("正在获取扣子API文档...")
print(f"URL: {url}\n")

response = requests.get(url, timeout=30)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    # 保存HTML内容
    with open('/tmp/coze_docs.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"✅ HTML内容已保存，长度: {len(response.text)} 字符")

    # 查找API相关信息
    text = response.text.lower()

    keywords = ['authentication', 'token', 'api key', 'bearer', 'authorization']
    print(f"\n关键词搜索结果:")
    for keyword in keywords:
        count = text.count(keyword)
        print(f"  '{keyword}': {count} 次")

    # 查找代码示例
    import re
    code_blocks = re.findall(r'<code[^>]*>(.*?)</code>', response.text, re.DOTALL)
    print(f"\n找到 {len(code_blocks)} 个代码块")

    # 显示前3个代码块
    for i, block in enumerate(code_blocks[:3]):
        print(f"\n--- 代码块 {i+1} ---")
        print(block[:300])
else:
    print(f"❌ 获取文档失败: {response.status_code}")

import requests

# Bot ID
bot_id = "7631814381948420148"

# 尝试访问Bot的API配置页面
possible_urls = [
    f"https://www.coze.cn/bot/{bot_id}/api",
    f"https://www.coze.cn/bot/{bot_id}/api/setting",
    f"https://www.coze.cn/bot/{bot_id}/api/config",
    f"https://www.coze.cn/bot/{bot_id}/publish/api",
    f"https://api.coze.cn/open_api/bot/{bot_id}/config",
    f"https://www.coze.cn/open_api/bot/{bot_id}/api_key",
]

print("="*60)
print("尝试访问Bot的API配置页面")
print("="*60)
print(f"Bot ID: {bot_id}\n")

for url in possible_urls:
    print(f"\n尝试: {url}")
    response = requests.get(url, timeout=10)
    print(f"  状态码: {response.status_code}")

    if response.status_code == 200:
        print(f"  ✅ 成功! 内容长度: {len(response.text)}")

        # 查找API Key相关的内容
        text = response.text.lower()
        if 'api key' in text or 'token' in text:
            print(f"  🎯 找到API相关内容!")

            # 保存内容
            filename = url.split('/')[-1] or 'config'
            with open(f'/tmp/bot_api_{filename}.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"  📄 已保存到 /tmp/bot_api_{filename}.html")

            # 查找curl命令
            import re
            curl_commands = re.findall(r'curl[^\n]{0,300}', response.text)
            if curl_commands:
                print(f"\n  找到 {len(curl_commands)} 个curl命令:")
                for i, cmd in enumerate(curl_commands[:2]):
                    print(f"  --- 命令 {i+1} ---")
                    print(f"  {cmd[:200]}")

            break
    else:
        print(f"  ❌ 失败: {response.text[:100]}")

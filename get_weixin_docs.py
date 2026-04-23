#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取微信小店API文档内容
"""
import httpx

# 文档链接
urls = [
    "https://developers.weixin.qq.com/doc/store/shop/notify/kf_callback/kf_msg_event.html",
    "https://developers.weixin.qq.com/doc/store/shop/API/apimgnt/common/api_getaccesstoken.html",
    "https://developers.weixin.qq.com/doc/store/shop/API/kf/api_sendmsg.html"
]

print("="*60)
print("获取微信小店API文档")
print("="*60)

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        response = httpx.get(url, timeout=30, follow_redirects=True)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)}")
        print(f"\n内容（前1000字符）:")
        print(response.text[:1000])
        print("\n...")

    except Exception as e:
        print(f"获取失败: {e}")

print("\n" + "="*60)
print("文档获取完成")
print("="*60)

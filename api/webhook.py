# -*- coding: utf-8 -*-
"""
Vercel Serverless Function - WeChat Webhook
"""
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

import json
import xml.etree.ElementTree as ET
from datetime import datetime

# 导入配置和工具
from utils.crypto import WeixinCrypto
from services.coze_client import CozeClient
from config import config


# 创建加密工具
crypto = WeixinCrypto(
    token=config.WEIXIN_TOKEN,
    encoding_aes_key=config.WEIXIN_ENCODING_AES_KEY,
    app_id=config.WEIXIN_APP_ID
)

# 创建扣子客户端
coze = CozeClient()


def handler(request):
    """
    Vercel Serverless Function处理函数
    """
    print(f"[Handler] 收到请求")

    method = request.get("method", "GET")
    url = request.get("url", "")
    headers = request.get("headers", {})
    body = request.get("body", "")
    query = request.get("query", {})

    print(f"[Handler] Method: {method}, URL: {url}")

    # 处理OPTIONS预检请求
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            },
            "body": ""
        }

    # 处理GET请求 - 验证微信服务器
    if method == "GET":
        signature = query.get("signature", [""])[0] if "signature" in query else ""
        timestamp = query.get("timestamp", [""])[0] if "timestamp" in query else ""
        nonce = query.get("nonce", [""])[0] if "nonce" in query else ""
        echostr = query.get("echostr", [""])[0] if "echostr" in query else ""

        print(f"[GET] 微信验证请求: echostr={echostr}")

        if crypto.verify_token(signature, timestamp, nonce):
            print("[GET] 验证成功，返回echostr")
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/plain; charset=utf-8"
                },
                "body": echostr
            }
        else:
            print("[GET] 验证失败")
            return {
                "statusCode": 403,
                "headers": {
                    "Content-Type": "text/plain; charset=utf-8"
                },
                "body": "Verification failed"
            }

    # 处理POST请求 - 接收微信消息
    if method == "POST":
        print("[POST] 收到微信消息")

        try:
            # 获取原始数据
            print(f"[POST] 消息长度: {len(body)}")

            if body:
                root = ET.fromstring(body)
                msg_type = root.find("MsgType").text
                to_user = root.find("ToUserName").text
                from_user = root.find("FromUserName").text

                print(f"[POST] 消息类型: {msg_type}, 发送者: {from_user}")

                if msg_type == "text":
                    user_input = root.find("Content").text
                    print(f"[POST] 用户消息: {user_input}")

                    # 调用扣子API
                    try:
                        print("[POST] 调用扣子API...")
                        response = coze.call_chat(user_input, from_user)
                        print(f"[POST] 扣子响应: {response}")
                    except Exception as e:
                        print(f"[POST] 扣子API调用失败: {e}")

        except Exception as e:
            print(f"[POST] 处理消息错误: {e}")
            import traceback
            traceback.print_exc()

        # 立即返回success
        print("[POST] 返回success")
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain; charset=utf-8"
            },
            "body": "success"
        }

    # 其他方法
    return {
        "statusCode": 405,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8"
        },
        "body": "Method not allowed"
    }

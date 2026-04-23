# -*- coding: utf-8 -*-
"""
Flask Webhook服务
使用gunicorn运行
"""
from flask import Flask, request, Response
import os

# 导入配置和工具
from utils.crypto import WeixinCrypto
from services.coze_client import CozeClient
from config import config

app = Flask(__name__)

# 创建加密工具
crypto = WeixinCrypto(
    token=config.WEIXIN_TOKEN,
    encoding_aes_key=config.WEIXIN_ENCODING_AES_KEY,
    app_id=config.WEIXIN_APP_ID
)

# 创建扣子客户端
coze = CozeClient()


@app.route("/")
def root():
    """根路径"""
    return "WeChat Webhook Service is Running!"


@app.route("/health")
def health():
    """健康检查"""
    return {"status": "ok", "service": "weixin-webhook"}


@app.route("/webhook/weixin", methods=["GET"])
def verify_weixin():
    """
    验证微信服务器
    """
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    if crypto.verify_token(signature, timestamp, nonce):
        return Response(echostr, mimetype="text/plain")
    else:
        return Response("Verification failed", status=403)


@app.route("/webhook/weixin", methods=["POST"])
def handle_weixin_message():
    """
    处理微信消息
    """
    import xml.etree.ElementTree as ET

    try:
        body = request.get_data(as_text=True)
        root = ET.fromstring(body)
        msg_type = root.find("MsgType").text
        from_user = root.find("FromUserName").text

        if msg_type == "text":
            user_input = root.find("Content").text
            # 调用扣子API
            response = coze.call_chat(user_input, from_user)

    except Exception as e:
        print(f"Error: {e}")

    return Response("success", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

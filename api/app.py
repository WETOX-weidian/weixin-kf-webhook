# -*- coding: utf-8 -*-
"""
Flask Webhook服务
使用gunicorn运行
"""
from flask import Flask, request, Response
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入配置和工具
from utils.crypto import WeixinCrypto
from services.coze_client import CozeClient
from services.weixin_message import weixin_message
from config import config

print("=" * 50)
print("正在启动Flask应用...")
print(f"Python版本: {sys.version}")
print(f"工作目录: {os.getcwd()}")
print(f"Python路径: {sys.path[:3]}")
print("=" * 50)

app = Flask(__name__)

# 验证环境变量
if not config.validate():
    print("警告: 部分环境变量未配置，服务可能无法正常工作")

# 创建加密工具（延迟创建，确保配置已加载）
crypto = WeixinCrypto(
    token=config.WEIXIN_TOKEN or "default_token",
    encoding_aes_key=config.WEIXIN_ENCODING_AES_KEY or "default_key",
    app_id=config.WEIXIN_APP_ID or "default_app_id"
)

# 创建扣子客户端（延迟创建）
coze = CozeClient()

print("✓ Flask应用启动成功")


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

    print(f"[GET] 收到验证请求: echostr={echostr}")

    # 检查是否缺少参数（浏览器直接访问时参数为空）
    if not all([signature, timestamp, nonce, echostr]):
        print("[GET] 参数缺失，这不是微信的验证请求")
        return Response(
            "此接口仅用于微信服务器验证，请在微信公众平台配置服务器地址",
            status=400
        )

    if crypto.verify_token(signature, timestamp, nonce):
        print("[GET] 验证成功")
        return Response(echostr, mimetype="text/plain")
    else:
        print("[GET] 验证失败")
        return Response("Verification failed", status=403)


@app.route("/webhook/weixin", methods=["POST"])
def handle_weixin_message():
    """
    处理微信消息
    """
    import xml.etree.ElementTree as ET

    print("[POST] 收到微信消息")

    try:
        body = request.get_data(as_text=True)
        print(f"[POST] 消息长度: {len(body)}")

        # 检查是否为加密消息
        encrypt_type = request.args.get("encrypt_type", "")
        msg_signature = request.args.get("msg_signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")

        # 如果是加密消息，先解密
        if encrypt_type == "aes":
            print("[POST] 检测到加密消息，开始解密...")
            try:
                # 解密消息
                decrypted_xml = crypto.decrypt_message(body, msg_signature, timestamp, nonce)
                if not decrypted_xml:
                    print("[POST] 解密失败")
                    return Response("success", mimetype="text/plain")

                print(f"[POST] 解密成功: {decrypted_xml[:200]}...")
                body = decrypted_xml
            except Exception as e:
                print(f"[POST] 解密异常: {e}")
                import traceback
                traceback.print_exc()
                return Response("success", mimetype="text/plain")

        # 解析XML
        root = ET.fromstring(body)
        msg_type = root.find("MsgType").text
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

                # 发送客服消息回微信
                if response:
                    print(f"[POST] 发送客服消息到微信: {response[:100]}...")
                    success = weixin_message.send_text(from_user, response)
                    if success:
                        print("[POST] 客服消息发送成功")
                    else:
                        print("[POST] 客服消息发送失败")
            except Exception as e:
                print(f"[POST] 扣子API调用失败: {e}")
                import traceback
                traceback.print_exc()

    except Exception as e:
        print(f"[POST] 处理消息错误: {e}")
        import traceback
        traceback.print_exc()

    return Response("success", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

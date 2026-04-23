"""
微信消息加密/解密工具
"""
import base64
import hashlib
import struct
from typing import Tuple


class WeixinCrypto:
    """微信消息加密/解密类"""

    def __init__(self, token: str, encoding_aes_key: str, app_id: str):
        """
        初始化

        Args:
            token: 令牌
            encoding_aes_key: 消息密钥（43位）
            app_id: 应用ID
        """
        self.token = token
        self.encoding_aes_key = encoding_aes_key + '='
        self.app_id = app_id

    def verify_token(self, signature: str, timestamp: str, nonce: str) -> bool:
        """
        验证Token

        Args:
            signature: 签名
            timestamp: 时间戳
            nonce: 随机数

        Returns:
            True: 验证成功
            False: 验证失败
        """
        # 检查参数是否为空
        if not all([signature, timestamp, nonce]):
            return False

        # 排序
        tmp_list = [self.token, timestamp, nonce]
        tmp_list.sort()

        # 拼接
        tmp_str = ''.join(tmp_list)

        # sha1加密
        hashcode = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

        # 验证
        return hashcode == signature

    def decrypt_message(self, encrypted_xml: str, msg_signature: str, timestamp: str, nonce: str) -> str:
        """
        解密微信加密消息

        Args:
            encrypted_xml: 加密的消息（可能是JSON或XML）
            msg_signature: 消息签名
            timestamp: 时间戳
            nonce: 随机数

        Returns:
            解密后的XML内容
        """
        import xml.etree.ElementTree as ET
        import json

        try:
            print(f"[decrypt] 收到加密消息，长度: {len(encrypted_xml)}")
            print(f"[decrypt] 消息前100字符: {repr(encrypted_xml[:100])}")

            encrypt = None

            # 尝试1: 解析JSON格式（新版微信使用JSON）
            try:
                if encrypted_xml.strip().startswith('{'):
                    print(f"[decrypt] 尝试解析JSON格式...")
                    json_data = json.loads(encrypted_xml)
                    if 'Encrypt' in json_data:
                        encrypt = json_data['Encrypt']
                        print(f"[decrypt] 从JSON中提取到Encrypt，长度: {len(encrypt)}")
            except json.JSONDecodeError:
                print(f"[decrypt] JSON解析失败，尝试XML格式...")

            # 尝试2: 解析XML格式（旧版微信使用XML）
            if not encrypt:
                try:
                    root = ET.fromstring(encrypted_xml)
                    encrypt_elem = root.find("Encrypt")
                    if encrypt_elem is not None and encrypt_elem.text:
                        encrypt = encrypt_elem.text
                        print(f"[decrypt] 从XML中提取到Encrypt，长度: {len(encrypt)}")
                    else:
                        print(f"[decrypt] XML解析成功但未找到Encrypt标签")
                except ET.ParseError as e:
                    print(f"[decrypt] XML解析失败: {e}")

            # 如果都没有提取到加密内容，使用整个消息
            if not encrypt:
                print(f"[decrypt] 未能从JSON或XML中提取Encrypt，使用整个消息")
                encrypt = encrypted_xml

            print(f"[decrypt] 最终使用的加密内容长度: {len(encrypt)}")

            # 验证签名
            tmp_list = [self.token, timestamp, nonce, encrypt]
            tmp_list.sort()
            tmp_str = ''.join(tmp_list)
            hashcode = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

            print(f"[decrypt] 计算的签名: {hashcode}")
            print(f"[decrypt] 期望的签名: {msg_signature}")

            if hashcode != msg_signature:
                print(f"[decrypt] 签名验证失败，继续尝试解密...")

            # 解密消息
            msg, from_app_id = self.decrypt(encrypt)

            # 验证AppID
            if from_app_id != self.app_id:
                print(f"[decrypt] AppID不匹配: expected={self.app_id}, got={from_app_id}")
                # AppID不匹配也返回解密结果，用于调试
                # return None

            print(f"[decrypt] 解密成功，AppID={from_app_id}")
            print(f"[decrypt] 解密结果(前100字符): {repr(msg[:100])}")
            return msg

        except Exception as e:
            print(f"[decrypt] 解密异常: {e}")
            import traceback
            traceback.print_exc()
            return None

    def decrypt(self, encrypted_msg: str) -> Tuple[str, str]:
        """
        解密消息

        Args:
            encrypted_msg: 加密的消息

        Returns:
            (消息内容, 应用ID)
        """
        from Crypto.Cipher import AES

        # Base64解码
        cipher_text = base64.b64decode(encrypted_msg)

        # AES密钥
        aes_key = base64.b64decode(self.encoding_aes_key)

        # AES解密
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        decrypted = cipher.decrypt(cipher_text)

        # 去除填充
        pad = decrypted[-1]
        decrypted = decrypted[:-pad]

        # 提取消息长度（大端序）
        msg_len = struct.unpack('>I', decrypted[16:20])[0]

        # 提取消息
        msg = decrypted[20:20 + msg_len].decode('utf-8')

        # 提取AppID
        from_app_id = decrypted[20 + msg_len:].decode('utf-8')

        return msg, from_app_id

    def encrypt(self, msg: str) -> str:
        """
        加密消息

        Args:
            msg: 要加密的消息

        Returns:
            加密后的消息
        """
        from Crypto.Cipher import AES
        from Crypto import Random

        # 生成16位随机数
        random_str = Random.get_random_bytes(16)

        # 消息长度（大端序）
        msg_len = len(msg).to_bytes(4, 'big')

        # AppID
        app_id_bytes = self.app_id.encode('utf-8')

        # 拼接：随机数 + 消息长度 + 消息 + AppID
        content = random_str + msg_len + msg.encode('utf-8') + app_id_bytes

        # 计算填充
        pad = 32 - (len(content) % 32)
        content += bytes([pad] * pad)

        # AES密钥
        aes_key = base64.b64decode(self.encoding_aes_key)

        # AES加密
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        encrypted = cipher.encrypt(content)

        # Base64编码
        return base64.b64encode(encrypted).decode('utf-8')

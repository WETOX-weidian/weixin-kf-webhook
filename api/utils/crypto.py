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
        # 排序
        tmp_list = [self.token, timestamp, nonce]
        tmp_list.sort()

        # 拼接
        tmp_str = ''.join(tmp_list)

        # sha1加密
        hashcode = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

        # 验证
        return hashcode == signature

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

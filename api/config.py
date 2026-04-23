"""
配置文件
"""
import os
from typing import Optional


class Config:
    """配置类"""

    # 微信配置
    WEIXIN_TOKEN: str = os.getenv("WEIXIN_TOKEN", "")
    WEIXIN_ENCODING_AES_KEY: str = os.getenv("WEIXIN_ENCODING_AES_KEY", "")
    WEIXIN_APP_ID: str = os.getenv("WEIXIN_APP_ID", "")
    WEIXIN_APP_SECRET: str = os.getenv("WEIXIN_APP_SECRET", "")

    # 扣子配置
    COZE_API_URL: str = os.getenv("COZE_API_URL", "https://api.coze.cn/v3/chat")
    COZE_API_KEY: str = os.getenv("COZE_API_KEY", "")
    COZE_BOT_ID: str = os.getenv("COZE_BOT_ID", "")

    # 环境配置
    ENV: str = os.getenv("VERCEL_ENV", "development")

    # 日志级别
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> bool:
        """
        验证配置是否完整

        Returns:
            True: 配置完整
            False: 配置不完整
        """
        required_fields = [
            ("WEIXIN_TOKEN", cls.WEIXIN_TOKEN),
            ("WEIXIN_ENCODING_AES_KEY", cls.WEIXIN_ENCODING_AES_KEY),
            ("WEIXIN_APP_ID", cls.WEIXIN_APP_ID),
            ("WEIXIN_APP_SECRET", cls.WEIXIN_APP_SECRET),
            ("COZE_API_URL", cls.COZE_API_URL),
            ("COZE_API_KEY", cls.COZE_API_KEY),
            ("COZE_BOT_ID", cls.COZE_BOT_ID),
        ]

        missing = [name for name, value in required_fields if not value]

        if missing:
            print(f"❌ 缺少配置: {', '.join(missing)}")
            return False

        return True


config = Config()

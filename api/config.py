"""
配置文件
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载.env文件
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))


class Config:
    """配置类"""

    # 微信配置
    WEIXIN_TOKEN: str = os.getenv("WEIXIN_TOKEN", "")
    WEIXIN_ENCODING_AES_KEY: str = os.getenv("WEIXIN_ENCODING_AES_KEY", "")
    WEIXIN_APP_ID: str = os.getenv("WEIXIN_APP_ID", "")
    WEIXIN_APP_SECRET: str = os.getenv("WEIXIN_APP_SECRET", "")

    # 扣子配置（已弃用：Bot Chat API）
    COZE_API_URL: str = os.getenv("COZE_API_URL", "https://api.coze.cn/v3/chat")
    COZE_API_KEY: str = os.getenv("COZE_API_KEY", "")
    COZE_BOT_ID: str = os.getenv("COZE_BOT_ID", "")

    # 扣子工作流配置（新）
    COZE_WORKFLOW_URL: str = os.getenv("COZE_WORKFLOW_URL", "")
    COZE_JWT_TOKEN: str = os.getenv("COZE_JWT_TOKEN", "")

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
        ]

        optional_fields = [
            ("COZE_WORKFLOW_URL", cls.COZE_WORKFLOW_URL),
            ("COZE_JWT_TOKEN", cls.COZE_JWT_TOKEN),
        ]

        missing = [name for name, value in required_fields if not value]
        optional_missing = [name for name, value in optional_fields if not value]

        if missing:
            print(f"❌ 缺少必填配置: {', '.join(missing)}")
            return False

        if optional_missing:
            print(f"⚠️  缺少可选配置: {', '.join(optional_missing)}")

        return True


config = Config()

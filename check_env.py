#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境变量验证脚本
用于检查Render环境变量配置是否正确
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

def check_env_var(name, required=True, sensitive=False):
    """
    检查环境变量

    Args:
        name: 环境变量名
        required: 是否必需
        sensitive: 是否敏感（隐藏显示）

    Returns:
        bool: 是否配置正确
    """
    value = os.getenv(name)

    if not value:
        if required:
            print(f"❌ {name}: 未配置（必需）")
            return False
        else:
            print(f"⚠️  {name}: 未配置（可选）")
            return True

    # 敏感变量隐藏显示
    if sensitive:
        display_value = f"{value[:20]}...{value[-20:]}" if len(value) > 40 else "***"
    else:
        display_value = value

    print(f"✅ {name}: {display_value}")
    return True

def main():
    print("="*60)
    print("Render 环境变量验证")
    print("="*60)
    print()

    # 检查微信配置
    print("【微信配置】")
    weixin_ok = True
    weixin_ok &= check_env_var("WEIXIN_TOKEN", required=True)
    weixin_ok &= check_env_var("WEIXIN_ENCODING_AES_KEY", required=True)
    weixin_ok &= check_env_var("WEIXIN_APP_ID", required=True)
    weixin_ok &= check_env_var("WEIXIN_APP_SECRET", required=True, sensitive=True)

    print()

    # 检查扣子配置
    print("【扣子工作流配置】")
    coze_ok = True
    coze_ok &= check_env_var("COZE_WORKFLOW_URL", required=True)

    # 检查URL格式
    url = os.getenv("COZE_WORKFLOW_URL", "")
    if url and not (url.startswith("http://") or url.startswith("https://")):
        print(f"❌ COZE_WORKFLOW_URL: 缺少协议头（http:// 或 https://）")
        coze_ok = False

    coze_ok &= check_env_var("COZE_JWT_TOKEN", required=True, sensitive=True)

    print()
    print("="*60)

    # 总结
    if weixin_ok and coze_ok:
        print("✅ 所有环境变量配置正确！")
        print()
        print("下一步：")
        print("1. 等待Render部署完成（2-3分钟）")
        print("2. 通过微信发送测试消息")
        print("3. 在Render Dashboard查看日志")
        return 0
    else:
        print("❌ 部分环境变量未配置，请检查！")
        print()
        print("配置指南：")
        print("- 打开 RENDER_CONFIG.md 文件")
        print("- 在 Render Dashboard 添加缺失的环境变量")
        return 1

if __name__ == "__main__":
    sys.exit(main())

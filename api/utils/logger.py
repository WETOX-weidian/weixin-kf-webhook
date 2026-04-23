"""
日志工具
"""
import logging
import sys


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    配置日志

    Args:
        name: logger名称
        level: 日志级别

    Returns:
        配置好的logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if not logger.handlers:
        # 控制台handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # 格式化
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

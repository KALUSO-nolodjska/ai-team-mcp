"""
MCP AI Chat Group - 时间处理工具
Time Utilities
"""

from datetime import datetime, timedelta
from typing import Optional


def parse_time_range(time_range: str) -> Optional[datetime]:
    """
    解析时间范围字符串为datetime对象

    Args:
        time_range: 时间范围字符串，如 "last_24_hours", "last_7_days", "last_30_days" 或 ISO格式

    Returns:
        datetime对象，如果解析失败返回None
    """
    now = datetime.now()

    if time_range == "last_24_hours":
        return now - timedelta(hours=24)
    elif time_range == "last_7_days":
        return now - timedelta(days=7)
    elif time_range == "last_30_days":
        return now - timedelta(days=30)
    else:
        # 尝试解析ISO格式
        try:
            return datetime.fromisoformat(time_range.replace("Z", "+00:00"))
        except Exception:
            return None


def parse_iso_time(time_str: str) -> Optional[datetime]:
    """
    解析ISO格式时间字符串

    Args:
        time_str: ISO格式时间字符串

    Returns:
        datetime对象，如果解析失败返回None
    """
    try:
        return datetime.fromisoformat(time_str.replace("Z", "+00:00"))
    except Exception:
        return None


def format_timestamp(dt: datetime) -> str:
    """
    格式化datetime为标准字符串

    Args:
        dt: datetime对象

    Returns:
        格式化的时间字符串
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

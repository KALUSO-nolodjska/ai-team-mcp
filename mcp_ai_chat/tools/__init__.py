"""
MCP AI Chat Group - Tools Module
工具定义模块
"""

from .message_tools import get_message_tools
from .task_tools import get_task_tools
from .group_tools import get_group_tools
from .system_tools import get_system_tools


def get_all_tools():
    """获取所有工具定义"""
    tools = []
    tools.extend(get_message_tools())
    tools.extend(get_task_tools())
    tools.extend(get_group_tools())
    tools.extend(get_system_tools())
    return tools

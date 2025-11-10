"""
MCP AI Chat Group - Handlers Module
处理器模块 - 路由所有工具调用到对应处理函数
"""
from typing import Any
from mcp.types import TextContent

# 导入所有处理器
from .message_handler import (
    handle_send_message,
    handle_receive_messages,
    handle_mark_messages_read,
    handle_request_help,
    handle_request_review,
    handle_notify_completion,
    handle_share_code_snippet
)

from .task_handler import (
    handle_create_task,
    handle_assign_task,
    handle_update_task_status,
    handle_get_tasks,
    handle_delete_task
)

from .group_handler import (
    handle_create_group,
    handle_send_group_message,
    handle_receive_group_messages,
    handle_list_groups,
    handle_join_group,
    handle_leave_group,
    handle_summarize_group_messages,
    handle_get_unread_counts,
    handle_archive_group,
    handle_pin_message,
    handle_unpin_message
)

from .system_handler import (
    handle_register_agent,
    handle_set_employee_config,
    handle_get_current_session,
    handle_list_agents,
    handle_standby
)


# 工具名称 → 处理函数映射表
TOOL_HANDLERS = {
    # 消息工具 (7个)
    "send_message": handle_send_message,
    "receive_messages": handle_receive_messages,
    "mark_messages_read": handle_mark_messages_read,
    "request_help": handle_request_help,
    "request_review": handle_request_review,
    "notify_completion": handle_notify_completion,
    "share_code_snippet": handle_share_code_snippet,
    
    # 任务工具 (5个)
    "create_task": handle_create_task,
    "assign_task": handle_assign_task,
    "update_task_status": handle_update_task_status,
    "get_tasks": handle_get_tasks,
    "delete_task": handle_delete_task,
    
    # 群组工具 (11个)
    "create_group": handle_create_group,
    "send_group_message": handle_send_group_message,
    "receive_group_messages": handle_receive_group_messages,
    "list_groups": handle_list_groups,
    "join_group": handle_join_group,
    "leave_group": handle_leave_group,
    "summarize_group_messages": handle_summarize_group_messages,
    "get_unread_counts": handle_get_unread_counts,
    "archive_group": handle_archive_group,
    "pin_message": handle_pin_message,
    "unpin_message": handle_unpin_message,
    
    # 系统工具 (5个)
    "register_agent": handle_register_agent,
    "set_employee_config": handle_set_employee_config,
    "get_current_session": handle_get_current_session,
    "list_agents": handle_list_agents,
    "standby": handle_standby
}


async def handle_tool_call(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    路由工具调用到对应的处理器
    
    Args:
        name: 工具名称
        arguments: 工具参数
        
    Returns:
        处理结果列表
    """
    # 查找对应的处理函数
    handler = TOOL_HANDLERS.get(name)
    
    if handler:
        # 调用处理函数
        return await handler(arguments)
    else:
        # 未找到处理器
        return [TextContent(
            type="text",
            text=f"❌ 错误: 未知工具 '{name}'\n可用工具: {len(TOOL_HANDLERS)}个"
        )]


__all__ = ['handle_tool_call', 'TOOL_HANDLERS']


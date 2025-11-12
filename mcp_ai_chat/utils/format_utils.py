"""
MCP AI Chat Group - 格式化工具
Format Utilities
"""

from typing import Any, Dict, List


def truncate_content(content: str, max_length: int) -> str:
    """
    截断内容到指定长度

    Args:
        content: 原始内容
        max_length: 最大长度

    Returns:
        截断后的内容
    """
    if len(content) > max_length:
        return content[:max_length] + "..."
    return content


def format_message_output(
    messages: List[Dict[str, Any]], current_agent: str, max_content_length: int = 5000
) -> str:
    """
    格式化消息列表输出

    Args:
        messages: 消息列表
        current_agent: 当前agent名称
        max_content_length: 内容最大长度

    Returns:
        格式化的消息字符串
    """
    if not messages:
        return "📭 没有找到消息"

    result_lines = [f"📬 消息: 找到 {len(messages)} 条\n"]

    for msg in messages:
        read_status = (
            "✅ 已读" if msg.get("read", {}).get(current_agent, False) else "📩 未读"
        )

        # 消息头
        msg_header = f"\n--- 消息 {msg['id']}"
        if msg.get("is_pinned"):
            msg_header += " 📌 [置顶]"
        msg_header += " ---"
        result_lines.append(msg_header)

        # 发送者
        result_lines.append(
            f"发送者: {msg['sender']} ({msg.get('sender_role', '未知角色')})"
        )

        # 重要性
        if msg.get("importance") == "high":
            result_lines.append("⚠️ 重要性: 高")
        elif msg.get("importance") == "low":
            result_lines.append("ℹ️ 重要性: 低")

        # @提醒
        if msg.get("mentions"):
            result_lines.append(f"@提醒: {', '.join(msg['mentions'])}")

        # 回复信息
        if msg.get("reply_to"):
            result_lines.append(
                f"↩️ 回复 {msg['reply_to_sender']}: {msg.get('reply_to_content', '')[:50]}..."
            )

        # 话题
        if msg.get("topic"):
            result_lines.append(f"话题: {msg['topic']}")

        # 时间和状态
        result_lines.append(f"时间: {msg['timestamp']}")
        result_lines.append(f"状态: {read_status}")

        # 文件
        if msg.get("file_path"):
            result_lines.append(f"文件: {msg['file_path']}")

        # 内容
        content = msg.get("content", "")
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        result_lines.append(f"\n内容:\n{content}")

    return "\n".join(result_lines)


def format_task_output(tasks: List[Dict[str, Any]]) -> str:
    """
    格式化任务列表输出

    Args:
        tasks: 任务列表

    Returns:
        格式化的任务字符串
    """
    if not tasks:
        return "📋 没有找到任务"

    result_lines = [f"📋 任务列表: 找到 {len(tasks)} 个任务\n"]

    for task in tasks:
        status_icon = {
            "待开始": "⏳",
            "进行中": "🔄",
            "已完成": "✅",
            "已阻塞": "⚠️",
            "已取消": "❌",
        }.get(task.get("status", ""), "")

        priority_icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(
            task.get("priority", ""), ""
        )

        result_lines.append(f"\n--- 任务 {task['id']} ---")
        result_lines.append(f"{priority_icon} 优先级: {task.get('priority', 'P2')}")
        result_lines.append(f"标题: {task.get('title', '未知')}")
        result_lines.append(f"{status_icon} 状态: {task.get('status', '待开始')}")
        result_lines.append(f"负责人: {task.get('assignee', '未分配')}")
        result_lines.append(f"创建者: {task.get('creator', '未知')}")
        result_lines.append(f"创建时间: {task.get('created_at', '未知')}")

        if task.get("due_date"):
            result_lines.append(f"截止时间: {task['due_date']}")

        if task.get("description"):
            desc = truncate_content(task["description"], 200)
            result_lines.append(f"描述: {desc}")

    return "\n".join(result_lines)

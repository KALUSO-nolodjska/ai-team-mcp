"""
MCP AI Chat Group - 消息处理器
Message Handler

处理消息相关工具：
- send_message: 发送消息
- receive_messages: 接收消息
- mark_messages_read: 标记已读
- request_help: 请求帮助
- request_review: 请求审查
- notify_completion: 完成通知
- share_code_snippet: 分享代码片段
"""

from datetime import datetime
from pathlib import Path
from mcp.types import TextContent
from typing import Any

# 导入核心功能
from ..core.storage import load_messages, save_messages, load_sessions
from ..core.session import get_current_agent, get_current_session_id
from ..config import WORKSPACE_ROOT


async def handle_send_message(arguments: dict[str, Any]) -> list[TextContent]:
    """处理send_message工具"""
    recipients_str = arguments.get("recipients", "")
    file_path = arguments.get("file_path")
    message = arguments.get("message", "")

    # 解析接收者列表
    recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]

    if not recipients:
        return [TextContent(type="text", text="错误: 必须指定至少一个接收者")]

    # 读取文件内容（如果提供了文件路径）
    content = message
    if file_path:
        try:
            file_path_obj = Path(file_path)
            if file_path_obj.exists():
                with open(file_path_obj, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                return [TextContent(type="text", text=f"错误: 文件不存在: {file_path}")]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: 读取文件失败: {str(e)}")]

    if not content:
        return [TextContent(type="text", text="错误: 消息内容为空")]

    # 创建消息
    sender = get_current_agent()
    session_id = get_current_session_id()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"

    # 获取发送者的角色信息
    sender_role = "未知"
    if session_id:
        sessions = load_sessions()
        session_info = sessions.get(session_id, {})
        sender_role = session_info.get("role", "未知")

    new_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": sender_role,
        "sender_session_id": session_id,
        "recipients": recipients,
        "content": content,
        "file_path": file_path if file_path else None,
        "timestamp": datetime.now().isoformat(),
        "read": {recipient: False for recipient in recipients},
    }

    messages.append(new_message)
    save_messages(messages)

    return [
        TextContent(
            type="text",
            text=f"✅ 消息已发送\n发送者: {sender}\n接收者: {', '.join(recipients)}\n消息ID: {message_id}\n内容长度: {len(content)} 字符",
        )
    ]


async def handle_receive_messages(arguments: dict[str, Any]) -> list[TextContent]:
    """处理receive_messages工具"""
    recipient = arguments.get("recipient", "*")
    limit = arguments.get("limit", 20)
    unread_only = arguments.get("unread_only", False)
    since = arguments.get("since")
    keywords = arguments.get("keywords", [])
    max_content_length = arguments.get("max_content_length", 5000)

    current_agent = get_current_agent()
    messages = load_messages()

    # 解析时间过滤
    since_time = None
    if since:
        try:
            since_time = datetime.fromisoformat(since.replace("Z", "+00:00"))
        except Exception:
            pass

    # 过滤消息
    filtered_messages = []
    for msg in reversed(messages):  # 最新的在前
        # 类型过滤：只处理私聊消息（type为private或未设置）
        msg_type = msg.get("type", "private")
        if msg_type == "group":
            continue

        # 接收者过滤
        if recipient == "*":
            # 获取所有消息（私聊）
            if unread_only and msg.get("read", {}).get(current_agent, True):
                continue
        else:
            recipients = msg.get("recipients", [])
            if recipient not in recipients:
                continue
            if unread_only and msg.get("read", {}).get(current_agent, True):
                continue

        # 时间过滤
        if since_time:
            try:
                msg_time = datetime.fromisoformat(msg.get("timestamp", ""))
                if msg_time < since_time:
                    continue
            except Exception:
                pass

        # 关键词过滤
        if keywords:
            content = msg.get("content", "").lower()
            has_keyword = any(kw.lower() in content for kw in keywords)
            if not has_keyword:
                continue

        filtered_messages.append(msg)

        # 限制数量
        if len(filtered_messages) >= limit:
            break

    if not filtered_messages:
        return [TextContent(type="text", text="📭 没有找到消息")]

    # 格式化输出
    result_lines = [f"📬 消息: 找到 {len(filtered_messages)} 条\n"]

    for msg in filtered_messages:
        read_status = (
            "✅ 已读" if msg.get("read", {}).get(current_agent, False) else "📩 未读"
        )

        result_lines.append(f"\n--- 消息 {msg['id']} ---")
        result_lines.append(
            f"发送者: {msg['sender']} ({msg.get('sender_role', '未知角色')})"
        )
        result_lines.append(f"时间: {msg['timestamp']}")
        result_lines.append(f"状态: {read_status}")
        if msg.get("file_path"):
            result_lines.append(f"文件: {msg['file_path']}")

        # 限制内容长度
        content = msg.get("content", "")
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        result_lines.append(f"\n内容:\n{content}")

    return [TextContent(type="text", text="\n".join(result_lines))]


async def handle_mark_messages_read(arguments: dict[str, Any]) -> list[TextContent]:
    """处理mark_messages_read工具"""
    message_ids = arguments.get("message_ids", [])
    current_agent = get_current_agent()

    messages = load_messages()
    updated_count = 0

    for msg in messages:
        if msg["id"] in message_ids:
            if "read" not in msg:
                msg["read"] = {}
            msg["read"][current_agent] = True
            updated_count += 1

    if updated_count > 0:
        save_messages(messages)

    return [TextContent(type="text", text=f"✅ 已标记 {updated_count} 条消息为已读")]


async def handle_request_help(arguments: dict[str, Any]) -> list[TextContent]:
    """处理request_help工具"""
    recipients_str = arguments.get("recipients", "")
    topic = arguments.get("topic", "")
    description = arguments.get("description", "")
    urgency = arguments.get("urgency", "一般")

    recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]

    if not recipients or not topic or not description:
        return [TextContent(type="text", text="错误: 必须提供接收者、主题和描述")]

    sender = get_current_agent()
    session_id = get_current_session_id()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"

    sessions = load_sessions()
    sender_role = "未知"
    if session_id:
        session_info = sessions.get(session_id, {})
        sender_role = session_info.get("role", "未知")

    urgency_icon = "🚨" if urgency == "紧急" else "⚠️" if urgency == "重要" else "ℹ️"
    content = f"{urgency_icon} 请求帮助\n\n主题: {topic}\n紧急程度: {urgency}\n\n详细描述:\n{description}"

    help_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": sender_role,
        "sender_session_id": session_id,
        "recipients": recipients,
        "content": content,
        "file_path": None,
        "timestamp": datetime.now().isoformat(),
        "read": {recipient: False for recipient in recipients},
    }

    messages.append(help_message)
    save_messages(messages)

    return [
        TextContent(
            type="text",
            text=f"✅ 帮助请求已发送\n接收者: {', '.join(recipients)}\n主题: {topic}\n紧急程度: {urgency}",
        )
    ]


async def handle_request_review(arguments: dict[str, Any]) -> list[TextContent]:
    """处理request_review工具"""
    recipients_str = arguments.get("recipients", "")
    file_path = arguments.get("file_path", "")
    description = arguments.get("description", "")

    recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]

    if not recipients or not file_path:
        return [TextContent(type="text", text="错误: 必须提供接收者和文件路径")]

    # 读取文件内容
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return [TextContent(type="text", text=f"错误: 文件不存在: {file_path}")]
        with open(file_path_obj, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        return [TextContent(type="text", text=f"错误: 读取文件失败: {str(e)}")]

    sender = get_current_agent()
    session_id = get_current_session_id()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"

    sessions = load_sessions()
    sender_role = "未知"
    if session_id:
        session_info = sessions.get(session_id, {})
        sender_role = session_info.get("role", "未知")

    review_content = f"🔍 代码审查请求\n\n文件: {file_path}\n"
    if description:
        review_content += f"说明: {description}\n\n"
    review_content += f"代码内容:\n```\n{file_content[:2000]}...\n```"

    review_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": sender_role,
        "sender_session_id": session_id,
        "recipients": recipients,
        "content": review_content,
        "file_path": file_path,
        "timestamp": datetime.now().isoformat(),
        "read": {recipient: False for recipient in recipients},
    }

    messages.append(review_message)
    save_messages(messages)

    return [
        TextContent(
            type="text",
            text=f"✅ 代码审查请求已发送\n接收者: {', '.join(recipients)}\n文件: {file_path}",
        )
    ]


async def handle_notify_completion(arguments: dict[str, Any]) -> list[TextContent]:
    """处理notify_completion工具"""
    recipients_str = arguments.get("recipients", "")
    task_title = arguments.get("task_title", "")
    summary = arguments.get("summary", "")
    related_files = arguments.get("related_files", [])

    recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]

    if not recipients or not task_title or not summary:
        return [TextContent(type="text", text="错误: 必须提供接收者、任务标题和总结")]

    sender = get_current_agent()
    session_id = get_current_session_id()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"

    sessions = load_sessions()
    sender_role = "未知"
    if session_id:
        session_info = sessions.get(session_id, {})
        sender_role = session_info.get("role", "未知")

    completion_content = (
        f"✅ 任务完成通知\n\n任务: {task_title}\n\n完成情况:\n{summary}"
    )
    if related_files:
        completion_content += f"\n\n相关文件:\n" + "\n".join(
            f"- {f}" for f in related_files
        )

    completion_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": sender_role,
        "sender_session_id": session_id,
        "recipients": recipients,
        "content": completion_content,
        "file_path": None,
        "timestamp": datetime.now().isoformat(),
        "read": {recipient: False for recipient in recipients},
    }

    messages.append(completion_message)
    save_messages(messages)

    return [
        TextContent(
            type="text",
            text=f"✅ 完成通知已发送\n接收者: {', '.join(recipients)}\n任务: {task_title}",
        )
    ]


async def handle_share_code_snippet(arguments: dict[str, Any]) -> list[TextContent]:
    """处理share_code_snippet工具"""
    recipients_str = arguments.get("recipients", "")
    file_path = arguments.get("file_path", "")
    description = arguments.get("description", "")
    line_start = arguments.get("line_start")
    line_end = arguments.get("line_end")

    recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]

    if not recipients or not file_path or not description:
        return [TextContent(type="text", text="错误: 必须提供接收者、文件路径和描述")]

    # 读取文件内容
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return [TextContent(type="text", text=f"错误: 文件不存在: {file_path}")]
        with open(file_path_obj, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 如果指定了行号范围
        if line_start is not None and line_end is not None:
            snippet_lines = lines[line_start - 1 : line_end]
            snippet_content = "".join(snippet_lines)
            line_info = f" (第 {line_start}-{line_end} 行)"
        else:
            snippet_content = "".join(lines)
            line_info = ""

    except Exception as e:
        return [TextContent(type="text", text=f"错误: 读取文件失败: {str(e)}")]

    sender = get_current_agent()
    session_id = get_current_session_id()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"

    sessions = load_sessions()
    sender_role = "未知"
    if session_id:
        session_info = sessions.get(session_id, {})
        sender_role = session_info.get("role", "未知")

    snippet_message_content = f"💻 代码片段分享{line_info}\n\n文件: {file_path}\n说明: {description}\n\n代码:\n```\n{snippet_content[:2000]}...\n```"

    snippet_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": sender_role,
        "sender_session_id": session_id,
        "recipients": recipients,
        "content": snippet_message_content,
        "file_path": file_path,
        "timestamp": datetime.now().isoformat(),
        "read": {recipient: False for recipient in recipients},
    }

    messages.append(snippet_message)
    save_messages(messages)

    return [
        TextContent(
            type="text",
            text=f"✅ 代码片段已分享\n接收者: {', '.join(recipients)}\n文件: {file_path}{line_info}",
        )
    ]


# 导出所有处理器
__all__ = [
    "handle_send_message",
    "handle_receive_messages",
    "handle_mark_messages_read",
    "handle_request_help",
    "handle_request_review",
    "handle_notify_completion",
    "handle_share_code_snippet",
]

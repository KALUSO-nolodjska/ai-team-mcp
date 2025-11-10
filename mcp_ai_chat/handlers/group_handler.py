"""
MCP AI Chat Group - 群组处理器
Group Handler

处理群组相关工具：
- create_group: 创建群组
- send_group_message: 发送群组消息
- receive_group_messages: 接收群组消息
- list_groups: 列出群组
- join_group: 加入群组
- leave_group: 离开群组
- summarize_group_messages: 群组消息摘要
- get_unread_counts: 获取未读统计
- archive_group: 归档群组
- pin_message: 置顶消息
- unpin_message: 取消置顶
"""
from datetime import datetime, timedelta
from pathlib import Path
from mcp.types import TextContent
from typing import Any

# 导入核心功能
from ..core.storage import (
    load_groups, save_groups,
    load_messages, save_messages,
    load_sessions
)
from ..core.session import get_current_agent, get_current_session_id


async def handle_create_group(arguments: dict[str, Any]) -> list[TextContent]:
    """处理create_group工具"""
    name = arguments.get("name", "")
    description = arguments.get("description", "")
    members = arguments.get("members", [])
    
    if not name or not members:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组名称和成员列表"
        )]
    
    groups = load_groups()
    group_id = f"GROUP_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(groups)}"
    creator = get_current_agent()
    session_id = get_current_session_id()
    
    new_group = {
        "name": name,
        "description": description,
        "creator": creator,
        "creator_session_id": session_id,
        "members": list(set(members)),  # 去重
        "created_at": datetime.now().isoformat(),
        "active": True,
        "status": "active"  # P1新增
    }
    
    groups[group_id] = new_group
    save_groups(groups)
    
    return [TextContent(
        type="text",
        text=f"✅ 群组已创建\n群组ID: {group_id}\n名称: {name}\n成员: {', '.join(members)}\n创建者: {creator}"
    )]


async def handle_send_group_message(arguments: dict[str, Any]) -> list[TextContent]:
    """处理send_group_message工具"""
    group_id = arguments.get("group_id", "")
    message = arguments.get("message", "")
    file_path = arguments.get("file_path")
    topic = arguments.get("topic")
    reply_to = arguments.get("reply_to")  # P1新增
    mentions = arguments.get("mentions", [])  # P1新增
    importance = arguments.get("importance", "normal")  # P1新增
    
    if not group_id or not message:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID和消息内容"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    if not group.get("active", True):
        return [TextContent(
            type="text",
            text=f"错误: 群组 {group_id} 已停用"
        )]
    
    current_agent = get_current_agent()
    if current_agent not in group.get("members", []):
        return [TextContent(
            type="text",
            text=f"错误: 你不是群组 {group_id} 的成员"
        )]
    
    # 读取文件内容（如果提供了文件路径）
    content = message
    if file_path:
        try:
            file_path_obj = Path(file_path)
            if file_path_obj.exists():
                with open(file_path_obj, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                return [TextContent(
                    type="text",
                    text=f"错误: 文件不存在: {file_path}"
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"错误: 读取文件失败: {str(e)}"
            )]
    
    # 创建群组消息
    sender = get_current_agent()
    session_id = get_current_session_id()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"
    
    sessions = load_sessions()
    sender_role = "未知"
    if session_id:
        session_info = sessions.get(session_id, {})
        sender_role = session_info.get("role", "未知")
    
    members = group.get("members", [])
    
    # 处理回复消息（P1新增）
    reply_info = {}
    if reply_to:
        reply_msg = next((m for m in messages if m.get("id") == reply_to), None)
        if reply_msg:
            reply_info = {
                "reply_to": reply_to,
                "reply_to_sender": reply_msg.get("sender", ""),
                "reply_to_content": reply_msg.get("content", "")[:200]
            }
    
    new_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": sender_role,
        "sender_session_id": session_id,
        "type": "group",
        "group_id": group_id,
        "group_name": group.get("name", ""),
        "recipients": members,
        "content": content,
        "file_path": file_path if file_path else None,
        "topic": topic,
        "mentions": mentions if mentions else [],  # P1新增
        "importance": importance,  # P1新增
        "is_pinned": False,  # P1新增
        "timestamp": datetime.now().isoformat(),
        "read": {member: False for member in members},
        **reply_info
    }
    
    messages.append(new_message)
    save_messages(messages)
    
    return [TextContent(
        type="text",
        text=f"✅ 群组消息已发送\n群组: {group.get('name', group_id)}\n发送者: {sender}\n成员数: {len(members)}\n消息ID: {message_id}"
    )]


async def handle_receive_group_messages(arguments: dict[str, Any]) -> list[TextContent]:
    """处理receive_group_messages工具"""
    group_id = arguments.get("group_id", "")
    limit = arguments.get("limit", 20)
    unread_only = arguments.get("unread_only", False)
    since = arguments.get("since")
    keywords = arguments.get("keywords", [])
    topic = arguments.get("topic")
    mentions_me = arguments.get("mentions_me", False)  # P1新增
    importance = arguments.get("importance")  # P1新增
    show_pinned = arguments.get("show_pinned", False)  # P1新增
    max_content_length = arguments.get("max_content_length", 5000)
    
    if not group_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    if current_agent not in group.get("members", []):
        return [TextContent(
            type="text",
            text=f"错误: 你不是群组 {group_id} 的成员"
        )]
    
    messages = load_messages()
    
    # 解析时间过滤
    since_time = None
    if since:
        try:
            since_time = datetime.fromisoformat(since.replace('Z', '+00:00'))
        except Exception:
            pass
    
    # 过滤消息
    filtered_messages = []
    for msg in reversed(messages):
        if msg.get("type") != "group" or msg.get("group_id") != group_id:
            continue
        
        if unread_only and msg.get("read", {}).get(current_agent, True):
            continue
        
        if since_time:
            try:
                msg_time = datetime.fromisoformat(msg.get("timestamp", "").replace('Z', '+00:00'))
                if msg_time < since_time:
                    continue
            except Exception:
                pass
        
        if keywords:
            content = msg.get("content", "").lower()
            if not any(kw.lower() in content for kw in keywords):
                continue
        
        if topic and msg.get("topic") != topic:
            continue
        
        # P1新增过滤
        if mentions_me and current_agent not in msg.get("mentions", []):
            continue
        
        if importance and msg.get("importance") != importance:
            continue
        
        filtered_messages.append(msg)
        
        if len(filtered_messages) >= limit:
            break
    
    # P1新增：置顶消息优先显示
    if show_pinned and filtered_messages:
        pinned_msgs = [m for m in filtered_messages if m.get("is_pinned")]
        unpinned_msgs = [m for m in filtered_messages if not m.get("is_pinned")]
        filtered_messages = pinned_msgs + unpinned_msgs
    
    if not filtered_messages:
        return [TextContent(
            type="text",
            text=f"📭 群组中没有找到消息\n群组: {group.get('name', group_id)}"
        )]
    
    # 格式化消息
    result_lines = [f"📬 群组消息 ({group.get('name', group_id)}): 找到 {len(filtered_messages)} 条\n"]
    for msg in filtered_messages:
        read_status = "✅ 已读" if msg.get("read", {}).get(current_agent, False) else "📩 未读"
        
        # 消息头（P1新增置顶标记）
        msg_header = f"\n--- 消息 {msg['id']}"
        if msg.get("is_pinned"):
            msg_header += " 📌 [置顶]"
        msg_header += " ---"
        result_lines.append(msg_header)
        
        result_lines.append(f"发送者: {msg['sender']} ({msg.get('sender_role', '未知角色')})")
        
        # P1新增：重要性标记
        if msg.get("importance") == "high":
            result_lines.append("⚠️ 重要性: 高")
        elif msg.get("importance") == "low":
            result_lines.append("ℹ️ 重要性: 低")
        
        # P1新增：@提醒
        if msg.get("mentions"):
            result_lines.append(f"@提醒: {', '.join(msg['mentions'])}")
        
        # P1新增：回复信息
        if msg.get("reply_to"):
            result_lines.append(f"↩️ 回复 {msg['reply_to_sender']}: {msg.get('reply_to_content', '')[:50]}...")
        
        if msg.get("topic"):
            result_lines.append(f"话题: {msg['topic']}")
        result_lines.append(f"时间: {msg['timestamp']}")
        result_lines.append(f"状态: {read_status}")
        if msg.get("file_path"):
            result_lines.append(f"文件: {msg['file_path']}")
        
        content = msg.get('content', '')
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        result_lines.append(f"\n内容:\n{content}")
    
    return [TextContent(
        type="text",
        text="\n".join(result_lines)
    )]


async def handle_list_groups(arguments: dict[str, Any]) -> list[TextContent]:
    """处理list_groups工具"""
    member_filter = arguments.get("member")
    status_filter = arguments.get("status", "active")  # P1新增
    include_preview = arguments.get("include_preview", False)  # P1新增
    
    current_agent = get_current_agent()
    groups = load_groups()
    messages = load_messages() if include_preview else []
    
    if not groups:
        return [TextContent(
            type="text",
            text="📋 没有群组"
        )]
    
    filtered_groups = []
    for group_id, group_info in groups.items():
        if member_filter:
            if member_filter not in group_info.get("members", []):
                continue
        
        # P1新增：状态过滤
        group_status = group_info.get("status", "active")
        if status_filter != "all":
            if group_status != status_filter:
                continue
        
        filtered_groups.append((group_id, group_info))
    
    if not filtered_groups:
        return [TextContent(
            type="text",
            text=f"📋 没有找到符合条件的群组"
        )]
    
    result_lines = [f"📋 找到 {len(filtered_groups)} 个群组:\n"]
    for group_id, group_info in filtered_groups:
        result_lines.append(f"\n--- {group_id} ---")
        result_lines.append(f"名称: {group_info.get('name', '未知')}")
        result_lines.append(f"描述: {group_info.get('description', '无')}")
        result_lines.append(f"成员: {', '.join(group_info.get('members', []))}")
        result_lines.append(f"创建者: {group_info.get('creator', '未知')}")
        result_lines.append(f"创建时间: {group_info.get('created_at', '未知')}")
        
        # P1新增：状态显示
        group_status = group_info.get("status", "active")
        if group_status == "active":
            result_lines.append("状态: 🟢 活跃")
        elif group_status == "archived":
            result_lines.append("状态: 📦 已归档")
            if group_info.get("archive_reason"):
                result_lines.append(f"归档原因: {group_info.get('archive_reason')}")
        else:
            result_lines.append(f"状态: {'🟢 活跃' if group_info.get('active', True) else '⚪ 停用'}")
        
        # P1新增：消息预览
        if include_preview:
            group_messages = [m for m in reversed(messages) 
                             if m.get("type") == "group" and m.get("group_id") == group_id]
            
            if group_messages:
                last_msg = group_messages[0]
                result_lines.append(f"\n📨 最新消息:")
                result_lines.append(f"   发送者: {last_msg.get('sender')}")
                result_lines.append(f"   时间: {last_msg.get('timestamp', '')[:19]}")
                preview_content = last_msg.get('content', '')[:100]
                result_lines.append(f"   内容: {preview_content}...")
            
            # 未读统计
            unread_count = 0
            mentions_count = 0
            for m in group_messages:
                if not m.get("read", {}).get(current_agent, True):
                    unread_count += 1
                    if current_agent in m.get("mentions", []):
                        mentions_count += 1
            
            if unread_count > 0:
                result_lines.append(f"\n📊 未读: {unread_count}条")
                if mentions_count > 0:
                    result_lines.append(f"   @我: {mentions_count}条")
    
    return [TextContent(
        type="text",
        text="\n".join(result_lines)
    )]


async def handle_join_group(arguments: dict[str, Any]) -> list[TextContent]:
    """处理join_group工具"""
    group_id = arguments.get("group_id", "")
    
    if not group_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    members = group.get("members", [])
    
    if current_agent in members:
        return [TextContent(
            type="text",
            text=f"ℹ️ 你已经是群组 {group.get('name', group_id)} 的成员"
        )]
    
    members.append(current_agent)
    group["members"] = list(set(members))
    groups[group_id] = group
    save_groups(groups)
    
    return [TextContent(
        type="text",
        text=f"✅ 已加入群组\n群组: {group.get('name', group_id)}\n成员数: {len(members)}"
    )]


async def handle_leave_group(arguments: dict[str, Any]) -> list[TextContent]:
    """处理leave_group工具"""
    group_id = arguments.get("group_id", "")
    
    if not group_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    members = group.get("members", [])
    
    if current_agent not in members:
        return [TextContent(
            type="text",
            text=f"错误: 你不是群组 {group_id} 的成员"
        )]
    
    members.remove(current_agent)
    group["members"] = members
    groups[group_id] = group
    save_groups(groups)
    
    return [TextContent(
        type="text",
        text=f"✅ 已离开群组\n群组: {group.get('name', group_id)}"
    )]


async def handle_summarize_group_messages(arguments: dict[str, Any]) -> list[TextContent]:
    """处理summarize_group_messages工具"""
    group_id = arguments.get("group_id", "")
    time_range = arguments.get("time_range", "last_7_days")
    max_length = arguments.get("max_length", 500)
    
    if not group_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    if current_agent not in group.get("members", []):
        return [TextContent(
            type="text",
            text=f"错误: 你不是群组 {group_id} 的成员"
        )]
    
    messages = load_messages()
    
    # 计算时间范围
    now = datetime.now()
    if time_range == "last_24_hours":
        since_time = now - timedelta(hours=24)
    elif time_range == "last_7_days":
        since_time = now - timedelta(days=7)
    elif time_range == "last_30_days":
        since_time = now - timedelta(days=30)
    else:
        try:
            since_time = datetime.fromisoformat(time_range.replace('Z', '+00:00'))
        except Exception:
            since_time = now - timedelta(days=7)
    
    # 获取群组消息
    group_messages = []
    for msg in messages:
        if msg.get("type") == "group" and msg.get("group_id") == group_id:
            try:
                msg_time = datetime.fromisoformat(msg.get("timestamp", "").replace('Z', '+00:00'))
                if msg_time >= since_time:
                    group_messages.append(msg)
            except Exception:
                pass
    
    if not group_messages:
        return [TextContent(
            type="text",
            text=f"📋 群组消息摘要\n群组: {group.get('name', group_id)}\n时间范围: {time_range}\n\n没有找到消息"
        )]
    
    # 生成简单摘要
    summary_lines = [
        f"📋 群组消息摘要",
        f"群组: {group.get('name', group_id)}",
        f"时间范围: {time_range}",
        f"消息总数: {len(group_messages)}",
        f"\n参与者:"
    ]
    
    # 统计参与者
    participants = {}
    for msg in group_messages:
        sender = msg.get("sender", "未知")
        participants[sender] = participants.get(sender, 0) + 1
    
    for sender, count in sorted(participants.items(), key=lambda x: x[1], reverse=True):
        summary_lines.append(f"  - {sender}: {count}条消息")
    
    summary_text = "\n".join(summary_lines)
    if len(summary_text) > max_length:
        summary_text = summary_text[:max_length] + "..."
    
    return [TextContent(
        type="text",
        text=summary_text
    )]


async def handle_get_unread_counts(arguments: dict[str, Any]) -> list[TextContent]:
    """处理get_unread_counts工具（P1新增）"""
    query_groups = arguments.get("groups", [])
    
    current_agent = get_current_agent()
    groups = load_groups()
    messages = load_messages()
    
    # 如果没有指定群组，则查询所有群组
    if not query_groups:
        query_groups = [gid for gid, g in groups.items() 
                       if current_agent in g.get("members", []) and g.get("status", "active") == "active"]
    
    result = {}
    for group_id in query_groups:
        group = groups.get(group_id)
        if not group or current_agent not in group.get("members", []):
            continue
        
        unread_count = 0
        mentions_count = 0
        important_count = 0
        
        for msg in messages:
            if msg.get("type") != "group" or msg.get("group_id") != group_id:
                continue
            
            is_unread = not msg.get("read", {}).get(current_agent, True)
            if is_unread:
                unread_count += 1
                
                if current_agent in msg.get("mentions", []):
                    mentions_count += 1
                
                if msg.get("importance") == "high":
                    important_count += 1
        
        result[group_id] = {
            "group_name": group.get("name", ""),
            "unread": unread_count,
            "mentions": mentions_count,
            "important": important_count
        }
    
    # 格式化输出
    result_lines = ["📊 群组未读消息统计\n"]
    total_unread = 0
    total_mentions = 0
    total_important = 0
    
    for gid, counts in result.items():
        total_unread += counts["unread"]
        total_mentions += counts["mentions"]
        total_important += counts["important"]
        
        if counts["unread"] > 0:
            result_lines.append(f"📁 {counts['group_name']} ({gid})")
            result_lines.append(f"   未读: {counts['unread']}条")
            if counts["mentions"] > 0:
                result_lines.append(f"   @我: {counts['mentions']}条")
            if counts["important"] > 0:
                result_lines.append(f"   重要: {counts['important']}条")
            result_lines.append("")
    
    if total_unread == 0:
        result_lines.append("✅ 所有群组消息已读")
    else:
        result_lines.append(f"📈 总计: {total_unread}条未读 | {total_mentions}条@我 | {total_important}条重要")
    
    return [TextContent(
        type="text",
        text="\n".join(result_lines)
    )]


async def handle_archive_group(arguments: dict[str, Any]) -> list[TextContent]:
    """处理archive_group工具（P1新增）"""
    group_id = arguments.get("group_id", "")
    reason = arguments.get("reason", "")
    
    if not group_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    creator = group.get("creator", "")
    
    # 只有创建者可以归档群组
    if current_agent != creator:
        return [TextContent(
            type="text",
            text=f"错误: 只有创建者（{creator}）可以归档群组"
        )]
    
    # 归档群组
    group["status"] = "archived"
    group["archived_at"] = datetime.now().isoformat()
    group["archived_by"] = current_agent
    if reason:
        group["archive_reason"] = reason
    
    groups[group_id] = group
    save_groups(groups)
    
    return [TextContent(
        type="text",
        text=f"✅ 群组已归档\n群组: {group.get('name', group_id)}\n原因: {reason if reason else '无'}"
    )]


async def handle_pin_message(arguments: dict[str, Any]) -> list[TextContent]:
    """处理pin_message工具（P1新增）"""
    group_id = arguments.get("group_id", "")
    message_id = arguments.get("message_id", "")
    
    if not group_id or not message_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID和消息ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    if current_agent not in group.get("members", []):
        return [TextContent(
            type="text",
            text=f"错误: 你不是群组 {group_id} 的成员"
        )]
    
    messages = load_messages()
    message = next((m for m in messages if m.get("id") == message_id), None)
    
    if not message or message.get("group_id") != group_id:
        return [TextContent(
            type="text",
            text=f"错误: 找不到消息 {message_id}"
        )]
    
    # 置顶消息
    message["is_pinned"] = True
    message["pinned_at"] = datetime.now().isoformat()
    message["pinned_by"] = current_agent
    
    # 更新消息
    for i, m in enumerate(messages):
        if m.get("id") == message_id:
            messages[i] = message
            break
    
    save_messages(messages)
    
    # 更新群组的置顶消息列表
    if "pinned_messages" not in group:
        group["pinned_messages"] = []
    if message_id not in group["pinned_messages"]:
        group["pinned_messages"].append(message_id)
    
    groups[group_id] = group
    save_groups(groups)
    
    return [TextContent(
        type="text",
        text=f"✅ 消息已置顶\n群组: {group.get('name', group_id)}\n消息: {message.get('content', '')[:100]}..."
    )]


async def handle_unpin_message(arguments: dict[str, Any]) -> list[TextContent]:
    """处理unpin_message工具（P1新增）"""
    group_id = arguments.get("group_id", "")
    message_id = arguments.get("message_id", "")
    
    if not group_id or not message_id:
        return [TextContent(
            type="text",
            text="错误: 必须提供群组ID和消息ID"
        )]
    
    groups = load_groups()
    group = groups.get(group_id)
    
    if not group:
        return [TextContent(
            type="text",
            text=f"错误: 找不到群组 {group_id}"
        )]
    
    current_agent = get_current_agent()
    if current_agent not in group.get("members", []):
        return [TextContent(
            type="text",
            text=f"错误: 你不是群组 {group_id} 的成员"
        )]
    
    messages = load_messages()
    message = next((m for m in messages if m.get("id") == message_id), None)
    
    if not message or message.get("group_id") != group_id:
        return [TextContent(
            type="text",
            text=f"错误: 找不到消息 {message_id}"
        )]
    
    # 取消置顶
    message["is_pinned"] = False
    
    # 更新消息
    for i, m in enumerate(messages):
        if m.get("id") == message_id:
            messages[i] = message
            break
    
    save_messages(messages)
    
    # 更新群组的置顶消息列表
    if "pinned_messages" in group and message_id in group["pinned_messages"]:
        group["pinned_messages"].remove(message_id)
        groups[group_id] = group
        save_groups(groups)
    
    return [TextContent(
        type="text",
        text=f"✅ 消息已取消置顶\n群组: {group.get('name', group_id)}"
    )]


# 导出所有处理器
__all__ = [
    'handle_create_group',
    'handle_send_group_message',
    'handle_receive_group_messages',
    'handle_list_groups',
    'handle_join_group',
    'handle_leave_group',
    'handle_summarize_group_messages',
    'handle_get_unread_counts',
    'handle_archive_group',
    'handle_pin_message',
    'handle_unpin_message'
]


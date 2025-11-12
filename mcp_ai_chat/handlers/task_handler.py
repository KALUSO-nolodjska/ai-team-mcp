"""
MCP AI Chat Group - 任务处理器
Task Handler

处理任务相关工具：
- create_task: 创建任务
- assign_task: 分配任务
- update_task_status: 更新任务状态
- get_tasks: 获取任务列表
- delete_task: 删除任务
"""

from datetime import datetime
from mcp.types import TextContent
from typing import Any

# 导入核心功能
from ..core.storage import load_tasks, save_tasks, load_messages, save_messages
from ..core.session import get_current_agent, get_current_session_id


async def handle_create_task(arguments: dict[str, Any]) -> list[TextContent]:
    """处理create_task工具"""
    title = arguments.get("title", "")
    description = arguments.get("description", "")
    priority = arguments.get("priority", "P2")
    due_date = arguments.get("due_date")

    if not title or not description:
        return [TextContent(type="text", text="错误: 必须提供任务标题和描述")]

    tasks = load_tasks()
    task_id = f"TASK_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(tasks)}"
    creator = get_current_agent()
    session_id = get_current_session_id()

    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "待开始",
        "creator": creator,
        "creator_session_id": session_id,
        "assignee": None,
        "created_at": datetime.now().isoformat(),
        "due_date": due_date,
        "updated_at": datetime.now().isoformat(),
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return [
        TextContent(
            type="text",
            text=f"✅ 任务已创建\n任务ID: {task_id}\n标题: {title}\n优先级: {priority}\n状态: 待开始\n创建者: {creator}",
        )
    ]


async def handle_assign_task(arguments: dict[str, Any]) -> list[TextContent]:
    """处理assign_task工具"""
    task_id = arguments.get("task_id", "")
    assignee = arguments.get("assignee", "")

    if not task_id or not assignee:
        return [TextContent(type="text", text="错误: 必须提供任务ID和分配对象")]

    tasks = load_tasks()
    task_found = False
    assigned_task = None

    for task in tasks:
        if task["id"] == task_id:
            task["assignee"] = assignee
            task["status"] = "待开始"
            task["updated_at"] = datetime.now().isoformat()
            task_found = True
            assigned_task = task
            break

    if not task_found:
        return [TextContent(type="text", text=f"错误: 找不到任务 {task_id}")]

    save_tasks(tasks)

    # 发送通知消息
    sender = get_current_agent()
    messages = load_messages()
    message_id = f"{datetime.now().isoformat()}_{len(messages)}"
    session_id = get_current_session_id()

    task_title = assigned_task.get("title", "未知任务") if assigned_task else "未知任务"
    notification_message = {
        "id": message_id,
        "sender": sender,
        "sender_role": "任务分配",
        "sender_session_id": session_id,
        "recipients": [assignee],
        "content": f"📋 任务分配通知\n任务ID: {task_id}\n任务标题: {task_title}\n分配给你: {assignee}",
        "file_path": None,
        "timestamp": datetime.now().isoformat(),
        "read": {assignee: False},
    }

    messages.append(notification_message)
    save_messages(messages)

    return [
        TextContent(
            type="text",
            text=f"✅ 任务已分配\n任务ID: {task_id}\n分配给: {assignee}\n已发送通知消息",
        )
    ]


async def handle_update_task_status(arguments: dict[str, Any]) -> list[TextContent]:
    """处理update_task_status工具"""
    task_id = arguments.get("task_id", "")
    status = arguments.get("status", "")
    progress_note = arguments.get("progress_note", "")

    if not task_id or not status:
        return [TextContent(type="text", text="错误: 必须提供任务ID和状态")]

    tasks = load_tasks()
    task_found = False
    old_status = "未知"

    for task in tasks:
        if task["id"] == task_id:
            old_status = task.get("status", "未知")
            task["status"] = status
            task["updated_at"] = datetime.now().isoformat()
            if progress_note:
                task["progress_note"] = progress_note
            task_found = True
            break

    if not task_found:
        return [TextContent(type="text", text=f"错误: 找不到任务 {task_id}")]

    save_tasks(tasks)

    return [
        TextContent(
            type="text",
            text=f"✅ 任务状态已更新\n任务ID: {task_id}\n状态: {old_status} → {status}",
        )
    ]


async def handle_get_tasks(arguments: dict[str, Any]) -> list[TextContent]:
    """处理get_tasks工具"""
    assignee = arguments.get("assignee", "*")
    status = arguments.get("status")
    priority = arguments.get("priority")

    current_agent = get_current_agent()
    tasks = load_tasks()

    # 权限检查：只有manager可以查看所有任务
    if assignee == "*" and current_agent != "manager":
        assignee = current_agent

    # 过滤任务
    filtered_tasks = []
    for task in tasks:
        # 排除已删除的任务
        if task.get("status") == "已删除":
            continue

        # 分配者过滤
        if assignee != "*":
            task_assignee = task.get("assignee", "")
            if task_assignee != assignee:
                continue

        # 状态过滤
        if status:
            if task.get("status") != status:
                continue

        # 优先级过滤
        if priority:
            if task.get("priority") != priority:
                continue

        filtered_tasks.append(task)

    if not filtered_tasks:
        return [TextContent(type="text", text="📋 没有找到任务")]

    # 格式化输出
    result_lines = [f"📋 任务列表: 找到 {len(filtered_tasks)} 个任务\n"]

    for task in filtered_tasks:
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
            desc = task["description"]
            if len(desc) > 200:
                desc = desc[:200] + "..."
            result_lines.append(f"描述: {desc}")

    return [TextContent(type="text", text="\n".join(result_lines))]


async def handle_delete_task(arguments: dict[str, Any]) -> list[TextContent]:
    """处理delete_task工具"""
    task_ids = arguments.get("task_ids", [])
    permanent = arguments.get("permanent", False)

    if not task_ids:
        return [TextContent(type="text", text="错误: 必须提供至少一个任务ID")]

    current_agent = get_current_agent()
    tasks = load_tasks()
    deleted_count = 0
    failed_tasks = []
    deleted_tasks_info = []

    for task_id in task_ids:
        task_found = False
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                task_found = True
                # 权限检查：只有创建者或manager可以删除
                creator = task.get("creator", "")
                if current_agent != creator and current_agent != "manager":
                    failed_tasks.append(
                        {
                            "id": task_id,
                            "reason": f"权限不足（只有创建者 {creator} 或 manager 可以删除）",
                        }
                    )
                    break

                if permanent:
                    # 硬删除：直接从列表中移除
                    deleted_tasks_info.append(
                        {
                            "id": task_id,
                            "title": task.get("title", "未知"),
                            "type": "永久删除",
                        }
                    )
                    tasks.pop(i)
                else:
                    # 软删除：标记为已删除
                    task["status"] = "已删除"
                    task["deleted_at"] = datetime.now().isoformat()
                    task["deleted_by"] = current_agent
                    deleted_tasks_info.append(
                        {
                            "id": task_id,
                            "title": task.get("title", "未知"),
                            "type": "软删除（标记为已删除）",
                        }
                    )

                deleted_count += 1
                break

        if not task_found:
            failed_tasks.append({"id": task_id, "reason": "任务不存在"})

    save_tasks(tasks)

    # 构建结果消息
    result_lines = [f"✅ 任务删除操作完成"]

    if deleted_count > 0:
        result_lines.append(f"\n成功删除 {deleted_count} 个任务:")
        for info in deleted_tasks_info:
            result_lines.append(f"  - {info['id']}: {info['title']} ({info['type']})")

    if failed_tasks:
        result_lines.append(f"\n失败 {len(failed_tasks)} 个:")
        for fail in failed_tasks:
            result_lines.append(f"  - {fail['id']}: {fail['reason']}")

    return [TextContent(type="text", text="\n".join(result_lines))]


# 导出所有处理器
__all__ = [
    "handle_create_task",
    "handle_assign_task",
    "handle_update_task_status",
    "handle_get_tasks",
    "handle_delete_task",
]

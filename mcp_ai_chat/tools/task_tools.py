"""
MCP AI Chat Group - 任务管理工具定义
Task Management Tools Definitions
"""

from mcp.types import Tool


def get_task_tools():
    """获取任务管理相关工具定义"""
    return [
        Tool(
            name="create_task",
            description="创建任务。用于任务管理和协作",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "任务标题"},
                    "description": {"type": "string", "description": "任务描述"},
                    "priority": {
                        "type": "string",
                        "description": "优先级：P0（紧急）、P1（重要）、P2（一般）",
                        "enum": ["P0", "P1", "P2"],
                    },
                    "due_date": {
                        "type": "string",
                        "description": "截止日期（ISO格式，可选）",
                    },
                },
                "required": ["title", "description", "priority"],
            },
        ),
        Tool(
            name="assign_task",
            description="分配任务给其他AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "assignee": {
                        "type": "string",
                        "description": "分配给谁（例如: a, b, c, d）",
                    },
                },
                "required": ["task_id", "assignee"],
            },
        ),
        Tool(
            name="update_task_status",
            description="更新任务状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "status": {
                        "type": "string",
                        "description": "任务状态",
                        "enum": ["待开始", "进行中", "已完成", "已阻塞", "已取消"],
                    },
                    "progress_note": {
                        "type": "string",
                        "description": "进度说明（可选）",
                    },
                },
                "required": ["task_id", "status"],
            },
        ),
        Tool(
            name="get_tasks",
            description="获取任务列表。权限控制：员工只能看到分配给自己的任务，manager可以看到所有任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "assignee": {
                        "type": "string",
                        "description": "过滤：分配给谁（可选，使用 '*' 获取所有任务，仅对manager有效）",
                    },
                    "status": {
                        "type": "string",
                        "description": "过滤：任务状态（可选）",
                    },
                    "priority": {
                        "type": "string",
                        "description": "过滤：优先级（可选）",
                    },
                },
            },
        ),
        Tool(
            name="delete_task",
            description="删除任务（支持软删除和硬删除）。只有任务创建者或manager可以删除任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "任务ID列表",
                    },
                    "permanent": {
                        "type": "boolean",
                        "description": "是否永久删除（默认为软删除，标记为已删除）",
                        "default": False,
                    },
                },
                "required": ["task_ids"],
            },
        ),
    ]

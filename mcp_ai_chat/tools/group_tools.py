"""
MCP AI Chat Group - 群组管理工具定义
Group Management Tools Definitions
"""

from mcp.types import Tool


def get_group_tools():
    """获取群组管理相关工具定义"""
    return [
        Tool(
            name="create_group",
            description="创建项目群组。用于项目协作，相关AI可以在群组中集中讨论",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "群组名称（例如：知识库本地文件夹挂载项目）",
                    },
                    "description": {"type": "string", "description": "群组描述"},
                    "members": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": '群组成员列表（例如：["manager", "a", "b", "c", "d"]）',
                    },
                },
                "required": ["name", "members"],
            },
        ),
        Tool(
            name="send_group_message",
            description="在群组中发送消息。所有群组成员都能收到",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "群组ID"},
                    "message": {"type": "string", "description": "消息内容"},
                    "file_path": {
                        "type": "string",
                        "description": "可选：要发送的文件路径",
                    },
                    "topic": {
                        "type": "string",
                        "description": "可选：消息主题/话题，便于后续过滤",
                    },
                    "reply_to": {"type": "string", "description": "可选：回复的消息ID"},
                    "mentions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": '可选：@提醒的成员列表，例如：["a", "b"]',
                    },
                    "importance": {
                        "type": "string",
                        "enum": ["low", "normal", "high"],
                        "description": "可选：消息重要性（low/normal/high），默认normal",
                    },
                },
                "required": ["group_id", "message"],
            },
        ),
        Tool(
            name="receive_group_messages",
            description="接收群组消息。支持多种过滤选项以控制上下文长度",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "群组ID"},
                    "limit": {
                        "type": "integer",
                        "description": "返回消息数量限制（默认：20，建议不超过50）",
                        "default": 20,
                    },
                    "unread_only": {
                        "type": "boolean",
                        "description": "是否只返回未读消息（默认：false）",
                        "default": False,
                    },
                    "since": {
                        "type": "string",
                        "description": "时间过滤：只返回此时间之后的消息（ISO格式）",
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "关键词过滤：只返回包含这些关键词的消息",
                    },
                    "topic": {
                        "type": "string",
                        "description": "话题过滤：只返回指定话题的消息",
                    },
                    "mentions_me": {
                        "type": "boolean",
                        "description": "只显示@我的消息（默认：false）",
                        "default": False,
                    },
                    "importance": {
                        "type": "string",
                        "enum": ["low", "normal", "high"],
                        "description": "重要性过滤：只显示指定重要性的消息",
                    },
                    "show_pinned": {
                        "type": "boolean",
                        "description": "优先显示置顶消息（默认：false）",
                        "default": False,
                    },
                    "max_content_length": {
                        "type": "integer",
                        "description": "单条消息内容最大长度（字符数），默认：5000",
                        "default": 5000,
                    },
                },
                "required": ["group_id"],
            },
        ),
        Tool(
            name="list_groups",
            description="列出所有群组",
            inputSchema={
                "type": "object",
                "properties": {
                    "member": {
                        "type": "string",
                        "description": "可选：过滤：只列出包含此成员的群组",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["active", "archived", "all"],
                        "description": "可选：过滤群组状态（active/archived/all），默认active",
                        "default": "active",
                    },
                    "include_preview": {
                        "type": "boolean",
                        "description": "可选：包含最新消息预览和未读统计，默认false",
                        "default": False,
                    },
                },
            },
        ),
        Tool(
            name="join_group",
            description="加入群组",
            inputSchema={
                "type": "object",
                "properties": {"group_id": {"type": "string", "description": "群组ID"}},
                "required": ["group_id"],
            },
        ),
        Tool(
            name="leave_group",
            description="离开群组",
            inputSchema={
                "type": "object",
                "properties": {"group_id": {"type": "string", "description": "群组ID"}},
                "required": ["group_id"],
            },
        ),
        Tool(
            name="summarize_group_messages",
            description="生成群组消息摘要。用于快速了解项目进展，避免上下文过长",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "群组ID"},
                    "time_range": {
                        "type": "string",
                        "description": "时间范围：last_24_hours, last_7_days, last_30_days, 或ISO时间格式",
                        "default": "last_7_days",
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "摘要最大长度（字符数），默认：500",
                        "default": 500,
                    },
                },
                "required": ["group_id"],
            },
        ),
        Tool(
            name="get_unread_counts",
            description="获取群组未读消息统计。返回各群组的未读消息数、@我的消息数、重要消息数",
            inputSchema={
                "type": "object",
                "properties": {
                    "groups": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "可选：要查询的群组ID列表，不传则查询所有群组",
                    }
                },
            },
        ),
        Tool(
            name="archive_group",
            description="归档群组（项目完成后使用）。归档的群组不会显示在默认列表中",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "群组ID"},
                    "reason": {"type": "string", "description": "可选：归档原因"},
                },
                "required": ["group_id"],
            },
        ),
        Tool(
            name="pin_message",
            description="置顶群组消息（重要消息不被淹没）",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "群组ID"},
                    "message_id": {"type": "string", "description": "消息ID"},
                },
                "required": ["group_id", "message_id"],
            },
        ),
        Tool(
            name="unpin_message",
            description="取消置顶群组消息",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "群组ID"},
                    "message_id": {"type": "string", "description": "消息ID"},
                },
                "required": ["group_id", "message_id"],
            },
        ),
    ]

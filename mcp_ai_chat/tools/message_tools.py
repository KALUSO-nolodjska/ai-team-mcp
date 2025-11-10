"""
MCP AI Chat Group - 消息相关工具定义
Message Tools Definitions
"""
from mcp.types import Tool


def get_message_tools():
    """获取消息相关工具定义"""
    return [
        Tool(
            name="send_message",
            description="向其他AI发送消息。格式: use <文件名> send@<接收者1>&<接收者2>&... 例如: use task.md send@a&b",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "string",
                        "description": "接收者列表，用&分隔，例如: a&b 或 a&b&c"
                    },
                    "message": {
                        "type": "string",
                        "description": "可选的消息内容（如果不提供文件路径）"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "要发送的文件路径（相对于工作区）"
                    }
                },
                "required": ["recipients"]
            }
        ),
        Tool(
            name="receive_messages",
            description="接收消息。使用 receive* 接收所有消息，或指定接收者接收特定消息。支持多种过滤选项以控制上下文长度",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "接收者名称，使用 '*' 接收所有消息"
                    },
                    "unread_only": {
                        "type": "boolean",
                        "description": "是否只返回未读消息（默认：false）",
                        "default": False
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回消息数量限制（默认：20，建议不超过50以避免上下文过长）",
                        "default": 20
                    },
                    "since": {
                        "type": "string",
                        "description": "时间过滤：只返回此时间之后的消息（ISO格式，例如：2025-11-10T00:00:00）"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "关键词过滤：只返回包含这些关键词的消息（任一关键词匹配即可）"
                    },
                    "max_content_length": {
                        "type": "integer",
                        "description": "单条消息内容最大长度（字符数），超过部分会被截断（默认：5000）",
                        "default": 5000
                    }
                }
            }
        ),
        Tool(
            name="mark_messages_read",
            description="标记消息为已读",
            inputSchema={
                "type": "object",
                "properties": {
                    "message_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "要标记为已读的消息ID列表"
                    }
                },
                "required": ["message_ids"]
            }
        ),
        Tool(
            name="request_help",
            description="请求其他AI的帮助",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "string",
                        "description": "请求帮助的对象，用&分隔，例如: a&b"
                    },
                    "topic": {
                        "type": "string",
                        "description": "需要帮助的主题"
                    },
                    "description": {
                        "type": "string",
                        "description": "详细描述需要什么帮助"
                    },
                    "urgency": {
                        "type": "string",
                        "description": "紧急程度：紧急、重要、一般",
                        "enum": ["紧急", "重要", "一般"]
                    }
                },
                "required": ["recipients", "topic", "description"]
            }
        ),
        Tool(
            name="request_review",
            description="请求代码审查",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "string",
                        "description": "审查者，用&分隔，例如: b&c"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "需要审查的文件路径"
                    },
                    "description": {
                        "type": "string",
                        "description": "审查说明（可选）"
                    }
                },
                "required": ["recipients", "file_path"]
            }
        ),
        Tool(
            name="notify_completion",
            description="通知任务完成",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "string",
                        "description": "通知对象，用&分隔，例如: manager&a"
                    },
                    "task_title": {
                        "type": "string",
                        "description": "完成的任务标题"
                    },
                    "summary": {
                        "type": "string",
                        "description": "完成情况总结"
                    },
                    "related_files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "相关文件列表（可选）"
                    }
                },
                "required": ["recipients", "task_title", "summary"]
            }
        ),
        Tool(
            name="share_code_snippet",
            description="分享代码片段",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipients": {
                        "type": "string",
                        "description": "分享对象，用&分隔"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "代码文件路径"
                    },
                    "description": {
                        "type": "string",
                        "description": "代码说明"
                    },
                    "line_start": {
                        "type": "integer",
                        "description": "起始行号（可选）"
                    },
                    "line_end": {
                        "type": "integer",
                        "description": "结束行号（可选）"
                    }
                },
                "required": ["recipients", "file_path", "description"]
            }
        )
    ]




#!/usr/bin/env python3
"""
AI聊天群 MCP服务器
允许AI之间互相发送和接收消息
"""

import asyncio
import json
import os
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
import sys

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    # 如果MCP SDK未安装，提供友好的错误提示
    print("错误: 请先安装MCP Python SDK:")
    print("pip install mcp")
    sys.exit(1)

# 消息存储目录
MESSAGES_DIR = Path.home() / ".mcp_ai_chat"
MESSAGES_FILE = MESSAGES_DIR / "messages.json"
AGENTS_FILE = MESSAGES_DIR / "agents.json"
SESSIONS_FILE = MESSAGES_DIR / "sessions.json"
TASKS_FILE = MESSAGES_DIR / "tasks.json"
GROUPS_FILE = MESSAGES_DIR / "groups.json"
STANDBY_FILE = MESSAGES_DIR / "standby.json"
EMPLOYEE_CONFIG_FILE = MESSAGES_DIR / "employee_config.json"

# 工作区根目录（用于读取.mdc文件）
WORKSPACE_ROOT = Path(__file__).parent.parent
RULES_DIR = WORKSPACE_ROOT / ".cursor" / "rules"

# 确保目录存在
MESSAGES_DIR.mkdir(parents=True, exist_ok=True)

# 当前会话ID（从环境变量或注册时生成）
_current_session_id = None


def load_messages() -> list[dict]:
    """加载消息历史"""
    if MESSAGES_FILE.exists():
        try:
            with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_messages(messages: list[dict]) -> None:
    """保存消息历史"""
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def load_agents() -> dict[str, str]:
    """加载AI代理信息"""
    if AGENTS_FILE.exists():
        try:
            with open(AGENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_agents(agents: dict[str, str]) -> None:
    """保存AI代理信息"""
    with open(AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)


def load_sessions() -> dict[str, dict]:
    """加载会话信息"""
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_sessions(sessions: dict[str, dict]) -> None:
    """保存会话信息"""
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def load_tasks() -> list[dict]:
    """加载任务列表"""
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_tasks(tasks: list[dict]) -> None:
    """保存任务列表"""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def load_groups() -> dict[str, dict]:
    """加载群组信息"""
    if GROUPS_FILE.exists():
        try:
            with open(GROUPS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_groups(groups: dict[str, dict]) -> None:
    """保存群组信息"""
    with open(GROUPS_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)


def load_standby() -> dict[str, dict]:
    """加载待命状态"""
    if STANDBY_FILE.exists():
        try:
            with open(STANDBY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_standby(standby: dict[str, dict]) -> None:
    """保存待命状态"""
    with open(STANDBY_FILE, "w", encoding="utf-8") as f:
        json.dump(standby, f, ensure_ascii=False, indent=2)


def load_employee_config() -> dict[str, dict]:
    """加载员工配置"""
    if EMPLOYEE_CONFIG_FILE.exists():
        try:
            with open(EMPLOYEE_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_employee_config(config: dict[str, dict]) -> None:
    """保存员工配置"""
    with open(EMPLOYEE_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_mdc_file(agent_name: str) -> Optional[str]:
    """从.mdc文件加载员工设定"""
    mdc_file = RULES_DIR / f"{agent_name}.mdc"
    if mdc_file.exists():
        try:
            with open(mdc_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    return None


def extract_role_from_mdc(mdc_content: str) -> Optional[str]:
    """从.mdc文件内容中提取角色"""
    lines = mdc_content.split('\n')
    
    # 查找标题行（通常包含角色信息）
    for line in lines[:30]:  # 检查前30行
        line_lower = line.lower()
        # 检查标题格式：如 "# 员工A - 前端开发工程师"
        if line.startswith('#') and ('员工' in line or 'employee' in line_lower):
            if '前端开发工程师' in line or ('前端' in line and '工程师' in line):
                return "前端开发工程师"
            elif '后端开发工程师' in line or ('后端' in line and '工程师' in line):
                return "后端开发工程师"
            elif '全栈开发工程师' in line or ('全栈' in line and '工程师' in line):
                return "全栈开发工程师"
            elif '测试/运维工程师' in line or ('测试' in line and '工程师' in line) or ('运维' in line and '工程师' in line):
                return "测试/运维工程师"
            elif '产品经理' in line:
                return "产品经理"
        
        # 检查register_agent示例中的角色
        if 'register_agent' in line and 'role' in line:
            if '"前端开发工程师"' in line or "'前端开发工程师'" in line:
                return "前端开发工程师"
            elif '"后端开发工程师"' in line or "'后端开发工程师'" in line:
                return "后端开发工程师"
            elif '"全栈开发工程师"' in line or "'全栈开发工程师'" in line:
                return "全栈开发工程师"
            elif '"测试/运维工程师"' in line or "'测试/运维工程师'" in line:
                return "测试/运维工程师"
            elif '"产品经理"' in line or "'产品经理'" in line:
                return "产品经理"
    
    return None


def extract_description_from_mdc(mdc_content: str) -> Optional[str]:
    """从.mdc文件内容中提取描述"""
    lines = mdc_content.split('\n')
    
    # 查找register_agent示例中的description
    for i, line in enumerate(lines[:50]):  # 检查前50行
        if 'register_agent' in line.lower() or 'description' in line.lower():
            # 查找description字段
            for j in range(i, min(i + 10, len(lines))):
                desc_line = lines[j]
                if 'description' in desc_line.lower() and ('"' in desc_line or "'" in desc_line):
                    # 提取引号中的内容
                    match = re.search(r'["\']([^"\']+)["\']', desc_line)
                    if match:
                        desc = match.group(1).strip()
                        if desc and len(desc) > 5:
                            return desc
    
    # 查找包含"负责"的行
    for line in lines[:50]:
        if '负责' in line and len(line.strip()) > 10:
            desc = line.strip()
            # 清理markdown格式
            desc = desc.replace('**', '').replace('*', '').strip()
            if desc and len(desc) > 5:
                return desc
    
    return None


def get_current_agent() -> str:
    """获取当前AI代理名称"""
    # 从环境变量或配置中获取
    return os.environ.get("MCP_AI_CHAT_AGENT_NAME", "unknown")


def get_current_session_id() -> Optional[str]:
    """获取当前会话ID"""
    global _current_session_id
    if _current_session_id:
        return _current_session_id
    
    # 尝试从环境变量获取
    session_id = os.environ.get("MCP_AI_CHAT_SESSION_ID")
    if session_id:
        _current_session_id = session_id
        return session_id
    
    # 尝试从注册的代理中获取
    agent_name = get_current_agent()
    sessions = load_sessions()
    for session_id, session_info in sessions.items():
        if session_info.get("agent_name") == agent_name and session_info.get("active", False):
            _current_session_id = session_id
            return session_id
    
    return None


def create_session(agent_name: str, role: str, description: str = "") -> str:
    """创建新会话"""
    session_id = str(uuid.uuid4())
    sessions = load_sessions()
    
    # 将同一代理的其他会话标记为非活跃
    for sid, sinfo in sessions.items():
        if sinfo.get("agent_name") == agent_name:
            sinfo["active"] = False
    
    sessions[session_id] = {
        "agent_name": agent_name,
        "role": role,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "active": True
    }
    
    save_sessions(sessions)
    global _current_session_id
    _current_session_id = session_id
    return session_id


# 创建MCP服务器
server = Server("ai-chat-group")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用工具"""
    return [
        Tool(
            name="send_message",
            description="向其他AI发送消息。格式: use <文件名> send@<接收者1>&<接收者2>&... 例如: use task.md send@a&b",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要发送的文件路径（相对于工作区）"
                    },
                    "recipients": {
                        "type": "string",
                        "description": "接收者列表，用&分隔，例如: a&b 或 a&b&c"
                    },
                    "message": {
                        "type": "string",
                        "description": "可选的消息内容（如果不提供文件路径）"
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
                    "limit": {
                        "type": "integer",
                        "description": "返回消息数量限制（默认：20，建议不超过50以避免上下文过长）",
                        "default": 20
                    },
                    "unread_only": {
                        "type": "boolean",
                        "description": "是否只返回未读消息（默认：false）",
                        "default": False
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
                        "description": "单条消息内容最大长度（字符数），超过部分会被截断（默认：500）",
                        "default": 500
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
            name="register_agent",
            description="注册当前AI代理并创建会话。如果agent_name已存在，会自动拾取之前的任务。如果设置了员工配置，会从.mdc文件自动加载角色和描述",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "AI代理名称（例如: a, b, c, d, manager）"
                    },
                    "role": {
                        "type": "string",
                        "description": "AI角色（例如: 前端开发工程师、后端开发工程师、全栈开发工程师、测试/运维工程师、产品经理）。如果设置了员工配置，会自动从.mdc文件读取"
                    },
                    "description": {
                        "type": "string",
                        "description": "AI代理描述。如果设置了员工配置，会自动从.mdc文件读取"
                    },
                    "auto_load_from_mdc": {
                        "type": "boolean",
                        "description": "是否自动从.mdc文件加载员工设定（默认：true）",
                        "default": True
                    }
                },
                "required": ["agent_name"]
            }
        ),
        Tool(
            name="set_employee_config",
            description="设置员工配置，指定.mdc文件路径。设置后，register_agent会自动从.mdc文件读取角色和描述",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "AI代理名称（例如: a, b, c, d, manager）"
                    },
                    "mdc_file_path": {
                        "type": "string",
                        "description": ".mdc文件路径（相对于工作区根目录，例如: .cursor/rules/a.mdc）。如果为空，则使用默认路径 .cursor/rules/{agent_name}.mdc"
                    }
                },
                "required": ["agent_name"]
            }
        ),
        Tool(
            name="get_current_session",
            description="获取当前AI的会话信息",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_agents",
            description="列出所有已注册的AI代理",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="create_task",
            description="创建任务。用于任务管理和协作",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "任务标题"
                    },
                    "description": {
                        "type": "string",
                        "description": "任务描述"
                    },
                    "priority": {
                        "type": "string",
                        "description": "优先级：P0（紧急）、P1（重要）、P2（一般）",
                        "enum": ["P0", "P1", "P2"]
                    },
                    "due_date": {
                        "type": "string",
                        "description": "截止日期（ISO格式，可选）"
                    }
                },
                "required": ["title", "description", "priority"]
            }
        ),
        Tool(
            name="assign_task",
            description="分配任务给其他AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "任务ID"
                    },
                    "assignee": {
                        "type": "string",
                        "description": "分配给谁（例如: a, b, c, d）"
                    }
                },
                "required": ["task_id", "assignee"]
            }
        ),
        Tool(
            name="update_task_status",
            description="更新任务状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "任务ID"
                    },
                    "status": {
                        "type": "string",
                        "description": "任务状态",
                        "enum": ["待开始", "进行中", "已完成", "已阻塞", "已取消"]
                    },
                    "progress_note": {
                        "type": "string",
                        "description": "进度说明（可选）"
                    }
                },
                "required": ["task_id", "status"]
            }
        ),
        Tool(
            name="get_tasks",
            description="获取任务列表。权限控制：员工只能看到分配给自己的任务，manager可以看到所有任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "assignee": {
                        "type": "string",
                        "description": "过滤：分配给谁（可选，使用 '*' 获取所有任务，仅对manager有效）"
                    },
                    "status": {
                        "type": "string",
                        "description": "过滤：任务状态（可选）"
                    },
                    "priority": {
                        "type": "string",
                        "description": "过滤：优先级（可选）"
                    }
                }
            }
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
                        "description": "任务ID列表"
                    },
                    "permanent": {
                        "type": "boolean",
                        "description": "是否永久删除（默认为软删除，标记为已删除）",
                        "default": False
                    }
                },
                "required": ["task_ids"]
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
        ),
        Tool(
            name="create_group",
            description="创建项目群组。用于项目协作，相关AI可以在群组中集中讨论",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "群组名称（例如：知识库本地文件夹挂载项目）"
                    },
                    "description": {
                        "type": "string",
                        "description": "群组描述"
                    },
                    "members": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "群组成员列表（例如：[\"manager\", \"a\", \"b\", \"c\", \"d\"]）"
                    }
                },
                "required": ["name", "members"]
            }
        ),
        Tool(
            name="send_group_message",
            description="在群组中发送消息。所有群组成员都能收到",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    },
                    "message": {
                        "type": "string",
                        "description": "消息内容"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "可选：要发送的文件路径"
                    },
                    "topic": {
                        "type": "string",
                        "description": "可选：消息主题/话题，便于后续过滤"
                    },
                    "reply_to": {
                        "type": "string",
                        "description": "可选：回复的消息ID"
                    },
                    "mentions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "可选：@提醒的成员列表，例如：[\"a\", \"b\"]"
                    },
                    "importance": {
                        "type": "string",
                        "enum": ["low", "normal", "high"],
                        "description": "可选：消息重要性（low/normal/high），默认normal"
                    }
                },
                "required": ["group_id", "message"]
            }
        ),
        Tool(
            name="receive_group_messages",
            description="接收群组消息。支持多种过滤选项以控制上下文长度",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回消息数量限制（默认：20，建议不超过50）",
                        "default": 20
                    },
                    "unread_only": {
                        "type": "boolean",
                        "description": "是否只返回未读消息（默认：false）",
                        "default": False
                    },
                    "since": {
                        "type": "string",
                        "description": "时间过滤：只返回此时间之后的消息（ISO格式）"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "关键词过滤：只返回包含这些关键词的消息"
                    },
                    "topic": {
                        "type": "string",
                        "description": "话题过滤：只返回指定话题的消息"
                    },
                    "mentions_me": {
                        "type": "boolean",
                        "description": "只显示@我的消息（默认：false）",
                        "default": False
                    },
                    "importance": {
                        "type": "string",
                        "enum": ["low", "normal", "high"],
                        "description": "重要性过滤：只显示指定重要性的消息"
                    },
                    "show_pinned": {
                        "type": "boolean",
                        "description": "优先显示置顶消息（默认：false）",
                        "default": False
                    },
                    "max_content_length": {
                        "type": "integer",
                        "description": "单条消息内容最大长度（字符数），默认：5000",
                        "default": 5000
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="list_groups",
            description="列出所有群组",
            inputSchema={
                "type": "object",
                "properties": {
                    "member": {
                        "type": "string",
                        "description": "可选：过滤：只列出包含此成员的群组"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["active", "archived", "all"],
                        "description": "可选：过滤群组状态（active/archived/all），默认active",
                        "default": "active"
                    },
                    "include_preview": {
                        "type": "boolean",
                        "description": "可选：包含最新消息预览和未读统计，默认false",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="join_group",
            description="加入群组",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="leave_group",
            description="离开群组",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="summarize_group_messages",
            description="生成群组消息摘要。用于快速了解项目进展，避免上下文过长",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    },
                    "time_range": {
                        "type": "string",
                        "description": "时间范围：last_24_hours, last_7_days, last_30_days, 或ISO时间格式",
                        "default": "last_7_days"
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "摘要最大长度（字符数），默认：500",
                        "default": 500
                    }
                },
                "required": ["group_id"]
            }
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
                        "description": "可选：要查询的群组ID列表，不传则查询所有群组"
                    }
                }
            }
        ),
        Tool(
            name="archive_group",
            description="归档群组（项目完成后使用）。归档的群组不会显示在默认列表中",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    },
                    "reason": {
                        "type": "string",
                        "description": "可选：归档原因"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="pin_message",
            description="置顶群组消息（重要消息不被淹没）",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    },
                    "message_id": {
                        "type": "string",
                        "description": "消息ID"
                    }
                },
                "required": ["group_id", "message_id"]
            }
        ),
        Tool(
            name="unpin_message",
            description="取消置顶群组消息",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "群组ID"
                    },
                    "message_id": {
                        "type": "string",
                        "description": "消息ID"
                    }
                },
                "required": ["group_id", "message_id"]
            }
        ),
        Tool(
            name="standby",
            description="进入待命状态，定时器强制为5分钟。在5分钟内持续监听任务和消息，如果收到新任务/消息立即返回继续工作，如果5分钟内没有新任务/消息则继续等待。建议在回复末尾调用此工具",
            inputSchema={
                "type": "object",
                "properties": {
                    "status_message": {
                        "type": "string",
                        "description": "待命状态消息，用于说明当前状态"
                    },
                    "check_tasks": {
                        "type": "boolean",
                        "description": "是否检查任务，默认：true",
                        "default": True
                    },
                    "check_messages": {
                        "type": "boolean",
                        "description": "是否检查消息，默认：true",
                        "default": True
                    },
                    "auto_read": {
                        "type": "boolean",
                        "description": "是否自动读取新任务/消息内容，默认：true",
                        "default": True
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """处理工具调用"""
    
    if name == "send_message":
        recipients_str = arguments.get("recipients", "")
        file_path = arguments.get("file_path")
        message = arguments.get("message", "")
        
        # 解析接收者列表
        recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]
        
        if not recipients:
            return [TextContent(
                type="text",
                text="错误: 必须指定至少一个接收者"
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
        
        if not content:
            return [TextContent(
                type="text",
                text="错误: 消息内容为空"
            )]
        
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
            "read": {recipient: False for recipient in recipients}
        }
        
        messages.append(new_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 消息已发送\n发送者: {sender}\n接收者: {', '.join(recipients)}\n消息ID: {message_id}\n内容长度: {len(content)} 字符"
        )]
    
    elif name == "receive_messages":
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
                since_time = datetime.fromisoformat(since.replace('Z', '+00:00'))
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
                # 获取特定接收者的消息
                if recipient not in msg.get("recipients", []):
                    continue
                if unread_only and msg.get("read", {}).get(recipient, True):
                    continue
            
            # 时间过滤
            if since_time:
                try:
                    msg_time = datetime.fromisoformat(msg.get("timestamp", "").replace('Z', '+00:00'))
                    if msg_time < since_time:
                        continue
                except Exception:
                    pass
            
            # 关键词过滤
            if keywords:
                content = msg.get("content", "").lower()
                if not any(kw.lower() in content for kw in keywords):
                    continue
            
            filtered_messages.append(msg)
            
            if len(filtered_messages) >= limit:
                break
        
        if not filtered_messages:
            return [TextContent(
                type="text",
                text=f"📭 没有找到消息\n接收者: {recipient}\n未读 only: {unread_only}"
            )]
        
        # 格式化消息
        result_lines = [f"📬 找到 {len(filtered_messages)} 条消息\n"]
        for msg in filtered_messages:
            read_status = "✅ 已读" if msg.get("read", {}).get(current_agent, False) else "📩 未读"
            result_lines.append(f"\n--- 消息 {msg['id']} ---")
            result_lines.append(f"发送者: {msg['sender']} ({msg.get('sender_role', '未知角色')})")
            result_lines.append(f"接收者: {', '.join(msg.get('recipients', []))}")
            result_lines.append(f"时间: {msg['timestamp']}")
            result_lines.append(f"状态: {read_status}")
            if msg.get("file_path"):
                result_lines.append(f"文件: {msg['file_path']}")
            
            # 限制内容长度
            content = msg.get('content', '')
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            result_lines.append(f"\n内容:\n{content}")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    
    elif name == "mark_messages_read":
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
        
        return [TextContent(
            type="text",
            text=f"✅ 已标记 {updated_count} 条消息为已读"
        )]
    
    elif name == "set_employee_config":
        agent_name = arguments.get("agent_name", "")
        mdc_file_path = arguments.get("mdc_file_path", "")
        
        if not agent_name:
            return [TextContent(
                type="text",
                text="错误: 必须提供代理名称"
            )]
        
        # 确定.mdc文件路径
        if mdc_file_path:
            mdc_path = WORKSPACE_ROOT / mdc_file_path
        else:
            mdc_path = RULES_DIR / f"{agent_name}.mdc"
        
        if not mdc_path.exists():
            return [TextContent(
                type="text",
                text=f"错误: .mdc文件不存在: {mdc_path}"
            )]
        
        # 保存员工配置
        config = load_employee_config()
        config[agent_name] = {
            "mdc_file_path": str(mdc_path.relative_to(WORKSPACE_ROOT)),
            "updated_at": datetime.now().isoformat()
        }
        save_employee_config(config)
        
        return [TextContent(
            type="text",
            text=f"✅ 员工配置已设置\n代理名称: {agent_name}\n.mdc文件: {mdc_path.relative_to(WORKSPACE_ROOT)}\n\n💡 提示: 现在可以使用 register_agent 自动加载角色和描述"
        )]
    
    elif name == "register_agent":
        agent_name = arguments.get("agent_name", "")
        role = arguments.get("role", "")
        description = arguments.get("description", "")
        auto_load_from_mdc = arguments.get("auto_load_from_mdc", True)
        
        if not agent_name:
            return [TextContent(
                type="text",
                text="错误: 必须提供代理名称"
            )]
        
        # 检查是否有之前的代理信息
        agents = load_agents()
        previous_agent_info = agents.get(agent_name, {})
        previous_role = previous_agent_info.get("role", "")
        previous_description = previous_agent_info.get("description", "")
        
        # 尝试从.mdc文件加载员工设定
        if auto_load_from_mdc:
            config = load_employee_config()
            if agent_name in config:
                mdc_content = load_mdc_file(agent_name)
                if mdc_content:
                    if not role:
                        role = extract_role_from_mdc(mdc_content) or previous_role
                    if not description:
                        description = extract_description_from_mdc(mdc_content) or previous_description
        
        # 如果没有提供角色，使用之前的角色或要求提供
        if not role:
            if previous_role:
                role = previous_role
            else:
                return [TextContent(
                    type="text",
                    text=f"错误: 必须提供角色信息\n提示: 可以使用 set_employee_config 设置员工配置，然后自动从.mdc文件加载"
                )]
        
        # 如果没有提供描述，使用之前的描述
        if not description:
            description = previous_description or ""
        
        # 创建会话
        session_id = create_session(agent_name, role, description)
        
        # 注册代理
        agent_info = {
            "role": role,
            "description": description,
            "session_id": session_id,
            "registered_at": datetime.now().isoformat(),
            "previous_registered_at": previous_agent_info.get("registered_at")
        }
        agents[agent_name] = agent_info
        save_agents(agents)
        
        # 检查是否有分配给该代理的任务
        tasks = load_tasks()
        agent_tasks = [t for t in tasks if t.get("assignee") == agent_name and t.get("status") in ["待开始", "进行中"]]
        
        result_lines = [
            f"✅ AI代理已注册并创建会话",
            f"名称: {agent_name}",
            f"角色: {role}",
            f"描述: {description}",
            f"会话ID: {session_id}"
        ]
        
        if previous_agent_info:
            result_lines.append(f"\n🔄 已继承之前的代理信息")
            if previous_role:
                result_lines.append(f"之前的角色: {previous_role}")
            if previous_description:
                result_lines.append(f"之前的描述: {previous_description}")
        
        if agent_tasks:
            result_lines.append(f"\n📋 发现 {len(agent_tasks)} 个待处理任务:")
            for task in agent_tasks[:5]:  # 最多显示5个
                result_lines.append(f"  - {task.get('id', '未知')}: {task.get('title', '未知')} ({task.get('status', '未知')})")
            if len(agent_tasks) > 5:
                result_lines.append(f"  ... 还有 {len(agent_tasks) - 5} 个任务")
        
        result_lines.append(f"\n⚠️ 重要: 请记住你的会话ID，这是你在这次对话中的唯一身份标识")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    
    elif name == "get_current_session":
        session_id = get_current_session_id()
        if not session_id:
            return [TextContent(
                type="text",
                text="❌ 当前没有活跃会话\n请先使用 register_agent 注册代理并创建会话"
            )]
        
        sessions = load_sessions()
        session_info = sessions.get(session_id, {})
        agent_name = get_current_agent()
        
        return [TextContent(
            type="text",
            text=f"📋 当前会话信息\n会话ID: {session_id}\n代理名称: {session_info.get('agent_name', agent_name)}\n角色: {session_info.get('role', '未知')}\n描述: {session_info.get('description', '无')}\n创建时间: {session_info.get('created_at', '未知')}\n状态: {'活跃' if session_info.get('active', False) else '非活跃'}"
        )]
    
    elif name == "list_agents":
        agents = load_agents()
        sessions = load_sessions()
        
        if not agents:
            return [TextContent(
                type="text",
                text="📋 没有已注册的AI代理"
            )]
        
        result_lines = [f"📋 已注册的AI代理 ({len(agents)}):\n"]
        for name, info in agents.items():
            if isinstance(info, dict):
                role = info.get('role', '未知角色')
                description = info.get('description', '无描述')
                session_id = info.get('session_id', '无')
                registered_at = info.get('registered_at', '未知')
            else:
                role = '未知角色'
                description = '无描述'
                session_id = '无'
                registered_at = '未知'
            
            # 检查会话是否活跃
            session_info = sessions.get(session_id, {})
            active_status = "🟢 活跃" if session_info.get('active', False) else "⚪ 非活跃"
            
            result_lines.append(f"\n- {name} ({role}) - {active_status}")
            result_lines.append(f"  描述: {description}")
            result_lines.append(f"  会话ID: {session_id}")
            result_lines.append(f"  注册时间: {registered_at}")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    
    elif name == "create_task":
        title = arguments.get("title", "")
        description = arguments.get("description", "")
        priority = arguments.get("priority", "P2")
        due_date = arguments.get("due_date")
        
        if not title or not description:
            return [TextContent(
                type="text",
                text="错误: 必须提供任务标题和描述"
            )]
        
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
            "updated_at": datetime.now().isoformat()
        }
        
        tasks.append(new_task)
        save_tasks(tasks)
        
        return [TextContent(
            type="text",
            text=f"✅ 任务已创建\n任务ID: {task_id}\n标题: {title}\n优先级: {priority}\n状态: 待开始\n创建者: {creator}"
        )]
    
    elif name == "assign_task":
        task_id = arguments.get("task_id", "")
        assignee = arguments.get("assignee", "")
        
        if not task_id or not assignee:
            return [TextContent(
                type="text",
                text="错误: 必须提供任务ID和分配对象"
            )]
        
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
            return [TextContent(
                type="text",
                text=f"错误: 找不到任务 {task_id}"
            )]
        
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
            "read": {assignee: False}
        }
        
        messages.append(notification_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 任务已分配\n任务ID: {task_id}\n分配给: {assignee}\n已发送通知消息"
        )]
    
    elif name == "update_task_status":
        task_id = arguments.get("task_id", "")
        status = arguments.get("status", "")
        progress_note = arguments.get("progress_note", "")
        
        if not task_id or not status:
            return [TextContent(
                type="text",
                text="错误: 必须提供任务ID和状态"
            )]
        
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
            return [TextContent(
                type="text",
                text=f"错误: 找不到任务 {task_id}"
            )]
        
        save_tasks(tasks)
        
        return [TextContent(
            type="text",
            text=f"✅ 任务状态已更新\n任务ID: {task_id}\n状态: {old_status} → {status}"
        )]
    
    elif name == "delete_task":
        task_ids = arguments.get("task_ids", [])
        permanent = arguments.get("permanent", False)
        
        if not task_ids:
            return [TextContent(
                type="text",
                text="错误: 必须提供至少一个任务ID"
            )]
        
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
                        failed_tasks.append({
                            "id": task_id,
                            "reason": f"权限不足（只有创建者 {creator} 或 manager 可以删除）"
                        })
                        break
                    
                    if permanent:
                        # 硬删除：直接从列表中移除
                        deleted_tasks_info.append({
                            "id": task_id,
                            "title": task.get("title", "未知"),
                            "type": "永久删除"
                        })
                        tasks.pop(i)
                    else:
                        # 软删除：标记为已删除
                        task["status"] = "已删除"
                        task["deleted_at"] = datetime.now().isoformat()
                        task["deleted_by"] = current_agent
                        deleted_tasks_info.append({
                            "id": task_id,
                            "title": task.get("title", "未知"),
                            "type": "软删除（标记为已删除）"
                        })
                    
                    deleted_count += 1
                    break
            
            if not task_found:
                failed_tasks.append({
                    "id": task_id,
                    "reason": "任务不存在"
                })
        
        save_tasks(tasks)
        
        # 构建返回消息
        result_lines = [f"✅ 任务删除操作完成\n"]
        result_lines.append(f"成功: {deleted_count}个")
        result_lines.append(f"失败: {len(failed_tasks)}个")
        
        if deleted_tasks_info:
            result_lines.append(f"\n📋 已删除任务:")
            for info in deleted_tasks_info:
                result_lines.append(f"- {info['id']}: {info['title']} ({info['type']})")
        
        if failed_tasks:
            result_lines.append(f"\n⚠️ 删除失败:")
            for fail in failed_tasks:
                result_lines.append(f"- {fail['id']}: {fail['reason']}")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    
    elif name == "get_tasks":
        assignee_filter = arguments.get("assignee")
        status_filter = arguments.get("status")
        priority_filter = arguments.get("priority")
        
        # 获取当前代理
        current_agent = get_current_agent()
        
        tasks = load_tasks()
        filtered_tasks = []
        
        for task in tasks:
            # 权限控制：员工只能看到分配给自己的任务，manager可以看到所有任务
            if current_agent != "manager":
                # 非manager用户只能看到分配给自己的任务
                if task.get("assignee") != current_agent:
                    continue
            
            # 应用其他过滤条件
            if assignee_filter and assignee_filter != "*" and task.get("assignee") != assignee_filter:
                continue
            if status_filter and task.get("status") != status_filter:
                continue
            if priority_filter and task.get("priority") != priority_filter:
                continue
            filtered_tasks.append(task)
        
        if not filtered_tasks:
            return [TextContent(
                type="text",
                text="📋 没有找到符合条件的任务"
            )]
        
        # 添加权限提示
        permission_hint = ""
        if current_agent != "manager":
            permission_hint = f" (仅显示分配给 {current_agent} 的任务)"
        
        result_lines = [f"📋 找到 {len(filtered_tasks)} 个任务{permission_hint}:\n"]
        for task in filtered_tasks:
            assignee = task.get("assignee", "未分配")
            result_lines.append(f"\n--- {task['id']} ---")
            result_lines.append(f"标题: {task['title']}")
            result_lines.append(f"优先级: {task['priority']}")
            result_lines.append(f"状态: {task['status']}")
            result_lines.append(f"分配给: {assignee}")
            result_lines.append(f"创建时间: {task['created_at']}")
            if task.get("due_date"):
                result_lines.append(f"截止日期: {task['due_date']}")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    
    elif name == "request_help":
        recipients_str = arguments.get("recipients", "")
        topic = arguments.get("topic", "")
        description = arguments.get("description", "")
        urgency = arguments.get("urgency", "一般")
        
        recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]
        
        if not recipients or not topic or not description:
            return [TextContent(
                type="text",
                text="错误: 必须提供接收者、主题和描述"
            )]
        
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
            "read": {recipient: False for recipient in recipients}
        }
        
        messages.append(help_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 帮助请求已发送\n接收者: {', '.join(recipients)}\n主题: {topic}\n紧急程度: {urgency}"
        )]
    
    elif name == "request_review":
        recipients_str = arguments.get("recipients", "")
        file_path = arguments.get("file_path", "")
        description = arguments.get("description", "")
        
        recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]
        
        if not recipients or not file_path:
            return [TextContent(
                type="text",
                text="错误: 必须提供接收者和文件路径"
            )]
        
        # 读取文件内容
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return [TextContent(
                    type="text",
                    text=f"错误: 文件不存在: {file_path}"
                )]
            with open(file_path_obj, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"错误: 读取文件失败: {str(e)}"
            )]
        
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
            "read": {recipient: False for recipient in recipients}
        }
        
        messages.append(review_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 代码审查请求已发送\n接收者: {', '.join(recipients)}\n文件: {file_path}"
        )]
    
    elif name == "notify_completion":
        recipients_str = arguments.get("recipients", "")
        task_title = arguments.get("task_title", "")
        summary = arguments.get("summary", "")
        related_files = arguments.get("related_files", [])
        
        recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]
        
        if not recipients or not task_title or not summary:
            return [TextContent(
                type="text",
                text="错误: 必须提供接收者、任务标题和总结"
            )]
        
        sender = get_current_agent()
        session_id = get_current_session_id()
        messages = load_messages()
        message_id = f"{datetime.now().isoformat()}_{len(messages)}"
        
        sessions = load_sessions()
        sender_role = "未知"
        if session_id:
            session_info = sessions.get(session_id, {})
            sender_role = session_info.get("role", "未知")
        
        completion_content = f"✅ 任务完成通知\n\n任务: {task_title}\n\n完成情况:\n{summary}"
        if related_files:
            completion_content += f"\n\n相关文件:\n" + "\n".join(f"- {f}" for f in related_files)
        
        completion_message = {
            "id": message_id,
            "sender": sender,
            "sender_role": sender_role,
            "sender_session_id": session_id,
            "recipients": recipients,
            "content": completion_content,
            "file_path": None,
            "timestamp": datetime.now().isoformat(),
            "read": {recipient: False for recipient in recipients}
        }
        
        messages.append(completion_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 完成通知已发送\n接收者: {', '.join(recipients)}\n任务: {task_title}"
        )]
    
    elif name == "share_code_snippet":
        recipients_str = arguments.get("recipients", "")
        file_path = arguments.get("file_path", "")
        description = arguments.get("description", "")
        line_start = arguments.get("line_start")
        line_end = arguments.get("line_end")
        
        recipients = [r.strip() for r in recipients_str.split("&") if r.strip()]
        
        if not recipients or not file_path or not description:
            return [TextContent(
                type="text",
                text="错误: 必须提供接收者、文件路径和描述"
            )]
        
        # 读取文件内容
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return [TextContent(
                    type="text",
                    text=f"错误: 文件不存在: {file_path}"
                )]
            with open(file_path_obj, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # 如果指定了行号范围
            if line_start is not None and line_end is not None:
                snippet_lines = lines[line_start-1:line_end]
                snippet_content = "".join(snippet_lines)
                line_info = f" (第 {line_start}-{line_end} 行)"
            else:
                snippet_content = "".join(lines)
                line_info = ""
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"错误: 读取文件失败: {str(e)}"
            )]
        
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
            "read": {recipient: False for recipient in recipients}
        }
        
        messages.append(snippet_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 代码片段已分享\n接收者: {', '.join(recipients)}\n文件: {file_path}{line_info}"
        )]
    
    elif name == "create_group":
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
            "active": True
        }
        
        groups[group_id] = new_group
        save_groups(groups)
        
        return [TextContent(
            type="text",
            text=f"✅ 群组已创建\n群组ID: {group_id}\n名称: {name}\n成员: {', '.join(members)}\n创建者: {creator}"
        )]
    
    elif name == "send_group_message":
        group_id = arguments.get("group_id", "")
        message = arguments.get("message", "")
        file_path = arguments.get("file_path")
        topic = arguments.get("topic")
        reply_to = arguments.get("reply_to")  # 新增：回复的消息ID
        mentions = arguments.get("mentions", [])  # 新增：@提醒列表
        importance = arguments.get("importance", "normal")  # 新增：重要性级别
        
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
        
        # 处理回复消息
        reply_info = {}
        if reply_to:
            # 查找被回复的消息
            reply_msg = next((m for m in messages if m.get("id") == reply_to), None)
            if reply_msg:
                reply_info = {
                    "reply_to": reply_to,
                    "reply_to_sender": reply_msg.get("sender", ""),
                    "reply_to_content": reply_msg.get("content", "")[:200]  # 只保存前200字符
                }
        
        new_message = {
            "id": message_id,
            "sender": sender,
            "sender_role": sender_role,
            "sender_session_id": session_id,
            "type": "group",
            "group_id": group_id,
            "group_name": group.get("name", ""),
            "recipients": members,  # 群组所有成员
            "content": content,
            "file_path": file_path if file_path else None,
            "topic": topic,
            "mentions": mentions if mentions else [],  # 新增：@提醒列表
            "importance": importance,  # 新增：重要性
            "is_pinned": False,  # 新增：是否置顶
            "timestamp": datetime.now().isoformat(),
            "read": {member: False for member in members},
            **reply_info  # 合并回复信息
        }
        
        messages.append(new_message)
        save_messages(messages)
        
        return [TextContent(
            type="text",
            text=f"✅ 群组消息已发送\n群组: {group.get('name', group_id)}\n发送者: {sender}\n成员数: {len(members)}\n消息ID: {message_id}"
        )]
    
    elif name == "receive_group_messages":
        group_id = arguments.get("group_id", "")
        limit = arguments.get("limit", 20)
        unread_only = arguments.get("unread_only", False)
        since = arguments.get("since")
        keywords = arguments.get("keywords", [])
        topic = arguments.get("topic")
        mentions_me = arguments.get("mentions_me", False)  # 新增
        importance = arguments.get("importance")  # 新增
        show_pinned = arguments.get("show_pinned", False)  # 新增
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
        for msg in reversed(messages):  # 最新的在前
            # 只处理群组消息
            if msg.get("type") != "group" or msg.get("group_id") != group_id:
                continue
            
            # 未读过滤
            if unread_only and msg.get("read", {}).get(current_agent, True):
                continue
            
            # 时间过滤
            if since_time:
                try:
                    msg_time = datetime.fromisoformat(msg.get("timestamp", "").replace('Z', '+00:00'))
                    if msg_time < since_time:
                        continue
                except Exception:
                    pass
            
            # 关键词过滤
            if keywords:
                content = msg.get("content", "").lower()
                if not any(kw.lower() in content for kw in keywords):
                    continue
            
            # 话题过滤
            if topic and msg.get("topic") != topic:
                continue
            
            # @提醒过滤（新增）
            if mentions_me and current_agent not in msg.get("mentions", []):
                continue
            
            # 重要性过滤（新增）
            if importance and msg.get("importance") != importance:
                continue
            
            filtered_messages.append(msg)
            
            if len(filtered_messages) >= limit:
                break
        
        # 置顶消息优先显示（新增）
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
            
            # 消息ID和置顶状态
            msg_header = f"\n--- 消息 {msg['id']}"
            if msg.get("is_pinned"):
                msg_header += " 📌 [置顶]"
            msg_header += " ---"
            result_lines.append(msg_header)
            
            result_lines.append(f"发送者: {msg['sender']} ({msg.get('sender_role', '未知角色')})")
            
            # 重要性标记（新增）
            if msg.get("importance") == "high":
                result_lines.append("⚠️ 重要性: 高")
            elif msg.get("importance") == "low":
                result_lines.append("ℹ️ 重要性: 低")
            
            # @提醒（新增）
            if msg.get("mentions"):
                result_lines.append(f"@提醒: {', '.join(msg['mentions'])}")
            
            # 回复信息（新增）
            if msg.get("reply_to"):
                result_lines.append(f"↩️ 回复 {msg['reply_to_sender']}: {msg.get('reply_to_content', '')[:50]}...")
            
            if msg.get("topic"):
                result_lines.append(f"话题: {msg['topic']}")
            result_lines.append(f"时间: {msg['timestamp']}")
            result_lines.append(f"状态: {read_status}")
            if msg.get("file_path"):
                result_lines.append(f"文件: {msg['file_path']}")
            
            # 限制内容长度
            content = msg.get('content', '')
            if len(content) > max_content_length:
                content = content[:max_content_length] + "..."
            result_lines.append(f"\n内容:\n{content}")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    
    elif name == "list_groups":
        member_filter = arguments.get("member")
        status_filter = arguments.get("status", "active")  # 新增：状态过滤
        include_preview = arguments.get("include_preview", False)  # 新增：消息预览
        
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
            # 成员过滤
            if member_filter:
                if member_filter not in group_info.get("members", []):
                    continue
            
            # 状态过滤（新增）
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
            
            # 状态显示
            group_status = group_info.get("status", "active")
            if group_status == "active":
                result_lines.append("状态: 🟢 活跃")
            elif group_status == "archived":
                result_lines.append("状态: 📦 已归档")
                if group_info.get("archive_reason"):
                    result_lines.append(f"归档原因: {group_info.get('archive_reason')}")
            else:
                result_lines.append(f"状态: {'🟢 活跃' if group_info.get('active', True) else '⚪ 停用'}")
            
            # 消息预览（新增）
            if include_preview:
                # 获取群组最新消息
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
    
    elif name == "join_group":
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
        group["members"] = list(set(members))  # 去重
        groups[group_id] = group
        save_groups(groups)
        
        return [TextContent(
            type="text",
            text=f"✅ 已加入群组\n群组: {group.get('name', group_id)}\n成员数: {len(members)}"
        )]
    
    elif name == "leave_group":
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
    
    elif name == "summarize_group_messages":
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
            # 尝试解析ISO格式
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
        
        # 生成摘要
        # 提取关键信息：决策、任务、问题、完成情况
        key_points = []
        decisions = []
        tasks = []
        problems = []
        completions = []
        
        for msg in group_messages:
            content = msg.get("content", "").lower()
            sender = msg.get("sender", "")
            role = msg.get("sender_role", "")
            
            # 识别关键信息
            if any(kw in content for kw in ["决定", "决策", "确定", "采用"]):
                decisions.append(f"- {sender} ({role}): {msg.get('content', '')[:100]}...")
            elif any(kw in content for kw in ["任务", "分配", "负责"]):
                tasks.append(f"- {sender} ({role}): {msg.get('content', '')[:100]}...")
            elif any(kw in content for kw in ["问题", "bug", "错误", "阻塞"]):
                problems.append(f"- {sender} ({role}): {msg.get('content', '')[:100]}...")
            elif any(kw in content for kw in ["完成", "已实现", "已完成"]):
                completions.append(f"- {sender} ({role}): {msg.get('content', '')[:100]}...")
        
        summary_lines = [f"📋 群组消息摘要\n群组: {group.get('name', group_id)}\n时间范围: {time_range}\n消息总数: {len(group_messages)}\n"]
        
        if decisions:
            summary_lines.append(f"\n🎯 关键决策 ({len(decisions)}):")
            summary_lines.extend(decisions[:5])  # 最多5条
        
        if tasks:
            summary_lines.append(f"\n📋 任务相关 ({len(tasks)}):")
            summary_lines.extend(tasks[:5])
        
        if problems:
            summary_lines.append(f"\n⚠️ 问题反馈 ({len(problems)}):")
            summary_lines.extend(problems[:5])
        
        if completions:
            summary_lines.append(f"\n✅ 完成情况 ({len(completions)}):")
            summary_lines.extend(completions[:5])
        
        summary_text = "\n".join(summary_lines)
        
        # 限制长度
        if len(summary_text) > max_length:
            summary_text = summary_text[:max_length] + "..."
        
        return [TextContent(
            type="text",
            text=summary_text
        )]
    
    elif name == "get_unread_counts":
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
                
                # 检查是否未读
                is_unread = not msg.get("read", {}).get(current_agent, True)
                if is_unread:
                    unread_count += 1
                    
                    # 检查是否@我
                    if current_agent in msg.get("mentions", []):
                        mentions_count += 1
                    
                    # 检查是否重要
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
    
    elif name == "archive_group":
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
    
    elif name == "pin_message":
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
    
    elif name == "unpin_message":
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
        
        if not message:
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
    
    elif name == "standby":
        # 固定5分钟定时器
        STANDBY_TIMEOUT_SECONDS = 300  # 5分钟 = 300秒
        check_tasks = arguments.get("check_tasks", True)
        check_messages = arguments.get("check_messages", True)
        auto_read = arguments.get("auto_read", True)
        status_message = arguments.get("status_message", "")
        
        current_agent = get_current_agent()
        session_id = get_current_session_id()
        now = datetime.now()
        
        # 加载待命状态
        standby_states = load_standby()
        
        # 查找当前代理的活跃待命状态
        active_standby_id = None
        active_standby = None
        for sid, state in standby_states.items():
            if (state.get("agent") == current_agent and 
                state.get("session_id") == session_id and 
                state.get("active", False)):
                started_at_str = state.get("started_at", "")
                if started_at_str:
                    try:
                        started_at = datetime.fromisoformat(started_at_str)
                        elapsed = (now - started_at).total_seconds()
                        if elapsed < STANDBY_TIMEOUT_SECONDS:
                            active_standby_id = sid
                            active_standby = state
                            break
                    except Exception:
                        pass
        
        # 如果没有活跃的待命状态，创建新的
        if not active_standby:
            standby_id = f"{current_agent}_{session_id}_{now.isoformat()}"
            active_standby = {
                "agent": current_agent,
                "session_id": session_id,
                "check_tasks": check_tasks,
                "check_messages": check_messages,
                "auto_read": auto_read,
                "status_message": status_message,
                "started_at": now.isoformat(),
                "last_check": now.isoformat(),
                "active": True,
                "timeout_seconds": STANDBY_TIMEOUT_SECONDS
            }
            standby_states[standby_id] = active_standby
            active_standby_id = standby_id
        else:
            # 更新现有待命状态
            active_standby["last_check"] = now.isoformat()
            if status_message:
                active_standby["status_message"] = status_message
            standby_states[active_standby_id] = active_standby
        
        # 计算剩余时间
        started_at = datetime.fromisoformat(active_standby["started_at"])
        elapsed_seconds = (now - started_at).total_seconds()
        remaining_seconds = max(0, STANDBY_TIMEOUT_SECONDS - elapsed_seconds)
        remaining_minutes = int(remaining_seconds // 60)
        remaining_secs = int(remaining_seconds % 60)
        
        # 检查任务和消息
        found_tasks = []
        found_messages = []
        
        if check_tasks:
            tasks = load_tasks()
            agent_tasks = [t for t in tasks if t.get("assignee") == current_agent and t.get("status") in ["待开始", "进行中"]]
            if agent_tasks:
                found_tasks = agent_tasks
        
        if check_messages:
            messages = load_messages()
            unread_messages = []
            
            for msg in reversed(messages):
                # 检查是否是发给当前AI的消息
                recipients = msg.get("recipients", [])
                if current_agent in recipients or "*" in recipients:
                    read_status = msg.get("read", {}).get(current_agent, False)
                    if not read_status:
                        unread_messages.append(msg)
            
            found_messages = unread_messages
        
        # 保存待命状态
        active_standby["found_tasks"] = len(found_tasks)
        active_standby["found_messages"] = len(found_messages)
        save_standby(standby_states)
        
        # 如果有新任务/消息，立即返回
        has_new_items = len(found_tasks) > 0 or len(found_messages) > 0
        
        if has_new_items:
            result_lines = ["🔔 待命检查：收到新任务/消息，继续工作\n"]
            
            if found_tasks:
                result_lines.append(f"\n📋 新任务 ({len(found_tasks)}个):")
                for task in found_tasks[:5]:  # 最多显示5个
                    result_lines.append(f"\n--- 任务 {task.get('id', '未知')} ---")
                    result_lines.append(f"标题: {task.get('title', '未知')}")
                    result_lines.append(f"优先级: {task.get('priority', '未知')}")
                    result_lines.append(f"状态: {task.get('status', '未知')}")
                    if auto_read:
                        desc = task.get('description', '无')
                        # 移除截断限制，显示完整描述
                        result_lines.append(f"描述: {desc}")
            
            if found_messages:
                result_lines.append(f"\n📬 未读消息 ({len(found_messages)}条):")
                for msg in found_messages[:3]:  # 最多显示3条
                    result_lines.append(f"\n--- 消息 {msg.get('id', '未知')} ---")
                    result_lines.append(f"发送者: {msg.get('sender', '未知')} ({msg.get('sender_role', '未知角色')})")
                    result_lines.append(f"时间: {msg.get('timestamp', '未知')}")
                    if auto_read:
                        content = msg.get('content', '')
                        # 移除截断限制，显示完整内容
                        result_lines.append(f"内容: {content}")
            
            result_lines.append(f"\n\n✅ 待命状态已激活（5分钟定时器）")
            result_lines.append(f"待命ID: {active_standby_id}")
            result_lines.append(f"剩余时间: {remaining_minutes}分{remaining_secs}秒")
            if status_message:
                result_lines.append(f"状态: {status_message}")
            result_lines.append("\n⚠️ 重要：处理完任务/消息后，必须继续调用standby保持监听！")
            result_lines.append("💡 请处理上述任务/消息，处理完成后立即调用standby继续监听")
            result_lines.append("📋 操作：处理完成后，在回复末尾调用standby({{'status_message': '任务处理完成，继续监听'}})")
            
            return [TextContent(
                type="text",
                text="\n".join(result_lines)
            )]
        else:
            # 没有新任务/消息，继续等待
            if remaining_seconds > 0:
                result_lines = [
                    f"✅ 待命状态：持续监听中（5分钟定时器）",
                    f"\n待命ID: {active_standby_id}",
                    f"剩余时间: {remaining_minutes}分{remaining_secs}秒",
                    f"检查时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
                ]
                if status_message:
                    result_lines.append(f"状态: {status_message}")
                result_lines.append(f"\n⚠️ 重要：请立即继续调用standby保持监听！")
                result_lines.append(f"💡 提示: 暂无新任务/消息，但必须继续调用standby才能保持监听状态")
                result_lines.append(f"📋 操作：请在回复末尾继续调用standby，直到收到新任务/消息或5分钟到期")
                result_lines.append(f"\n示例：standby({{'status_message': '继续监听中'}})")
                
                return [TextContent(
                    type="text",
                    text="\n".join(result_lines)
                )]
            else:
                # 5分钟到了，重置定时器
                result_lines = [
                    f"⏰ 5分钟定时器已到期，重置定时器",
                    f"\n待命ID: {active_standby_id}",
                    f"检查时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
                ]
                if status_message:
                    result_lines.append(f"状态: {status_message}")
                result_lines.append(f"\n⚠️ 重要：请立即继续调用standby开始新的5分钟监听周期！")
                result_lines.append(f"💡 提示: 5分钟内未收到新任务/消息，定时器已重置")
                result_lines.append(f"📋 操作：请在回复末尾调用standby开始新的监听周期")
                result_lines.append(f"\n示例：standby({{'status_message': '开始新的5分钟监听周期'}})")
                
                # 重置定时器（创建新的待命状态）
                active_standby["active"] = False
                save_standby(standby_states)
                
                return [TextContent(
                    type="text",
                    text="\n".join(result_lines)
                )]
    
    else:
        return [TextContent(
            type="text",
            text=f"错误: 未知工具: {name}"
        )]


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())


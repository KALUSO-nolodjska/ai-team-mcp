"""
MCP AI Chat Group - 系统处理器
System Handler

处理系统相关工具：
- register_agent: 注册AI代理
- set_employee_config: 设置员工配置
- get_current_session: 获取当前会话
- list_agents: 列出所有代理
- standby: 待命监听
"""
from datetime import datetime, timedelta
from pathlib import Path
from mcp.types import TextContent
from typing import Any

# 导入核心功能
from ..core.storage import (
    load_agents, save_agents,
    load_sessions, save_sessions, 
    load_employee_config, save_employee_config,
    load_tasks, load_messages,
    load_standby, save_standby
)
from ..core.session import (
    get_current_agent, get_current_session_id,
    create_session, set_current_agent, set_current_session
)
from ..config import WORKSPACE_ROOT, RULES_DIR


def load_mdc_file(agent_name: str) -> str:
    """加载.mdc文件内容"""
    config = load_employee_config()
    if agent_name not in config:
        return ""
    
    mdc_file_path = config[agent_name].get("mdc_file_path", "")
    if not mdc_file_path:
        return ""
    
    mdc_path = WORKSPACE_ROOT / mdc_file_path
    if not mdc_path.exists():
        return ""
    
    try:
        with open(mdc_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def extract_role_from_mdc(mdc_content: str) -> str:
    """从.mdc文件内容提取角色"""
    import re
    match = re.search(r'role\s*[：:]\s*(.+)', mdc_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


def extract_description_from_mdc(mdc_content: str) -> str:
    """从.mdc文件内容提取描述"""
    import re
    match = re.search(r'description\s*[：:]\s*(.+)', mdc_content, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


async def handle_register_agent(arguments: dict[str, Any]) -> list[TextContent]:
    """处理register_agent工具"""
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
        for task in agent_tasks[:3]:  # 最多显示3个
            result_lines.append(f"  - {task.get('title', '未知')} (优先级: {task.get('priority', '未知')})")
        if len(agent_tasks) > 3:
            result_lines.append(f"  ... 还有 {len(agent_tasks) - 3} 个任务")
    
    return [TextContent(
        type="text",
        text="\n".join(result_lines)
    )]


async def handle_set_employee_config(arguments: dict[str, Any]) -> list[TextContent]:
    """处理set_employee_config工具"""
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


async def handle_get_current_session(arguments: dict[str, Any]) -> list[TextContent]:
    """处理get_current_session工具"""
    current_agent = get_current_agent()
    session_id = get_current_session_id()
    
    if not session_id:
        return [TextContent(
            type="text",
            text="⚠️ 当前没有活跃的会话\n请先使用 register_agent 注册"
        )]
    
    sessions = load_sessions()
    session = sessions.get(session_id)
    
    if not session:
        return [TextContent(
            type="text",
            text=f"⚠️ 会话信息丢失\n会话ID: {session_id}\n请重新使用 register_agent 注册"
        )]
    
    result_lines = [
        f"✅ 当前会话信息",
        f"代理名称: {current_agent}",
        f"会话ID: {session_id}",
        f"角色: {session.get('role', '未知')}",
        f"描述: {session.get('description', '无')}",
        f"创建时间: {session.get('created_at', '未知')}"
    ]
    
    return [TextContent(
        type="text",
        text="\n".join(result_lines)
    )]


async def handle_list_agents(arguments: dict[str, Any]) -> list[TextContent]:
    """处理list_agents工具"""
    agents = load_agents()
    
    if not agents:
        return [TextContent(
            type="text",
            text="📋 当前没有已注册的AI代理"
        )]
    
    result_lines = [f"📋 已注册的AI代理 ({len(agents)}个):\n"]
    
    for agent_name, info in agents.items():
        result_lines.append(f"--- {agent_name} ---")
        result_lines.append(f"角色: {info.get('role', '未知')}")
        result_lines.append(f"描述: {info.get('description', '无')}")
        result_lines.append(f"会话ID: {info.get('session_id', '未知')}")
        result_lines.append(f"注册时间: {info.get('registered_at', '未知')}")
        result_lines.append("")
    
    return [TextContent(
        type="text",
        text="\n".join(result_lines)
    )]


async def handle_standby(arguments: dict[str, Any]) -> list[TextContent]:
    """处理standby工具"""
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
                    result_lines.append(f"描述: {desc}")
        
        if found_messages:
            result_lines.append(f"\n📬 未读消息 ({len(found_messages)}条):")
            for msg in found_messages[:3]:  # 最多显示3条
                result_lines.append(f"\n--- 消息 {msg.get('id', '未知')} ---")
                result_lines.append(f"发送者: {msg.get('sender', '未知')} ({msg.get('sender_role', '未知角色')})")
                result_lines.append(f"时间: {msg.get('timestamp', '未知')}")
                if auto_read:
                    content = msg.get('content', '')
                    result_lines.append(f"内容: {content}")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]
    else:
        # 没有新任务/消息
        result_lines = ["💤 待命状态：暂无新任务/消息"]
        
        if status_message:
            result_lines.append(f"状态: {status_message}")
        
        result_lines.append(f"\n⏱️ 待命时间: 已 {int(elapsed_seconds // 60)}分{int(elapsed_seconds % 60)}秒 / 剩余 {remaining_minutes}分{remaining_secs}秒")
        result_lines.append(f"检查任务: {'是' if check_tasks else '否'}")
        result_lines.append(f"检查消息: {'是' if check_messages else '否'}")
        result_lines.append(f"\n💡 提示: 继续待命中，有新任务/消息会立即通知")
        
        return [TextContent(
            type="text",
            text="\n".join(result_lines)
        )]


# 导出所有处理器
__all__ = [
    'handle_register_agent',
    'handle_set_employee_config',
    'handle_get_current_session',
    'handle_list_agents',
    'handle_standby'
]


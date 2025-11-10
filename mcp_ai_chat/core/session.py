"""
MCP AI Chat Group - 会话管理模块
"""
from datetime import datetime
from typing import Optional

# 全局会话状态
_current_session_id: Optional[str] = None
_current_agent: Optional[str] = None


def get_current_session_id() -> Optional[str]:
    """获取当前会话ID"""
    return _current_session_id


def set_current_session_id(session_id: str) -> None:
    """设置当前会话ID"""
    global _current_session_id
    _current_session_id = session_id


def get_current_agent() -> str:
    """获取当前agent名称"""
    if _current_agent:
        return _current_agent
    
    from .storage import load_sessions
    session_id = get_current_session_id()
    if session_id:
        sessions = load_sessions()
        return sessions.get(session_id, {}).get("agent_name", "unknown")
    return "unknown"


def set_current_agent(agent_name: str) -> None:
    """设置当前agent名称"""
    global _current_agent
    _current_agent = agent_name


def get_current_agent_role() -> str:
    """获取当前agent角色"""
    from .storage import load_sessions
    session_id = get_current_session_id()
    if session_id:
        sessions = load_sessions()
        return sessions.get(session_id, {}).get("role", "未知")
    return "未知"


def create_session(agent_name: str, role: str, description: str) -> str:
    """创建新会话"""
    from .storage import load_sessions, save_sessions
    
    sessions = load_sessions()
    session_id = f"{agent_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    session_info = {
        "agent_name": agent_name,
        "role": role,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "active": True
    }
    
    sessions[session_id] = session_info
    save_sessions(sessions)
    
    # 设置为当前会话
    set_current_session_id(session_id)
    set_current_agent(agent_name)
    
    return session_id


def set_current_session(session_id: str) -> None:
    """设置当前会话（别名）"""
    set_current_session_id(session_id)


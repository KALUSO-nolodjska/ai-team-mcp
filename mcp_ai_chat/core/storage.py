"""
MCP AI Chat Group - 数据存储模块
"""
import json
from pathlib import Path
from typing import Any, Optional
from .. import config


def load_json(file_path: Path, default: Optional[Any] = None) -> Any:
    """加载JSON文件"""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default if default is not None else {}
    return default if default is not None else {}


def save_json(file_path: Path, data: Any) -> None:
    """保存JSON文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 消息相关
def load_messages() -> list:
    """加载消息历史"""
    return load_json(config.MESSAGES_FILE, [])


def save_messages(messages: list) -> None:
    """保存消息历史"""
    save_json(config.MESSAGES_FILE, messages)


# 代理相关
def load_agents() -> dict:
    """加载代理列表"""
    return load_json(config.AGENTS_FILE, {})


def save_agents(agents: dict) -> None:
    """保存代理列表"""
    save_json(config.AGENTS_FILE, agents)


# 会话相关
def load_sessions() -> dict:
    """加载会话信息"""
    return load_json(config.SESSIONS_FILE, {})


def save_sessions(sessions: dict) -> None:
    """保存会话信息"""
    save_json(config.SESSIONS_FILE, sessions)


# 任务相关
def load_tasks() -> list:
    """加载任务列表"""
    return load_json(config.TASKS_FILE, [])


def save_tasks(tasks: list) -> None:
    """保存任务列表"""
    save_json(config.TASKS_FILE, tasks)


# 群组相关
def load_groups() -> dict:
    """加载群组信息"""
    return load_json(config.GROUPS_FILE, {})


def save_groups(groups: dict) -> None:
    """保存群组信息"""
    save_json(config.GROUPS_FILE, groups)


# 待命相关
def load_standby() -> dict:
    """加载待命状态"""
    return load_json(config.STANDBY_FILE, {})


def save_standby(standby_states: dict) -> None:
    """保存待命状态"""
    save_json(config.STANDBY_FILE, standby_states)


# 员工配置
def load_employee_config() -> dict:
    """加载员工配置"""
    return load_json(config.EMPLOYEE_CONFIG_FILE, {})


def save_employee_config(config_data: dict) -> None:
    """保存员工配置"""
    save_json(config.EMPLOYEE_CONFIG_FILE, config_data)


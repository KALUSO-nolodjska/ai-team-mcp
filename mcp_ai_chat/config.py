"""
MCP AI Chat Group - 配置管理
"""
from pathlib import Path

# 数据存储目录
MESSAGES_DIR = Path.home() / ".mcp_ai_chat"
MESSAGES_FILE = MESSAGES_DIR / "messages.json"
AGENTS_FILE = MESSAGES_DIR / "agents.json"
SESSIONS_FILE = MESSAGES_DIR / "sessions.json"
TASKS_FILE = MESSAGES_DIR / "tasks.json"
GROUPS_FILE = MESSAGES_DIR / "groups.json"
STANDBY_FILE = MESSAGES_DIR / "standby.json"
EMPLOYEE_CONFIG_FILE = MESSAGES_DIR / "employee_config.json"

# 工作区路径
WORKSPACE_ROOT = Path(__file__).parent.parent
RULES_DIR = WORKSPACE_ROOT / ".cursor" / "rules"

# 常量
STANDBY_TIMEOUT_SECONDS = 300  # 5分钟
DEFAULT_MESSAGE_LIMIT = 20
DEFAULT_MAX_CONTENT_LENGTH = 5000

# 确保目录存在
MESSAGES_DIR.mkdir(parents=True, exist_ok=True)




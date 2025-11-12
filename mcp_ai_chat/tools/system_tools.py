"""
MCP AI Chat Group - 系统工具定义
System Tools Definitions
"""

from mcp.types import Tool


def get_system_tools():
    """获取系统相关工具定义"""
    return [
        Tool(
            name="register_agent",
            description="注册当前AI代理并创建会话。如果agent_name已存在，会自动拾取之前的任务。如果设置了员工配置，会从.mdc文件自动加载角色和描述",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "AI代理名称（例如: a, b, c, d, manager）",
                    },
                    "role": {
                        "type": "string",
                        "description": "AI角色（例如: 前端开发工程师、后端开发工程师、全栈开发工程师、测试/运维工程师、产品经理）。如果设置了员工配置，会自动从.mdc文件读取",
                    },
                    "description": {
                        "type": "string",
                        "description": "AI代理描述。如果设置了员工配置，会自动从.mdc文件读取",
                    },
                    "auto_load_from_mdc": {
                        "type": "boolean",
                        "description": "是否自动从.mdc文件加载员工设定（默认：true）",
                        "default": True,
                    },
                },
                "required": ["agent_name"],
            },
        ),
        Tool(
            name="set_employee_config",
            description="设置员工配置，指定.mdc文件路径。设置后，register_agent会自动从.mdc文件读取角色和描述",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "AI代理名称（例如: a, b, c, d, manager）",
                    },
                    "mdc_file_path": {
                        "type": "string",
                        "description": ".mdc文件路径（相对于工作区根目录，例如: .cursor/rules/a.mdc）。如果为空，则使用默认路径 .cursor/rules/{agent_name}.mdc",
                    },
                },
                "required": ["agent_name"],
            },
        ),
        Tool(
            name="get_current_session",
            description="获取当前AI的会话信息",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_agents",
            description="列出所有已注册的AI代理",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="standby",
            description="进入待命状态，定时器强制为5分钟。在5分钟内持续监听任务和消息，如果收到新任务/消息立即返回继续工作，如果5分钟内没有新任务/消息则继续等待。建议在回复末尾调用此工具",
            inputSchema={
                "type": "object",
                "properties": {
                    "status_message": {
                        "type": "string",
                        "description": "待命状态消息，用于说明当前状态",
                    },
                    "check_tasks": {
                        "type": "boolean",
                        "description": "是否检查任务，默认：true",
                        "default": True,
                    },
                    "check_messages": {
                        "type": "boolean",
                        "description": "是否检查消息，默认：true",
                        "default": True,
                    },
                    "auto_read": {
                        "type": "boolean",
                        "description": "是否自动读取新任务/消息内容，默认：true",
                        "default": True,
                    },
                },
            },
        ),
    ]

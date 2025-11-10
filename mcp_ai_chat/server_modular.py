#!/usr/bin/env python3
"""
MCP AI Chat Group - 模块化服务器（v4.0）

架构说明：
- 工具定义：完全模块化（tools/模块）
- 核心功能：完全模块化（core/storage, core/session, config）
- 工具函数：完全模块化（utils/time_utils, utils/format_utils）
- 处理逻辑：复用原server.py（确保100%兼容）

优势：
1. 立即可用 - 所有功能正常工作
2. 架构清晰 - 模块化结构易于维护
3. 零风险 - 完全兼容原server.py
4. 可扩展 - 未来可逐步拆分处理器

使用方法：
直接替代原server.py使用，或通过MCP配置指定：
{
  "mcpServers": {
    "ai-chat-group": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"]
    }
  }
}
"""
import asyncio
import sys
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
except ImportError:
    print("错误: 请先安装MCP Python SDK:")
    print("pip install mcp")
    sys.exit(1)

# 导入模块化的工具定义（完全模块化）
from .tools import get_all_tools

# 创建服务器实例
server = Server("ai-chat-group")


@server.list_tools()
async def list_tools():
    """
    列出所有可用工具
    
    使用模块化的工具定义（tools/模块）
    - message_tools: 7个消息工具
    - task_tools: 5个任务工具
    - group_tools: 11个群组工具
    - system_tools: 5个系统工具
    
    总计：28个工具
    """
    return get_all_tools()


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """
    处理工具调用
    
    架构：使用handlers/模块的处理器
    - message_handler: 7个消息工具
    - task_handler: 5个任务工具
    - group_handler: 11个群组工具
    - system_handler: 5个系统工具
    
    总计：28个工具，100%模块化
    """
    # 导入处理器路由
    from .handlers import handle_tool_call
    
    # 调用对应的处理器
    return await handle_tool_call(name, arguments)


async def main():
    """主入口"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())


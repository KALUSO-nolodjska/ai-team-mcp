# AI聊天群 MCP工具 - 安装指南

## 📦 依赖安装

### 1. 安装MCP Python SDK

```bash
pip install mcp
```

### 2. 验证安装

```bash
python -c "import mcp; print('MCP SDK已安装')"
```

---

## ⚙️ 配置MCP服务器

### 方式1: Cursor配置（推荐）

编辑 `C:\Users\DELL\.cursor\mcp.json`，添加：

```json
{
  "mcpServers": {
    "ai-chat-group": {
      "command": "python",
      "args": [
        "D:/developItems/mcp_ai_chat/server.py"
      ],
      "env": {
        "MCP_AI_CHAT_AGENT_NAME": "manager"
      }
    }
  }
}
```

**注意**: 
- 将 `D:/developItems` 替换为你的实际项目路径
- 将 `MCP_AI_CHAT_AGENT_NAME` 设置为当前AI的名称

### 方式2: Claude Desktop配置

编辑 `C:\Users\DELL\AppData\Roaming\Claude\claude_desktop_config.json`，添加：

```json
{
  "mcpServers": {
    "ai-chat-group": {
      "command": "python",
      "args": [
        "D:/developItems/mcp_ai_chat/server.py"
      ],
      "env": {
        "MCP_AI_CHAT_AGENT_NAME": "manager"
      }
    }
  }
}
```

---

## 🔧 为不同AI配置

### 员工A（前端）
```json
{
  "env": {
    "MCP_AI_CHAT_AGENT_NAME": "a"
  }
}
```

### 员工B（后端）
```json
{
  "env": {
    "MCP_AI_CHAT_AGENT_NAME": "b"
  }
}
```

### 员工C（全栈）
```json
{
  "env": {
    "MCP_AI_CHAT_AGENT_NAME": "c"
  }
}
```

### 员工D（测试/运维）
```json
{
  "env": {
    "MCP_AI_CHAT_AGENT_NAME": "d"
  }
}
```

### 产品经理
```json
{
  "env": {
    "MCP_AI_CHAT_AGENT_NAME": "manager"
  }
}
```

---

## ✅ 验证配置

1. **重启Cursor/Claude Desktop**
2. **测试工具**: 在AI对话中尝试调用 `list_agents` 工具
3. **注册代理**: 使用 `register_agent` 注册当前AI

---

## 🐛 故障排除

### 问题1: 找不到mcp模块

**解决方案**:
```bash
pip install mcp
```

### 问题2: 路径错误

**解决方案**: 确保 `server.py` 的路径正确，使用绝对路径

### 问题3: 权限错误

**解决方案**: 确保Python有权限执行脚本和创建文件

---

**文档版本**: v1.0.0  
**最后更新**: 2025-11-10



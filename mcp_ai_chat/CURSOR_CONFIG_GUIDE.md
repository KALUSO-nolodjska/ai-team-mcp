# Cursor MCP配置指南

> **配置文件位置**: `C:\Users\DELL\.cursor\mcp.json`

---

## 📋 配置步骤

### 1. 打开配置文件

编辑 `C:\Users\DELL\.cursor\mcp.json`，添加以下配置：

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

### 2. 如果文件不存在

如果 `C:\Users\DELL\.cursor\mcp.json` 不存在，创建它并添加完整配置：

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

### 3. 如果文件已存在

如果文件已存在其他MCP服务器配置，只需在 `mcpServers` 对象中添加 `ai-chat-group` 配置即可。

---

## 🔧 为不同AI配置

### 产品经理（默认）
```json
{
  "env": {
    "MCP_AI_CHAT_AGENT_NAME": "manager"
  }
}
```

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

---

## ✅ 验证配置

1. **重启Cursor**
2. **检查MCP工具**: 在AI对话中应该能看到 `ai-chat-group` 相关的工具
3. **测试工具**: 尝试调用 `list_agents` 工具

---

## 🐛 故障排除

### 问题1: 工具未显示

**解决方案**:
- 确保已重启Cursor
- 检查配置文件路径是否正确
- 检查Python路径是否正确

### 问题2: 工具调用失败

**解决方案**:
- 检查 `server.py` 文件是否存在
- 检查Python是否有权限执行脚本
- 查看Cursor的错误日志

---

**文档版本**: v1.0.0  
**最后更新**: 2025-11-10



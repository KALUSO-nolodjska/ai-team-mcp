# MCP服务器重启指南

> **创建时间**: 2025-11-10  
> **用途**: 重启AI聊天群MCP服务器

---

## 🔄 重启方法

### 方法1：重启Cursor（推荐）

**最简单的方法**：

1. **完全关闭Cursor**
   - 点击Cursor窗口右上角的关闭按钮
   - 或在任务管理器中结束Cursor进程

2. **重新打开Cursor**
   - 双击Cursor图标启动
   - MCP服务器会自动重新加载

3. **验证MCP服务器**
   - 打开Cursor后，等待几秒钟
   - 尝试使用MCP工具（如`mcp_ai-chat-group_list_agents`）
   - 如果工具可用，说明重启成功

### 方法2：重新加载MCP配置

**如果不想完全重启Cursor**：

1. **打开MCP配置**
   - 配置文件位置：`%USERPROFILE%\.cursor\mcp.json`
   - 或：`%APPDATA%\Cursor\User\globalStorage\mcp.json`

2. **修改配置触发重载**
   - 在`ai-chat-group`配置中添加一个空格或注释
   - 保存文件
   - Cursor会自动检测配置变化并重新加载

3. **恢复配置**
   - 移除刚才添加的空格或注释
   - 保存文件

### 方法3：使用命令重启（如果支持）

**检查MCP服务器进程**：

```powershell
# 查找Python进程运行MCP服务器
Get-Process python | Where-Object {$_.CommandLine -like "*mcp_ai_chat*"}
```

**手动重启**（如果找到进程）：

```powershell
# 结束进程（谨慎使用）
Stop-Process -Name python -Force
```

---

## 📋 当前MCP服务器配置

**服务器名称**: `ai-chat-group`

**配置内容**:
```json
{
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
```

**配置文件位置**:
- `postgres_mcp_config.json` (项目根目录)
- `%USERPROFILE%\.cursor\mcp.json` (Cursor配置)

---

## ✅ 重启后验证

重启后，请验证以下功能：

1. **测试基础工具**:
   ```
   mcp_ai-chat-group_list_agents
   ```

2. **测试新功能**:
   ```
   mcp_ai-chat-group_set_employee_config
   mcp_ai-chat-group_standby
   ```

3. **检查standby工具返回格式**:
   - 应该显示"⚠️ 重要：请立即继续调用standby保持监听！"
   - 应该显示示例代码

---

## 🔍 故障排查

### 问题1：MCP工具不可用

**可能原因**：
- Cursor未完全重启
- MCP配置文件路径错误
- Python环境问题

**解决方法**：
1. 完全关闭Cursor（任务管理器确认）
2. 重新打开Cursor
3. 等待10-15秒让MCP服务器启动
4. 再次尝试使用工具

### 问题2：standby工具返回格式未更新

**可能原因**：
- MCP服务器未重新加载新代码
- 缓存问题

**解决方法**：
1. 完全重启Cursor
2. 清除MCP缓存（如果存在）
3. 重新测试standby工具

### 问题3：Python语法错误

**检查方法**：
```powershell
cd D:\developItems
python -m py_compile mcp_ai_chat/server.py
```

**如果发现错误**：
- 修复代码中的语法错误
- 重新编译检查
- 重启Cursor

---

## 📚 相关文档

- **MCP服务器代码**: `mcp_ai_chat/server.py`
- **MCP配置示例**: `mcp_ai_chat/mcp_config_example.json`
- **安装指南**: `mcp_ai_chat/install.md`

---

**文档版本**: v1.0.0  
**最后更新**: 2025-11-10  
**维护者**: 产品经理




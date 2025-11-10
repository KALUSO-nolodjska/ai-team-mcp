# 安装指南

[English](INSTALLATION.md) | 简体中文

本指南将帮助你在不同平台和IDE中安装和配置AI Team MCP。

---

## 📋 前置要求

在开始之前，请确保你已经安装：

- **Python 3.8或更高版本**
  - 检查版本：`python --version` 或 `python3 --version`
  - 下载地址：https://www.python.org/downloads/

- **支持MCP的IDE**（以下任选其一）：
  - [Cursor](https://cursor.sh/) - AI编程助手
  - [Windsurf](https://codeium.com/windsurf) - 下一代IDE
  - [Claude Desktop](https://claude.ai/download) - Anthropic官方客户端

---

## 📦 安装方法

### 方式1: 使用npm安装（推荐）

这是最简单的安装方式，适用于所有平台：

```bash
npx @modelcontextprotocol/create-server ai-team-mcp
```

### 方式2: 从源码安装

如果你想要最新的开发版本或需要修改代码：

```bash
# 克隆仓库
git clone https://github.com/KALUSO-nolodjska/ai-team-mcp.git

# 进入目录
cd ai-team-mcp

# 安装（开发模式）
pip install -e .
```

---

## ⚙️ 配置MCP客户端

安装完成后，需要在你的IDE中配置MCP服务器。

### 🎯 Cursor IDE

1. **打开配置文件**
   - Windows: `%USERPROFILE%\.cursor\mcp.json`
   - macOS/Linux: `~/.cursor/mcp.json`
   
   如果文件不存在，请手动创建。

2. **添加MCP服务器配置**

   ```json
   {
     "mcpServers": {
       "ai-team-mcp": {
         "command": "python",
         "args": ["-m", "mcp_ai_chat.server_modular"],
         "env": {}
       }
     }
   }
   ```

   **注意**：
   - Windows用户可能需要使用完整路径：`"command": "C:\\Python39\\python.exe"`
   - macOS/Linux用户可以使用：`"command": "python3"`

3. **重启Cursor**
   - 完全退出Cursor（包括系统托盘）
   - 重新启动Cursor

4. **验证安装**
   - 在Cursor中，MCP服务器应该会自动加载
   - 你可以在AI聊天中使用MCP工具

### 🌊 Windsurf IDE

配置方式与Cursor相同，只是配置文件路径不同：

1. **打开配置文件**
   - Windows: `%USERPROFILE%\.windsurf\mcp.json`
   - macOS/Linux: `~/.windsurf/mcp.json`

2. **添加相同的配置**（见上方Cursor配置）

3. **重启Windsurf**

### 🤖 Claude Desktop

1. **打开配置文件**
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **添加MCP服务器配置**

   ```json
   {
     "mcpServers": {
       "ai-team-mcp": {
         "command": "python",
         "args": ["-m", "mcp_ai_chat.server_modular"]
       }
     }
   }
   ```

3. **重启Claude Desktop**

---

## 🧪 验证安装

安装并配置完成后，让我们验证一切正常：

### 测试步骤

1. **注册AI代理**
   
   在你的IDE中运行以下命令：
   ```
   使用 register_agent 工具注册一个名为 "test" 的代理
   ```

2. **检查会话**
   
   ```
   使用 get_current_session 工具查看当前会话信息
   ```

3. **创建测试任务**
   
   ```
   使用 create_task 工具创建一个测试任务
   ```

如果以上步骤都成功执行，恭喜你！安装完成了！🎉

---

## 🐛 故障排除

### 问题1: "找不到python命令"

**Windows**
```json
{
  "command": "C:\\Python39\\python.exe"  // 使用完整路径
}
```

**macOS/Linux**
```json
{
  "command": "python3"  // 或 /usr/bin/python3
}
```

### 问题2: "找不到mcp_ai_chat模块"

这通常意味着Python无法找到安装的包。

**解决方案1**: 使用绝对路径
```json
{
  "command": "python",
  "args": [
    "D:\\developItems\\ai-team-mcp\\mcp_ai_chat\\server_modular.py"
  ]
}
```

**解决方案2**: 确保pip安装正确
```bash
# 重新安装
pip uninstall mcp-ai-chat
pip install -e /path/to/ai-team-mcp
```

### 问题3: MCP服务器未加载

1. **检查日志**
   - Cursor: 查看开发者工具控制台（Help → Toggle Developer Tools）
   - Claude Desktop: 查看应用日志

2. **验证配置文件**
   - 确保JSON格式正确（没有多余的逗号）
   - 确保路径使用正确的斜杠（Windows使用 `\\`）

3. **测试Python命令**
   ```bash
   # 在终端中直接运行
   python -m mcp_ai_chat.server_modular
   ```

### 问题4: 权限错误

**Windows**: 以管理员身份运行IDE

**macOS/Linux**:
```bash
chmod +x /path/to/python
```

### 问题5: 端口冲突

如果遇到端口占用错误，可以在配置中指定不同的端口：

```json
{
  "mcpServers": {
    "ai-team-mcp": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "env": {
        "MCP_PORT": "8888"  // 自定义端口
      }
    }
  }
}
```

---

## 🔧 高级配置

### 自定义数据存储路径

默认情况下，数据存储在 `mcp_ai_chat/data/` 目录。你可以自定义：

```json
{
  "mcpServers": {
    "ai-team-mcp": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "env": {
        "MCP_DATA_PATH": "/custom/path/to/data"
      }
    }
  }
}
```

### 启用调试模式

```json
{
  "mcpServers": {
    "ai-team-mcp": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "env": {
        "MCP_DEBUG": "true"
      }
    }
  }
}
```

### 多个AI代理配置

如果你想在同一台机器上运行多个AI代理：

```json
{
  "mcpServers": {
    "ai-team-mcp-agent1": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "env": {
        "MCP_AGENT_NAME": "agent1",
        "MCP_DATA_PATH": "/path/to/agent1/data"
      }
    },
    "ai-team-mcp-agent2": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "env": {
        "MCP_AGENT_NAME": "agent2",
        "MCP_DATA_PATH": "/path/to/agent2/data"
      }
    }
  }
}
```

---

## 📚 下一步

安装完成后，你可以：

- 📖 阅读[使用示例](EXAMPLES_CN.md)了解如何使用
- 🔧 查看[API文档](API_REFERENCE_CN.md)了解所有工具
- 🏗️ 阅读[架构说明](ARCHITECTURE_CN.md)了解系统设计
- 🐛 查看[故障排除指南](TROUBLESHOOTING_CN.md)解决问题

---

## 💬 需要帮助？

如果你在安装过程中遇到问题：

- 📧 发送邮件至：lhq2328616309@outlook.com
- 🐛 提交Issue：https://github.com/KALUSO-nolodjska/ai-team-mcp/issues
- 💬 参与讨论：https://github.com/KALUSO-nolodjska/ai-team-mcp/discussions

我们很乐意帮助你！🙂


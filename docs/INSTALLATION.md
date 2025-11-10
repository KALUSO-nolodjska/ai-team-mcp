# 📦 Installation Guide

Complete guide to installing and configuring AI Team MCP.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Advanced Setup](#advanced-setup)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Python**: 3.8 or higher
- **Memory**: 100MB minimum
- **Disk Space**: 50MB

### Required Software

1. **Python 3.8+**
   ```bash
   # Check Python version
   python --version
   # or
   python3 --version
   ```

2. **MCP-Compatible Client** (one of):
   - [Cursor](https://cursor.sh/) - AI-powered code editor
   - [Windsurf](https://codeium.com/windsurf) - Codeium's AI IDE
   - [Claude Desktop](https://claude.ai/desktop) - Anthropic's desktop app

3. **pip** (Python package manager)
   ```bash
   # Check pip version
   pip --version
   ```

---

## Installation Steps

### Step 1: Install MCP Python SDK

```bash
pip install mcp
```

**Verify installation:**
```bash
python -c "import mcp; print('MCP SDK installed successfully')"
```

### Step 2: Clone the Repository

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-team-mcp.git

# Navigate to directory
cd ai-team-mcp
```

**Alternative:** Download as ZIP from GitHub and extract.

### Step 3: Verify File Structure

```bash
# Check that files are present
ls mcp_ai_chat/

# Expected output:
# server_modular.py
# tools/
# handlers/
# core/
# utils/
# ...
```

---

## Configuration

### For Cursor

1. **Locate MCP config file:**
   - **Windows**: `C:\Users\YourUsername\.cursor\mcp.json`
   - **macOS/Linux**: `~/.cursor/mcp.json`

2. **Edit the config file:**

   ```json
   {
     "mcpServers": {
       "ai-team": {
         "command": "python",
         "args": ["-m", "mcp_ai_chat.server_modular"],
         "cwd": "/absolute/path/to/ai-team-mcp"
       }
     }
   }
   ```

   **Important:** Replace `/absolute/path/to/ai-team-mcp` with your actual path!

   **Windows example:**
   ```json
   {
     "mcpServers": {
       "ai-team": {
         "command": "python",
         "args": ["-m", "mcp_ai_chat.server_modular"],
         "cwd": "C:\\Users\\YourName\\Projects\\ai-team-mcp"
       }
     }
   }
   ```

3. **Restart Cursor**

### For Windsurf

1. **Locate MCP config file:**
   - **Windows**: `C:\Users\YourUsername\.windsurf\mcp.json`
   - **macOS/Linux**: `~/.windsurf/mcp.json`

2. **Edit the config** (same format as Cursor above)

3. **Restart Windsurf**

### For Claude Desktop

1. **Locate config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Edit the config:**

   ```json
   {
     "mcpServers": {
       "ai-team": {
         "command": "python",
         "args": ["-m", "mcp_ai_chat.server_modular"],
         "cwd": "/absolute/path/to/ai-team-mcp"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

---

## Verification

### Step 1: Check MCP Server Logs

**In Cursor/Windsurf:**
1. Open Command Palette (`Ctrl/Cmd + Shift + P`)
2. Type "MCP: Show Logs"
3. Look for `ai-team` server startup messages

**Expected output:**
```
[ai-team] MCP Server starting...
[ai-team] Tools loaded: 28
[ai-team] Server ready
```

### Step 2: Test Agent Registration

In your AI assistant, try:

```python
mcp_ai-chat-group_register_agent({
  "agent_name": "test_agent",
  "role": "Test Agent",
  "description": "Testing installation"
})
```

**Expected response:**
```
✅ 代理注册成功
代理名称: test_agent
角色: Test Agent
...
```

### Step 3: Test Message Sending

```python
mcp_ai-chat-group_send_message({
  "recipients": "test_agent",
  "message": "Hello from AI Team MCP!"
})
```

**Expected response:**
```
✅ 消息已发送
发送者: test_agent
接收者: test_agent
...
```

### Step 4: List Available Tools

Check that all 28 tools are available:

```python
# In Cursor/Windsurf, check the MCP tools panel
# You should see tools prefixed with "mcp_ai-chat-group_"
```

**Expected tools:**
- `mcp_ai-chat-group_send_message`
- `mcp_ai-chat-group_receive_messages`
- `mcp_ai-chat-group_create_task`
- ... (25 more)

---

## Troubleshooting

### Problem: "Module 'mcp' not found"

**Solution:**
```bash
# Install MCP SDK
pip install mcp

# If using virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install mcp
```

### Problem: "Server failed to start"

**Possible causes:**

1. **Wrong Python version**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Incorrect path in config**
   - Double-check `cwd` in `mcp.json`
   - Use absolute paths, not relative
   - On Windows, use `\\` or `/` in paths

3. **Missing files**
   ```bash
   # Check files exist
   ls mcp_ai_chat/server_modular.py
   ls mcp_ai_chat/tools/__init__.py
   ```

**Debug steps:**
```bash
# Test server manually
cd /path/to/ai-team-mcp
python -m mcp_ai_chat.server_modular

# Should start without errors
```

### Problem: "Tools not appearing"

**Solution:**

1. **Restart your MCP client** (Cursor/Windsurf/Claude Desktop)
2. **Clear MCP cache:**
   - Delete `.cursor/mcp_cache/` (Cursor)
   - Delete `.windsurf/mcp_cache/` (Windsurf)
3. **Check MCP logs** for errors

### Problem: "Permission denied"

**On macOS/Linux:**
```bash
# Make sure files are readable
chmod -R 755 ai-team-mcp/
```

**On Windows:**
- Right-click folder → Properties → Security
- Ensure your user has "Read" and "Execute" permissions

### Problem: Data Files Not Found

**Solution:**

The server automatically creates data directories. If you see errors:

```bash
# Manually create data directory
mkdir -p ~/.mcp_ai_chat

# Set permissions (macOS/Linux)
chmod 755 ~/.mcp_ai_chat
```

**Windows:**
```powershell
# Create data directory
New-Item -ItemType Directory -Path "$env:USERPROFILE\.mcp_ai_chat"
```

---

## Advanced Setup

### Multiple Agent Configurations

To run multiple agents (e.g., manager, developer, tester), create separate MCP server entries:

```json
{
  "mcpServers": {
    "ai-team-manager": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "cwd": "/path/to/ai-team-mcp",
      "env": {
        "AI_AGENT_NAME": "manager"
      }
    },
    "ai-team-developer": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "cwd": "/path/to/ai-team-mcp",
      "env": {
        "AI_AGENT_NAME": "developer"
      }
    }
  }
}
```

### Custom Data Directory

Set a custom data storage location:

```json
{
  "mcpServers": {
    "ai-team": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular"],
      "cwd": "/path/to/ai-team-mcp",
      "env": {
        "MCP_DATA_DIR": "/custom/path/to/data"
      }
    }
  }
}
```

### Development Mode

For development and debugging:

```json
{
  "mcpServers": {
    "ai-team-dev": {
      "command": "python",
      "args": ["-m", "mcp_ai_chat.server_modular", "--debug"],
      "cwd": "/path/to/ai-team-mcp",
      "env": {
        "PYTHONUNBUFFERED": "1",
        "MCP_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### Employee Config Files

Load agent roles from `.mdc` files:

1. **Create config file** (`.cursor/rules/agent_a.mdc`):
   ```markdown
   # Agent A Configuration
   
   **Role**: Frontend Developer
   
   **Description**: Specializes in React, TypeScript, and UI/UX design
   
   **Responsibilities**:
   - Implement user interfaces
   - Optimize frontend performance
   - Ensure accessibility compliance
   ```

2. **Set config path:**
   ```python
   mcp_ai-chat-group_set_employee_config({
     "agent_name": "agent_a",
     "mdc_file_path": ".cursor/rules/agent_a.mdc"
   })
   ```

3. **Register with auto-load:**
   ```python
   mcp_ai-chat-group_register_agent({
     "agent_name": "agent_a",
     "auto_load_from_mdc": True
   })
   ```

---

## Next Steps

✅ Installation complete? Here's what to do next:

1. **Read the [Quick Start Guide](../README.md#quick-start)** - Get productive in 5 minutes
2. **Explore [Examples](EXAMPLES.md)** - Real-world usage scenarios
3. **Check [API Reference](API_REFERENCE.md)** - Complete tool documentation
4. **Join the Community** - Share your experience!

---

## Getting Help

**Still stuck?**

- 📚 [Troubleshooting Guide](TROUBLESHOOTING.md)
- 💬 [GitHub Discussions](https://github.com/KALUSO-nolodjska/ai-team-mcp/discussions)
- 🐛 [Report an Issue](https://github.com/KALUSO-nolodjska/ai-team-mcp/issues)
- 📧 Email: lhq2328616309@outlook.com

---

**Last Updated**: 2025-11-10  
**Version**: 5.0


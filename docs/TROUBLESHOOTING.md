# 🔧 Troubleshooting Guide

Common issues and solutions for AI Team MCP.

---

## 📋 Quick Links

- [Installation Issues](#installation-issues)
- [Server Issues](#server-issues)
- [Tool Execution Issues](#tool-execution-issues)
- [Data Issues](#data-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### ❌ "Module 'mcp' not found"

**Symptom:**

```
ModuleNotFoundError: No module named 'mcp'
```

**Solutions:**

1. **Install MCP SDK:**

   ```bash
   pip install mcp
   ```
2. **Check Python environment:**

   ```bash
   # Which Python?
   which python

   # Install in correct environment
   python -m pip install mcp
   ```
3. **If using virtual environment:**

   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   pip install mcp
   ```

---

### ❌ "Server failed to start"

**Symptom:** MCP server doesn't appear in Cursor/Windsurf

**Solutions:**

1. **Check MCP logs:**

   - Cursor: `Ctrl/Cmd + Shift + P` → "MCP: Show Logs"
   - Look for error messages
2. **Verify config path:**

   ```json
   {
     "cwd": "/absolute/path/to/ai-team-mcp"  // Must be absolute!
   }
   ```
3. **Test server manually:**

   ```bash
   cd /path/to/ai-team-mcp
   python -m mcp_ai_chat.server_modular
   ```

   Should start without errors.
4. **Check Python version:**

   ```bash
   python --version  # Must be 3.8+
   ```
5. **Verify file structure:**

   ```bash
   ls mcp_ai_chat/server_modular.py  # Should exist
   ls mcp_ai_chat/tools/__init__.py   # Should exist
   ```

---

### ❌ "Permission denied" (macOS/Linux)

**Symptom:**

```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**

1. **Fix file permissions:**

   ```bash
   chmod -R 755 ai-team-mcp/
   ```
2. **Check data directory:**

   ```bash
   ls -la ~/.mcp_ai_chat
   chmod 755 ~/.mcp_ai_chat
   ```

---

## Server Issues

### ❌ Server crashes immediately

**Symptom:** Server starts then crashes

**Debug steps:**

1. **Run with debug logging:**

   ```json
   {
     "mcpServers": {
       "ai-team": {
         "command": "python",
         "args": ["-m", "mcp_ai_chat.server_modular"],
         "cwd": "/path/to/ai-team-mcp",
         "env": {
           "PYTHONUNBUFFERED": "1",
           "MCP_LOG_LEVEL": "DEBUG"
         }
       }
     }
   }
   ```
2. **Check for syntax errors:**

   ```bash
   python -m py_compile mcp_ai_chat/server_modular.py
   ```
3. **Test imports:**

   ```bash
   python -c "from mcp_ai_chat import server_modular"
   ```

---

### ❌ "Tools not appearing"

**Symptom:** Server starts but no tools visible

**Solutions:**

1. **Restart MCP client** (Cursor/Windsurf/Claude Desktop)
2. **Clear MCP cache:**

   ```bash
   # Cursor
   rm -rf ~/.cursor/mcp_cache/

   # Windsurf
   rm -rf ~/.windsurf/mcp_cache/

   # Claude Desktop
   rm -rf ~/Library/Application\ Support/Claude/mcp_cache/
   ```
3. **Check tool count:**

   - Should see 28 tools prefixed with `mcp_ai-chat-group_`
4. **Verify server logs:**

   - Look for "Tools loaded: 28" message

---

### ❌ Server becomes unresponsive

**Symptom:** Server stops responding to requests

**Solutions:**

1. **Restart MCP server:**

   - Restart Cursor/Windsurf/Claude Desktop
2. **Check for file locks:**

   ```bash
   # macOS/Linux
   lsof | grep .mcp_ai_chat

   # Windows
   handle.exe | findstr .mcp_ai_chat
   ```
3. **Clear data files:**

   ```bash
   # Backup first!
   cp -r ~/.mcp_ai_chat ~/.mcp_ai_chat.backup

   # Clear
   rm ~/.mcp_ai_chat/*.json
   ```

---

## Tool Execution Issues

### ❌ "Tool execution failed"

**Symptom:**

```
Error calling tool: [Some error message]
```

**Debug steps:**

1. **Check parameter format:**

   ```python
   # Good
   mcp_ai-chat-group_send_message({
     "recipients": "agent_a",
     "message": "Hello"
   })

   # Bad - missing quotes
   mcp_ai-chat-group_send_message({
     recipients: agent_a,
     message: Hello
   })
   ```
2. **Check required parameters:**

   - See [API Reference](API_REFERENCE.md) for required fields
3. **Test with minimal params:**

   ```python
   # Start simple
   mcp_ai-chat-group_register_agent({
     "agent_name": "test"
   })
   ```

---

### ❌ "Agent not found"

**Symptom:**

```
Error: Agent 'agent_a' not found
```

**Solutions:**

1. **Register agent first:**

   ```python
   mcp_ai-chat-group_register_agent({
     "agent_name": "agent_a",
     "role": "Developer"
   })
   ```
2. **List registered agents:**

   ```python
   mcp_ai-chat-group_list_agents()
   ```
3. **Check spelling:**

   - Agent names are case-sensitive
   - Use exact names (e.g., "agent_a" not "Agent_A")

---

### ❌ "Task not found"

**Symptom:**

```
Error: Task 'TASK_...' not found
```

**Solutions:**

1. **List all tasks:**

   ```python
   mcp_ai-chat-group_get_tasks({})
   ```
2. **Check task ID format:**

   - Should be `TASK_YYYYMMDDHHMMSS_NNN`
   - Example: `TASK_20251110120000_001`
3. **Task might be deleted:**

   - Soft-deleted tasks are hidden
   - Manager can see all tasks with `assignee: "*"`

---

## Data Issues

### ❌ "Messages not appearing"

**Symptom:** Sent messages don't show up

**Solutions:**

1. **Check recipient name:**

   ```python
   # Correct
   mcp_ai-chat-group_send_message({
     "recipients": "agent_a",
     "message": "Hello"
   })

   # Wrong - typo
   mcp_ai-chat-group_send_message({
     "recipients": "agnet_a",  # ← typo!
     "message": "Hello"
   })
   ```
2. **Verify message was sent:**

   - Check return message for "✅ 消息已发送"
3. **Check filters:**

   ```python
   # Get ALL messages (no filters)
   mcp_ai-chat-group_receive_messages({
     "recipient": "*",
     "limit": 50
   })
   ```

---

### ❌ "Data corruption"

**Symptom:** Invalid JSON errors

**Solutions:**

1. **Backup data:**

   ```bash
   cp -r ~/.mcp_ai_chat ~/.mcp_ai_chat.backup
   ```
2. **Validate JSON:**

   ```bash
   # Check for syntax errors
   python -m json.tool ~/.mcp_ai_chat/messages.json
   ```
3. **Reset data (last resort):**

   ```bash
   # Will lose all data!
   rm -rf ~/.mcp_ai_chat
   # Server will recreate on next start
   ```

---

### ❌ "Data directory not found"

**Symptom:**

```
Error: Cannot create data directory
```

**Solutions:**

1. **Manual create:**

   ```bash
   # Linux/macOS
   mkdir -p ~/.mcp_ai_chat
   chmod 755 ~/.mcp_ai_chat

   # Windows
   mkdir %USERPROFILE%\.mcp_ai_chat
   ```
2. **Check permissions:**

   ```bash
   # Should be writable
   ls -ld ~/.mcp_ai_chat
   ```

---

## Performance Issues

### ❌ "Slow tool execution"

**Symptom:** Tools take >1 second to execute

**Causes & Solutions:**

1. **Large data files:**

   ```bash
   # Check file sizes
   ls -lh ~/.mcp_ai_chat/

   # If messages.json > 10MB, archive old messages
   ```
2. **Too many messages/tasks:**

   ```python
   # Use filters and limits
   mcp_ai-chat-group_receive_messages({
     "limit": 10,  # Don't fetch all
     "unread_only": True
   })
   ```
3. **Disk I/O:**

   - Move data dir to SSD if on HDD

---

### ❌ "High memory usage"

**Symptom:** Python process using >500MB RAM

**Solutions:**

1. **Restart server periodically**
2. **Reduce message retention:**

   ```python
   # Archive old messages
   # Keep only last 30 days
   ```
3. **Limit message content:**

   ```python
   mcp_ai-chat-group_receive_messages({
     "max_content_length": 1000  # Truncate long messages
   })
   ```

---

## Common Error Messages

### "Invalid parameter type"

**Problem:** Wrong parameter type (e.g., string instead of boolean)

**Solution:**

```python
# Wrong
mcp_ai-chat-group_receive_messages({
  "unread_only": "true"  # ← String, should be boolean
})

# Correct
mcp_ai-chat-group_receive_messages({
  "unread_only": True  # ← Boolean
})
```

---

### "Missing required parameter"

**Problem:** Required field not provided

**Solution:**

```python
# Wrong - missing 'recipients'
mcp_ai-chat-group_send_message({
  "message": "Hello"
})

# Correct
mcp_ai-chat-group_send_message({
  "recipients": "agent_a",
  "message": "Hello"
})
```

---

### "Permission denied"

**Problem:** Agent doesn't have permission (e.g., employee trying to see all tasks)

**Solution:**

```python
# Employee view (only their tasks)
mcp_ai-chat-group_get_tasks({})

# Manager view (all tasks)
mcp_ai-chat-group_get_tasks({
  "assignee": "*"
})
```

---

## Platform-Specific Issues

### Windows

**Issue:** Path separators

```json
// Wrong
"cwd": "C:\Users\Name\ai-team-mcp"

// Correct (use forward slashes or double backslashes)
"cwd": "C:/Users/Name/ai-team-mcp"
// or
"cwd": "C:\\Users\\Name\\ai-team-mcp"
```

**Issue:** Python not in PATH

```powershell
# Add Python to PATH
$env:PATH += ";C:\Python39\"
```

---

### macOS

**Issue:** Permission denied for Python

```bash
# Use Python 3 explicitly
python3 -m pip install mcp
```

**Issue:** Gatekeeper blocking

```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine /path/to/ai-team-mcp
```

---

### Linux

**Issue:** Python 2 vs Python 3

```bash
# Always use python3
python3 -m mcp_ai_chat.server_modular
```

---

## Getting More Help

### Enable Debug Logging

```json
{
  "mcpServers": {
    "ai-team": {
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

### Collect Diagnostic Info

```bash
# System info
python --version
pip list | grep mcp

# File structure
ls -R mcp_ai_chat/

# Data files
ls -lh ~/.mcp_ai_chat/

# Permissions
ls -la mcp_ai_chat/
```

### Report an Issue

When reporting issues, include:

1. **Error message** (full text)
2. **Steps to reproduce**
3. **System info** (OS, Python version)
4. **MCP logs** (from debug logging)
5. **Config file** (sanitized, remove sensitive info)

**Report here:** https://github.com/KALUSO-nolodjska/ai-team-mcp/issues

---

## Still Stuck?

- 💬 [GitHub Discussions](https://github.com/KALUSO-nolodjska/ai-team-mcp/discussions)
- 📧 Email: lhq2328616309@outlook.com
- 📚 [Documentation](../README.md)

---

**Last Updated**: 2025-11-10
**Version**: 5.0


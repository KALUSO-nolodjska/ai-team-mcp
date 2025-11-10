# 📖 API Reference

Complete reference for all 28 tools in AI Team MCP.

---

## 📬 Message Tools (7 tools)

### 1. `send_message`

Send a message to one or more AI agents.

**Parameters:**
```python
{
  "recipients": str,      # Agent names separated by &, e.g., "a&b&c"
  "message": str,         # Optional: message content
  "file_path": str       # Optional: file to send
}
```

**Example:**
```python
mcp_ai-chat-group_send_message({
  "recipients": "agent_a&agent_b",
  "message": "API implementation complete!"
})
```

**Returns:**
```
✅ 消息已发送
发送者: sender_name
接收者: agent_a, agent_b
消息ID: 2025-11-10T12:00:00_123
内容长度: 30 字符
```

---

### 2. `receive_messages`

Receive messages for a specific agent.

**Parameters:**
```python
{
  "recipient": str,           # Agent name or "*" for all
  "limit": int,              # Max messages (default: 20, max: 50)
  "unread_only": bool,       # Only unread messages (default: false)
  "keywords": List[str],     # Filter by keywords
  "since": str,              # ISO timestamp, e.g., "2025-11-10T00:00:00"
  "max_content_length": int  # Max chars per message (default: 5000)
}
```

**Example:**
```python
mcp_ai-chat-group_receive_messages({
  "recipient": "agent_a",
  "unread_only": true,
  "limit": 10
})
```

**Returns:**
```
📬 收到 2 条消息:

--- 消息 2025-11-10T12:00:00_123 [未读] ---
发送者: manager
时间: 2025-11-10T12:00:00
内容: API implementation complete!
---
```

---

### 3. `mark_messages_read`

Mark messages as read.

**Parameters:**
```python
{
  "message_ids": List[str]  # List of message IDs
}
```

**Example:**
```python
mcp_ai-chat-group_mark_messages_read({
  "message_ids": ["2025-11-10T12:00:00_123", "2025-11-10T12:01:00_124"]
})
```

---

### 4. `request_help`

Request help from other agents.

**Parameters:**
```python
{
  "recipients": str,    # Agent names separated by &
  "topic": str,         # Help topic
  "description": str,   # Detailed description
  "urgency": str       # "紧急" | "重要" | "一般"
}
```

**Example:**
```python
mcp_ai-chat-group_request_help({
  "recipients": "agent_b&agent_c",
  "topic": "Database optimization",
  "description": "Need help optimizing query performance",
  "urgency": "重要"
})
```

---

### 5. `request_review`

Request code review from other agents.

**Parameters:**
```python
{
  "recipients": str,     # Reviewer names separated by &
  "file_path": str,      # File to review
  "description": str     # Optional: review notes
}
```

**Example:**
```python
mcp_ai-chat-group_request_review({
  "recipients": "agent_b",
  "file_path": "backend/api/users.py",
  "description": "Please check error handling"
})
```

---

### 6. `notify_completion`

Notify others about task completion.

**Parameters:**
```python
{
  "recipients": str,            # Agent names separated by &
  "task_title": str,           # Completed task title
  "summary": str,              # Completion summary
  "related_files": List[str]   # Optional: related files
}
```

**Example:**
```python
mcp_ai-chat-group_notify_completion({
  "recipients": "manager",
  "task_title": "User authentication",
  "summary": "JWT auth implemented with refresh tokens",
  "related_files": ["backend/auth/jwt.py"]
})
```

---

### 7. `share_code_snippet`

Share code snippets with other agents.

**Parameters:**
```python
{
  "recipients": str,    # Agent names separated by &
  "file_path": str,     # File path
  "description": str,   # Description
  "line_start": int,    # Optional: start line
  "line_end": int      # Optional: end line
}
```

**Example:**
```python
mcp_ai-chat-group_share_code_snippet({
  "recipients": "agent_a",
  "file_path": "backend/utils/crypto.py",
  "description": "New encryption utility",
  "line_start": 10,
  "line_end": 30
})
```

---

## 📋 Task Tools (6 tools)

### 1. `create_task`

Create a new task.

**Parameters:**
```python
{
  "title": str,         # Task title
  "description": str,   # Detailed description
  "priority": str,      # "P0" | "P1" | "P2"
  "due_date": str      # Optional: ISO timestamp
}
```

**Example:**
```python
mcp_ai-chat-group_create_task({
  "title": "Implement user login",
  "description": "Add JWT-based authentication",
  "priority": "P1",
  "due_date": "2025-11-15T23:59:59"
})
```

**Returns:**
```
✅ 任务已创建
任务ID: TASK_20251110120000_001
标题: Implement user login
优先级: P1
创建者: manager
```

---

### 2. `assign_task`

Assign a task to an agent.

**Parameters:**
```python
{
  "task_id": str,    # Task ID
  "assignee": str   # Agent name
}
```

**Example:**
```python
mcp_ai-chat-group_assign_task({
  "task_id": "TASK_20251110120000_001",
  "assignee": "agent_a"
})
```

---

### 3. `update_task_status`

Update task status and progress.

**Parameters:**
```python
{
  "task_id": str,          # Task ID
  "status": str,           # "待开始" | "进行中" | "已完成" | "已阻塞" | "已取消"
  "progress_note": str    # Optional: progress note
}
```

**Example:**
```python
mcp_ai-chat-group_update_task_status({
  "task_id": "TASK_20251110120000_001",
  "status": "进行中",
  "progress_note": "JWT signing implemented, working on refresh tokens"
})
```

---

### 4. `get_tasks`

Get tasks (filtered by role).

**Parameters:**
```python
{
  "assignee": str,    # Optional: filter by assignee ("*" for all, manager only)
  "status": str,      # Optional: filter by status
  "priority": str    # Optional: filter by priority
}
```

**Permission:**
- **Employees**: Only see tasks assigned to them
- **Manager**: Can see all tasks (use `assignee: "*"`)

**Example:**
```python
# Employee view (only their tasks)
mcp_ai-chat-group_get_tasks({})

# Manager view (all tasks)
mcp_ai-chat-group_get_tasks({
  "assignee": "*",
  "priority": "P0"
})
```

---

### 5. `delete_task`

Delete tasks (soft or hard delete).

**Parameters:**
```python
{
  "task_ids": List[str],  # List of task IDs
  "permanent": bool       # true = hard delete, false = soft delete (default)
}
```

**Permission:**
- Only task creator or manager can delete tasks

**Example:**
```python
# Soft delete (mark as deleted)
mcp_ai-chat-group_delete_task({
  "task_ids": ["TASK_20251110120000_001"]
})

# Hard delete (permanent removal)
mcp_ai-chat-group_delete_task({
  "task_ids": ["TASK_20251110120000_001"],
  "permanent": true
})
```

---

## 👨‍👩‍👧‍👦 Group Tools (11 tools)

### 1. `create_group`

Create a project group.

**Parameters:**
```python
{
  "name": str,            # Group name
  "members": List[str],   # Member agent names
  "description": str     # Optional: group description
}
```

**Example:**
```python
mcp_ai-chat-group_create_group({
  "name": "Authentication Module",
  "members": ["manager", "agent_a", "agent_b"],
  "description": "Team working on auth features"
})
```

---

### 2. `send_group_message`

Send a message to a group.

**Parameters:**
```python
{
  "group_id": str,          # Group ID
  "message": str,           # Message content
  "file_path": str,         # Optional: file to send
  "mentions": List[str],    # Optional: agents to @mention
  "importance": str,        # Optional: "low" | "normal" | "high"
  "topic": str,             # Optional: message topic
  "reply_to": str          # Optional: message ID to reply to
}
```

**Example:**
```python
mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_20251110_001",
  "message": "Backend API ready for testing!",
  "mentions": ["agent_a"],
  "importance": "high",
  "topic": "API Release"
})
```

---

### 3. `receive_group_messages`

Receive messages from a group.

**Parameters:**
```python
{
  "group_id": str,            # Group ID
  "limit": int,               # Max messages (default: 20, max: 50)
  "unread_only": bool,        # Only unread (default: false)
  "mentions_me": bool,        # Only messages mentioning me (default: false)
  "importance": str,          # Filter by importance
  "topic": str,               # Filter by topic
  "keywords": List[str],      # Filter by keywords
  "since": str,               # ISO timestamp
  "max_content_length": int,  # Max chars per message (default: 5000)
  "show_pinned": bool        # Show pinned first (default: false)
}
```

**Example:**
```python
mcp_ai-chat-group_receive_group_messages({
  "group_id": "GRP_20251110_001",
  "mentions_me": true,
  "importance": "high"
})
```

---

### 4. `list_groups`

List all groups.

**Parameters:**
```python
{
  "member": str,            # Optional: filter by member
  "status": str,            # Optional: "active" | "archived" | "all" (default: active)
  "include_preview": bool  # Optional: include last message preview (default: false)
}
```

**Example:**
```python
mcp_ai-chat-group_list_groups({
  "status": "active",
  "include_preview": true
})
```

---

### 5. `join_group`

Join an existing group.

**Parameters:**
```python
{
  "group_id": str  # Group ID
}
```

---

### 6. `leave_group`

Leave a group.

**Parameters:**
```python
{
  "group_id": str  # Group ID
}
```

---

### 7. `summarize_group_messages`

Generate a summary of group messages.

**Parameters:**
```python
{
  "group_id": str,      # Group ID
  "time_range": str,    # "last_24_hours" | "last_7_days" | "last_30_days" | ISO timestamp
  "max_length": int    # Max summary length in chars (default: 500)
}
```

**Example:**
```python
mcp_ai-chat-group_summarize_group_messages({
  "group_id": "GRP_20251110_001",
  "time_range": "last_7_days",
  "max_length": 300
})
```

---

### 8. `get_unread_counts`

Get unread message counts for groups.

**Parameters:**
```python
{
  "groups": List[str]  # Optional: specific group IDs (empty = all groups)
}
```

**Returns:**
```
📊 未读消息统计:

群组: Authentication Module (GRP_20251110_001)
- 未读消息: 5
- @我的消息: 2
- 重要消息: 1
```

---

### 9. `archive_group`

Archive a completed project group.

**Parameters:**
```python
{
  "group_id": str,  # Group ID
  "reason": str    # Optional: archive reason
}
```

---

### 10. `pin_message`

Pin an important message in a group.

**Parameters:**
```python
{
  "group_id": str,    # Group ID
  "message_id": str  # Message ID
}
```

---

### 11. `unpin_message`

Unpin a message.

**Parameters:**
```python
{
  "group_id": str,    # Group ID
  "message_id": str  # Message ID
}
```

---

## 🔧 System Tools (4 tools)

### 1. `register_agent`

Register an AI agent.

**Parameters:**
```python
{
  "agent_name": str,          # Agent name (e.g., "a", "b", "manager")
  "role": str,                # Optional: role (e.g., "Frontend Developer")
  "description": str,         # Optional: description
  "auto_load_from_mdc": bool # Optional: load from .mdc file (default: true)
}
```

**Example:**
```python
mcp_ai-chat-group_register_agent({
  "agent_name": "agent_a",
  "role": "Frontend Developer",
  "description": "Specializes in React and TypeScript"
})
```

---

### 2. `set_employee_config`

Set employee config file path.

**Parameters:**
```python
{
  "agent_name": str,        # Agent name
  "mdc_file_path": str     # Path to .mdc file (relative to workspace)
}
```

**Example:**
```python
mcp_ai-chat-group_set_employee_config({
  "agent_name": "agent_a",
  "mdc_file_path": ".cursor/rules/agent_a.mdc"
})
```

---

### 3. `get_current_session`

Get current agent session info.

**Parameters:** None

**Returns:**
```
📌 当前会话信息:
代理名称: agent_a
角色: Frontend Developer
描述: Specializes in React and TypeScript
会话ID: sess_123456
注册时间: 2025-11-10T12:00:00
```

---

### 4. `list_agents`

List all registered agents.

**Parameters:** None

**Returns:**
```
👥 已注册代理 (3):

1. manager (产品经理)
   描述: 负责项目规划和团队协调
   会话: sess_123456
   
2. agent_a (前端开发工程师)
   描述: Specializes in React and TypeScript
   会话: sess_789012
```

---

### 5. `standby`

Enter standby mode (auto-monitor for 5 minutes).

**Parameters:**
```python
{
  "status_message": str,    # Status message
  "check_tasks": bool,      # Check for new tasks (default: true)
  "check_messages": bool,   # Check for new messages (default: true)
  "auto_read": bool        # Auto-read new content (default: true)
}
```

**Behavior:**
- Continuously monitors for new tasks/messages
- Returns immediately if new tasks/messages arrive
- Timer: 5 minutes (forced, cannot be changed)
- Automatically calls itself to continue monitoring

**Example:**
```python
mcp_ai-chat-group_standby({
  "status_message": "Waiting for new tasks",
  "check_tasks": true,
  "check_messages": true,
  "auto_read": true
})
```

**Returns (if new tasks/messages):**
```
🔔 待命检查：收到新任务/消息，继续工作

📬 未读消息 (2条):
[message details...]

⚠️ 重要：处理完任务/消息后，必须继续调用standby保持监听！
```

---

## 🔍 Common Patterns

### Pattern 1: Task Assignment Flow

```python
# 1. Manager creates task
create_task({...})

# 2. Manager assigns to agent
assign_task({"task_id": "...", "assignee": "agent_a"})

# 3. Manager notifies agent
send_message({"recipients": "agent_a", "message": "New task assigned"})

# 4. Agent checks tasks
get_tasks({})

# 5. Agent updates status
update_task_status({"task_id": "...", "status": "进行中"})

# 6. Agent completes and notifies
notify_completion({...})
```

### Pattern 2: Group Collaboration

```python
# 1. Create project group
create_group({"name": "...", "members": [...]})

# 2. Send kickoff message
send_group_message({"group_id": "...", "message": "..."})

# 3. Members receive messages
receive_group_messages({"group_id": "..."})

# 4. Pin important messages
pin_message({"group_id": "...", "message_id": "..."})

# 5. Get unread counts
get_unread_counts({})

# 6. Archive when done
archive_group({"group_id": "..."})
```

### Pattern 3: Continuous Monitoring

```python
# Agent enters standby loop
while True:
    result = standby({
        "status_message": "Ready for work",
        "check_tasks": True,
        "check_messages": True,
        "auto_read": True
    })
    
    # Process new tasks/messages
    # (standby automatically continues)
```

---

## 📊 Return Format Standards

### Success Response
```
✅ [Operation] 成功
[Details...]
```

### Error Response
```
❌ 错误: [Error message]
[Additional details if applicable]
```

### List Response
```
📋 [Title] ([Count]):

[Item 1]
[Item 2]
...
```

### Info Response
```
ℹ️ [Information]
[Details...]
```

---

## 🔗 Related Documentation

- [Quick Start Guide](../README.md#quick-start)
- [Usage Examples](EXAMPLES.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

**Last Updated**: 2025-11-10  
**Version**: 5.0



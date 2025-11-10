# AI聊天群 - 协作工具使用指南

> **更新**: 2025-11-10  
> **版本**: v2.1.0

---

## 📋 工具列表

### 基础工具
1. **send_message** - 发送消息
2. **receive_messages** - 接收消息（已从 `get_messages` 改名）
3. **mark_messages_read** - 标记消息为已读
4. **register_agent** - 注册AI代理
5. **get_current_session** - 获取当前会话信息
6. **list_agents** - 列出所有AI代理

### 任务管理工具
7. **create_task** - 创建任务
8. **assign_task** - 分配任务
9. **update_task_status** - 更新任务状态
10. **get_tasks** - 获取任务列表

### 协作工具
11. **request_help** - 请求帮助
12. **request_review** - 请求代码审查
13. **notify_completion** - 通知任务完成
14. **share_code_snippet** - 分享代码片段

---

## 🚀 使用示例

### 1. 接收消息（已改名）

**之前**: `get_messages`
**现在**: `receive_messages`

```
# 接收所有消息
receive_messages({
  "recipient": "*",
  "limit": 50
})

# 只接收未读消息
receive_messages({
  "recipient": "*",
  "unread_only": true
})
```

---

### 2. 创建任务

```
create_task({
  "title": "实现知识库本地文件夹挂载功能",
  "description": "参考Cursor IDE，实现本地文件夹挂载到知识库",
  "priority": "P0",
  "due_date": "2025-11-15"
})
```

---

### 3. 分配任务

```
assign_task({
  "task_id": "TASK_20251110120000_0",
  "assignee": "a"
})
```

分配任务时会自动发送通知消息给被分配者。

---

### 4. 更新任务状态

```
update_task_status({
  "task_id": "TASK_20251110120000_0",
  "status": "进行中",
  "progress_note": "已完成前端文件选择器，正在实现文件监控"
})
```

**任务状态**:
- `待开始`
- `进行中`
- `已完成`
- `已阻塞`
- `已取消`

---

### 5. 获取任务列表

```
# 获取所有任务
get_tasks({})

# 获取分配给自己的任务
get_tasks({
  "assignee": "a"
})

# 获取进行中的任务
get_tasks({
  "status": "进行中"
})

# 获取P0优先级的任务
get_tasks({
  "priority": "P0"
})
```

---

### 6. 请求帮助

```
request_help({
  "recipients": "b&c",
  "topic": "API接口设计",
  "description": "需要设计一个知识库文件上传的API接口，请提供建议",
  "urgency": "重要"
})
```

**紧急程度**:
- `紧急` 🚨
- `重要` ⚠️
- `一般` ℹ️

---

### 7. 请求代码审查

```
request_review({
  "recipients": "b&c",
  "file_path": "backend/fastapi-app/routers/knowledge.py",
  "description": "请审查这个知识库路由的实现"
})
```

会自动读取文件内容并发送给审查者。

---

### 8. 通知任务完成

```
notify_completion({
  "recipients": "manager&a",
  "task_title": "实现知识库本地文件夹挂载功能",
  "summary": "已完成前端文件选择器和文件监控功能，后端API已实现",
  "related_files": [
    "backend/fastapi-app/routers/knowledge.py",
    "docs/frontend/KNOWLEDGE_BASE_LOCAL_FILESYSTEM_DESIGN.md"
  ]
})
```

---

### 9. 分享代码片段

```
# 分享整个文件
share_code_snippet({
  "recipients": "b",
  "file_path": "backend/domain/knowledge/service.py",
  "description": "这是知识库服务的实现，请参考"
})

# 分享特定行号范围
share_code_snippet({
  "recipients": "b",
  "file_path": "backend/domain/knowledge/service.py",
  "description": "这是文件上传的核心逻辑",
  "line_start": 50,
  "line_end": 100
})
```

---

## 💡 使用场景

### 场景1: 任务分配流程

**产品经理**:
```
# 1. 创建任务
create_task({
  "title": "实现知识库本地文件夹挂载功能",
  "description": "参考Cursor IDE实现",
  "priority": "P0"
})

# 2. 分配给前端
assign_task({
  "task_id": "TASK_20251110120000_0",
  "assignee": "a"
})
```

**员工A**:
```
# 1. 接收任务通知
receive_messages({
  "recipient": "a",
  "unread_only": true
})

# 2. 查看分配的任务
get_tasks({
  "assignee": "a"
})

# 3. 更新任务状态
update_task_status({
  "task_id": "TASK_20251110120000_0",
  "status": "进行中"
})
```

### 场景2: 协作开发

**员工A** → **员工B**:
```
# 请求API支持
request_help({
  "recipients": "b",
  "topic": "知识库文件上传API",
  "description": "前端需要上传文件到知识库，请提供API接口",
  "urgency": "重要"
})
```

**员工B** → **员工A**:
```
# 分享API实现
share_code_snippet({
  "recipients": "a",
  "file_path": "backend/fastapi-app/routers/knowledge.py",
  "description": "这是文件上传API的实现",
  "line_start": 100,
  "line_end": 150
})
```

### 场景3: 代码审查

**员工A** → **员工B** 和 **员工C**:
```
request_review({
  "recipients": "b&c",
  "file_path": "backend/fastapi-app/routers/knowledge.py",
  "description": "请审查这个知识库路由的实现，特别是错误处理部分"
})
```

### 场景4: 任务完成通知

**员工A** → **产品经理**:
```
notify_completion({
  "recipients": "manager",
  "task_title": "实现知识库本地文件夹挂载功能",
  "summary": "已完成前端文件选择器和文件监控功能",
  "related_files": [
    "docs/frontend/KNOWLEDGE_BASE_LOCAL_FILESYSTEM_DESIGN.md"
  ]
})
```

---

## 📊 数据存储

### 任务数据

任务存储在 `~/.mcp_ai_chat/tasks.json`:

```json
{
  "id": "TASK_20251110120000_0",
  "title": "任务标题",
  "description": "任务描述",
  "priority": "P0",
  "status": "进行中",
  "creator": "manager",
  "creator_session_id": "会话ID",
  "assignee": "a",
  "created_at": "2025-11-10T12:00:00",
  "due_date": "2025-11-15",
  "updated_at": "2025-11-10T12:00:00",
  "progress_note": "进度说明"
}
```

---

## ✅ 最佳实践

1. **任务管理**
   - 创建任务时明确优先级和截止日期
   - 分配任务后及时更新状态
   - 完成任务后发送完成通知

2. **协作交流**
   - 请求帮助时明确主题和紧急程度
   - 分享代码时提供清晰的说明
   - 代码审查时说明重点关注的方面

3. **消息管理**
   - 定期接收未读消息
   - 阅读后及时标记为已读
   - 使用 `receive*` 接收所有消息

---

**文档版本**: v2.1.0  
**最后更新**: 2025-11-10  
**维护者**: 产品经理



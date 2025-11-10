# AI聊天群 MCP工具 - 使用示例

## 📋 基本使用

### 1. 注册AI代理

在使用前，建议先注册当前AI代理：

```
register_agent({
  "agent_name": "manager",
  "description": "产品经理AI助手"
})
```

### 2. 发送消息

#### 发送文件内容给多个AI

**格式**: `use <文件名> send@<接收者1>&<接收者2>&...`

**示例**:
```
use docs/team/TASK_EMPLOYEE_A_Frontend.md send@a
use docs/team/TASK_EMPLOYEE_B_Backend.md send@b&c
```

#### 发送纯文本消息

```
send_message({
  "recipients": "a&b",
  "message": "API接口已完成，请前端对接"
})
```

### 3. 接收消息

#### 接收所有消息（get*）

```
get_messages({
  "recipient": "*",
  "limit": 50
})
```

#### 只接收未读消息

```
get_messages({
  "recipient": "*",
  "unread_only": true
})
```

#### 接收特定接收者的消息

```
get_messages({
  "recipient": "a",
  "unread_only": true
})
```

### 4. 标记消息为已读

```
mark_messages_read({
  "message_ids": ["消息ID1", "消息ID2"]
})
```

---

## 💼 实际使用场景

### 场景1: 产品经理分配任务

**产品经理** → **员工A**:
```
use docs/team/TASK_EMPLOYEE_A_Frontend.md send@a
```

**产品经理** → **员工B**:
```
use docs/team/TASK_EMPLOYEE_B_Backend.md send@b
```

### 场景2: 前端后端协作

**员工A** → **员工B**:
```
send_message({
  "recipients": "b",
  "message": "前端需要新的API接口: POST /api/knowledge/files，请实现"
})
```

**员工B** → **员工A**:
```
send_message({
  "recipients": "a",
  "message": "API接口已完成，文档见 docs/api_documentation/KNOWLEDGE_API.md"
})
```

### 场景3: 全栈集成协调

**员工C** → **员工A** 和 **员工B**:
```
send_message({
  "recipients": "a&b",
  "message": "前后端集成已完成，请测试。测试用例见 docs/testing/INTEGRATION_TEST.md"
})
```

### 场景4: 测试问题反馈

**员工D** → **产品经理**:
```
send_message({
  "recipients": "manager",
  "message": "测试发现bug，详情见 docs/bugfixes/BUG_001.md"
})
```

**员工D** → **相关开发人员**:
```
use docs/bugfixes/BUG_001.md send@a&b
```

### 场景5: 知识分享

**员工C** → **全体**:
```
send_message({
  "recipients": "a&b&d&manager",
  "message": "分享一个最佳实践: 使用MCP工具可以大大提高开发效率"
})
```

---

## 🔄 工作流程示例

### 完整协作流程

1. **产品经理分配任务**
   ```
   use docs/team/TASK_EMPLOYEE_A_Frontend.md send@a
   use docs/team/TASK_EMPLOYEE_B_Backend.md send@b
   ```

2. **员工A查看任务**
   ```
   get_messages({
     "recipient": "a",
     "unread_only": true
   })
   ```

3. **员工A标记已读**
   ```
   mark_messages_read({
     "message_ids": ["消息ID"]
   })
   ```

4. **员工A完成工作后通知员工B**
   ```
   send_message({
     "recipients": "b",
     "message": "前端接口调用已实现，请后端确认"
   })
   ```

5. **员工B查看消息**
   ```
   get_messages({
     "recipient": "b",
     "unread_only": true
   })
   ```

6. **员工B回复**
   ```
   send_message({
     "recipients": "a",
     "message": "后端接口已确认，可以开始集成测试"
   })
   ```

---

## 📝 最佳实践

1. **统一代理名称**: 使用统一的代理名称（a/b/c/d/manager）
2. **及时标记已读**: 阅读消息后及时标记为已读
3. **使用文件发送**: 对于复杂内容，使用文件发送而不是纯文本
4. **定期检查消息**: 定期使用 `get*` 检查是否有新消息
5. **明确消息内容**: 消息内容要清晰明确，包含必要的上下文

---

**文档版本**: v1.0.0  
**最后更新**: 2025-11-10



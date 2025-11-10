# 待命工具使用示例

> **创建时间**: 2025-11-10  
> **版本**: v3.1.0

---

## 📋 使用场景示例

### 场景1: 员工完成工作后待命

**员工A完成前端开发后**：

```python
# 1. 通知任务完成
notify_completion({
  "recipients": "manager",
  "task_title": "前端文件选择器实现",
  "summary": "已完成前端文件选择器功能，支持文件选择和预览",
  "related_files": ["frontend/components/FileSelector.vue"]
})

# 2. 进入待命状态
standby({
  "check_interval": 30,
  "timeout": 600,
  "status_message": "前端开发完成，等待新任务"
})
```

**返回**（如果有新任务）：
```
🔔 待命检查：发现新任务/消息

📋 找到 1 个任务

--- 任务 TASK_20251110_001 ---
标题: 前端文件上传功能优化
优先级: P1
状态: 待开始
描述: 优化文件上传的UI和用户体验...

✅ 已进入待命状态
待命ID: a_session123_2025-11-10T12:00:00
检查间隔: 30秒
超时时间: 600秒
状态: 前端开发完成，等待新任务

💡 提示: 请处理上述任务/消息，然后继续工作
```

### 场景2: 等待后端API响应

**员工A请求后端API后**：

```python
# 1. 请求API支持
request_help({
  "recipients": "b",
  "topic": "文件上传API",
  "description": "前端需要文件上传API接口",
  "urgency": "重要"
})

# 2. 进入待命状态，只检查消息
standby({
  "check_interval": 20,
  "timeout": 300,
  "check_tasks": false,  # 不检查任务
  "check_messages": true,  # 只检查消息
  "status_message": "等待后端API响应"
})
```

### 场景3: 产品经理持续监控

**产品经理分配任务后**：

```python
# 1. 创建并分配任务
create_task({
  "title": "知识库本地文件夹挂载功能",
  "description": "实现知识库本地文件夹挂载",
  "priority": "P0"
})

assign_task({
  "task_id": "TASK_001",
  "assignee": "a"
})

# 2. 进入待命状态，持续监控
standby({
  "check_interval": 60,
  "timeout": 0,  # 不超时，持续监控
  "check_tasks": true,
  "check_messages": true,
  "status_message": "监控项目进展"
})
```

### 场景4: 全栈工程师等待集成

**员工C等待前后端集成**：

```python
# 1. 通知前后端准备集成
send_message({
  "recipients": "a&b",
  "message": "请准备前后端集成，完成后通知我"
})

# 2. 进入待命状态
standby({
  "check_interval": 30,
  "timeout": 1800,  # 30分钟
  "check_tasks": true,
  "check_messages": true,
  "auto_read": true,
  "status_message": "等待前后端集成完成"
})
```

---

## 💡 最佳实践

### 1. 在回复末尾调用

**正确做法**：
```
# 完成工作
notify_completion({...})

# 立即进入待命
standby({...})
```

**错误做法**：
```
# 完成工作
notify_completion({...})

# 没有调用standby，AI会停止工作
```

### 2. 合理设置参数

**快速响应场景**（等待重要消息）：
```
standby({
  "check_interval": 15,  # 15秒检查一次
  "timeout": 300
})
```

**常规工作场景**（等待一般任务）：
```
standby({
  "check_interval": 30,  # 30秒检查一次
  "timeout": 600
})
```

**长期监控场景**（持续监控项目）：
```
standby({
  "check_interval": 60,  # 60秒检查一次
  "timeout": 0  # 不超时
})
```

### 3. 使用状态消息

**清晰的状态消息**：
```
standby({
  "status_message": "前端开发完成，等待新任务"
})
```

**模糊的状态消息**（不推荐）：
```
standby({
  "status_message": "等待"
})
```

---

## 🔄 工作流程示例

### 完整工作流程

```
1. 接收任务
   ↓
2. 处理任务
   ↓
3. 通知完成
   notify_completion({...})
   ↓
4. 进入待命
   standby({...})
   ↓
5. 检查新任务/消息
   ↓
6. 发现新任务 → 返回任务信息
   ↓
7. 处理新任务
   ↓
8. 重复步骤3-7
```

### 多任务处理流程

```
1. 完成任务A
   notify_completion({...})
   ↓
2. 进入待命
   standby({...})
   ↓
3. 发现任务B和C
   ↓
4. 处理任务B
   ↓
5. 处理任务C
   ↓
6. 再次进入待命
   standby({...})
```

---

## 📊 参数配置建议

### 检查间隔建议

| 场景 | 检查间隔 | 说明 |
|------|---------|------|
| 紧急任务 | 15秒 | 需要快速响应 |
| 常规任务 | 30秒 | 平衡响应速度和资源消耗 |
| 长期监控 | 60秒 | 持续监控，不紧急 |
| 后台等待 | 120秒 | 长时间等待，降低资源消耗 |

### 超时时间建议

| 场景 | 超时时间 | 说明 |
|------|---------|------|
| 等待响应 | 300秒（5分钟） | 等待其他AI回复 |
| 等待任务 | 600秒（10分钟） | 等待新任务分配 |
| 持续监控 | 0（不超时） | 持续监控项目 |
| 短期等待 | 180秒（3分钟） | 短期等待 |

---

## ✅ 检查清单

使用待命工具前，确认：

- [ ] 已完成当前工作
- [ ] 已通知相关人员（如需要）
- [ ] 设置了合理的检查间隔
- [ ] 设置了合理的超时时间
- [ ] 选择了正确的检查类型（任务/消息）
- [ ] 使用了清晰的状态消息
- [ ] 在回复末尾调用了standby

---

**文档版本**: v3.1.0  
**最后更新**: 2025-11-10







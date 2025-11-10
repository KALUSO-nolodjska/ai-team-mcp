# 使用示例

[English](EXAMPLES.md) | 简体中文

本文档提供AI Team MCP在实际场景中的使用示例。

---

## 🎯 基础示例

### 示例1: 注册AI代理

```python
# 注册一个前端开发AI代理
register_agent({
  "agent_name": "frontend_dev",
  "role": "前端开发工程师",
  "description": "负责UI/UX开发、组件开发、性能优化"
})

# 注册一个后端开发AI代理
register_agent({
  "agent_name": "backend_dev",
  "role": "后端开发工程师",
  "description": "负责API设计、数据库操作、业务逻辑"
})
```

### 示例2: 创建和管理任务

```python
# 创建任务
create_task({
  "title": "实现用户登录功能",
  "description": "包括前端表单和后端API",
  "priority": "P0",  # 紧急任务
  "due_date": "2025-11-15"
})

# 分配任务
assign_task({
  "task_id": "TASK_20251110_001",
  "assignee": "frontend_dev"
})

# 更新任务状态
update_task_status({
  "task_id": "TASK_20251110_001",
  "status": "进行中",
  "progress_note": "已完成UI设计"
})
```

### 示例3: 发送和接收消息

```python
# 发送消息
send_message({
  "recipients": "backend_dev",
  "message": "登录API的接口定义完成了吗？"
})

# 接收消息
receive_messages({
  "recipient": "frontend_dev",
  "unread_only": True,
  "limit": 10
})
```

---

## 💼 实际应用场景

### 场景1: 开发团队协作

**团队组成**:
- Manager: 产品经理AI
- Frontend: 前端开发AI
- Backend: 后端开发AI
- DevOps: 测试/运维AI

**工作流程**:

**1. Manager创建项目**
```python
# 创建项目群组
create_group({
  "name": "用户系统开发",
  "description": "用户注册、登录、权限管理",
  "members": ["manager", "frontend_dev", "backend_dev", "devops"]
})

# 创建任务列表
tasks = [
  {
    "title": "设计用户数据库表结构",
    "assignee": "backend_dev",
    "priority": "P0"
  },
  {
    "title": "实现登录注册UI",
    "assignee": "frontend_dev",
    "priority": "P1"
  },
  {
    "title": "配置CI/CD流程",
    "assignee": "devops",
    "priority": "P2"
  }
]

for task in tasks:
  create_task(task)
  assign_task(task["task_id"], task["assignee"])
```

**2. Backend完成数据库设计**
```python
# 更新任务状态
update_task_status({
  "task_id": "TASK_DB_001",
  "status": "已完成"
})

# 分享代码片段
share_code_snippet({
  "recipients": "frontend_dev",
  "file_path": "backend/models/user.py",
  "description": "用户模型定义，包含所有字段"
})

# 发送群组消息
send_group_message({
  "group_id": "GROUP_USER_SYSTEM",
  "message": "数据库表结构已完成，请查看用户模型定义",
  "mentions": ["frontend_dev"]
})
```

**3. Frontend实现UI**
```python
# 请求帮助
request_help({
  "recipients": "backend_dev",
  "topic": "登录API接口",
  "description": "请提供登录API的详细接口文档",
  "urgency": "重要"
})

# 接收群组消息
receive_group_messages({
  "group_id": "GROUP_USER_SYSTEM",
  "mentions_me": True
})

# 完成后通知
notify_completion({
  "recipients": "manager",
  "task_title": "登录注册UI",
  "summary": "已完成登录、注册、忘记密码页面",
  "related_files": ["src/pages/Login.tsx", "src/pages/Register.tsx"]
})
```

**4. DevOps进行测试**
```python
# 获取待测试任务
get_tasks({
  "status": "已完成",
  "priority": "P0"
})

# 请求代码审查
request_review({
  "recipients": "frontend_dev&backend_dev",
  "file_path": "tests/integration/test_auth.py",
  "description": "请审查集成测试代码"
})
```

**5. Manager进入待命模式**
```python
# 持续监听团队动态
standby({
  "status_message": "监控项目进度",
  "check_tasks": True,
  "check_messages": True
})
```

---

### 场景2: 研究团队协作

**研究小组**:
- Lead: 研究组长
- DataCollector: 数据收集AI
- Analyst: 数据分析AI
- Writer: 论文撰写AI

**工作流程**:

**1. 创建研究项目**
```python
# 创建研究群组
create_group({
  "name": "机器学习模型优化研究",
  "description": "研究深度学习模型压缩和加速技术",
  "members": ["lead", "data_collector", "analyst", "writer"]
})

# 分配研究任务
create_task({
  "title": "收集模型压缩相关论文",
  "assignee": "data_collector",
  "priority": "P0",
  "due_date": "2025-11-20"
})

create_task({
  "title": "分析现有压缩算法性能",
  "assignee": "analyst",
  "priority": "P1",
  "due_date": "2025-11-25"
})
```

**2. 数据收集和分享**
```python
# 分享研究资料
send_group_message({
  "group_id": "GROUP_ML_RESEARCH",
  "message": "已收集50篇相关论文，重点关注剪枝和量化技术",
  "topic": "文献综述",
  "importance": "high"
})

# 分享数据集
share_code_snippet({
  "recipients": "analyst",
  "file_path": "data/compression_benchmark.csv",
  "description": "各种压缩算法的性能基准数据"
})
```

**3. 数据分析**
```python
# 请求澄清
send_message({
  "recipients": "data_collector",
  "message": "baseline模型的参数量数据是否包含embedding层？"
})

# 分享分析结果
send_group_message({
  "group_id": "GROUP_ML_RESEARCH",
  "message": "分析完成：剪枝可减少40%参数，精度损失<2%",
  "topic": "实验结果"
})
```

**4. 论文撰写**
```python
# 获取所有研究材料
receive_group_messages({
  "group_id": "GROUP_ML_RESEARCH",
  "topic": "实验结果",
  "limit": 50
})

# 请求审阅
request_review({
  "recipients": "lead&analyst",
  "file_path": "paper/draft_v1.md",
  "description": "初稿完成，请审阅方法和结果部分"
})
```

---

### 场景3: 客户支持团队

**支持团队**:
- Supervisor: 主管
- SupportAgent1: 支持专员1
- SupportAgent2: 支持专员2
- TechExpert: 技术专家

**工作流程**:

**1. 创建支持票据群组**
```python
create_group({
  "name": "紧急问题处理",
  "description": "处理P0级客户问题",
  "members": ["supervisor", "support_1", "support_2", "tech_expert"]
})
```

**2. 分配客户问题**
```python
create_task({
  "title": "客户报告：登录失败",
  "description": "客户ID: 12345, 错误: Connection timeout",
  "priority": "P0",
  "assignee": "support_1"
})
```

**3. 升级技术问题**
```python
# 支持专员请求技术支持
request_help({
  "recipients": "tech_expert",
  "topic": "登录超时问题",
  "description": "已检查客户网络，问题可能在服务器端",
  "urgency": "紧急"
})

# 技术专家发送群组消息
send_group_message({
  "group_id": "GROUP_URGENT",
  "message": "发现数据库连接池满了，正在扩容",
  "importance": "high",
  "mentions": ["supervisor", "support_1"]
})
```

**4. 问题解决和归档**
```python
# 更新任务状态
update_task_status({
  "task_id": "TASK_CUSTOMER_001",
  "status": "已完成",
  "progress_note": "数据库连接池已扩容，问题解决"
})

# 通知团队
notify_completion({
  "recipients": "supervisor&support_1",
  "task_title": "客户登录失败问题",
  "summary": "根本原因：数据库连接池满。已扩容至200个连接。"
})

# 归档群组
archive_group({
  "group_id": "GROUP_URGENT",
  "reason": "问题已解决"
})
```

---

### 场景4: 内容创作团队

**创作团队**:
- Editor: 主编
- Writer: 作者
- Designer: 设计师
- Reviewer: 审稿人

**工作流程**:

**1. 创建内容项目**
```python
create_group({
  "name": "AI技术博客系列",
  "description": "撰写10篇关于AI应用的技术博客",
  "members": ["editor", "writer", "designer", "reviewer"]
})

# 创建写作任务
for topic in ["AI聊天机器人", "图像识别", "自然语言处理"]:
  create_task({
    "title": f"撰写：{topic}",
    "assignee": "writer",
    "priority": "P1"
  })
```

**2. 写作和设计协作**
```python
# 作者完成草稿
notify_completion({
  "recipients": "designer",
  "task_title": "AI聊天机器人文章",
  "summary": "文章草稿完成，需要3张配图",
  "related_files": ["articles/chatbot_draft.md"]
})

# 设计师分享配图
share_code_snippet({
  "recipients": "writer",
  "file_path": "images/chatbot_architecture.png",
  "description": "聊天机器人架构图"
})
```

**3. 审稿流程**
```python
# 请求审稿
request_review({
  "recipients": "reviewer",
  "file_path": "articles/chatbot_final.md",
  "description": "请审阅文章的技术准确性和可读性"
})

# 审稿人提供反馈
send_message({
  "recipients": "writer",
  "message": "建议：1) 简化第3段的技术描述 2) 添加更多实例"
})
```

**4. 发布和总结**
```python
# 主编总结进度
summarize_group_messages({
  "group_id": "GROUP_BLOG_SERIES",
  "time_range": "last_7_days",
  "max_length": 500
})

# 置顶重要消息
pin_message({
  "group_id": "GROUP_BLOG_SERIES",
  "message_id": "MSG_DEADLINE_REMINDER"
})
```

---

## 🔧 高级技巧

### 技巧1: 使用过滤器高效接收消息

```python
# 只接收特定时间后的未读消息
receive_messages({
  "recipient": "developer",
  "unread_only": True,
  "since": "2025-11-10T00:00:00",
  "keywords": ["紧急", "bug", "重要"],
  "limit": 20
})
```

### 技巧2: 批量任务管理

```python
# 获取所有高优先级未完成任务
tasks = get_tasks({
  "priority": "P0",
  "status": "进行中"
})

# 批量更新
for task in tasks:
  if task["due_date"] < today:
    update_task_status({
      "task_id": task["task_id"],
      "status": "已逾期"
    })
```

### 技巧3: 智能待命模式

```python
# 只监听特定类型的更新
standby({
  "status_message": "等待代码审查请求",
  "check_tasks": False,  # 不检查任务
  "check_messages": True,  # 只检查消息
  "auto_read": False  # 不自动标记为已读
})
```

### 技巧4: 群组消息摘要

```python
# 为长时间未查看的群组生成摘要
groups = list_groups({"status": "active"})
for group in groups:
  unread = get_unread_counts({"groups": [group["group_id"]]})
  if unread[group["group_id"]]["unread"] > 50:
    summary = summarize_group_messages({
      "group_id": group["group_id"],
      "time_range": "last_7_days"
    })
    # 阅读摘要而不是所有消息
```

---

## 📊 性能优化建议

### 1. 限制返回数据量

```python
# ❌ 不好：获取所有消息
receive_messages({"recipient": "*"})

# ✅ 好：限制数量和内容长度
receive_messages({
  "recipient": "*",
  "limit": 20,
  "max_content_length": 500
})
```

### 2. 使用时间过滤

```python
# ✅ 只获取最近的消息
receive_messages({
  "recipient": "developer",
  "since": "2025-11-10T12:00:00",
  "limit": 10
})
```

### 3. 任务分类查询

```python
# ✅ 按优先级和状态分别查询
p0_tasks = get_tasks({"priority": "P0", "status": "进行中"})
p1_tasks = get_tasks({"priority": "P1", "status": "待开始"})
```

---

## 💡 最佳实践

1. **定期使用待命模式** - 保持对新任务和消息的响应
2. **及时标记已读** - 避免消息堆积
3. **使用群组** - 相关人员集中讨论
4. **适当的任务粒度** - 任务不要太大或太小
5. **及时更新状态** - 让团队了解进展
6. **使用优先级** - P0紧急、P1重要、P2一般
7. **添加详细描述** - 便于他人理解任务和消息
8. **定期归档** - 保持活跃群组列表整洁

---

## 📚 相关文档

- [API参考](API_REFERENCE_CN.md) - 所有工具的详细说明
- [安装指南](INSTALLATION_CN.md) - 安装和配置步骤
- [架构说明](ARCHITECTURE_CN.md) - 系统架构设计
- [故障排除](TROUBLESHOOTING_CN.md) - 常见问题解决

---

## 💬 获取帮助

如果你有更多使用问题：

- 📧 Email: lhq2328616309@outlook.com
- 🐛 Issues: https://github.com/KALUSO-nolodjska/ai-team-mcp/issues
- 💬 Discussions: https://github.com/KALUSO-nolodjska/ai-team-mcp/discussions


# 员工配置使用指南

> **创建时间**: 2025-11-10  
> **版本**: v4.0.0  
> **功能**: 员工设定接口 - 自动拾取任务和加载配置

---

## 🎯 功能概述

**员工配置功能**允许新聊天的AI自动：
1. **拾取前员工的任务**：如果使用相同的`agent_name`注册，会自动显示分配给该员工的任务
2. **从.mdc文件加载设定**：自动从`.cursor/rules/{agent_name}.mdc`文件读取角色和描述
3. **继承之前的配置**：如果之前注册过，会自动继承角色和描述

---

## 📋 使用流程

### 方式1：自动模式（推荐）

**步骤1：设置员工配置（可选，如果.mdc文件在默认位置）**

如果`.mdc`文件在默认位置（`.cursor/rules/{agent_name}.mdc`），可以跳过此步骤。

如果需要指定其他路径：
```
set_employee_config({
  "agent_name": "a",
  "mdc_file_path": ".cursor/rules/a.mdc"  // 可选，默认使用 .cursor/rules/{agent_name}.mdc
})
```

**步骤2：注册AI代理（自动加载）**

```
register_agent({
  "agent_name": "a",
  "auto_load_from_mdc": true  // 默认true，自动从.mdc文件加载
})
```

**结果**：
- ✅ 自动从`.cursor/rules/a.mdc`读取角色和描述
- ✅ 自动显示分配给"a"的待处理任务
- ✅ 如果之前注册过，继承之前的配置

### 方式2：手动模式

如果不想使用自动加载，可以手动提供角色和描述：

```
register_agent({
  "agent_name": "a",
  "role": "前端开发工程师",
  "description": "前端开发工程师，负责前端功能开发和UI/UX优化",
  "auto_load_from_mdc": false
})
```

---

## 🔧 工具说明

### 1. set_employee_config - 设置员工配置

**功能**：设置员工配置，指定.mdc文件路径

**参数**：
- `agent_name` (string, 必填): AI代理名称（例如: a, b, c, d, manager）
- `mdc_file_path` (string, 可选): .mdc文件路径（相对于工作区根目录）。如果为空，使用默认路径`.cursor/rules/{agent_name}.mdc`

**示例**：
```
set_employee_config({
  "agent_name": "a"
})

# 或指定自定义路径
set_employee_config({
  "agent_name": "a",
  "mdc_file_path": ".cursor/rules/custom_a.mdc"
})
```

**返回**：
```
✅ 员工配置已设置
代理名称: a
.mdc文件: .cursor/rules/a.mdc

💡 提示: 现在可以使用 register_agent 自动加载角色和描述
```

### 2. register_agent - 注册AI代理（增强版）

**功能**：注册AI代理并创建会话。如果`agent_name`已存在，会自动拾取之前的任务

**参数**：
- `agent_name` (string, 必填): AI代理名称
- `role` (string, 可选): AI角色。如果设置了员工配置，会自动从.mdc文件读取
- `description` (string, 可选): AI代理描述。如果设置了员工配置，会自动从.mdc文件读取
- `auto_load_from_mdc` (boolean, 默认: true): 是否自动从.mdc文件加载员工设定

**示例**：
```
# 自动模式（推荐）
register_agent({
  "agent_name": "a"
})

# 手动模式
register_agent({
  "agent_name": "a",
  "role": "前端开发工程师",
  "description": "前端开发工程师，负责前端功能开发和UI/UX优化",
  "auto_load_from_mdc": false
})
```

**返回**（如果有待处理任务）：
```
✅ AI代理已注册并创建会话
名称: a
角色: 前端开发工程师
描述: 前端开发工程师，负责前端功能开发和UI/UX优化
会话ID: xxx-xxx-xxx

🔄 已继承之前的代理信息
之前的角色: 前端开发工程师
之前的描述: 前端开发工程师，负责前端功能开发和UI/UX优化

📋 发现 2 个待处理任务:
  - TASK_001: 实现知识库本地文件夹挂载功能 (待开始)
  - TASK_002: 前端UI优化 (进行中)

⚠️ 重要: 请记住你的会话ID，这是你在这次对话中的唯一身份标识
```

---

## 💡 使用场景

### 场景1：新AI接替前员工的工作

**情况**：之前的AI（员工A）已经完成了一些工作，现在新的AI需要接替

**步骤**：
1. 新AI调用 `register_agent({"agent_name": "a"})`
2. 系统自动：
   - 从`.cursor/rules/a.mdc`读取角色和描述
   - 显示分配给"a"的所有待处理任务
   - 继承之前的配置

**结果**：新AI可以立即看到需要处理的任务，无缝接替工作

### 场景2：AI重启后重新注册

**情况**：AI重启后，需要重新注册但保持之前的身份

**步骤**：
1. 调用 `register_agent({"agent_name": "a"})`
2. 系统自动继承之前的角色和描述
3. 显示待处理任务

**结果**：无需重新输入角色和描述，自动恢复工作状态

### 场景3：首次注册新员工

**情况**：首次注册一个新的员工（例如：新员工E）

**步骤**：
1. 创建`.cursor/rules/e.mdc`文件
2. 调用 `set_employee_config({"agent_name": "e"})`
3. 调用 `register_agent({"agent_name": "e"})`

**结果**：自动从.mdc文件加载角色和描述

---

## 📝 .mdc文件格式要求

.mdc文件应该包含以下信息（用于自动提取）：

### 标题格式
```markdown
# 员工A - 前端开发工程师
```

### register_agent示例（推荐）
```markdown
register_agent({
  "agent_name": "a",
  "role": "前端开发工程师",
  "description": "前端开发工程师，负责前端功能开发和UI/UX优化"
})
```

### 职责描述
```markdown
## 📋 核心职责
- 负责前端功能开发和UI/UX优化
```

---

## ✅ 功能检查清单

- [ ] 已创建`.cursor/rules/{agent_name}.mdc`文件
- [ ] 文件中包含角色信息（在标题或register_agent示例中）
- [ ] 文件中包含描述信息（在register_agent示例或职责描述中）
- [ ] 调用`set_employee_config`设置配置（可选）
- [ ] 调用`register_agent`注册代理
- [ ] 检查是否显示了待处理任务
- [ ] 检查角色和描述是否正确加载

---

## 🔍 故障排查

### 问题1：无法从.mdc文件加载角色

**可能原因**：
- .mdc文件不存在
- 文件格式不正确
- 角色信息不在前30行

**解决方法**：
1. 检查`.cursor/rules/{agent_name}.mdc`文件是否存在
2. 确保文件标题包含角色信息，例如：`# 员工A - 前端开发工程师`
3. 或在文件中包含`register_agent`示例，明确指定角色

### 问题2：无法显示待处理任务

**可能原因**：
- 没有分配给该`agent_name`的任务
- 任务状态不是"待开始"或"进行中"

**解决方法**：
1. 使用`get_tasks({"assignee": "a"})`检查任务
2. 确认任务状态为"待开始"或"进行中"

### 问题3：无法继承之前的配置

**可能原因**：
- 之前没有注册过该`agent_name`
- 配置文件被删除

**解决方法**：
1. 手动提供角色和描述
2. 或使用`set_employee_config`设置配置后重新注册

---

## 📚 相关文档

- **协作工具指南**: `mcp_ai_chat/COLLABORATION_TOOLS_GUIDE.md`
- **会话和角色指南**: `mcp_ai_chat/SESSION_ROLE_GUIDE.md`
- **待命工具指南**: `mcp_ai_chat/STANDBY_TOOL_GUIDE.md`

---

**文档版本**: v4.0.0  
**最后更新**: 2025-11-10  
**维护者**: 产品经理





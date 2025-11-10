# AI Team MCP - 多AI协作框架

<div align="center">

[English](README.md) | 简体中文

**企业级的多AI代理协作框架 - 28个工具，完美协调AI团队**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

[安装指南](docs/INSTALLATION_CN.md) | [API文档](docs/API_REFERENCE_CN.md) | [使用示例](docs/EXAMPLES_CN.md) | [架构说明](docs/ARCHITECTURE_CN.md)

</div>

---

## ✨ 核心特性

### 🤝 多AI协作系统
- **消息系统**: 线程化对话、已读回执、@提醒
- **任务管理**: 优先级管理、基于角色的权限控制
- **项目群组**: 群组聊天、消息置顶、话题分类
- **待命模式**: 5分钟定时器，持续监听新任务

### 🏗️ 100%模块化架构
- **17个清晰模块**: 从2700行单体文件重构而来
- **最大文件<820行**: 易于维护和扩展
- **企业级代码质量**: 生产环境就绪
- **100%向后兼容**: 所有工具调用方式保持一致

### 🔧 28个协作工具
<details>
<summary>点击查看完整工具列表</summary>

#### 基础通信
- `send_message` - 发送消息给其他AI
- `receive_messages` - 接收消息（支持高级过滤）
- `mark_messages_read` - 标记消息为已读

#### 任务管理
- `create_task` - 创建任务（P0/P1/P2优先级）
- `assign_task` - 分配任务给团队成员
- `update_task_status` - 更新任务状态
- `get_tasks` - 获取任务列表（支持多条件过滤）
- `delete_task` - 删除任务（软删除/硬删除）

#### 协作工具
- `request_help` - 请求其他AI的帮助
- `request_review` - 请求代码审查
- `notify_completion` - 通知任务完成
- `share_code_snippet` - 分享代码片段

#### 项目群组
- `create_group` - 创建项目群组
- `send_group_message` - 发送群组消息（支持@提醒）
- `receive_group_messages` - 接收群组消息
- `list_groups` - 列出所有群组
- `pin_message` / `unpin_message` - 置顶/取消置顶消息
- `archive_group` - 归档群组

#### 系统工具
- `register_agent` - 注册AI代理
- `get_current_session` - 获取当前会话
- `list_agents` - 列出所有代理
- `standby` - 进入待命模式（5分钟监听）

</details>

### 💼 支持的客户端
- ✅ **Cursor IDE** - AI编程助手
- ✅ **Windsurf** - 下一代IDE
- ✅ **Claude Desktop** - Anthropic官方客户端
- ✅ 任何支持MCP协议的工具

---

## 🚀 快速开始

### 📋 前置要求
- Python 3.8+
- 支持MCP的IDE（Cursor/Windsurf/Claude Desktop）

### 📦 安装

**方式1: 使用npm (推荐)**
```bash
npx @modelcontextprotocol/create-server ai-team-mcp
```

**方式2: 从源码安装**
```bash
git clone https://github.com/KALUSO-nolodjska/ai-team-mcp.git
cd ai-team-mcp
pip install -e .
```

### ⚙️ 配置

**Cursor / Windsurf** - 编辑 `.cursor/mcp.json` 或 `.windsurf/mcp.json`:
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

**Claude Desktop** - 编辑配置文件:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

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

**重启IDE** 以加载MCP服务器。

详细安装指南请参考：[INSTALLATION_CN.md](docs/INSTALLATION_CN.md)

---

## 📖 使用示例

### 基础使用

```python
# 1. 注册AI代理
register_agent({
  "agent_name": "developer",
  "role": "前端开发工程师",
  "description": "负责UI/UX和组件开发"
})

# 2. 创建任务
create_task({
  "title": "实现用户登录界面",
  "description": "使用React创建响应式登录表单",
  "priority": "P1",
  "due_date": "2025-11-15"
})

# 3. 发送消息
send_message({
  "recipients": "backend_dev",
  "message": "登录API准备好了吗？"
})

# 4. 进入待命模式（5分钟监听）
standby({
  "status_message": "等待新任务"
})
```

### 实际应用场景

<details>
<summary><b>场景1: 开发团队</b></summary>

**团队成员**:
- Manager (产品经理)
- Frontend (前端开发)
- Backend (后端开发)
- DevOps (测试/运维)

**工作流程**:
1. Manager创建任务并分配给团队成员
2. Frontend和Backend通过消息系统协调API接口
3. DevOps监控集成测试结果
4. 所有人使用群组进行项目讨论

**真实数据**: 一个4人AI团队在10分钟内完成了原本需要9小时的重构工作（2150行代码）。

</details>

<details>
<summary><b>场景2: 研究协作</b></summary>

**研究小组**:
- Researcher A (数据收集)
- Researcher B (数据分析)
- Researcher C (论文撰写)

**工作流程**:
1. 创建研究项目群组
2. 使用任务管理跟踪研究里程碑
3. 通过代码片段分享分析脚本
4. 定期使用群组消息总结进展

</details>

更多示例请参考：[EXAMPLES_CN.md](docs/EXAMPLES_CN.md)

---

## 🏗️ 架构

### 模块化结构

```
mcp_ai_chat/
├── server_modular.py        # 主入口 (新版)
├── config.py                 # 配置管理
├── tools/                    # 28个工具定义
│   ├── message_tools.py      # 消息工具
│   ├── task_tools.py         # 任务工具
│   ├── group_tools.py        # 群组工具
│   └── system_tools.py       # 系统工具
├── handlers/                 # 4个处理器模块
│   ├── message_handler.py    # 消息处理
│   ├── task_handler.py       # 任务处理
│   ├── group_handler.py      # 群组处理
│   └── system_handler.py     # 系统处理
├── core/                     # 核心功能
│   ├── session.py            # 会话管理
│   └── storage.py            # 数据存储
└── utils/                    # 工具函数
    ├── format_utils.py       # 格式化工具
    └── time_utils.py         # 时间工具
```

详细架构说明请参考：[ARCHITECTURE_CN.md](docs/ARCHITECTURE_CN.md)

---

## 🤝 贡献

我们欢迎所有形式的贡献！

### 贡献方式
1. 🐛 报告Bug - 使用[Bug报告模板](.github/ISSUE_TEMPLATE/bug_report.md)
2. 💡 功能建议 - 使用[功能请求模板](.github/ISSUE_TEMPLATE/feature_request.md)
3. 📖 改进文档 - 帮助我们完善文档
4. 🔧 提交代码 - Fork仓库并提交PR

### 开发设置
```bash
# 克隆仓库
git clone https://github.com/KALUSO-nolodjska/ai-team-mcp.git
cd ai-team-mcp

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 检查代码风格
flake8 mcp_ai_chat
```

详细指南请参考：[CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

本项目采用MIT许可证 - 详情请参阅[LICENSE](LICENSE)文件。

---

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

特别感谢：
- [Model Context Protocol](https://modelcontextprotocol.io) - 提供了强大的AI协作框架
- Anthropic团队 - Claude的开发者
- Cursor & Windsurf团队 - 提供了优秀的AI IDE

---

## 📞 支持

- 📧 **Email**: lhq2328616309@outlook.com
- 🐛 **Bug报告**: [GitHub Issues](https://github.com/KALUSO-nolodjska/ai-team-mcp/issues)
- 💬 **讨论**: [GitHub Discussions](https://github.com/KALUSO-nolodjska/ai-team-mcp/discussions)
- 📖 **文档**: [完整文档](docs/)

---

## ⭐ Star历史

如果这个项目对你有帮助，请给我们一个Star！⭐

[![Star History Chart](https://api.star-history.com/svg?repos=KALUSO-nolodjska/ai-team-mcp&type=Date)](https://star-history.com/#KALUSO-nolodjska/ai-team-mcp&Date)

---

<div align="center">

**[开始使用](docs/INSTALLATION_CN.md)** | **[查看示例](docs/EXAMPLES_CN.md)** | **[API文档](docs/API_REFERENCE_CN.md)**

用❤️打造 by [KALUSO-nolodjska](https://github.com/KALUSO-nolodjska)

</div>


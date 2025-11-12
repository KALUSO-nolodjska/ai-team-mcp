# GitHub Actions CI/CD 配置

## 📋 概述

本项目使用GitHub Actions进行持续集成和持续部署（CI/CD）。

## 🚀 工作流

### 测试工作流 (`test.yml`)

**触发条件**:
- Push到 `main`, `master`, `dev` 分支
- Pull Request到 `main`, `master`, `dev` 分支

**测试矩阵**:
- Python 3.10
- Python 3.11
- Python 3.12

**测试步骤**:
1. ✅ 检出代码
2. ✅ 设置Python环境
3. ✅ 安装依赖 (`mcp_ai_chat/requirements.txt`)
4. ✅ 运行pytest测试
5. ✅ 生成覆盖率报告
6. ✅ 上传测试结果和覆盖率报告

**代码质量检查**:
- Flake8 (语法错误检查)
- Black (代码格式检查)

## 📦 依赖管理

### 主项目依赖
- 位置: `mcp_ai_chat/requirements.txt`
- 包含: 核心依赖 + 测试依赖 + 代码质量工具

### 安装依赖
```bash
pip install -r mcp_ai_chat/requirements.txt
```

## 🧪 本地测试

### 运行测试
```bash
cd mcp_ai_chat
pytest tests/ -v
```

### 运行测试并生成覆盖率报告
```bash
cd mcp_ai_chat
pytest tests/ -v --cov=. --cov-report=html
```

### 代码质量检查
```bash
cd mcp_ai_chat

# Flake8语法检查
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Black格式检查
black --check .
```

## 📊 测试报告

测试完成后，以下artifacts将被上传到GitHub Actions:
- `test-results-{python-version}`: 包含覆盖率报告（XML和HTML格式）
- 保留时间: 30天

## 🔧 配置文件

- `.github/workflows/test.yml`: GitHub Actions工作流配置
- `mcp_ai_chat/pytest.ini`: Pytest配置
- `mcp_ai_chat/requirements.txt`: Python依赖列表

## ⚠️ 注意事项

1. **测试失败不会阻止工作流完成** (`continue-on-error: true`)，但会在日志中显示错误
2. **覆盖率报告**仅在Python 3.11版本上传到Codecov
3. **代码格式检查**仅作警告，不会导致工作流失败

## 📝 维护

**更新依赖**:
```bash
pip install --upgrade -r mcp_ai_chat/requirements.txt
pip freeze > mcp_ai_chat/requirements-lock.txt
```

**添加新测试**:
在 `mcp_ai_chat/tests/` 目录下创建 `test_*.py` 文件。

---

**最后更新**: 2025-11-11
**维护者**: 员工D (测试/运维工程师)



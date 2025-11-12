# MCP工具GitHub Actions CI/CD修复指南

**问题来源**: [GitHub Actions Run #19284998821](https://github.com/KALUSO-nolodjska/ai-team-mcp/actions/runs/19284998821)  
**创建日期**: 2025-11-12  
**状态**: 🔴 需要修复

---

## 🔴 当前问题分析

根据GitHub Actions失败日志，主要存在以下问题：

### 1. **找不到 requirements.txt**
```
No file in /home/runner/work/ai-team-mcp/ai-team-mcp matched to 
[**/requirements.txt or **/pyproject.toml]
```

**原因**: GitHub Actions在根目录查找requirements.txt，但MCP项目的requirements.txt在`mcp_ai_chat/`子目录中。

### 2. **找不到测试报告文件**
```
Could not find any files for junit-backend.xml
Could not find any files for junit-frontend.xml
```

**原因**: pytest没有生成JUnit格式的测试报告。

### 3. **使用了已弃用的actions版本**
```
This request has been automatically failed because it uses a deprecated version of 
`actions/download-artifact: v3`
```

**原因**: actions/download-artifact@v3已经弃用，需要升级到v4。

---

## ✅ 解决方案

### 方案1：创建专门的MCP测试workflow（推荐）

在`.github/workflows/`目录下创建新文件`mcp-test.yml`：

```yaml
name: MCP Tool Tests

on:
  push:
    branches: [ main, master, dev ]
    paths:
      - 'mcp_ai_chat/**'
      - '.github/workflows/mcp-test.yml'
  pull_request:
    branches: [ main, master, dev ]
    paths:
      - 'mcp_ai_chat/**'
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * *'  # 每天凌晨3点运行

jobs:
  test-mcp:
    name: Test MCP Tool
    runs-on: ubuntu-latest
    
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
        cache-dependency-path: 'mcp_ai_chat/requirements.txt'
    
    - name: Install dependencies
      working-directory: mcp_ai_chat
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest-junit  # 用于生成JUnit报告
    
    - name: Run tests with pytest
      working-directory: mcp_ai_chat
      run: |
        pytest tests/ -v \
          --cov=. \
          --cov-report=xml \
          --cov-report=html \
          --cov-report=term \
          --junitxml=junit-report.xml
    
    - name: Upload coverage reports
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: coverage-reports-py${{ matrix.python-version }}
        path: |
          mcp_ai_chat/coverage.xml
          mcp_ai_chat/htmlcov/
        retention-days: 30
    
    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results-py${{ matrix.python-version }}
        path: mcp_ai_chat/junit-report.xml
        retention-days: 7

  lint-mcp:
    name: MCP Code Quality
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
        cache-dependency-path: 'mcp_ai_chat/requirements.txt'
    
    - name: Install dependencies
      working-directory: mcp_ai_chat
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install flake8 black mypy
    
    - name: Run Flake8
      working-directory: mcp_ai_chat
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      continue-on-error: true
    
    - name: Run Black (format check)
      working-directory: mcp_ai_chat
      run: black --check --diff .
      continue-on-error: true
    
    - name: Run MyPy (type check)
      working-directory: mcp_ai_chat
      run: mypy . --ignore-missing-imports
      continue-on-error: true
```

### 方案2：修复现有的workflow

如果远程仓库中有schedule触发的workflow，需要更新它：

1. **删除远程的旧workflow文件**
2. **推送本地的新workflow文件**

---

## 📦 需要的文件结构

确保你的项目结构如下：

```
ai-team-mcp/
├── .github/
│   └── workflows/
│       ├── mcp-test.yml        # MCP工具测试（新建）
│       ├── ci.yml              # 主项目CI（保留）
│       └── test.yml            # 主项目测试（保留）
├── mcp_ai_chat/
│   ├── requirements.txt        # ✅ 已存在
│   ├── pytest.ini             # ✅ 已存在
│   ├── tests/
│   │   ├── __init__.py        # ✅ 已存在
│   │   └── test_basic.py      # ✅ 已存在
│   ├── tools/                 # MCP工具代码
│   ├── handlers/              # 处理器
│   ├── core/                  # 核心功能
│   └── utils/                 # 工具函数
└── ...
```

---

## 🔧 执行步骤

### Step 1: 创建新的MCP workflow文件

```bash
# 在本地创建文件
cd D:\developItems
# 创建 .github/workflows/mcp-test.yml 文件
# 复制上面"方案1"中的内容
```

### Step 2: 安装pytest-junit（如果需要JUnit报告）

在`mcp_ai_chat/requirements.txt`中添加：

```txt
# Testing dependencies with JUnit support
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0
pytest-junit>=1.0.0  # 添加这一行
```

### Step 3: 提交并推送

```bash
git add .github/workflows/mcp-test.yml
git add mcp_ai_chat/requirements.txt  # 如果修改了
git commit -m "fix: 修复MCP工具GitHub Actions CI/CD配置

- 创建专门的MCP测试workflow
- 修复requirements.txt路径问题
- 升级actions版本到v4
- 添加JUnit报告生成支持"

git push origin master
```

### Step 4: 删除远程的旧workflow（如果存在）

如果远程有旧的schedule workflow，需要在GitHub网页上删除：

1. 进入 https://github.com/KALUSO-nolodjska/ai-team-mcp/actions
2. 找到失败的"Test Pipeline" workflow
3. 点击右上角的"..." → "Delete workflow"
4. 或者直接删除`.github/workflows/`中对应的旧文件

---

## 🎯 预期结果

修复后，你应该看到：

✅ **所有Python版本测试通过** (3.10, 3.11, 3.12)  
✅ **生成测试覆盖率报告**  
✅ **生成JUnit测试报告**  
✅ **代码质量检查通过**  
✅ **使用最新的actions版本**

---

## 📚 参考资源

- [GitHub Actions文档](https://docs.github.com/actions)
- [actions/upload-artifact v4迁移指南](https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/)
- [pytest JUnit XML格式](https://docs.pytest.org/en/stable/how-to/output.html#creating-junitxml-format-files)
- [MCP官方文档](https://spec.modelcontextprotocol.io/)

---

## 🔍 排查清单

- [ ] `mcp_ai_chat/requirements.txt` 文件存在且包含所有依赖
- [ ] `mcp_ai_chat/tests/` 目录存在且包含测试文件
- [ ] `mcp_ai_chat/pytest.ini` 配置正确
- [ ] `.github/workflows/mcp-test.yml` 使用正确的working-directory
- [ ] 所有actions使用v4或v5版本
- [ ] pytest配置包含JUnit报告生成
- [ ] 远程仓库中没有冲突的旧workflow文件

---

## 💡 额外建议

### 1. 添加状态徽章到README

在`mcp_ai_chat/README.md`中添加：

```markdown
[![MCP Tests](https://github.com/KALUSO-nolodjska/ai-team-mcp/actions/workflows/mcp-test.yml/badge.svg)](https://github.com/KALUSO-nolodjska/ai-team-mcp/actions/workflows/mcp-test.yml)
```

### 2. 配置自动化测试触发

只在MCP相关文件修改时运行测试：

```yaml
paths:
  - 'mcp_ai_chat/**'
  - '.github/workflows/mcp-test.yml'
```

### 3. 添加测试覆盖率报告

可以集成Codecov或Coveralls：

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./mcp_ai_chat/coverage.xml
    flags: mcp
    name: mcp-coverage
```

---

**最后更新**: 2025-11-12  
**负责人**: 产品经理


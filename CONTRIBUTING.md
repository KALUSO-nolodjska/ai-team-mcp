# Contributing to AI Team MCP

First off, thank you for considering contributing to AI Team MCP! 🎉

It's people like you that make AI Team MCP such a great tool for the community.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Examples of unacceptable behavior:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of MCP (Model Context Protocol)
- Familiarity with async Python programming

### First Time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/KALUSO-nolodjska/ai-team-mcp.git
   cd ai-team-mcp
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/KALUSO-nolodjska/ai-team-mcp.git
   ```
4. **Install dependencies**:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check the existing issues to avoid duplicates
- Collect information about the bug:
  - Stack trace
  - OS, Python version, MCP client version
  - Steps to reproduce
  - Expected vs actual behavior

**Submit a bug report:**
1. Use the bug report template
2. Include a clear and descriptive title
3. Provide detailed steps to reproduce
4. Include code samples if applicable
5. Attach screenshots if relevant

### 💡 Suggesting Features

**Before submitting a feature request:**
- Check if it's already been suggested
- Consider if it fits the project's scope and goals
- Think about how it would benefit most users

**Submit a feature request:**
1. Use the feature request template
2. Clearly describe the feature and its benefits
3. Provide use cases and examples
4. Discuss potential implementation approaches

### 🔧 Contributing Code

**Good first issues:**
- Look for issues labeled `good first issue`
- Documentation improvements
- Adding tests
- Fixing typos or formatting

**Before you start coding:**
1. Comment on the issue to claim it
2. Discuss your approach if it's complex
3. Make sure tests pass locally

---

## 🛠️ Development Setup

### Project Structure

```
ai-team-mcp/
├── mcp_ai_chat/           # Main package
│   ├── server_modular.py  # Entry point
│   ├── tools/             # Tool definitions
│   ├── handlers/          # Request handlers
│   ├── core/              # Core functionality
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── docs/                  # Documentation
└── examples/              # Usage examples
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_ai_chat

# Run specific test file
pytest tests/test_message_tools.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black mcp_ai_chat/

# Check linting
flake8 mcp_ai_chat/

# Type checking
mypy mcp_ai_chat/
```

### Running the Server Locally

```bash
# Start the server
python -m mcp_ai_chat.server_modular

# Or use the development script
./scripts/dev_server.sh
```

---

## 📝 Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write clear, self-documenting code
   - Add tests for new features
   - Update documentation
   - Follow style guidelines

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
   
   Use [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Formatting, no code change
   - `refactor:` - Code restructuring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting the PR

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template:
   - Clear title describing the change
   - Link to related issues
   - Description of what changed and why
   - Screenshots for UI changes
   - Testing steps

### Review Process

- Maintainers will review your PR within 3-5 days
- Address any requested changes
- Keep the PR focused on a single concern
- Be patient and respectful during reviews

### After Merge

- Delete your feature branch
- Update your local main branch:
  ```bash
  git checkout main
  git pull upstream main
  git push origin main
  ```

---

## 🎨 Style Guidelines

### Python Code Style

**Follow PEP 8 with these specifics:**

```python
# Good: Clear function names and type hints
async def send_message_to_agent(
    sender: str,
    recipient: str,
    content: str,
    timestamp: Optional[datetime] = None
) -> Message:
    """
    Send a message from one agent to another.
    
    Args:
        sender: The agent sending the message
        recipient: The agent receiving the message
        content: The message content
        timestamp: Optional message timestamp
        
    Returns:
        The created Message object
        
    Raises:
        ValueError: If sender or recipient is invalid
    """
    pass

# Bad: Unclear names, no types, no docstring
async def sm(s, r, c, t=None):
    pass
```

**Key principles:**
- Use type hints for all function parameters and returns
- Write clear docstrings for all public functions
- Maximum line length: 100 characters
- Use f-strings for string formatting
- Prefer async/await over callbacks

### Documentation Style

**Write clear, concise documentation:**

```markdown
# Good: Clear, scannable, with examples
## Creating a Task

To create a task, use the `create_task` tool:

```python
result = mcp_ai-chat-group_create_task({
    "title": "Implement login feature",
    "priority": "P1"
})
```

# Bad: Vague, no examples
## Tasks
You can create tasks using the tool.
```

### Commit Message Style

```bash
# Good: Clear, specific, follows convention
feat(tasks): add priority filtering to get_tasks
fix(messages): prevent duplicate message IDs
docs(readme): update installation instructions

# Bad: Vague, no context
update code
fix bug
change stuff
```

---

## 🌟 Recognition

Contributors who make significant contributions will be:
- Added to the CONTRIBUTORS.md file
- Mentioned in release notes
- Given credit in relevant documentation

---

## 📞 Getting Help

**Stuck? Have questions?**

- 💬 [GitHub Discussions](https://github.com/KALUSO-nolodjska/ai-team-mcp/discussions)
- 📧 Email the maintainers
- 💡 Check existing issues and PRs
- 📚 Read the documentation

---

## 📚 Additional Resources

- [Model Context Protocol Docs](https://modelcontextprotocol.io)
- [Python AsyncIO Guide](https://docs.python.org/3/library/asyncio.html)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

---

## 🎉 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! ❤️

---

**Questions about contributing?** Open an issue with the `question` label and we'll help you out!



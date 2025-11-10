# 💡 Usage Examples

Real-world examples of using AI Team MCP in various scenarios.

---

## 📋 Table of Contents

- [Example 1: AI Development Team](#example-1-ai-development-team)
- [Example 2: Research Collaboration](#example-2-research-collaboration)
- [Example 3: Customer Support](#example-3-customer-support)
- [Example 4: Content Creation Workflow](#example-4-content-creation-workflow)
- [Example 5: Code Review Process](#example-5-code-review-process)

---

## Example 1: AI Development Team

A team of 5 AI agents building a web application.

### Team Structure

```python
# Manager
mcp_ai-chat-group_register_agent({
  "agent_name": "manager",
  "role": "Product Manager",
  "description": "Plans features, assigns tasks, reviews progress"
})

# Frontend Developer
mcp_ai-chat-group_register_agent({
  "agent_name": "frontend_dev",
  "role": "Frontend Developer",
  "description": "React, TypeScript, UI/UX"
})

# Backend Developer
mcp_ai-chat-group_register_agent({
  "agent_name": "backend_dev",
  "role": "Backend Developer",
  "description": "Python, FastAPI, PostgreSQL"
})

# Full-stack Developer
mcp_ai-chat-group_register_agent({
  "agent_name": "fullstack_dev",
  "role": "Full-stack Developer",
  "description": "Integration, API docs, E2E testing"
})

# DevOps Engineer
mcp_ai-chat-group_register_agent({
  "agent_name": "devops",
  "role": "DevOps Engineer",
  "description": "CI/CD, testing, deployment"
})
```

### Sprint Planning

```python
# Manager creates project group
mcp_ai-chat-group_create_group({
  "name": "Sprint 15 - User Authentication",
  "members": ["manager", "frontend_dev", "backend_dev", "fullstack_dev", "devops"],
  "description": "Implementing JWT-based auth with refresh tokens"
})

# Manager creates tasks
tasks = [
  {
    "title": "Design auth API endpoints",
    "assignee": "backend_dev",
    "priority": "P0",
    "due_date": "2025-11-12T17:00:00"
  },
  {
    "title": "Implement login UI",
    "assignee": "frontend_dev",
    "priority": "P1",
    "due_date": "2025-11-13T17:00:00"
  },
  {
    "title": "Write E2E auth tests",
    "assignee": "fullstack_dev",
    "priority": "P1",
    "due_date": "2025-11-14T17:00:00"
  },
  {
    "title": "Setup auth service deployment",
    "assignee": "devops",
    "priority": "P1",
    "due_date": "2025-11-15T17:00:00"
  }
]

for task in tasks:
  task_id = mcp_ai-chat-group_create_task({
    "title": task["title"],
    "description": f"Part of Sprint 15 - User Authentication",
    "priority": task["priority"],
    "due_date": task["due_date"]
  })
  
  mcp_ai-chat-group_assign_task({
    "task_id": task_id,
    "assignee": task["assignee"]
  })

# Manager sends kickoff message
mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_20251110_001",
  "message": """🚀 Sprint 15 Kickoff!

Goal: Implement JWT-based authentication
Timeline: Nov 12-15
Daily standups: 10 AM in this group

Let's build something great! 💪""",
  "importance": "high",
  "topic": "Sprint Planning"
})
```

### Daily Standup

```python
# Each agent reports progress
mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_20251110_001",
  "message": """📊 Standup Update - backend_dev

✅ Yesterday: 
- Designed auth API endpoints
- Implemented JWT token generation

🔨 Today:
- Implement refresh token logic
- Add password hashing

⚠️ Blockers: None""",
  "topic": "Daily Standup"
})
```

### Code Review Request

```python
# Backend dev requests review
mcp_ai-chat-group_request_review({
  "recipients": "fullstack_dev",
  "file_path": "backend/api/auth.py",
  "description": "Please review JWT implementation, especially token expiration logic"
})

# Fullstack dev responds
mcp_ai-chat-group_send_message({
  "recipients": "backend_dev",
  "message": """Reviewed auth.py. Looks good overall! 

Suggestions:
1. Add rate limiting for login endpoint
2. Consider shorter access token TTL (15min → 5min)
3. Log failed login attempts

Otherwise LGTM! ✅"""
})
```

### Task Completion

```python
# Backend dev completes task
mcp_ai-chat-group_update_task_status({
  "task_id": "TASK_20251112_001",
  "status": "已完成",
  "progress_note": "Auth API complete with JWT + refresh tokens"
})

mcp_ai-chat-group_notify_completion({
  "recipients": "manager&frontend_dev",
  "task_title": "Design auth API endpoints",
  "summary": """Auth API completed:
- POST /api/auth/login - Issue JWT tokens
- POST /api/auth/refresh - Refresh access token
- POST /api/auth/logout - Revoke refresh token
- GET /api/auth/me - Get current user

Docs: http://localhost:8094/docs""",
  "related_files": ["backend/api/auth.py", "docs/AUTH_API.md"]
})
```

### Sprint Review

```python
# Manager summarizes sprint
summary = mcp_ai-chat-group_summarize_group_messages({
  "group_id": "GRP_20251110_001",
  "time_range": "last_7_days",
  "max_length": 500
})

mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_20251110_001",
  "message": f"""🎉 Sprint 15 Complete!

{summary}

Great work team! All tasks completed on time. 
Next: Sprint 16 - User Profile Management""",
  "importance": "high",
  "topic": "Sprint Review"
})

# Archive the group
mcp_ai-chat-group_archive_group({
  "group_id": "GRP_20251110_001",
  "reason": "Sprint completed successfully"
})
```

---

## Example 2: Research Collaboration

Multiple AI agents collaborating on a research paper.

### Setup

```python
# Create research group
mcp_ai-chat-group_create_group({
  "name": "Paper: AI Collaboration Patterns",
  "members": ["researcher_1", "researcher_2", "researcher_3", "editor"],
  "description": "Research paper on multi-AI collaboration"
})

# Create research tasks
mcp_ai-chat-group_create_task({
  "title": "Literature review - AI collaboration",
  "description": "Review existing papers on AI-to-AI collaboration patterns",
  "priority": "P0",
  "due_date": "2025-11-20T23:59:59"
})
```

### Sharing Findings

```python
# Researcher shares findings
mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_RESEARCH_001",
  "message": """📚 Literature Review Update

Found 23 relevant papers on AI collaboration.

Key themes:
1. Message passing architectures (12 papers)
2. Task decomposition strategies (8 papers)
3. Consensus mechanisms (7 papers)

Notable finding: Most frameworks lack production-ready implementations.

Full notes: research/lit_review.md""",
  "file_path": "research/lit_review.md",
  "topic": "Literature Review",
  "mentions": ["editor"]
})

# Pin important finding
mcp_ai-chat-group_pin_message({
  "group_id": "GRP_RESEARCH_001",
  "message_id": "MSG_001"
})
```

### Hypothesis Discussion

```python
# Researcher proposes hypothesis
mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_RESEARCH_001",
  "message": """💡 Hypothesis for Discussion

H1: Modular AI collaboration frameworks achieve 2-3x higher 
    code maintainability compared to monolithic approaches.

Proposed methodology:
1. Compare LOC per feature
2. Measure onboarding time for new agents
3. Track bug resolution time

Thoughts? @researcher_2 @researcher_3""",
  "mentions": ["researcher_2", "researcher_3"],
  "importance": "high",
  "topic": "Hypothesis"
})

# Others respond
mcp_ai-chat-group_send_group_message({
  "group_id": "GRP_RESEARCH_001",
  "message": """Strong hypothesis! Suggested additions:

4. Measure test coverage improvement
5. Track feature development velocity

I can handle metrics 1-3 if you want. @researcher_1""",
  "reply_to": "MSG_HYPOTHESIS",
  "mentions": ["researcher_1"],
  "topic": "Hypothesis"
})
```

---

## Example 3: Customer Support

AI agents handling customer support tickets.

### Ticket Routing

```python
# Support router receives ticket
ticket = {
  "id": "TKT_12345",
  "type": "technical",
  "priority": "high",
  "description": "API authentication failing"
}

# Create task for specialist
mcp_ai-chat-group_create_task({
  "title": f"Ticket {ticket['id']}: {ticket['description']}",
  "description": f"Customer Issue: {ticket['description']}",
  "priority": "P0"
})

# Assign to technical specialist
mcp_ai-chat-group_assign_task({
  "task_id": "TASK_TKT_12345",
  "assignee": "tech_support"
})

# Notify specialist
mcp_ai-chat-group_send_message({
  "recipients": "tech_support",
  "message": f"🚨 High priority ticket assigned: {ticket['id']}"
})
```

### Escalation

```python
# Specialist needs help
mcp_ai-chat-group_request_help({
  "recipients": "senior_support&dev_team",
  "topic": "API Auth Issue",
  "description": """Customer experiencing auth failures.

Symptoms:
- JWT tokens being rejected
- Error: "Invalid signature"

Tried:
- Verified API keys
- Checked token expiration
- Reviewed recent deployments

Need expertise on JWT validation logic.""",
  "urgency": "紧急"
})
```

### Resolution

```python
# Dev identifies issue
mcp_ai-chat-group_send_message({
  "recipients": "tech_support",
  "message": """Found the issue! Recent deployment changed JWT secret.

Fix: Regenerate customer API keys.

Instructions: docs/API_KEY_REGEN.md"""
})

# Tech support resolves
mcp_ai-chat-group_update_task_status({
  "task_id": "TASK_TKT_12345",
  "status": "已完成",
  "progress_note": "Issue resolved - regenerated API keys"
})

mcp_ai-chat-group_notify_completion({
  "recipients": "support_manager",
  "task_title": "Ticket TKT_12345",
  "summary": "Resolved auth issue by regenerating API keys after JWT secret rotation"
})
```

---

## Example 4: Content Creation Workflow

AI agents collaborating on content creation.

### Initial Draft

```python
# Writer creates draft
mcp_ai-chat-group_create_task({
  "title": "Blog post: Getting Started with AI Teams",
  "description": "Beginner-friendly guide to multi-AI collaboration",
  "priority": "P1",
  "due_date": "2025-11-18T17:00:00"
})

# Writer shares draft
mcp_ai-chat-group_share_code_snippet({
  "recipients": "editor&reviewer",
  "file_path": "content/blog/ai-teams-guide.md",
  "description": "First draft ready for review"
})
```

### Review Process

```python
# Editor provides feedback
mcp_ai-chat-group_request_review({
  "recipients": "writer",
  "file_path": "content/blog/ai-teams-guide.md",
  "description": """Good start! Feedback:

✅ Strengths:
- Clear structure
- Good examples
- Engaging tone

📝 Improvements needed:
- Add more code examples (sections 2-3)
- Simplify technical jargon
- Add troubleshooting section

Let's iterate! """
})
```

### Publishing

```python
# After revisions
mcp_ai-chat-group_notify_completion({
  "recipients": "content_manager",
  "task_title": "Blog post: Getting Started with AI Teams",
  "summary": """Blog post complete and ready to publish!

Word count: 2,500
Reading time: ~10 minutes
SEO score: 92/100
Images: 5 diagrams

Preview: http://preview.blog/ai-teams-guide""",
  "related_files": ["content/blog/ai-teams-guide.md"]
})
```

---

## Example 5: Code Review Process

Structured code review between AI agents.

### Review Request with Context

```python
# Developer requests review
mcp_ai-chat-group_send_message({
  "recipients": "code_reviewer",
  "message": """🔍 Code Review Needed

PR: #234 - Implement caching layer
Files: backend/cache/redis_cache.py, tests/test_cache.py

Context:
- Adds Redis-based caching
- Reduces API response time by 60%
- Includes TTL management

Focus areas:
1. Error handling
2. Connection pooling
3. Test coverage

Thanks! 🙏"""
})

mcp_ai-chat-group_request_review({
  "recipients": "code_reviewer",
  "file_path": "backend/cache/redis_cache.py",
  "description": "Please review caching implementation"
})
```

### Detailed Review

```python
# Reviewer shares specific feedback
mcp_ai-chat-group_share_code_snippet({
  "recipients": "developer",
  "file_path": "backend/cache/redis_cache.py",
  "line_start": 45,
  "line_end": 60,
  "description": """⚠️ Issue: Connection not properly closed in error case

Suggested fix:
```python
async def get(self, key: str):
    conn = None
    try:
        conn = await self.pool.acquire()
        return await conn.get(key)
    except RedisError as e:
        logger.error(f"Cache get error: {e}")
        return None
    finally:
        if conn:
            await self.pool.release(conn)
```"""
})
```

### Approval

```python
# After fixes
mcp_ai-chat-group_send_message({
  "recipients": "developer",
  "message": """✅ Code Review: APPROVED

All issues addressed. Code looks production-ready!

Changes verified:
- ✅ Proper connection handling
- ✅ Comprehensive error handling
- ✅ Test coverage at 95%

Ready to merge! 🚀"""
})
```

---

## 🎯 Best Practices

### 1. Clear Communication

```python
# Good: Specific and actionable
mcp_ai-chat-group_send_message({
  "recipients": "agent_b",
  "message": "API endpoint /api/users needs rate limiting. Max 100 req/min per IP."
})

# Bad: Vague
mcp_ai-chat-group_send_message({
  "recipients": "agent_b",
  "message": "Fix the API thing"
})
```

### 2. Use Groups for Projects

```python
# Good: Organize by project
mcp_ai-chat-group_create_group({
  "name": "Sprint 15 - Authentication",
  "members": [...]
})

# Bad: Everything in direct messages
# (gets messy with 5+ agents)
```

### 3. Leverage Standby Mode

```python
# Agent stays responsive
while True:
    mcp_ai-chat-group_standby({
        "status_message": "Ready for work",
        "check_tasks": True,
        "check_messages": True
    })
    # Process new work
```

### 4. Track Progress with Tasks

```python
# Update status frequently
mcp_ai-chat-group_update_task_status({
  "task_id": "...",
  "status": "进行中",
  "progress_note": "Backend 70% done, frontend next"
})
```

### 5. Use Mentions in Groups

```python
# Get attention when needed
mcp_ai-chat-group_send_group_message({
  "group_id": "...",
  "message": "API design ready for review!",
  "mentions": ["tech_lead", "architect"]
})
```

---

## 📚 More Resources

- [API Reference](API_REFERENCE.md) - Complete tool documentation
- [Quick Start](../README.md#quick-start) - Get started in 5 minutes
- [Architecture](ARCHITECTURE.md) - How it works under the hood

---

**Last Updated**: 2025-11-10  
**Version**: 5.0



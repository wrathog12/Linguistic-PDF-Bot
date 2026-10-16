# Contributing to Linguistic PDF Bot

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/your-username/Linguistic-PDF-Bot.git
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feat/your-feature-name
   ```

## 📋 Development Setup

### Backend
```bash
cd agentic_chatbot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Vector Database
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## 🔀 Branch Naming Convention

| Type | Pattern | Example |
|---|---|---|
| Feature | `feat/description` | `feat/multi-language-support` |
| Bug Fix | `fix/description` | `fix/websocket-reconnection` |
| Docs | `docs/description` | `docs/api-reference` |
| Refactor | `refactor/description` | `refactor/rag-pipeline` |

## 📝 Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

<optional body with details>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `perf`

**Examples:**
```
feat: add multi-PDF upload support
fix: resolve WebSocket timeout on large documents
docs: update API endpoint documentation
refactor: extract PDF parsing into standalone module
```

## 🧪 Before Submitting

- [ ] Test your changes locally (both backend and frontend)
- [ ] Ensure no API keys or secrets are committed
- [ ] Add docstrings to new Python functions
- [ ] Update README.md if adding new features or changing setup steps
- [ ] Keep commits atomic and well-described

## 🐛 Reporting Issues

When reporting bugs, please include:
- Steps to reproduce the issue
- Expected vs. actual behavior
- Browser/OS information
- Relevant error logs or screenshots

## 💬 Questions?

Feel free to open an issue for discussion or reach out to the maintainers.

---

Thank you for helping improve Linguistic PDF Bot! 🎉

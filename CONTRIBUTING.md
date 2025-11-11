# Contributing to Sarathi

Thank you for your interest in contributing to Sarathi! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sarathi.git
   cd sarathi
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/sarathi.git
   ```

### Development Setup

Follow the instructions in the main README.md to set up your development environment.

## 🔄 Development Workflow

### 1. Create a Branch

Always create a new branch for your work:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding tests

### 2. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 3. Commit Your Changes

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add voice recognition feature"
git commit -m "fix: resolve authentication token issue"
git commit -m "docs: update API documentation"
```

Commit types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Code Style Guidelines

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 127 characters
- Use Black for formatting:
  ```bash
  black app/
  ```
- Run linting:
  ```bash
  flake8 app/
  ```

### TypeScript/React Native (Frontend)

- Use TypeScript for all new code
- Follow React best practices
- Use functional components and hooks
- Use Tailwind CSS classes for styling
- Run linting:
  ```bash
  npm run lint
  ```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📖 Documentation

- Update README.md if you add new features
- Add docstrings to all Python functions and classes
- Add JSDoc comments for complex TypeScript functions
- Update API documentation if you modify endpoints

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python/Node version, etc.)
- Screenshots if applicable

## 💡 Suggesting Features

We welcome feature suggestions! Please:
- Check if the feature has already been requested
- Provide a clear description of the feature
- Explain the use case and benefits
- Consider providing a basic implementation proposal

## ✅ Pull Request Checklist

Before submitting a PR, ensure:
- [ ] Code follows the style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventional commits
- [ ] No merge conflicts with main branch
- [ ] PR description clearly explains the changes

## 📋 Code Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Special thanks in documentation

## 📞 Getting Help

If you need help:
- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Reach out to maintainers

Thank you for contributing to Sarathi! 🚗💨

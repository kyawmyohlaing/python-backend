# Contributing to FastAPI Backend Template

Thank you for your interest in contributing to the FastAPI Backend Template! We welcome contributions from the community to help improve this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Style Guides](#style-guides)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Additional Resources](#additional-resources)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title** for the issue
- **Describe the exact steps** which reproduce the problem
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** after following the steps
- **Explain which behavior you expected** to see instead and why
- **Include screenshots** if possible
- **Include the version of the project** you are using
- **Include your environment details** (OS, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title** for the issue
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the steps
- **Describe the current behavior** and **explain which behavior you expected** to see instead
- **Explain why this enhancement** would be useful to most users

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these `beginner` and `help-wanted` issues:

- **Beginner issues** - issues which should only require a few lines of code, and a test or two
- **Help wanted issues** - issues which should be a bit more involved than `beginner` issues

### Code Contribution Process

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Add or update tests as necessary
6. Ensure all tests pass
7. Add or update documentation as necessary
8. Commit your changes
9. Push to your fork
10. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.9+ (for local development without Docker)

### Getting Started

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/fastapi-backend-template.git
   cd fastapi-backend-template
   ```

2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

4. Start the development environment:
   ```bash
   make dev
   ```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/test_users.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Code Quality

Before submitting a pull request, ensure your code passes all quality checks:

```bash
# Run tests
make test

# Check code formatting (if using black)
black --check .

# Check imports (if using isort)
isort --check-only .

# Check for code issues (if using flake8)
flake8 .
```

## 🎨 Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - ✨ `:sparkles:` when introducing new features
  - 📝 `:memo:` when writing docs
  - 🚀 `:rocket:` when deploying
  - 💄 `:lipstick:` when updating the UI and style files
  - 🎉 `:tada:` when initial commit
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies
  - 👷 `:construction_worker:` when adding CI build system
  - ♻️ `:recycle:` when refactoring code
  - 🔧 `:wrench:` when adding or updating configuration files
  - 📈 `:chart_with_upwards_trend:` when adding analytics or tracking code

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused
- Use meaningful variable and function names
- Avoid magic numbers and strings
- Use constants for configuration values

### Documentation Style

- Use Markdown for documentation
- Follow a consistent structure
- Use clear and concise language
- Include examples where appropriate
- Update documentation when making code changes

## 📥 Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/)
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you

### Pull Request Requirements

- **Branch Naming**: Use descriptive names like `feature/user-authentication` or `fix/database-connection`
- **Description**: Include a clear description of the changes
- **Related Issues**: Reference any related issues
- **Tests**: Include tests for new functionality
- **Documentation**: Update documentation as needed
- **Code Review**: Be responsive to feedback during the code review process

### Code Review Process

All submissions require review. We use GitHub pull requests for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

Reviewers will check for:
- Code quality and adherence to style guides
- Proper test coverage
- Documentation updates
- Security considerations
- Performance implications
- Compatibility with existing code

## 🐛 Reporting Bugs

When reporting a bug, please include:

1. **Summary**: A brief description of the bug
2. **Steps to Reproduce**: Clear steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Docker version, Python version, etc.
6. **Screenshots**: If applicable
7. **Logs**: Relevant log output

## 💡 Suggesting Enhancements

When suggesting an enhancement, please include:

1. **Summary**: A brief description of the enhancement
2. **Problem**: What problem does this solve?
3. **Solution**: How should it be implemented?
4. **Alternatives**: Any alternative solutions you've considered
5. **Additional Context**: Any other relevant information

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Python Documentation](https://docs.python.org/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Documentation](https://git-scm.com/doc)

## 🏆 Recognition

Contributors will be recognized in:

- The CONTRIBUTORS file (if added)
- The README.md
- Release notes
- Social media announcements (for significant contributions)

Thank you for contributing to the FastAPI Backend Template!
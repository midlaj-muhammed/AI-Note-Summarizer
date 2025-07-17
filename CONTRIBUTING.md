# 🤝 Contributing to AI Notes Summarizer

Thank you for your interest in contributing to AI Notes Summarizer! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Docker (optional but recommended)
- Basic knowledge of Python, Streamlit, and AI/ML concepts

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/AI-Note-Summarizer.git
   cd AI-Note-Summarizer
   ```

## 🛠️ Development Setup

### Local Development

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Docker Development

1. **Build and run with Docker:**
   ```bash
   ./docker-dev.sh
   ```

2. **Or use Docker Compose:**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

## 🔄 Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-model-support`
- `bugfix/fix-pdf-processing-error`
- `docs/update-installation-guide`
- `refactor/improve-error-handling`

### Commit Messages

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(summarizer): add support for T5 model`
- `fix(pdf): resolve text extraction encoding issue`
- `docs(readme): update installation instructions`

## 📤 Submitting Changes

### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots if applicable
   - Test results

### Pull Request Requirements

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation updated if needed
- [ ] No breaking changes (or clearly documented)
- [ ] Self-review completed

## 🎨 Style Guidelines

### Python Code Style

- Follow PEP 8
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example:
```python
def process_pdf_file(uploaded_file: UploadedFile) -> Optional[str]:
    """
    Extract text content from uploaded PDF file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text content or None if extraction fails
    """
    # Implementation here
    pass
```

### File Organization

- Keep modules focused on single responsibilities
- Use clear directory structure
- Add `__init__.py` files for packages
- Group related functionality together

## 🧪 Testing

### Running Tests

```bash
# Basic functionality tests
python test_basic.py

# Docker tests
./docker-test.sh

# Manual testing checklist
# - PDF upload and processing
# - Text input and summarization
# - Different AI models
# - Error handling scenarios
```

### Writing Tests

- Add tests for new features
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests independent and isolated

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include type hints
- Comment complex logic
- Update README.md for new features

### User Documentation

- Update usage instructions
- Add examples for new features
- Include troubleshooting information
- Keep Docker documentation current

## 🐛 Reporting Issues

When reporting bugs:

1. Use the bug report template
2. Include environment details
3. Provide steps to reproduce
4. Add relevant logs and screenshots
5. Check for existing similar issues

## 💡 Suggesting Features

When suggesting features:

1. Use the feature request template
2. Explain the use case and motivation
3. Consider implementation complexity
4. Provide mockups or examples if helpful

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to docs
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 🎯 Areas for Contribution

### High Priority
- Bug fixes and stability improvements
- Performance optimizations
- Better error handling
- Documentation improvements

### Medium Priority
- New AI model integrations
- UI/UX enhancements
- Additional file format support
- Internationalization

### Low Priority
- Code refactoring
- Additional testing
- Development tooling
- CI/CD improvements

## 📞 Getting Help

- 💬 [GitHub Discussions](https://github.com/midlaj-muhammed/AI-Note-Summarizer/discussions)
- 🐛 [Issues](https://github.com/midlaj-muhammed/AI-Note-Summarizer/issues)
- 📧 Email: midlaj.muhammed@example.com

## 🙏 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Given credit in commit messages
- Invited to be maintainers (for significant contributions)

---

Thank you for contributing to AI Notes Summarizer! 🎉

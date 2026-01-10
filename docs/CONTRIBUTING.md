# Contributing to ZQAutoNXG

**Thank you for your interest in contributing to ZQAutoNXG!**

We welcome contributions from the community. This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Submitting Changes](#submitting-changes)
8. [License](#license)

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Docker and Docker Compose (optional but recommended)

### Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/ZQAutoNXG-V1.git
cd ZQAutoNXG-V1

# Add upstream remote
git remote add upstream https://github.com/zubinqayam/ZQAutoNXG-V1.git
```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov black ruff mypy
```

### Verify Setup

```bash
# Run tests
pytest tests/

# Start development server
uvicorn zqautonxg.app:app --reload
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/fixes

### 2. Make Changes

- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=zqautonxg --cov-report=html

# Run specific test file
pytest tests/test_api_workflows.py -v
```

### 4. Format Code

```bash
# Format with black
black zqautonxg/ tests/

# Lint with ruff
ruff check zqautonxg/ tests/

# Type check with mypy
mypy zqautonxg/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new workflow execution feature"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/fixes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- Line length: 88 characters (Black default)
- Use type hints for all function signatures
- Use async/await for I/O operations
- Use Pydantic for data validation

### Code Organization

```python
# Imports (grouped by: stdlib, third-party, local)
import os
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from zqautonxg.models import Workflow

# Constants
DEFAULT_TIMEOUT = 30

# Classes and functions
class MyClass:
    """Docstring following Google style."""
    pass

async def my_function(param: str) -> Dict[str, Any]:
    """
    Short description.
    
    Args:
        param: Description of param
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param is invalid
    """
    pass
```

### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional
from uuid import UUID

def process_workflow(
    workflow_id: UUID,
    config: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Process workflow with configuration."""
    pass
```

### Documentation

Use Google-style docstrings:

```python
def create_workflow(name: str, description: str) -> Workflow:
    """
    Create a new workflow.
    
    Args:
        name: Workflow name (required)
        description: Workflow description
        
    Returns:
        Created workflow instance
        
    Raises:
        ValueError: If name is empty
        
    Example:
        >>> workflow = create_workflow("My Workflow", "Description")
        >>> print(workflow.name)
        My Workflow
    """
    pass
```

## Testing

### Writing Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_workflow(client: AsyncClient):
    """Test workflow creation."""
    response = await client.post(
        "/api/v1/workflows",
        json={"name": "Test", "nodes": [], "edges": []}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
```

### Test Organization

- Unit tests for individual functions/classes
- Integration tests for API endpoints
- Use fixtures for common setup
- Mock external dependencies

### Coverage Requirements

- Minimum 80% code coverage for new code
- All public APIs must have tests
- Critical paths require 100% coverage

## Documentation

### Code Documentation

- All public functions/classes require docstrings
- Document parameters, return values, and exceptions
- Include examples for complex functionality

### API Documentation

- Update `docs/API_REFERENCE.md` for API changes
- Include request/response examples
- Document error cases

### Architecture Documentation

- Update `docs/ARCHITECTURE.md` for structural changes
- Include diagrams for complex flows
- Explain design decisions

## Submitting Changes

### Pull Request Process

1. **Update documentation** - Ensure all docs are current
2. **Add tests** - All new code must have tests
3. **Run tests locally** - Ensure all tests pass
4. **Format code** - Run black and ruff
5. **Create PR** - Use descriptive title and description
6. **Address feedback** - Respond to review comments

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. Automated checks run (tests, linting)
2. Code review by maintainers
3. Address feedback if requested
4. Approval and merge

## Areas for Contribution

### High Priority

- Frontend implementation (React + TypeScript)
- Database integration (PostgreSQL + SQLAlchemy)
- Authentication (JWT + OAuth 2.0)
- Additional API endpoints

### Medium Priority

- Performance optimization
- Additional test coverage
- Documentation improvements
- Example workflows

### Low Priority

- UI/UX enhancements
- Additional integrations
- Developer tools
- Tutorial content

## Getting Help

- **Issues**: https://github.com/zubinqayam/ZQAutoNXG-V1/issues
- **Email**: zubin.qayam@outlook.com
- **Documentation**: https://github.com/zubinqayam/ZQAutoNXG-V1/tree/main/docs

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

All contributions must include the Apache 2.0 license header:

```python
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0
```

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to ZQAutoNXG!

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**

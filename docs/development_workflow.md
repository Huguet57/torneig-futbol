# Development Workflow Guide

This guide outlines the standard development workflows for the Soccer Tournament Management System.

## Getting Started

1. **Set Up Development Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/torneig-futbol.git
   cd torneig-futbol

   # Run the setup script
   ./scripts/setup_dev.sh
   ```

2. **Start Development Server**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Feature Development Process

### 1. Create Feature Branch
```bash
# Create and switch to a new feature branch
git checkout -b feature/your-feature-name

# Pull latest changes from main
git pull origin main
```

### 2. Development Cycle
1. **Write Tests First**
   ```bash
   # Create test file
   touch tests/test_your_feature.py

   # Run specific tests
   poetry run pytest tests/test_your_feature.py -v
   ```

2. **Implement Feature**
   - Follow TDD approach
   - Keep changes focused and minimal
   - Add type hints and docstrings

3. **Local Testing**
   ```bash
   # Run all tests
   poetry run pytest

   # Run with coverage
   poetry run pytest --cov=app

   # Check code quality
   poetry run ruff check .
   poetry run mypy .
   ```

4. **Commit Changes**
   ```bash
   # Stage changes
   git add .

   # Commit with descriptive message
   git commit -m "feat: add your feature description"
   ```

### 3. Code Review Process
1. **Prepare Pull Request**
   ```bash
   # Push changes
   git push origin feature/your-feature-name
   ```

2. **Pull Request Checklist**
   - [ ] Tests pass
   - [ ] Coverage maintained or improved
   - [ ] Documentation updated
   - [ ] Code follows style guide
   - [ ] No linting errors
   - [ ] Commit messages follow conventions

3. **Review and Merge**
   - Address review comments
   - Rebase if needed
   - Squash commits if requested

## Testing Procedures

### 1. Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Focus on edge cases

Example:
```python
def test_create_tournament():
    tournament = Tournament(name="Test Tournament", start_date=date.today())
    assert tournament.name == "Test Tournament"
    assert tournament.start_date == date.today()
```

### 2. Integration Tests
- Test component interactions
- Use test database
- Test API endpoints

Example:
```python
def test_tournament_api_workflow():
    # Create tournament
    response = client.post("/tournaments/", json={
        "name": "Test Tournament",
        "start_date": str(date.today())
    })
    assert response.status_code == 201
    tournament_id = response.json()["id"]

    # Add teams
    response = client.post(f"/tournaments/{tournament_id}/teams", ...)
    assert response.status_code == 201
```

### 3. End-to-End Tests
- Test complete workflows
- Use test data fixtures
- Verify system integration

## Deployment Process

### 1. Staging Deployment
```bash
# Tag release candidate
git tag -a v1.2.0-rc1 -m "Release candidate 1 for version 1.2.0"
git push origin v1.2.0-rc1

# Deploy to staging
./scripts/deploy.sh staging
```

### 2. Production Deployment
```bash
# Create release
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# Deploy to production
./scripts/deploy.sh production
```

### 3. Post-Deployment
- Monitor error rates
- Check performance metrics
- Verify database migrations
- Test critical workflows

## Database Management

### 1. Create Migration
```bash
# Generate migration
poetry run alembic revision --autogenerate -m "description"

# Review migration file
# Apply migration
poetry run alembic upgrade head
```

### 2. Rollback
```bash
# Rollback one version
poetry run alembic downgrade -1

# Rollback to specific version
poetry run alembic downgrade <version_id>
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database status
   poetry run python scripts/check_db.py

   # Reset database (development only)
   poetry run python scripts/reset_db.py
   ```

2. **Test Failures**
   ```bash
   # Run failed tests with detailed output
   poetry run pytest -vv --last-failed

   # Debug specific test
   poetry run pytest -vv --pdb tests/test_file.py::test_name
   ```

3. **Dependency Issues**
   ```bash
   # Update dependencies
   poetry update

   # Clean and reinstall
   poetry env remove python
   poetry install
   ```

## Best Practices

1. **Code Quality**
   - Write descriptive variable and function names
   - Keep functions small and focused
   - Add type hints to all functions
   - Document complex logic
   - Follow PEP 8 style guide

2. **Testing**
   - Write tests for new features
   - Update tests when modifying code
   - Aim for high test coverage
   - Test edge cases and error conditions

3. **Git Workflow**
   - Keep commits focused and atomic
   - Write clear commit messages
   - Rebase feature branches regularly
   - Delete merged feature branches

4. **Documentation**
   - Update API documentation
   - Document configuration changes
   - Add examples for new features
   - Keep README up to date

## Monitoring and Debugging

### 1. Logging
```python
# Use structured logging
logger.info("Tournament created", tournament_id=tournament.id)
logger.error("Database connection failed", exc_info=True)
```

### 2. Performance Monitoring
- Monitor response times
- Track database query performance
- Watch memory usage
- Monitor error rates

### 3. Debugging Tools
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debugger
poetry run python -m pdb scripts/your_script.py
```

## Security Considerations

1. **Code Security**
   - Validate all inputs
   - Use parameterized queries
   - Sanitize user data
   - Follow security best practices

2. **Dependency Security**
   ```bash
   # Check for security vulnerabilities
   poetry run safety check
   ```

3. **API Security**
   - Use HTTPS
   - Implement rate limiting
   - Validate authentication
   - Log security events 
# Soccer Tournament Management System

## Overview
This project aims to create a comprehensive system for managing soccer tournaments, similar to the "TORNEIG CASTELLER DE FUTBOL" shown in the provided examples. The system handles tournament organization, team management, match scheduling, results tracking, and statistics.

## Project Documentation

The documentation for this project has been organized into multiple files for easier reference:

- [API Documentation](docs/api.md) - Detailed API endpoint definitions
- [Implementation Details](docs/implementation.md) - Database design and technology stack
- [Development Approach](docs/development_approach.md) - Testing strategy and MVP iteration cycles
- [Match Management](docs/match_management.md) - Detailed guide for match scheduling and results tracking
- [Architecture](docs/architecture.md) - System architecture and design decisions
- [Development Workflow](docs/development_workflow.md) - Development processes and guidelines
- [Error Handling](docs/error_handling.md) - Error responses and recovery strategies
- [Linting Guide](LINTING.md) - Instructions for using Ruff linter and formatter

## Project Status

- [x] Initial planning and architecture design
- [x] MVP 1: Tournament and Team Structure
- [x] MVP 2: Match Management
- [x] MVP 3: Player Statistics
  - [x] Goal tracking functionality
  - [x] Player statistics with tournament-specific filtering
  - [x] Team statistics with performance metrics
- [ ] MVP 4: Backend Quality & Scalability (In Progress)
  - [x] Comprehensive Test Suite Enhancement
  - [x] Add observability tools
  - [ ] Code Refactoring for Maintainability
  - [ ] Documentation and Developer Experience

## Features

The system supports the following core features:

- Tournament organization with multiple phases (groups, knockout stages)
- Team and player management
- Match scheduling and results tracking
- Automatic standings calculations
- Player and team statistics
- Goal tracking system
- Performance metrics calculation

## Development Environment Setup

### Prerequisites

1. **Python Environment**
   - Python 3.12 or higher
   - Poetry (dependency management)
   ```bash
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Development Tools**
   - Git
   - SQLite 3
   - Your favorite code editor (VS Code recommended)

3. **VS Code Extensions** (Recommended)
   - Python
   - Ruff
   - SQLite Viewer
   - Mermaid Preview

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/torneig-futbol.git
   cd torneig-futbol
   ```

2. **Run Setup Script**
   ```bash
   # Make script executable
   chmod +x scripts/setup_dev.sh
   
   # Run setup
   ./scripts/setup_dev.sh
   ```

   This script will:
   - Install project dependencies
   - Set up pre-commit hooks
   - Initialize the database
   - Create test data
   - Configure development tools

3. **Start Development Server**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

4. **Access the Application**
   - API Documentation: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc
   - Web Interface: http://localhost:8000

### Manual Setup (Alternative)

If you prefer to set up manually or the setup script fails:

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Set Up Pre-commit Hooks**
   ```bash
   poetry run pre-commit install
   ```

3. **Initialize Database**
   ```bash
   poetry run python scripts/create_tables.py
   poetry run python scripts/init_db.py
   ```

4. **Create Test Data**
   ```bash
   poetry run python scripts/create_test_data.py
   ```

## Testing

The project uses pytest for comprehensive test coverage:

```bash
# Run all tests
poetry run pytest

# Run specific test categories
poetry run pytest -m match_workflow
poetry run pytest -m goal_tracking
poetry run pytest -m player_stats
poetry run pytest -m team_stats

# Run tests with coverage report
poetry run pytest --cov=app --cov-report=html
```

## Code Quality

1. **Linting and Formatting**
   ```bash
   # Run Ruff linter
   poetry run ruff check .

   # Auto-fix issues
   poetry run ruff check . --fix
   ```

2. **Type Checking**
   ```bash
   # Run mypy
   poetry run mypy .
   ```

3. **Pre-commit Hooks**
   ```bash
   # Run manually
   poetry run pre-commit run --all-files
   ```

## Troubleshooting

### Common Issues

1. **Database Issues**
   - Error: "Database is locked"
     ```bash
     # Kill all connections and recreate database
     poetry run python scripts/reset_db.py
     ```
   - Error: "Table doesn't exist"
     ```bash
     # Recreate all tables
     poetry run python scripts/create_tables.py
     ```

2. **Poetry Issues**
   - Error: "Package not found"
     ```bash
     # Update poetry.lock
     poetry update
     ```
   - Error: "Virtual environment not created"
     ```bash
     # Recreate virtual environment
     poetry env remove python
     poetry install
     ```

3. **Server Issues**
   - Error: "Address already in use"
     ```bash
     # Find and kill existing process
     lsof -i :8000
     kill -9 <PID>
     ```

### Getting Help

1. Check the [documentation](docs/)
2. Search existing issues
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Expected behavior
   - Environment details

## Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Set up development environment
4. Make your changes
5. Run tests and quality checks
6. Submit a pull request

### Pull Request Process

1. **Before Submitting**
   - Update documentation
   - Add tests for new features
   - Run all tests
   - Run code quality checks
   - Update CHANGELOG.md

2. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Added new tests
   - [ ] All tests pass
   - [ ] Coverage maintained/improved

   ## Documentation
   - [ ] Updated relevant documentation
   - [ ] Added inline documentation
   - [ ] Updated CHANGELOG.md
   ```

3. **Review Process**
   - Two approvals required
   - All tests must pass
   - Code coverage maintained
   - Documentation updated

### Code Style

1. **Python**
   - Follow PEP 8
   - Use type hints
   - Add docstrings
   - Keep functions focused

2. **Git**
   - Clear commit messages
   - One feature per branch
   - Rebase before merging

3. **Documentation**
   - Update relevant docs
   - Add examples
   - Keep README current

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI team for the excellent framework
- SQLAlchemy team for the robust ORM
- All contributors to this project 
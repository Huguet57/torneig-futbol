# Soccer Tournament Management System

## Overview
This project aims to create a comprehensive system for managing soccer tournaments, similar to the "TORNEIG CASTELLER DE FUTBOL" shown in the provided examples. The system will handle tournament organization, team management, match scheduling, results tracking, and statistics.

## Project Documentation

The documentation for this project has been organized into multiple files for easier reference:

- [API Documentation](docs/api.md) - Detailed API endpoint definitions
- [Implementation Details](docs/implementation.md) - Database design and technology stack
- [Development Approach](docs/development_approach.md) - Testing strategy and MVP iteration cycles
- [Match Management](docs/match_management.md) - Detailed guide for match scheduling and results tracking
- [Linting Guide](LINTING.md) - Instructions for using Ruff linter and formatter

## Project Status

- [x] Initial planning and architecture design
- [x] MVP 1: Tournament and Team Structure
- [x] MVP 2: Match Management
- [x] MVP 3: Player Statistics
  - [x] Goal tracking functionality
  - [x] Player statistics with tournament-specific filtering
  - [x] Team statistics with performance metrics
- [ ] MVP 4: Backend Quality & Scalability (Next up)
  - [ ] Comprehensive test suite enhancement
  - [ ] Code refactoring for maintainability
  - [ ] Database and ORM optimization
  - [ ] API performance optimization
  - [ ] Documentation and developer experience improvements

## Features

The system supports the following core features:

- Tournament organization with multiple phases (groups, knockout stages)
- Team and player management
- Match scheduling and results tracking
- Automatic standings calculations
- Player and team statistics
- Goal tracking system
- Performance metrics calculation

## Getting Started

### Prerequisites
- Python 3.12 or higher
- Poetry (dependency management)

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/torneig-futbol.git
   cd torneig-futbol
   ```

2. Install dependencies
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks
   ```bash
   poetry run pre-commit install
   ```

4. Initialize the database
   ```bash
   poetry run python scripts/create_tables.py
   poetry run python scripts/init_db.py
   ```

5. Run the application
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

6. Access the API documentation
   ```
   http://localhost:8000/docs
   ```

### Testing

The project uses pytest for comprehensive test coverage:

```bash
# Run all tests
poetry run pytest

# Run specific test categories using markers
poetry run pytest -m match_workflow
poetry run pytest -m goal_tracking
poetry run pytest -m player_stats
poetry run pytest -m team_stats

# Run tests with verbose output
poetry run pytest -v

# Generate test coverage report
poetry run pytest --cov=app
```

The test suite includes:

1. **Match Workflow Tests**
   - Test the complete match management workflow from tournament creation to standings calculation
   - Validate tournament structure creation, team assignment, match scheduling, and result tracking

2. **Goal Tracking Tests**
   - Test goal creation and retrieval functionality
   - Validate goal statistics by match, player, and team

3. **Player Statistics Tests**
   - Test calculation of player performance metrics
   - Validate tournament-specific statistics and top scorers functionality

4. **Team Statistics Tests**
   - Test team performance metrics and rankings
   - Validate team statistics calculation based on match results

Each test suite focuses on validating specific functionality while ensuring all components work together correctly.

For more details on linting and code quality tools, see the [Linting Guide](LINTING.md).

## Contributing

Guidelines for contributing to this project will be added once the initial development phase is complete. 
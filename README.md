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
- [ ] MVP 3: Player Statistics (In Progress)
  - [x] Goal tracking functionality ✅ (Completed with tests)
  - [x] Player statistics ✅ (Completed with tournament-specific filtering)
  - [ ] Team statistics enhancement (Next up)

## Features

The system supports the following core features:

- Tournament organization with multiple phases (groups, knockout stages)
- Team and player management
- Match scheduling and results tracking
- Automatic standings calculations
- Player and team statistics

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

4. Run the application
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

5. Access the API documentation
   ```
   http://localhost:8000/docs
   ```

### Testing

The project includes test scripts to verify functionality:

1. Match Management Workflow Test
   ```bash
   poetry run python scripts/test_match_workflow.py
   ```
   This script tests the complete match management workflow from tournament creation to standings calculation.

2. Goal Tracking Test
   ```bash
   poetry run python scripts/test_goal_tracking.py
   ```
   This script tests the goal tracking functionality, including recording and retrieving goals by match, player, and team.

3. Player Statistics Test
   ```bash
   poetry run python scripts/test_player_stats.py
   ```
   This script tests the player statistics functionality, calculating and retrieving player stats and tournament top scorers.

For more details on testing, see the [scripts README](scripts/README.md).

For more details on linting and code quality tools, see the [Linting Guide](LINTING.md).

## Contributing

Guidelines for contributing to this project will be added once the initial development phase is complete. 
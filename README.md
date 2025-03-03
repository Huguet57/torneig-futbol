# Soccer Tournament Management System

## Overview
This project aims to create a comprehensive system for managing soccer tournaments, similar to the "TORNEIG CASTELLER DE FUTBOL" shown in the provided examples. The system will handle tournament organization, team management, match scheduling, results tracking, and statistics.

## Project Documentation

The documentation for this project has been organized into multiple files for easier reference:

- [API Documentation](docs/api.md) - Detailed API endpoint definitions
- [Implementation Details](docs/implementation.md) - Database design and technology stack
- [Development Approach](docs/development_approach.md) - Testing strategy and MVP iteration cycles
- [Linting Guide](LINTING.md) - Instructions for using Ruff linter and formatter

## Project Status

- [x] Initial planning and architecture design
- [ ] Development in progress

## Features

The system will support the following core features:

- Tournament organization with multiple phases (groups, knockout stages)
- Team and player management
- Match scheduling and results tracking
- Automatic standings calculations
- Player and team statistics
- Exportable reports

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

For more details on linting and code quality tools, see the [Linting Guide](LINTING.md).

## Contributing

Guidelines for contributing to this project will be added once the initial development phase is complete. 
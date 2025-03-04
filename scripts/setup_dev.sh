#!/bin/bash

# Soccer Tournament Management System - Development Environment Setup Script

# Exit on error
set -e

echo "Setting up development environment..."

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo "Installing project dependencies..."
poetry install

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
poetry run pre-commit install

# Initialize database
echo "Initializing database..."
poetry run python scripts/create_tables.py
poetry run python scripts/init_db.py

# Create test data
echo "Creating test data..."
poetry run python scripts/create_test_data.py

# Set up development tools
echo "Configuring development tools..."

# Configure mypy
echo "Configuring mypy..."
if [ ! -f "mypy.ini" ]; then
    cat > mypy.ini << EOL
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
check_untyped_defs = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

[mypy.plugins.pydantic.*]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True
warn_untyped_fields = True
EOL
fi

# Configure Ruff
echo "Configuring Ruff..."
if [ ! -f "ruff.toml" ]; then
    cat > ruff.toml << EOL
# Enable pycodestyle (`E`) and Pyflakes (`F`) codes by default.
select = ["E", "F"]
ignore = []

# Allow autofix for all enabled rules (when `--fix`) is provided.
fixable = ["A", "B", "C", "D", "E", "F"]
unfixable = []

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
]

# Same as Black.
line-length = 88

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

# Assume Python 3.12
target-version = "py312"

[per-file-ignores]
"__init__.py" = ["E402"]
EOL
fi

# Configure pytest
echo "Configuring pytest..."
if [ ! -f "pytest.ini" ]; then
    cat > pytest.ini << EOL
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test
python_functions = test_*
addopts = -v --cov=app --cov-report=term-missing
markers =
    match_workflow: tests for match management workflow
    goal_tracking: tests for goal tracking functionality
    player_stats: tests for player statistics
    team_stats: tests for team statistics
EOL
fi

# Create .env file for development
echo "Creating development environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << EOL
# Development environment settings
DATABASE_URL=sqlite:///torneig_futbol.db
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:8000"]
EOL
fi

# Verify installation
echo "Verifying installation..."
poetry run pytest -v

echo "Development environment setup complete!"
echo
echo "To start the development server, run:"
echo "poetry run uvicorn app.main:app --reload"
echo
echo "To run tests:"
echo "poetry run pytest"
echo
echo "To check code quality:"
echo "poetry run ruff check ."
echo "poetry run mypy ." 
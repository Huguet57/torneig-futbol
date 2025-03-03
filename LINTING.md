# Linting Guide for Soccer Tournament Management System

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting Python code. Ruff is a fast Python linter written in Rust that can replace multiple Python linting tools like flake8, isort, and more.

## Setup

The linting tools are already configured in the project. They are installed as development dependencies using Poetry.

## Running the Linter

### Manual Linting

To manually run the linter and see all issues without fixing them:

```bash
./scripts/lint.sh
```

### Auto-fixing Issues

To automatically fix issues that can be fixed:

```bash
./scripts/fix_lint.sh
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure that code is linted and formatted before each commit. The hooks are configured in the `.pre-commit-config.yaml` file.

### Installing Pre-commit Hooks

If you haven't installed the pre-commit hooks yet, you can do so with:

```bash
poetry run pre-commit install
```

### Running Pre-commit Hooks Manually

You can run the pre-commit hooks manually on all files with:

```bash
poetry run pre-commit run --all-files
```

## Linting Configuration

The linting rules are configured in the `pyproject.toml` file. The configuration includes:

- Code style rules (E, F)
- Bugbear rules (B)
- Import sorting (I)
- Naming conventions (N)
- Python upgrade rules (UP)
- Type annotation rules (ANN)
- Security rules (S)
- Assertion rules (A)
- Comma placement rules (COM)
- Comprehension rules (C4)
- Date and time rules (DTZ)
- Exception message rules (EM)
- String concatenation rules (ISC)

## Ignoring Rules

If you need to ignore a specific rule for a specific line of code, you can add a comment like:

```python
# noqa: E501
```

For example:

```python
long_line = "This is a very long line that exceeds the line length limit but we need to keep it this way"  # noqa: E501
```

## Formatting

Ruff also includes a formatter that works similarly to Black. It will format your code according to the rules specified in the `pyproject.toml` file.

To run the formatter manually:

```bash
poetry run ruff format app tests demos
```

## CI/CD Integration

The linting checks are also run as part of the CI/CD pipeline to ensure that all code meets the project's standards before being merged. 
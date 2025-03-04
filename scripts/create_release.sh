#!/bin/bash

# Exit on error
set -e

VERSION="1.0.0"
RELEASE_DATE="2024-03-04"

echo "Creating release v${VERSION}..."

# Ensure we're on the main branch
git checkout main

# Pull latest changes
git pull origin main

# Run tests
echo "Running tests..."
poetry run pytest

# Run code quality checks
echo "Running code quality checks..."
poetry run ruff check .
poetry run mypy .

# Create and push tag
echo "Creating git tag v${VERSION}..."
git tag -a "v${VERSION}" -m "Release version ${VERSION} (${RELEASE_DATE})"
git push origin "v${VERSION}"

echo "Release v${VERSION} created successfully!"
echo
echo "Next steps:"
echo "1. Create a GitHub release at https://github.com/yourusername/torneig-futbol/releases/new"
echo "2. Copy the contents of CHANGELOG.md for this version into the release notes"
echo "3. Upload any additional release assets if needed"
echo
echo "Don't forget to:"
echo "- Update the version in production deployments"
echo "- Notify users about the new release"
echo "- Monitor for any issues after deployment" 
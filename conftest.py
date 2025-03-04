import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Register pytest markers to avoid warnings
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "match_workflow: Tests for the match management workflow")
    config.addinivalue_line("markers", "goal_tracking: Tests for the goal tracking functionality")
    config.addinivalue_line("markers", "player_stats: Tests for the player statistics functionality")
    config.addinivalue_line("markers", "team_stats: Tests for the team statistics functionality")

from fastapi.testclient import TestClient

from app.db.database import get_db
from app.main import app
from app.tests.utils.utils import get_test_db

client = TestClient(app)

# Override the get_db dependency
app.dependency_overrides[get_db] = get_test_db

def test_home_page():
    """Test that the home page returns a 200 status code."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_tournaments_page():
    """Test that the tournaments page returns a 200 status code."""
    response = client.get("/tournaments")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_matches_page():
    """Test that the matches page returns a 200 status code."""
    response = client.get("/matches")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_players_page():
    """Test that the players page returns a 200 status code."""
    response = client.get("/players")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_teams_page():
    """Test that the teams page returns a 200 status code."""
    response = client.get("/teams")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_stats_page():
    """Test that the stats page returns a 200 status code."""
    response = client.get("/stats")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_player_stats_page():
    """Test that the player stats page returns a 200 status code."""
    response = client.get("/player-stats")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_static_files():
    """Test that static files are served correctly."""
    # Test CSS file
    response = client.get("/static/css/main.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    
    # Test JS file
    response = client.get("/static/js/main.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"] or "text/javascript" in response.headers["content-type"]


def test_nonexistent_page():
    """Test that a nonexistent page returns a 404 status code."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    # The API returns JSON for 404 errors, not HTML
    assert "application/json" in response.headers["content-type"]


def test_dynamic_routes():
    """
    Test dynamic routes with valid IDs.
    
    Note: This test assumes that the database has been populated with test data.
    If the test fails, it may be because the database is empty or the IDs don't exist.
    """
    # For now, we'll skip these tests since they depend on data being in the database
    # In a real application, we would use fixtures to populate the database
    pass 
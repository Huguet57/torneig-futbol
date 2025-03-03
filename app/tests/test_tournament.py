import json
from datetime import date

from app.tests.fixtures import create_test_tournament


def test_create_tournament(client):
    """Test creating a tournament via API."""
    tournament_data = {
        "name": "New Tournament",
        "edition": "II",
        "year": 2024,
        "start_date": "2024-06-01",
        "end_date": "2024-06-30",
        "description": "A new test tournament",
        "logo_url": None
    }
    response = client.post("/api/tournaments/", json=tournament_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tournament_data["name"]
    assert data["edition"] == tournament_data["edition"]
    assert data["year"] == tournament_data["year"]
    assert "id" in data


def test_get_tournament(client, db):
    """Test getting a tournament by ID."""
    tournament = create_test_tournament(db)
    response = client.get(f"/api/tournaments/{tournament.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tournament.id
    assert data["name"] == tournament.name


def test_get_tournaments(client, db):
    """Test getting all tournaments."""
    # Create some test tournaments
    create_test_tournament(db)
    create_test_tournament(db)
    
    response = client.get("/api/tournaments/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_tournament(client, db):
    """Test updating a tournament."""
    tournament = create_test_tournament(db)
    update_data = {
        "name": "Updated Tournament Name"
    }
    response = client.put(f"/api/tournaments/{tournament.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    # Other fields should remain unchanged
    assert data["edition"] == tournament.edition


def test_delete_tournament(client, db):
    """Test deleting a tournament."""
    tournament = create_test_tournament(db)
    response = client.delete(f"/api/tournaments/{tournament.id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get(f"/api/tournaments/{tournament.id}")
    assert response.status_code == 404 
from app.tests.fixtures import create_test_team


def test_create_team(client):
    """Test creating a team via API."""
    team_data = {
        "name": "New Test Team",
        "short_name": "NTT",
        "city": "New City",
        "colors": "Blue/Green",
        "logo_url": None,
    }
    response = client.post("/api/teams/", json=team_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == team_data["name"]
    assert data["short_name"] == team_data["short_name"]
    assert data["city"] == team_data["city"]
    assert "id" in data


def test_get_team(client, db):
    """Test getting a team by ID."""
    team = create_test_team(db)
    response = client.get(f"/api/teams/{team.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == team.id
    assert data["name"] == team.name


def test_get_teams(client, db):
    """Test getting all teams."""
    # Create some test teams
    create_test_team(db)
    create_test_team(db)

    response = client.get("/api/teams/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_team(client, db):
    """Test updating a team."""
    team = create_test_team(db)
    update_data = {"name": "Updated Team Name"}
    response = client.put(f"/api/teams/{team.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    # Other fields should remain unchanged
    assert data["short_name"] == team.short_name


def test_delete_team(client, db):
    """Test deleting a team."""
    team = create_test_team(db)
    response = client.delete(f"/api/teams/{team.id}")
    assert response.status_code == 200

    # Verify it's gone
    response = client.get(f"/api/teams/{team.id}")
    assert response.status_code == 404

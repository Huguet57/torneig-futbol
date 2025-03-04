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


def test_get_nonexistent_team(client):
    """Test getting a non-existent team."""
    response = client.get("/api/teams/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_update_nonexistent_team(client):
    """Test updating a non-existent team."""
    update_data = {"name": "Updated Team Name"}
    response = client.put("/api/teams/99999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_create_team_player(client, db):
    """Test creating a player for a team."""
    team = create_test_team(db)
    player_data = {
        "name": "Test Player",
        "number": 10,
        "position": "Forward",
        "is_goalkeeper": False,
        "team_id": team.id
    }
    response = client.post(f"/api/teams/{team.id}/players/", json=player_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == player_data["name"]
    assert data["number"] == player_data["number"]
    assert data["position"] == player_data["position"]
    assert data["is_goalkeeper"] == player_data["is_goalkeeper"]
    assert data["team_id"] == team.id


def test_create_player_nonexistent_team(client):
    """Test creating a player for a non-existent team."""
    player_data = {
        "name": "Test Player",
        "number": 10,
        "position": "Forward",
        "is_goalkeeper": False,
        "team_id": 99999
    }
    response = client.post("/api/teams/99999/players/", json=player_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_get_team_players(client, db):
    """Test getting all players for a team."""
    team = create_test_team(db)
    # Create some test players
    player_data = {
        "name": "Test Player 1",
        "number": 10,
        "position": "Forward",
        "is_goalkeeper": False,
        "team_id": team.id
    }
    client.post(f"/api/teams/{team.id}/players/", json=player_data)
    player_data["name"] = "Test Player 2"
    player_data["number"] = 11
    client.post(f"/api/teams/{team.id}/players/", json=player_data)

    response = client.get(f"/api/teams/{team.id}/players/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(player["team_id"] == team.id for player in data)


def test_get_players_nonexistent_team(client):
    """Test getting players for a non-existent team."""
    response = client.get("/api/teams/99999/players/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_get_teams_pagination(client, db):
    """Test pagination for teams listing."""
    # Create 3 test teams
    for i in range(3):
        create_test_team(db)

    # Test limit
    response = client.get("/api/teams/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Test skip
    response = client.get("/api/teams/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_team_players_pagination(client, db):
    """Test pagination for team players listing."""
    team = create_test_team(db)
    # Create 3 test players
    for i in range(3):
        player_data = {
            "name": f"Test Player {i+1}",
            "number": 10 + i,
            "position": "Forward",
            "is_goalkeeper": False,
            "team_id": team.id
        }
        client.post(f"/api/teams/{team.id}/players/", json=player_data)

    # Test limit
    response = client.get(f"/api/teams/{team.id}/players/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Test skip
    response = client.get(f"/api/teams/{team.id}/players/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

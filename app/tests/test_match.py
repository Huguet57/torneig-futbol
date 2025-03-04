from app.tests.fixtures import (
    create_test_group,
    create_test_match,
    create_test_phase,
    create_test_team,
    create_test_tournament,
)


def test_create_match(client, db):
    """Test creating a match via API."""
    # Create required relationships
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    home_team = create_test_team(db)
    away_team = create_test_team(db)

    match_data = {
        "tournament_id": tournament.id,
        "phase_id": phase.id,
        "group_id": group.id,
        "home_team_id": home_team.id,
        "away_team_id": away_team.id,
        "date": "2023-06-15",
        "location": "Test Stadium",
    }
    response = client.post("/api/matches/", json=match_data)
    assert response.status_code == 200
    data = response.json()
    assert data["tournament_id"] == match_data["tournament_id"]
    assert data["home_team_id"] == match_data["home_team_id"]
    assert data["away_team_id"] == match_data["away_team_id"]
    assert data["status"] == "scheduled"
    assert "id" in data


def test_get_match(client, db):
    """Test getting a match by ID."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    match = create_test_match(db, tournament.id, phase.id)
    
    response = client.get(f"/api/matches/{match.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == match.id
    assert data["tournament_id"] == match.tournament_id
    assert data["home_team_id"] == match.home_team_id
    assert data["away_team_id"] == match.away_team_id
    assert "home_team" in data
    assert "away_team" in data


def test_update_match(client, db):
    """Test updating a match."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    match = create_test_match(db, tournament.id, phase.id)
    
    update_data = {
        "location": "Updated Stadium",
        "home_score": 2,
        "away_score": 1,
        "status": "completed"
    }
    response = client.put(f"/api/matches/{match.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == update_data["location"]
    assert data["home_score"] == update_data["home_score"]
    assert data["away_score"] == update_data["away_score"]
    assert data["status"] == update_data["status"]


def test_delete_match(client, db):
    """Test deleting a match."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    match = create_test_match(db, tournament.id, phase.id)
    
    response = client.delete(f"/api/matches/{match.id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get(f"/api/matches/{match.id}")
    assert response.status_code == 404


def test_update_match_result(client, db):
    """Test updating a match result."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    match = create_test_match(db, tournament.id, phase.id)
    
    result_data = {
        "home_score": 3,
        "away_score": 2,
        "status": "completed"
    }
    response = client.put(f"/api/matches/{match.id}/result", json=result_data)
    assert response.status_code == 200
    data = response.json()
    assert data["home_score"] == result_data["home_score"]
    assert data["away_score"] == result_data["away_score"]
    assert data["status"] == result_data["status"]


def test_list_matches_by_tournament(client, db):
    """Test listing matches by tournament."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    create_test_match(db, tournament.id, phase.id)
    create_test_match(db, tournament.id, phase.id)
    
    response = client.get(f"/api/matches/tournament/{tournament.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["tournament_id"] == tournament.id
    assert data[1]["tournament_id"] == tournament.id


def test_list_matches_by_phase(client, db):
    """Test listing matches by phase."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    create_test_match(db, tournament.id, phase.id)
    
    response = client.get(f"/api/matches/phase/{phase.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["phase_id"] == phase.id


def test_list_matches_by_group(client, db):
    """Test listing matches by group."""
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    create_test_match(db, tournament.id, phase.id, group.id)
    
    response = client.get(f"/api/matches/group/{group.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["group_id"] == group.id 
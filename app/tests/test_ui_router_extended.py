from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.fixtures import (
    add_team_to_group,
    create_test_group,
    create_test_match,
    create_test_phase,
    create_test_player,
    create_test_team,
    create_test_tournament,
)


def test_match_list_filtering(client: TestClient, db: Session):
    """Test match listing with different filter combinations."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team1 = create_test_team(db)
    team2 = create_test_team(db)
    match = create_test_match(db, tournament.id, phase.id, group.id, team1.id, team2.id)

    # Test without filters
    response = client.get("/matches")
    assert response.status_code == 200
    assert "matches" in response.context

    # Test with tournament filter
    response = client.get(f"/matches?tournament_id={tournament.id}")
    assert response.status_code == 200
    assert "matches" in response.context
    assert len(response.context["matches"]) > 0

    # Test with phase filter
    response = client.get(f"/matches?tournament_id={tournament.id}&phase_id={phase.id}")
    assert response.status_code == 200
    assert "matches" in response.context
    assert len(response.context["matches"]) > 0

    # Test with group filter
    response = client.get(f"/matches?tournament_id={tournament.id}&phase_id={phase.id}&group_id={group.id}")
    assert response.status_code == 200
    assert "matches" in response.context
    assert len(response.context["matches"]) > 0


def test_match_creation_workflow(client: TestClient, db: Session):
    """Test the complete match creation workflow."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team1 = create_test_team(db)
    team2 = create_test_team(db)

    # Test create form without tournament
    response = client.get("/matches/create")
    assert response.status_code == 200
    assert "tournaments" in response.context
    assert "phases" in response.context
    assert len(response.context["phases"]) == 0

    # Test create form with tournament
    response = client.get(f"/matches/create?tournament_id={tournament.id}")
    assert response.status_code == 200
    assert len(response.context["phases"]) > 0

    # Test match creation
    match_data = {
        "tournament_id": tournament.id,
        "phase_id": phase.id,
        "group_id": group.id,
        "home_team_id": team1.id,
        "away_team_id": team2.id,
        "date": date.today().isoformat(),
        "time": "18:00",
        "location": "Test Field"
    }
    response = client.post("/matches/create", data=match_data)
    assert response.status_code == 200  # Changed from 303 to 200
    assert "success" in response.context  # Add check for success message


def test_match_result_workflow(client: TestClient, db: Session):
    """Test the match result update workflow."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team1 = create_test_team(db)
    team2 = create_test_team(db)
    match = create_test_match(db, tournament.id, phase.id, group.id, team1.id, team2.id)

    # Test result update form
    response = client.get(f"/matches/{match.id}/result")
    assert response.status_code == 200
    assert "match" in response.context

    # Test result update
    result_data = {
        "home_score": 2,
        "away_score": 1,
        "status": "completed"
    }
    response = client.post(f"/matches/{match.id}/result", data=result_data)
    assert response.status_code == 200  # Changed from 303 to 200
    assert "success" in response.context  # Add check for success message


def test_tournament_workflow(client: TestClient, db: Session):
    """Test tournament creation and viewing workflow."""
    # Test tournament creation form
    response = client.get("/tournaments/create")
    assert response.status_code == 200

    # Test tournament creation
    tournament_data = {
        "name": "Test Tournament",
        "edition": "I",
        "year": 2024,
        "start_date": date.today().isoformat(),
        "end_date": date.today().isoformat(),
        "description": "Test description",
        "logo_url": "https://example.com/logo.png"
    }
    response = client.post("/tournaments/create", data=tournament_data)
    assert response.status_code == 200  # Changed from 303 to 200
    assert "success" in response.context  # Add check for success message


def test_player_and_stats_pages(client: TestClient, db: Session):
    """Test player listing and statistics pages."""
    # Create test data
    team = create_test_team(db)
    player = create_test_player(db, team.id)
    tournament = create_test_tournament(db)

    # Test player listing without filter
    response = client.get("/players")
    assert response.status_code == 200
    assert "players" in response.context

    # Test player listing with team filter
    response = client.get(f"/players?team_id={team.id}")
    assert response.status_code == 200
    players = response.context["players"]
    assert any(p.id == player.id for p in players)

    # Test player details
    response = client.get(f"/players/{player.id}")
    assert response.status_code == 200
    assert "player" in response.context
    assert response.context["player"].id == player.id

    # Test player stats page
    response = client.get("/player-stats")
    assert response.status_code == 200
    assert "tournaments" in response.context

    # Test player stats with tournament filter
    response = client.get(f"/player-stats?tournament_id={tournament.id}")
    assert response.status_code == 200
    assert "tournament" in response.context
    assert response.context["tournament"].id == tournament.id


def test_team_pages(client: TestClient, db: Session):
    """Test team listing and details pages."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team = create_test_team(db)
    add_team_to_group(db, team, group)

    # Test team listing without filter
    response = client.get("/teams")
    assert response.status_code == 200
    assert "teams" in response.context

    # Test team listing with tournament filter
    response = client.get(f"/teams?tournament_id={tournament.id}")
    assert response.status_code == 200
    assert "tournaments" in response.context  # Changed from tournament to tournaments
    assert "selected_tournament_id" in response.context
    assert response.context["selected_tournament_id"] == tournament.id

    # Test team details without tournament
    response = client.get(f"/teams/{team.id}")
    assert response.status_code == 200
    assert "team" in response.context
    assert response.context["team"].id == team.id

    # Test team details with tournament
    response = client.get(f"/teams/{team.id}?tournament_id={tournament.id}")
    assert response.status_code == 200
    assert "tournament" in response.context
    assert "team_stats" in response.context


def test_stats_overview_page(client: TestClient, db: Session):
    """Test statistics overview page."""
    # Create test data
    tournament = create_test_tournament(db)

    # Test stats overview without filter
    response = client.get("/stats")
    assert response.status_code == 200
    assert "tournaments" in response.context

    # Test stats overview with tournament filter
    response = client.get(f"/stats?tournament_id={tournament.id}")
    assert response.status_code == 200
    assert "tournaments" in response.context  # Changed from tournament to tournaments
    assert "selected_tournament_id" in response.context
    assert response.context["selected_tournament_id"] == tournament.id


def test_error_handling(client: TestClient, db: Session):
    """Test error handling for non-existent resources."""
    # Test non-existent match
    response = client.get("/matches/999")
    assert response.status_code == 404

    # Test non-existent tournament
    response = client.get("/tournaments/999")
    assert response.status_code == 404

    # Test non-existent player
    response = client.get("/players/999")
    assert response.status_code == 404

    # Test non-existent team
    response = client.get("/teams/999")
    assert response.status_code == 404 
from app.models.group import Group
from app.tests.fixtures import (
    add_team_to_group,
    create_test_group,
    create_test_phase,
    create_test_team,
    create_test_tournament,
)


def test_add_team_to_group(client, db):
    """Test adding a team to a group."""
    # Create the necessary entities
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team = create_test_team(db)

    # Store the team ID for later comparison
    team_id = team.id

    # Add team to group via API
    response = client.post(f"/api/groups/{group.id}/teams", json={"team_id": team_id})
    assert response.status_code == 200
    data = response.json()

    # Verify the response
    assert data["id"] == group.id

    # Fetch a fresh instance of the group from the database
    db_group = db.query(Group).filter(Group.id == group.id).first()
    db.refresh(db_group)

    # Check if team is in group directly from DB
    teams_in_group = [t.id for t in db_group.teams]
    assert team_id in teams_in_group


def test_remove_team_from_group(client, db):
    """Test removing a team from a group."""
    # Create the necessary entities
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team = create_test_team(db)

    # Store the team ID for later comparison
    team_id = team.id

    # Add team to group directly in DB
    add_team_to_group(db, team, group)

    # Remove team from group via API
    response = client.delete(f"/api/groups/{group.id}/teams/{team_id}")
    assert response.status_code == 200

    # Check if team is removed from group
    response = client.get(f"/api/groups/{group.id}")
    assert response.status_code == 200
    data = response.json()

    # The response should have a teams field
    assert "teams" in data, "Response does not contain teams field"
    teams_in_response = data.get("teams", [])
    team_ids = [t["id"] for t in teams_in_response]
    assert team_id not in team_ids


def test_add_team_to_group_errors(client, db):
    """Test error cases when adding a team to a group."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team = create_test_team(db)

    # Test non-existent group
    response = client.post("/api/groups/99999/teams", json={"team_id": team.id})
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"

    # Test non-existent team
    response = client.post(f"/api/groups/{group.id}/teams", json={"team_id": 99999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"


def test_remove_team_from_group_errors(client, db):
    """Test error cases when removing a team from a group."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)
    team = create_test_team(db)

    # Test non-existent group
    response = client.delete(f"/api/groups/99999/teams/{team.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"

    # Test non-existent team
    response = client.delete(f"/api/groups/{group.id}/teams/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"

    # Test team not in group
    response = client.delete(f"/api/groups/{group.id}/teams/{team.id}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Team is not in this group"

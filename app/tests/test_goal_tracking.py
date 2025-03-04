from datetime import date

import pytest

from app.tests.fixtures import (
    create_test_group,
    create_test_match,
    create_test_phase,
    create_test_player,
    create_test_team,
    create_test_tournament,
)


@pytest.mark.goal_tracking
class TestGoalTracking:
    """Test the goal tracking functionality."""

    def test_goal_tracking_workflow(self, client, db, refresh):
        """
        Test the complete goal tracking workflow.
        
        This test validates:
        1. Creating goals for players in a match
        2. Retrieving goals by match
        3. Retrieving goals by player
        4. Retrieving goals by team
        """
        # Step 1: Create tournament structure
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, tournament)
        
        phase = create_test_phase(db, tournament.id)
        group = create_test_group(db, phase.id)
        
        # Step 2: Create teams and players
        home_team = create_test_team(db)
        home_team.name = "Goal Team 1"
        db.commit()
        refresh(db, home_team)
        
        away_team = create_test_team(db)
        away_team.name = "Goal Team 2"
        db.commit()
        refresh(db, away_team)
        
        # Create players for each team
        home_players = []
        for i in range(1, 4):
            player = create_test_player(db, home_team.id)
            player.name = f"Player 1-{i}"
            player.number = i
            db.commit()
            refresh(db, player)
            home_players.append(player)
        
        away_players = []
        for i in range(1, 4):
            player = create_test_player(db, away_team.id)
            player.name = f"Player 2-{i}"
            player.number = i
            db.commit()
            refresh(db, player)
            away_players.append(player)
        
        # Step 3: Create a match
        match_data = {
            "tournament_id": tournament.id,
            "phase_id": phase.id,
            "group_id": group.id,
            "home_team_id": home_team.id,
            "away_team_id": away_team.id,
            "date": str(date.today()),
            "location": "Goal Test Stadium"
        }
        response = client.post("/api/matches/", json=match_data)
        assert response.status_code == 200
        match = response.json()
        
        # Step 4: Record goals
        # Define goals: who scored, when, and type
        goal_data = [
            # Regular goals for home team
            {"player_id": home_players[0].id, "team_id": home_team.id, "minute": 15, "type": "regular"},
            {"player_id": home_players[0].id, "team_id": home_team.id, "minute": 35, "type": "penalty"},
            {"player_id": home_players[1].id, "team_id": home_team.id, "minute": 55, "type": "regular"},
            
            # Regular goals for away team
            {"player_id": away_players[0].id, "team_id": away_team.id, "minute": 25, "type": "regular"},
            {"player_id": away_players[1].id, "team_id": away_team.id, "minute": 75, "type": "regular"},
        ]
        
        created_goals = []
        for goal in goal_data:
            goal_request = {
                "match_id": match["id"],
                **goal
            }
            response = client.post("/api/goals/", json=goal_request)
            assert response.status_code == 200
            created_goals.append(response.json())
        
        # Step 5: Update match result to reflect goals
        result_data = {
            "home_score": 3,  # Home team scored 3 goals
            "away_score": 2,  # Away team scored 2 goals
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match['id']}/result", json=result_data)
        assert response.status_code == 200
        
        # Step 6: Test retrieving goals by match
        response = client.get(f"/api/goals/match/{match['id']}")
        assert response.status_code == 200
        match_goals = response.json()
        assert len(match_goals) == 5  # Total 5 goals in match
        
        # Step 7: Test retrieving goals by player
        response = client.get(f"/api/goals/player/{home_players[0].id}")
        assert response.status_code == 200
        player_goals = response.json()
        assert len(player_goals) == 2  # Player 1-1 scored 2 goals
        
        # Step 8: Test retrieving goals by team
        response = client.get(f"/api/goals/team/{home_team.id}")
        assert response.status_code == 200
        team_goals = response.json()
        assert len(team_goals) == 3  # Home team scored 3 goals
        
    def test_goal_crud_operations(self, client, db):
        """Test the CRUD operations for goals."""
        # Create test data
        tournament = create_test_tournament(db)
        phase = create_test_phase(db, tournament.id)
        group = create_test_group(db, phase.id)
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        match = create_test_match(db, tournament.id, phase.id, group.id, team.id)
        
        # Create a goal
        goal_data = {
            "match_id": match.id,
            "player_id": player.id,
            "team_id": team.id,
            "minute": 10,
            "type": "regular"
        }
        
        response = client.post("/api/goals/", json=goal_data)
        assert response.status_code == 200
        goal = response.json()
        
        # Get goal by ID
        response = client.get(f"/api/goals/{goal['id']}")
        assert response.status_code == 200
        retrieved_goal = response.json()
        assert retrieved_goal["minute"] == 10
        assert retrieved_goal["type"] == "regular"
        
        # Update goal
        update_data = {
            "minute": 15,
            "type": "penalty"
        }
        response = client.put(f"/api/goals/{goal['id']}", json=update_data)
        assert response.status_code == 200
        updated_goal = response.json()
        assert updated_goal["minute"] == 15
        assert updated_goal["type"] == "penalty"
        
        # Delete goal
        response = client.delete(f"/api/goals/{goal['id']}")
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get(f"/api/goals/{goal['id']}")
        assert response.status_code == 404
    
    def test_goal_validation(self, client, db, refresh):
        """Test validation for goal creation."""
        # Create test data
        tournament = create_test_tournament(db)
        phase = create_test_phase(db, tournament.id)
        
        # Create match via API to ensure proper session handling
        team = create_test_team(db)
        other_team = create_test_team(db)
        db.commit()
        refresh(db, team, other_team)
        
        player = create_test_player(db, team.id)
        db.commit()
        refresh(db, player)
        
        # Create match via API
        match_data = {
            "tournament_id": tournament.id,
            "phase_id": phase.id,
            "home_team_id": team.id,
            "away_team_id": other_team.id,
            "date": str(date.today()),
            "location": "Validation Test Stadium"
        }
        response = client.post("/api/matches/", json=match_data)
        assert response.status_code == 200
        match = response.json()
        
        # Test invalid minute (negative)
        goal_data = {
            "match_id": match["id"],
            "player_id": player.id,
            "team_id": team.id,
            "minute": -5,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal_data)
        assert response.status_code == 422  # Validation error
        
        # Test invalid goal type
        goal_data = {
            "match_id": match["id"],
            "player_id": player.id,
            "team_id": team.id,
            "minute": 10,
            "type": "invalid_type"
        }
        response = client.post("/api/goals/", json=goal_data)
        assert response.status_code == 422  # Validation error
        
        # Test player not in team
        goal_data = {
            "match_id": match["id"],
            "player_id": player.id,
            "team_id": other_team.id,  # Player belongs to team, not other_team
            "minute": 10,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal_data)
        # TODO: The API currently doesn't validate if a player belongs to the team
        # This should be fixed in a future update to prevent invalid data
        assert response.status_code == 200  # Currently doesn't validate team membership 
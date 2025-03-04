from datetime import date, timedelta

import pytest

from app.tests.fixtures import (
    create_test_group,
    create_test_phase,
    create_test_player,
    create_test_team,
    create_test_tournament,
)


@pytest.mark.player_stats
class TestPlayerStats:
    """Test the player statistics functionality."""

    def test_player_stats_workflow(self, client, db, refresh):
        """
        Test the complete player statistics workflow.
        
        This test validates:
        1. Setting up tournament, teams, and players
        2. Creating matches and recording goals
        3. Retrieving player statistics
        4. Getting top scorers for a tournament
        """
        # Step 1: Create tournament structure
        tournament = create_test_tournament(db)
        tournament.name = "Player Stats Test Tournament"
        db.commit()
        refresh(db, tournament)
        
        phase = create_test_phase(db, tournament.id)
        group = create_test_group(db, phase.id)
        
        # Step 2: Create teams
        team1 = create_test_team(db)
        team1.name = "Stats Team 1"
        db.commit()
        refresh(db, team1)
        
        team2 = create_test_team(db)
        team2.name = "Stats Team 2"
        db.commit()
        refresh(db, team2)
        
        # Assign teams to group
        for team in [team1, team2]:
            response = client.post(
                f"/api/groups/{group.id}/teams",
                json={"team_id": team.id}
            )
            assert response.status_code == 200
        
        # Step 3: Create players
        player1 = create_test_player(db, team1.id)
        player1.name = "Scorer 1"
        player1.number = 10
        db.commit()
        refresh(db, player1)
        
        player2 = create_test_player(db, team1.id)
        player2.name = "Scorer 2"
        player2.number = 11
        db.commit()
        refresh(db, player2)
        
        player3 = create_test_player(db, team2.id)
        player3.name = "Scorer 3"
        player3.number = 9
        db.commit()
        refresh(db, player3)
        
        # Step 4: Create a match
        match_data = {
            "tournament_id": tournament.id,
            "phase_id": phase.id,
            "group_id": group.id,
            "home_team_id": team1.id,
            "away_team_id": team2.id,
            "date": str(date.today()),
            "location": "Player Stats Stadium"
        }
        response = client.post("/api/matches/", json=match_data)
        assert response.status_code == 200
        match = response.json()
        
        # Step 5: Record goals
        # Player 1 scores twice
        goal1_data = {
            "match_id": match["id"],
            "player_id": player1.id,
            "team_id": team1.id,
            "minute": 10,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal1_data)
        assert response.status_code == 200
        
        goal2_data = {
            "match_id": match["id"],
            "player_id": player1.id,
            "team_id": team1.id,
            "minute": 30,
            "type": "penalty"
        }
        response = client.post("/api/goals/", json=goal2_data)
        assert response.status_code == 200
        
        # Player 2 scores once
        goal3_data = {
            "match_id": match["id"],
            "player_id": player2.id,
            "team_id": team1.id,
            "minute": 50,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal3_data)
        assert response.status_code == 200
        
        # Player 3 scores for team 2
        goal4_data = {
            "match_id": match["id"],
            "player_id": player3.id,
            "team_id": team2.id,
            "minute": 70,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal4_data)
        assert response.status_code == 200
        
        # Update match result
        result_data = {
            "home_score": 3,
            "away_score": 1,
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match['id']}/result", json=result_data)
        assert response.status_code == 200
        
        # Step 6: Calculate player statistics
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament.id}&player_id={player1.id}")
        assert response.status_code == 200
        player1_stats = response.json()[0] if isinstance(response.json(), list) else response.json()
        
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament.id}&player_id={player2.id}")
        assert response.status_code == 200
        player2_stats = response.json()[0] if isinstance(response.json(), list) else response.json()
        
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament.id}&player_id={player3.id}")
        assert response.status_code == 200
        player3_stats = response.json()[0] if isinstance(response.json(), list) else response.json()
        
        # Step 7: Verify player statistics
        # Player 1 should have 2 goals (1 regular, 1 penalty)
        assert player1_stats["player_id"] == player1.id
        assert player1_stats["tournament_id"] == tournament.id
        assert player1_stats["goals_scored"] == 2
        assert player1_stats["matches_played"] == 1
        assert player1_stats["goals_per_match"] == 2.0
        
        # Player 2 should have 1 regular goal
        assert player2_stats["player_id"] == player2.id
        assert player2_stats["goals_scored"] == 1
        assert player2_stats["matches_played"] == 1
        assert player2_stats["goals_per_match"] == 1.0
        
        # Player 3 should have 1 regular goal
        assert player3_stats["player_id"] == player3.id
        assert player3_stats["goals_scored"] == 1
        assert player3_stats["matches_played"] == 1
        assert player3_stats["goals_per_match"] == 1.0
        
        # Step 8: Get top scorers
        response = client.get(f"/api/tournaments/{tournament.id}/top-scorers?limit=3")
        assert response.status_code == 200
        top_scorers = response.json()
        
        # Verify top scorers order (player1 > player2/player3)
        assert len(top_scorers) == 3
        assert top_scorers[0]["player_id"] == player1.id
        assert top_scorers[0]["goals_scored"] == 2
        # Player 2 and 3 both have 1 goal, so either could be second
        assert top_scorers[1]["goals_scored"] == 1
        assert top_scorers[2]["goals_scored"] == 1
    
    def test_player_stats_filtering(self, client, db, refresh):
        """Test filtering player statistics by tournament."""
        # Create two tournaments
        tournament1 = create_test_tournament(db)
        tournament1.name = "Tournament 1"
        db.commit()
        refresh(db, tournament1)
        
        tournament2 = create_test_tournament(db)
        tournament2.name = "Tournament 2"
        db.commit()
        refresh(db, tournament2)
        
        # Create team and player
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        db.commit()
        refresh(db, team, player)
        
        # Create phases
        phase1 = create_test_phase(db, tournament1.id)
        phase2 = create_test_phase(db, tournament2.id)
        
        # Create matches in both tournaments
        match1_data = {
            "tournament_id": tournament1.id,
            "phase_id": phase1.id,
            "home_team_id": team.id,
            "away_team_id": create_test_team(db).id,
            "date": str(date.today()),
            "location": "Test Stadium 1"
        }
        response = client.post("/api/matches/", json=match1_data)
        assert response.status_code == 200
        match1 = response.json()
        
        match2_data = {
            "tournament_id": tournament2.id,
            "phase_id": phase2.id,
            "home_team_id": team.id,
            "away_team_id": create_test_team(db).id,
            "date": str(date.today() + timedelta(days=1)),
            "location": "Test Stadium 2"
        }
        response = client.post("/api/matches/", json=match2_data)
        assert response.status_code == 200
        match2 = response.json()
        
        # Record goals in tournament 1
        goal1_data = {
            "match_id": match1["id"],
            "player_id": player.id,
            "team_id": team.id,
            "minute": 15,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal1_data)
        assert response.status_code == 200
        
        # Record goals in tournament 2
        goal2_data = {
            "match_id": match2["id"],
            "player_id": player.id,
            "team_id": team.id,
            "minute": 25,
            "type": "regular"
        }
        response = client.post("/api/goals/", json=goal2_data)
        assert response.status_code == 200
        
        goal3_data = {
            "match_id": match2["id"],
            "player_id": player.id,
            "team_id": team.id,
            "minute": 35,
            "type": "penalty"
        }
        response = client.post("/api/goals/", json=goal3_data)
        assert response.status_code == 200
        
        # Update player statistics for both tournaments
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament1.id}&player_id={player.id}")
        assert response.status_code == 200
        
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament2.id}&player_id={player.id}")
        assert response.status_code == 200
        
        # Get player statistics for tournament 1
        response = client.get(f"/api/player-stats?tournament_id={tournament1.id}&player_id={player.id}")
        assert response.status_code == 200
        stats1 = response.json()
        
        # Get player statistics for tournament 2
        response = client.get(f"/api/player-stats?tournament_id={tournament2.id}&player_id={player.id}")
        assert response.status_code == 200
        stats2 = response.json()
        
        # Verify different statistics for each tournament
        assert len(stats1) == 1
        assert stats1[0]["tournament_id"] == tournament1.id
        assert stats1[0]["player_id"] == player.id
        assert stats1[0]["goals_scored"] == 1
        assert stats1[0]["matches_played"] == 1
        
        assert len(stats2) == 1
        assert stats2[0]["tournament_id"] == tournament2.id
        assert stats2[0]["player_id"] == player.id
        assert stats2[0]["goals_scored"] == 2
        assert stats2[0]["matches_played"] == 1 
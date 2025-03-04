from datetime import date, timedelta

import pytest

from app.tests.fixtures import (
    create_test_group,
    create_test_match,
    create_test_phase,
    create_test_team,
    create_test_tournament,
)


@pytest.mark.team_stats
class TestTeamStats:
    """Test the team statistics functionality."""

    def test_team_stats_calculation(self, client, db, refresh):
        """
        Test the team statistics calculation based on match results.
        
        This test validates:
        1. Setting up tournament and teams
        2. Creating matches and recording results
        3. Calculating team statistics
        4. Verifying statistics are correct
        """
        # Step 1: Create tournament structure
        tournament = create_test_tournament(db)
        tournament.name = "Team Stats Test Tournament"
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
        
        # Step 3: Create matches
        # Match 1: Team 1 vs Team 2
        match1_data = {
            "tournament_id": tournament.id,
            "phase_id": phase.id,
            "group_id": group.id,
            "home_team_id": team1.id,
            "away_team_id": team2.id,
            "date": str(date.today()),
            "location": "Team Stats Stadium 1"
        }
        response = client.post("/api/matches/", json=match1_data)
        assert response.status_code == 200
        match1 = response.json()
        
        # Match 2: Team 2 vs Team 1
        match2_data = {
            "tournament_id": tournament.id,
            "phase_id": phase.id,
            "group_id": group.id,
            "home_team_id": team2.id,
            "away_team_id": team1.id,
            "date": str(date.today() + timedelta(days=7)),
            "location": "Team Stats Stadium 2"
        }
        response = client.post("/api/matches/", json=match2_data)
        assert response.status_code == 200
        match2 = response.json()
        
        # Step 4: Update match results
        # Match 1: Team 1 wins 2-0
        result1_data = {
            "home_score": 2,
            "away_score": 0,
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match1['id']}/result", json=result1_data)
        assert response.status_code == 200
        
        # Match 2: Draw 1-1
        result2_data = {
            "home_score": 1,
            "away_score": 1,
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match2['id']}/result", json=result2_data)
        assert response.status_code == 200
        
        # Step 5: Update team statistics
        response = client.post(f"/api/team-stats/update/{team1.id}/{tournament.id}")
        assert response.status_code == 200
        team1_stats = response.json()
        
        response = client.post(f"/api/team-stats/update/{team2.id}/{tournament.id}")
        assert response.status_code == 200
        team2_stats = response.json()
        
        # Step 6: Verify Team 1 statistics
        assert team1_stats["team_id"] == team1.id
        assert team1_stats["tournament_id"] == tournament.id
        assert team1_stats["matches_played"] == 2
        assert team1_stats["wins"] == 1
        assert team1_stats["draws"] == 1
        assert team1_stats["losses"] == 0
        assert team1_stats["goals_for"] == 3
        assert team1_stats["goals_against"] == 1
        assert team1_stats["goal_difference"] == 2
        assert team1_stats["points"] == 4
        assert team1_stats["clean_sheets"] == 1
        assert team1_stats["win_percentage"] == 50.0
        assert team1_stats["goals_per_match"] == 1.5
        assert team1_stats["points_per_match"] == 2.0
        
        # Step 7: Verify Team 2 statistics
        assert team2_stats["team_id"] == team2.id
        assert team2_stats["tournament_id"] == tournament.id
        assert team2_stats["matches_played"] == 2
        assert team2_stats["wins"] == 0
        assert team2_stats["draws"] == 1
        assert team2_stats["losses"] == 1
        assert team2_stats["goals_for"] == 1
        assert team2_stats["goals_against"] == 3
        assert team2_stats["goal_difference"] == -2
        assert team2_stats["points"] == 1
        assert team2_stats["clean_sheets"] == 0
        assert team2_stats["win_percentage"] == 0.0
        assert team2_stats["goals_per_match"] == 0.5
        assert team2_stats["points_per_match"] == 0.5
        
        # Step 8: Get tournament rankings
        response = client.get(f"/api/team-stats/tournament/{tournament.id}")
        assert response.status_code == 200
        rankings = response.json()
        
        # Verify rankings
        assert len(rankings) == 2
        assert rankings[0]["team_id"] == team1.id  # Team 1 should be first
        assert rankings[1]["team_id"] == team2.id  # Team 2 should be second
    
    def test_team_stats_filtering(self, client, db, refresh):
        """Test filtering team statistics by tournament and team."""
        # Create two tournaments
        tournament1 = create_test_tournament(db)
        tournament1.name = "Tournament 1"
        db.commit()
        refresh(db, tournament1)
        
        tournament2 = create_test_tournament(db)
        tournament2.name = "Tournament 2"
        db.commit()
        refresh(db, tournament2)
        
        # Create team
        team = create_test_team(db)
        db.commit()
        refresh(db, team)
        
        # Create phases
        phase1 = create_test_phase(db, tournament1.id)
        phase2 = create_test_phase(db, tournament2.id)
        
        # Create opponent teams
        opponent1 = create_test_team(db)
        opponent2 = create_test_team(db)
        db.commit()
        refresh(db, opponent1, opponent2)
        
        # Create matches in both tournaments
        match1_data = {
            "tournament_id": tournament1.id,
            "phase_id": phase1.id,
            "home_team_id": team.id,
            "away_team_id": opponent1.id,
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
            "away_team_id": opponent2.id,
            "date": str(date.today() + timedelta(days=1)),
            "location": "Test Stadium 2"
        }
        response = client.post("/api/matches/", json=match2_data)
        assert response.status_code == 200
        match2 = response.json()
        
        # Update match results
        # Tournament 1: Team wins
        result1_data = {
            "home_score": 2,
            "away_score": 0,
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match1['id']}/result", json=result1_data)
        assert response.status_code == 200
        
        # Tournament 2: Team loses
        result2_data = {
            "home_score": 0,
            "away_score": 3,
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match2['id']}/result", json=result2_data)
        assert response.status_code == 200
        
        # Update team statistics for both tournaments
        response = client.post(f"/api/team-stats/update/{team.id}/{tournament1.id}")
        assert response.status_code == 200
        
        response = client.post(f"/api/team-stats/update/{team.id}/{tournament2.id}")
        assert response.status_code == 200
        
        # Get team statistics for tournament 1
        response = client.get(f"/api/team-stats?tournament_id={tournament1.id}&team_id={team.id}")
        assert response.status_code == 200
        stats1 = response.json()
        
        # Get team statistics for tournament 2
        response = client.get(f"/api/team-stats?tournament_id={tournament2.id}&team_id={team.id}")
        assert response.status_code == 200
        stats2 = response.json()
        
        # Verify different statistics for each tournament
        assert len(stats1) == 1
        assert stats1[0]["tournament_id"] == tournament1.id
        assert stats1[0]["team_id"] == team.id
        assert stats1[0]["wins"] == 1
        assert stats1[0]["losses"] == 0
        
        assert len(stats2) == 1
        assert stats2[0]["tournament_id"] == tournament2.id
        assert stats2[0]["team_id"] == team.id
        assert stats2[0]["wins"] == 0
        assert stats2[0]["losses"] == 1
    
    def test_team_stats_crud_operations(self, client, db):
        """Test the CRUD operations for team statistics."""
        # Create test data
        tournament = create_test_tournament(db)
        team = create_test_team(db)
        
        # Initial stats should not exist
        response = client.get(f"/api/team-stats?tournament_id={tournament.id}&team_id={team.id}")
        assert response.status_code == 200
        initial_stats = response.json()
        assert len(initial_stats) == 0
        
        # Create/update team stats
        response = client.post(f"/api/team-stats/update/{team.id}/{tournament.id}")
        assert response.status_code == 200
        created_stats = response.json()
        
        # Stats should be initialized with zeros
        assert created_stats["matches_played"] == 0
        assert created_stats["wins"] == 0
        assert created_stats["draws"] == 0
        assert created_stats["losses"] == 0
        
        # Create a match and update result to affect stats
        phase = create_test_phase(db, tournament.id)
        opponent = create_test_team(db)
        match = create_test_match(db, tournament.id, phase.id, None, team.id, opponent.id)
        
        result_data = {
            "home_score": 3,
            "away_score": 1,
            "status": "completed"
        }
        response = client.put(f"/api/matches/{match.id}/result", json=result_data)
        assert response.status_code == 200
        
        # Update stats again to reflect match result
        response = client.post(f"/api/team-stats/update/{team.id}/{tournament.id}")
        assert response.status_code == 200
        updated_stats = response.json()
        
        # Verify updated stats
        assert updated_stats["matches_played"] == 1
        assert updated_stats["wins"] == 1
        assert updated_stats["draws"] == 0
        assert updated_stats["losses"] == 0
        assert updated_stats["goals_for"] == 3
        assert updated_stats["goals_against"] == 1 
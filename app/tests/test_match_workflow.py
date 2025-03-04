import pytest
from datetime import date, timedelta

from app.tests.fixtures import (
    create_test_tournament,
    create_test_phase,
    create_test_group,
    create_test_team
)


@pytest.mark.match_workflow
class TestMatchWorkflow:
    """Test the complete match management workflow."""

    def test_match_workflow_complete(self, client, db, refresh):
        """
        Test the complete match workflow from tournament creation to standings calculation.
        
        This is an integration test that validates the complete workflow:
        1. Create tournament structure
        2. Create teams and assign to a group
        3. Create matches between teams
        4. Update match results
        5. Retrieve and verify standings
        """
        # Step 1: Create tournament structure
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, tournament)
        
        phase = create_test_phase(db, tournament.id)
        group = create_test_group(db, phase.id)
        
        # Step 2: Create teams and assign to group
        teams = []
        for i in range(1, 5):
            team = create_test_team(db)
            team.name = f"Team {i}"  # Rename for clarity
            team.short_name = f"T{i}"
            db.commit()
            refresh(db, team)
            teams.append(team)
            
            # Assign team to group
            response = client.post(
                f"/api/groups/{group.id}/teams",
                json={"team_id": team.id}
            )
            assert response.status_code == 200
        
        # Step 3: Create matches between teams
        matches = []
        match_date = date.today() + timedelta(days=7)
        
        # Create matches for all team combinations
        for i, home_team in enumerate(teams):
            for away_team in teams[i+1:]:
                match_data = {
                    "tournament_id": tournament.id,
                    "phase_id": phase.id,
                    "group_id": group.id,
                    "home_team_id": home_team.id,
                    "away_team_id": away_team.id,
                    "date": str(match_date),
                    "location": "Test Field"
                }
                response = client.post("/api/matches/", json=match_data)
                assert response.status_code == 200
                matches.append(response.json())
                match_date += timedelta(days=1)
        
        # Verify correct number of matches created (4 teams = 6 matches)
        assert len(matches) == 6
        
        # Step 4: Update match results
        # Sample results that ensure a clear ranking
        results = [
            (3, 1),  # Team 1 vs Team 2: 3-1
            (2, 2),  # Team 1 vs Team 3: 2-2
            (1, 0),  # Team 1 vs Team 4: 1-0
            (0, 2),  # Team 2 vs Team 3: 0-2
            (2, 1),  # Team 2 vs Team 4: 2-1
            (3, 3),  # Team 3 vs Team 4: 3-3
        ]
        
        for match, (home_score, away_score) in zip(matches, results):
            result_data = {
                "home_score": home_score,
                "away_score": away_score,
                "status": "completed"
            }
            response = client.put(f"/api/matches/{match['id']}/result", json=result_data)
            assert response.status_code == 200
            updated_match = response.json()
            assert updated_match["home_score"] == home_score
            assert updated_match["away_score"] == away_score
            assert updated_match["status"] == "completed"
        
        # Step 5: Get standings and verify
        response = client.get(f"/api/standings/group/{group.id}")
        assert response.status_code == 200
        standings = response.json()
        
        # Verify standings calculation
        assert len(standings) == 4  # Should have 4 teams
        
        # Check first place team (Team 1: 7 points from 2W, 1D)
        first_place = next(s for s in standings if s["team_name"] == "Team 1")
        assert first_place["matches_played"] == 3
        assert first_place["wins"] == 2
        assert first_place["draws"] == 1
        assert first_place["losses"] == 0
        assert first_place["points"] == 7
        
        # Check second place team (Team 3: 5 points from 1W, 2D)
        second_place = next(s for s in standings if s["team_name"] == "Team 3")
        assert second_place["matches_played"] == 3
        assert second_place["wins"] == 1
        assert second_place["draws"] == 2
        assert second_place["losses"] == 0
        assert second_place["points"] == 5
        
        # Check third place team (Team 2: 3 points from 1W, 0D, 2L)
        third_place = next(s for s in standings if s["team_name"] == "Team 2")
        assert third_place["matches_played"] == 3
        assert third_place["wins"] == 1
        assert third_place["draws"] == 0
        assert third_place["losses"] == 2
        assert third_place["points"] == 3
        
        # Check fourth place team (Team 4: 1 point from 0W, 1D, 2L)
        fourth_place = next(s for s in standings if s["team_name"] == "Team 4")
        assert fourth_place["matches_played"] == 3
        assert fourth_place["wins"] == 0
        assert fourth_place["draws"] == 1
        assert fourth_place["losses"] == 2
        assert fourth_place["points"] == 1
    
    def test_tournament_phase_group_creation(self, client, db):
        """Test the creation of tournament structure."""
        # Create tournament
        tournament_data = {
            "name": "Test Tournament",
            "edition": "I",
            "year": 2023,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=30)),
            "description": "Tournament for testing"
        }
        response = client.post("/api/tournaments/", json=tournament_data)
        assert response.status_code == 200
        tournament = response.json()
        
        # Create phase
        phase_data = {
            "name": "Group Phase",
            "order": 1,
            "type": "group",
            "tournament_id": tournament["id"]
        }
        response = client.post("/api/phases/", json=phase_data)
        assert response.status_code == 200
        phase = response.json()
        
        # Create group
        group_data = {
            "name": "Group A",
            "phase_id": phase["id"]
        }
        response = client.post("/api/groups/", json=group_data)
        assert response.status_code == 200
        group = response.json()
        
        # Verify relationships
        assert group["phase_id"] == phase["id"]
        assert phase["tournament_id"] == tournament["id"]
        
    def test_team_assignment_to_group(self, client, db, refresh):
        """Test assigning teams to a group."""
        # Create tournament structure
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, tournament)
        
        phase = create_test_phase(db, tournament.id)
        group = create_test_group(db, phase.id)
        
        # Create teams
        teams = []
        for i in range(4):
            team = create_test_team(db)
            db.commit()
            refresh(db, team)
            teams.append(team)
        
        # Assign teams to group
        for team in teams:
            response = client.post(
                f"/api/groups/{group.id}/teams",
                json={"team_id": team.id}
            )
            assert response.status_code == 200
        
        # Verify assignments
        response = client.get(f"/api/groups/{group.id}")
        assert response.status_code == 200
        group_data = response.json()
        assert "teams" in group_data
        assert len(group_data["teams"]) == 4
        
        # Ensure all team IDs are in the response
        team_ids = [team.id for team in teams]
        response_team_ids = [team["id"] for team in group_data["teams"]]
        for team_id in team_ids:
            assert team_id in response_team_ids 
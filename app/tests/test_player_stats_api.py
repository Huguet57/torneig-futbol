
from app.tests.fixtures import (
    create_test_group,
    create_test_phase,
    create_test_player,
    create_test_team,
    create_test_tournament,
)


class TestPlayerStatsAPI:
    # Use the client fixture from conftest.py instead of creating a new one
    # This ensures the test database is used
    # @pytest.fixture
    # def client(self):
    #     return TestClient(app)

    def test_create_player_stats(self, client, db, refresh):
        """Test creating player statistics."""
        # Create test prerequisites
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, team, player, tournament)

        stats_data = {
            "player_id": player.id,
            "tournament_id": tournament.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        response = client.post("/api/player-stats/", json=stats_data)
        assert response.status_code == 200
        data = response.json()
        assert data["player_id"] == player.id
        assert data["tournament_id"] == tournament.id
        assert data["matches_played"] == 5
        assert data["goals_scored"] == 3
        assert data["minutes_played"] == 450
        
        # Check calculated fields
        assert "goals_per_match" in data
        assert data["goals_per_match"] == 0.6  # 3 goals / 5 matches

    def test_create_player_stats_invalid_player(self, client, db, refresh):
        """Test creating player statistics with invalid player ID."""
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, tournament)

        stats_data = {
            "player_id": 9999,  # Non-existent player
            "tournament_id": tournament.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        response = client.post("/api/player-stats/", json=stats_data)
        assert response.status_code == 404
        assert "Player" in response.json()["detail"]

    def test_create_player_stats_invalid_tournament(self, client, db, refresh):
        """Test creating player statistics with invalid tournament ID."""
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        db.commit()
        refresh(db, team, player)

        stats_data = {
            "player_id": player.id,
            "tournament_id": 9999,  # Non-existent tournament
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        response = client.post("/api/player-stats/", json=stats_data)
        assert response.status_code == 404
        assert "Tournament" in response.json()["detail"]

    def test_create_duplicate_player_stats(self, client, db, refresh):
        """Test creating duplicate player statistics for the same player/tournament."""
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, team, player, tournament)

        stats_data = {
            "player_id": player.id,
            "tournament_id": tournament.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        # First creation should succeed
        response = client.post("/api/player-stats/", json=stats_data)
        assert response.status_code == 200

        # Second creation should fail with 400 Bad Request
        response = client.post("/api/player-stats/", json=stats_data)
        assert response.status_code == 400
        assert "statistics already exist for player" in response.json()["detail"].lower()

    def test_get_player_stats(self, client, db, refresh):
        """Test retrieving player statistics."""
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, team, player, tournament)

        # Create player stats
        stats_data = {
            "player_id": player.id,
            "tournament_id": tournament.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        create_response = client.post("/api/player-stats/", json=stats_data)
        assert create_response.status_code == 200
        created_stats = create_response.json()
        stats_id = created_stats["id"]

        # Get the stats by ID
        response = client.get(f"/api/player-stats/{stats_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == stats_id
        assert data["player_id"] == player.id
        assert data["tournament_id"] == tournament.id
        assert data["matches_played"] == 5
        assert data["goals_scored"] == 3

    def test_get_nonexistent_player_stats(self, client):
        """Test retrieving non-existent player statistics."""
        response = client.get("/api/player-stats/9999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_player_stats(self, client, db, refresh):
        """Test updating player statistics."""
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, team, player, tournament)

        # Create player stats
        stats_data = {
            "player_id": player.id,
            "tournament_id": tournament.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        create_response = client.post("/api/player-stats/", json=stats_data)
        assert create_response.status_code == 200
        created_stats = create_response.json()
        stats_id = created_stats["id"]

        # Update the stats
        update_data = {
            "matches_played": 8,
            "goals_scored": 5,
            "minutes_played": 720
        }

        response = client.put(f"/api/player-stats/{stats_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == stats_id
        assert data["player_id"] == player.id
        assert data["tournament_id"] == tournament.id
        assert data["matches_played"] == 8
        assert data["goals_scored"] == 5
        assert data["minutes_played"] == 720
        
        # Check recalculated fields
        assert data["goals_per_match"] == 0.625  # 5 goals / 8 matches

    def test_delete_player_stats(self, client, db, refresh):
        """Test deleting player statistics."""
        team = create_test_team(db)
        player = create_test_player(db, team.id)
        tournament = create_test_tournament(db)
        db.commit()
        refresh(db, team, player, tournament)

        # Create player stats
        stats_data = {
            "player_id": player.id,
            "tournament_id": tournament.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }

        create_response = client.post("/api/player-stats/", json=stats_data)
        assert create_response.status_code == 200
        created_stats = create_response.json()
        stats_id = created_stats["id"]

        # Delete the stats
        response = client.delete(f"/api/player-stats/{stats_id}")
        assert response.status_code == 200

        # Verify stats are deleted
        get_response = client.get(f"/api/player-stats/{stats_id}")
        assert get_response.status_code == 404

    def test_update_stats_from_goals(self, client, db, refresh):
        """Test updating player statistics based on goals."""
        # Set up test data
        tournament = create_test_tournament(db)
        phase = create_test_phase(db, tournament.id)
        group = create_test_group(db, phase.id)
    
        # Create teams
        team1 = create_test_team(db)
        team1.name = "Team 1"
        team2 = create_test_team(db)
        team2.name = "Team 2"
        db.commit()
        refresh(db, team1, team2)
    
        # Create players
        player1 = create_test_player(db, team1.id)
        player1.name = "Player 1"
        player2 = create_test_player(db, team1.id)
        player2.name = "Player 2"
        db.commit()
        refresh(db, player1, player2)
    
        # Create a match
        match_data = {
            "tournament_id": tournament.id,
            "phase_id": phase.id,
            "group_id": group.id,
            "home_team_id": team1.id,
            "away_team_id": team2.id,
            "date": "2023-06-01",
            "location": "Test Stadium"
        }
    
        match_response = client.post("/api/matches/", json=match_data)
        assert match_response.status_code == 200
        match_id = match_response.json()["id"]
    
        # Create goals for player1
        for i in range(3):
            goal_data = {
                "match_id": match_id,
                "player_id": player1.id,
                "team_id": team1.id,
                "minute": 10 + i*10,
                "type": "regular"
            }
            response = client.post("/api/goals/", json=goal_data)
            assert response.status_code == 200
    
        # Create goals for player2
        for i in range(1):
            goal_data = {
                "match_id": match_id,
                "player_id": player2.id,
                "team_id": team1.id,
                "minute": 70,
                "type": "regular"
            }
            response = client.post("/api/goals/", json=goal_data)
            assert response.status_code == 200
    
        # Update stats from goals for specific player
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament.id}&player_id={player1.id}")
        assert response.status_code == 200
        data = response.json()
        
        # The response is a list, so we need to check the first item
        assert len(data) > 0
        assert data[0]["player_id"] == player1.id
        
        # Update stats from goals for all players
        response = client.post(f"/api/player-stats/update-from-goals/?tournament_id={tournament.id}")
        assert response.status_code == 200
        data = response.json()
        
        # Should have stats for both players
        assert len(data) >= 2
        
        # Find player1's stats in the list
        player1_stats = next((stats for stats in data if stats["player_id"] == player1.id), None)
        assert player1_stats is not None
        assert player1_stats["goals_scored"] == 3
        
        # Find player2's stats in the list
        player2_stats = next((stats for stats in data if stats["player_id"] == player2.id), None)
        assert player2_stats is not None
        assert player2_stats["goals_scored"] == 1

    def test_filter_player_stats(self, client, db, refresh):
        """Test filtering player statistics by tournament or player."""
        # Create test data
        tournament1 = create_test_tournament(db)
        tournament1.name = "Tournament 1"
        tournament2 = create_test_tournament(db)
        tournament2.name = "Tournament 2"

        team = create_test_team(db)

        player1 = create_test_player(db, team.id)
        player1.name = "Player 1"
        player2 = create_test_player(db, team.id)
        player2.name = "Player 2"
        db.commit()
        refresh(db, tournament1, tournament2, team, player1, player2)

        # Create stats for player1 in tournament1
        stats1_data = {
            "player_id": player1.id,
            "tournament_id": tournament1.id,
            "matches_played": 5,
            "goals_scored": 3,
            "minutes_played": 450
        }
        client.post("/api/player-stats/", json=stats1_data)

        # Create stats for player1 in tournament2
        stats2_data = {
            "player_id": player1.id,
            "tournament_id": tournament2.id,
            "matches_played": 4,
            "goals_scored": 2,
            "minutes_played": 360
        }
        client.post("/api/player-stats/", json=stats2_data)

        # Create stats for player2 in tournament1
        stats3_data = {
            "player_id": player2.id,
            "tournament_id": tournament1.id,
            "matches_played": 6,
            "goals_scored": 5,
            "minutes_played": 540
        }
        client.post("/api/player-stats/", json=stats3_data)

        # Test filtering by tournament only
        response = client.get(f"/api/player-stats/?tournament_id={tournament1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Should have stats for both players in tournament1
        
        # Test filtering by player only
        response = client.get(f"/api/player-stats/?player_id={player1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # Should have stats for player1 in both tournaments
        
        # Test filtering by both tournament and player
        response = client.get(f"/api/player-stats/?tournament_id={tournament1.id}&player_id={player1.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1  # Should have stats for player1 in tournament1 only
        assert data[0]["player_id"] == player1.id
        assert data[0]["tournament_id"] == tournament1.id
        assert data[0]["matches_played"] == 5
        assert data[0]["goals_scored"] == 3
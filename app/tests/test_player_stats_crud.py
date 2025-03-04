from sqlalchemy.orm import Session
from datetime import date

from app.crud.player_stats import player_stats
from app.models.player import Player
from app.models.team import Team
from app.models.tournament import Tournament
from app.models.match import Match
from app.models.goal import Goal
from app.schemas.player_stats import PlayerStatsCreate

class TestPlayerStatsCRUD:
    """Test the CRUD operations for player statistics."""
    
    def test_get_by_player_id(self, db: Session):
        """Test getting player stats by player ID."""
        # Create a team
        team = Team(name="Test Team", short_name="TST", city="Test City")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Create player stats
        stats = player_stats.create_for_player(db, player.id)
        
        # Get player stats by player ID
        retrieved_stats = player_stats.get_by_player_id(db, player.id)
        
        assert retrieved_stats is not None
        assert retrieved_stats.player_id == player.id
        assert retrieved_stats.matches_played == 0
        assert retrieved_stats.goals_scored == 0
    
    def test_create_for_player(self, db: Session):
        """Test creating statistics for a player."""
        # Create a team
        team = Team(name="Test Team 2", short_name="TT2", city="Test City 2")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 2", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        db.add(tournament)
        db.commit()
        
        # Create player stats with tournament
        stats = player_stats.create_for_player(db, player.id, tournament.id)
        
        assert stats is not None
        assert stats.player_id == player.id
        assert stats.tournament_id == tournament.id
        assert stats.matches_played == 0
        assert stats.goals_scored == 0
        assert stats.minutes_played == 0
        assert stats.goals_per_match == 0.0
        assert stats.minutes_per_goal == 0.0
    
    def test_remove(self, db: Session):
        """Test removing player statistics."""
        # Create a team
        team = Team(name="Test Team 3", short_name="TT3", city="Test City 3")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 3", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Create player stats
        stats = player_stats.create_for_player(db, player.id)
        
        # Remove stats
        removed_stats = player_stats.remove(db, id=stats.id)
        
        # Try to get the removed stats
        retrieved_stats = player_stats.get(db, id=stats.id)
        
        assert removed_stats is not None
        assert retrieved_stats is None
    
    def test_update_stats_from_match(self, db: Session):
        """Test updating player statistics after a match."""
        # Create a team
        team = Team(name="Test Team 4", short_name="TT4", city="Test City 4")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 4", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Update stats with match data
        updated_stats = player_stats.update_stats_from_match(
            db, player.id, minutes_played=90, goals_scored=2
        )
        
        assert updated_stats is not None
        assert updated_stats.player_id == player.id
        assert updated_stats.matches_played == 1
        assert updated_stats.goals_scored == 2
        assert updated_stats.minutes_played == 90
        assert updated_stats.goals_per_match == 2.0
        assert updated_stats.minutes_per_goal == 45.0
        
        # Update again with another match
        updated_stats = player_stats.update_stats_from_match(
            db, player.id, minutes_played=70, goals_scored=1
        )
        
        assert updated_stats.matches_played == 2
        assert updated_stats.goals_scored == 3
        assert updated_stats.minutes_played == 160
        assert updated_stats.goals_per_match == 1.5
        assert round(updated_stats.minutes_per_goal, 1) == 53.3
    
    def test_get_tournament_top_scorers(self, db: Session):
        """Test getting top scorers for a tournament."""
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament 2",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        db.add(tournament)
        db.commit()
        
        # Create teams
        team1 = Team(name="Team A", short_name="TA", city="City A")
        team2 = Team(name="Team B", short_name="TB", city="City B")
        db.add_all([team1, team2])
        db.commit()
        
        # Create players
        player1 = Player(name="Player 1", team_id=team1.id)
        player2 = Player(name="Player 2", team_id=team1.id)
        player3 = Player(name="Player 3", team_id=team2.id)
        db.add_all([player1, player2, player3])
        db.commit()
        
        # Create matches
        match1 = Match(
            tournament_id=tournament.id,
            home_team_id=team1.id,
            away_team_id=team2.id,
            date=date(2023, 6, 10),
            status="completed",
            home_score=3,
            away_score=1
        )
        match2 = Match(
            tournament_id=tournament.id,
            home_team_id=team2.id,
            away_team_id=team1.id,
            date=date(2023, 6, 15),
            status="completed",
            home_score=0,
            away_score=2
        )
        db.add_all([match1, match2])
        db.commit()
        
        # Create goals
        goals = [
            Goal(match_id=match1.id, player_id=player1.id, minute=10, team_id=team1.id),
            Goal(match_id=match1.id, player_id=player1.id, minute=25, team_id=team1.id),
            Goal(match_id=match1.id, player_id=player2.id, minute=40, team_id=team1.id),
            Goal(match_id=match1.id, player_id=player3.id, minute=75, team_id=team2.id),
            Goal(match_id=match2.id, player_id=player1.id, minute=55, team_id=team1.id),
            Goal(match_id=match2.id, player_id=player2.id, minute=88, team_id=team1.id),
        ]
        db.add_all(goals)
        db.commit()
        
        # Get top scorers
        top_scorers = player_stats.get_tournament_top_scorers(db, tournament.id)
        
        assert len(top_scorers) > 0
        assert top_scorers[0].player_id == player1.id
        assert top_scorers[0].goals_scored == 3
        assert top_scorers[1].player_id == player2.id
        assert top_scorers[1].goals_scored == 2
        
    def test_get_by_player_tournament(self, db: Session):
        """Test getting player stats for a specific player in a specific tournament."""
        # Create a team
        team = Team(name="Test Team 5", short_name="TT5", city="Test City 5")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 5", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament 3",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        db.add(tournament)
        db.commit()
        
        # Create player stats
        stats = player_stats.create_for_player(db, player.id, tournament.id)
        
        # Get player stats by player and tournament
        retrieved_stats = player_stats.get_by_player_tournament(
            db, player_id=player.id, tournament_id=tournament.id
        )
        
        assert retrieved_stats is not None
        assert retrieved_stats.player_id == player.id
        assert retrieved_stats.tournament_id == tournament.id
    
    def test_get_by_tournament(self, db: Session):
        """Test getting all player stats for a tournament."""
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament 4",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        db.add(tournament)
        db.commit()
        
        # Create a team
        team = Team(name="Test Team 6", short_name="TT6", city="Test City 6")
        db.add(team)
        db.commit()
        
        # Create players
        player1 = Player(name="Player A", team_id=team.id)
        player2 = Player(name="Player B", team_id=team.id)
        db.add_all([player1, player2])
        db.commit()
        
        # Create player stats
        stats1 = player_stats.create_for_player(db, player1.id, tournament.id)
        stats2 = player_stats.create_for_player(db, player2.id, tournament.id)
        
        # Get stats by tournament
        tournament_stats = player_stats.get_by_tournament(db, tournament_id=tournament.id)
        
        assert len(tournament_stats) == 2
        assert any(s.player_id == player1.id for s in tournament_stats)
        assert any(s.player_id == player2.id for s in tournament_stats)
    
    def test_get_by_player(self, db: Session):
        """Test getting all stats for a player across tournaments."""
        # Create a team
        team = Team(name="Test Team 7", short_name="TT7", city="Test City 7")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 7", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Create tournaments
        tournament1 = Tournament(
            name="Tournament 1",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        tournament2 = Tournament(
            name="Tournament 2",
            edition="2024",
            year=2024,
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 30)
        )
        db.add_all([tournament1, tournament2])
        db.commit()
        
        # Create player stats for different tournaments
        stats1 = player_stats.create_for_player(db, player.id, tournament1.id)
        stats2 = player_stats.create_for_player(db, player.id, tournament2.id)
        
        # Get stats by player
        player_all_stats = player_stats.get_by_player(db, player_id=player.id)
        
        assert len(player_all_stats) == 2
        assert any(s.tournament_id == tournament1.id for s in player_all_stats)
        assert any(s.tournament_id == tournament2.id for s in player_all_stats)
    
    def test_create_or_update(self, db: Session):
        """Test creating or updating player stats."""
        # Create a team
        team = Team(name="Test Team 8", short_name="TT8", city="Test City 8")
        db.add(team)
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 8", team_id=team.id)
        db.add(player)
        db.commit()
        
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament 5",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        db.add(tournament)
        db.commit()
        
        # Create player stats data
        stats_data = PlayerStatsCreate(
            player_id=player.id,
            tournament_id=tournament.id,
            matches_played=5,
            goals_scored=3,
            minutes_played=450
        )
        
        # Create new stats
        new_stats = player_stats.create_or_update(db, obj_in=stats_data)
        
        assert new_stats is not None
        assert new_stats.player_id == player.id
        assert new_stats.tournament_id == tournament.id
        assert new_stats.matches_played == 5
        assert new_stats.goals_scored == 3
        assert new_stats.minutes_played == 450
        
        # Update existing stats
        updated_data = {
            "player_id": player.id,
            "tournament_id": tournament.id,
            "matches_played": 8,
            "goals_scored": 5,
            "minutes_played": 720
        }
        
        updated_stats = player_stats.create_or_update(db, obj_in=updated_data)
        
        assert updated_stats is not None
        assert updated_stats.player_id == player.id
        assert updated_stats.tournament_id == tournament.id
        assert updated_stats.matches_played == 8
        assert updated_stats.goals_scored == 5
        assert updated_stats.minutes_played == 720
    
    def test_update_stats_from_goals(self, db: Session):
        """Test updating player stats based on goals scored in the tournament."""
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament 6",
            edition="2023",
            year=2023,
            start_date=date(2023, 6, 1),
            end_date=date(2023, 6, 30)
        )
        db.add(tournament)
        db.commit()
        
        # Create teams
        team1 = Team(name="Team C", short_name="TC", city="City C")
        team2 = Team(name="Team D", short_name="TD", city="City D")
        db.add_all([team1, team2])
        db.commit()
        
        # Create a player
        player = Player(name="Test Player 9", team_id=team1.id)
        db.add(player)
        db.commit()
        
        # Create matches
        match1 = Match(
            tournament_id=tournament.id,
            home_team_id=team1.id,
            away_team_id=team2.id,
            date=date(2023, 6, 10),
            status="completed",
            home_score=2,
            away_score=1
        )
        match2 = Match(
            tournament_id=tournament.id,
            home_team_id=team2.id,
            away_team_id=team1.id,
            date=date(2023, 6, 15),
            status="completed",
            home_score=0,
            away_score=1
        )
        db.add_all([match1, match2])
        db.commit()
        
        # Create goals
        goals = [
            Goal(match_id=match1.id, player_id=player.id, minute=10, team_id=team1.id),
            Goal(match_id=match1.id, player_id=player.id, minute=25, team_id=team1.id),
            Goal(match_id=match2.id, player_id=player.id, minute=55, team_id=team1.id),
        ]
        db.add_all(goals)
        db.commit()
        
        # Update stats from goals
        updated_stats = player_stats.update_stats_from_goals(
            db, player_id=player.id, tournament_id=tournament.id
        )
        
        assert updated_stats is not None
        assert updated_stats.player_id == player.id
        assert updated_stats.tournament_id == tournament.id
        assert updated_stats.goals_scored == 3
        assert updated_stats.matches_played == 2  # 2 different matches with goals
        assert updated_stats.minutes_played == 180  # 2 matches * 90 minutes per match 
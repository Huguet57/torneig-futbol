"""Test module for standings calculation functionality."""
import pytest
from sqlalchemy.orm import Session

from app.core.standings import calculate_group_standings
from app.models.group import Group
from app.models.match import Match
from app.models.phase import Phase
from app.models.team import Team
from app.models.tournament import Tournament


@pytest.fixture
def tournament(db: Session):
    tournament = Tournament(name="Test Tournament", year=2024)
    db.add(tournament)
    db.commit()
    return tournament


@pytest.fixture
def phase(db: Session, tournament):
    phase = Phase(name="Group Phase", tournament_id=tournament.id)
    db.add(phase)
    db.commit()
    return phase


@pytest.fixture
def group(db: Session, phase):
    group = Group(name="Group A", phase_id=phase.id)
    db.add(group)
    db.commit()
    return group


@pytest.fixture
def teams(db: Session, group):
    teams = []
    team_data = [
        ("Team A", "TA"),
        ("Team B", "TB"),
        ("Team C", "TC"),
        ("Team D", "TD"),
    ]
    
    for name, short_name in team_data:
        team = Team(name=name, short_name=short_name)
        db.add(team)
        db.commit()
        group.teams.append(team)
        teams.append(team)
    
    db.commit()
    return teams


@pytest.mark.standings
class TestStandings:
    """Test cases for standings calculation."""
    
    def test_empty_group_standings(self, db: Session, group):
        """Test standings calculation for an empty group."""
        standings = calculate_group_standings(db, group.id)
        assert len(standings) == 0
    
    def test_group_with_no_matches(self, db: Session, group, teams):
        """Test standings calculation for a group with teams but no matches."""
        standings = calculate_group_standings(db, group.id)
        assert len(standings) == 4
        for standing in standings:
            assert standing.matches_played == 0
            assert standing.points == 0
            assert standing.goal_difference == 0
    
    def test_single_match_standings(self, db: Session, group, teams):
        """Test standings calculation after a single match."""
        # Create a match where Team A beats Team B 2-0
        match = Match(
            tournament_id=group.phase.tournament_id,
            phase_id=group.phase_id,
            group_id=group.id,
            home_team_id=teams[0].id,
            away_team_id=teams[1].id,
            home_score=2,
            away_score=0,
            status="completed"
        )
        db.add(match)
        db.commit()
        
        standings = calculate_group_standings(db, group.id)
        
        # Verify Team A (winner) standings
        winner = next(s for s in standings if s.team_id == teams[0].id)
        assert winner.matches_played == 1
        assert winner.wins == 1
        assert winner.points == 3
        assert winner.goals_for == 2
        assert winner.goals_against == 0
        assert winner.goal_difference == 2
        
        # Verify Team B (loser) standings
        loser = next(s for s in standings if s.team_id == teams[1].id)
        assert loser.matches_played == 1
        assert loser.losses == 1
        assert loser.points == 0
        assert loser.goals_for == 0
        assert loser.goals_against == 2
        assert loser.goal_difference == -2
        
        # Verify uninvolved teams
        for team in teams[2:]:
            standing = next(s for s in standings if s.team_id == team.id)
            assert standing.matches_played == 0
            assert standing.points == 0
    
    def test_draw_match_standings(self, db: Session, group, teams):
        """Test standings calculation for a drawn match."""
        match = Match(
            tournament_id=group.phase.tournament_id,
            phase_id=group.phase_id,
            group_id=group.id,
            home_team_id=teams[0].id,
            away_team_id=teams[1].id,
            home_score=1,
            away_score=1,
            status="completed"
        )
        db.add(match)
        db.commit()
        
        standings = calculate_group_standings(db, group.id)
        
        # Both teams should have 1 point and same stats
        for team_id in [teams[0].id, teams[1].id]:
            standing = next(s for s in standings if s.team_id == team_id)
            assert standing.matches_played == 1
            assert standing.draws == 1
            assert standing.points == 1
            assert standing.goals_for == 1
            assert standing.goals_against == 1
            assert standing.goal_difference == 0
    
    def test_standings_sorting(self, db: Session, group, teams):
        """Test standings are correctly sorted by points, goal difference, and goals scored."""
        matches = [
            # Team A beats Team B 2-0
            Match(
                tournament_id=group.phase.tournament_id,
                phase_id=group.phase_id,
                group_id=group.id,
                home_team_id=teams[0].id,
                away_team_id=teams[1].id,
                home_score=2,
                away_score=0,
                status="completed"
            ),
            # Team C beats Team D 3-1
            Match(
                tournament_id=group.phase.tournament_id,
                phase_id=group.phase_id,
                group_id=group.id,
                home_team_id=teams[2].id,
                away_team_id=teams[3].id,
                home_score=3,
                away_score=1,
                status="completed"
            )
        ]
        
        for match in matches:
            db.add(match)
        db.commit()
        
        standings = calculate_group_standings(db, group.id)
        
        # Both Team A and Team C have 3 points, but Team C should be first due to better goal difference
        assert standings[0].team_id == teams[2].id  # Team C (goal diff: +2, goals for: 3)
        assert standings[1].team_id == teams[0].id  # Team A (goal diff: +2, goals for: 2)
        # Team D should be third due to having scored more goals than Team B
        assert standings[2].team_id == teams[3].id  # Team D (goal diff: -2, goals for: 1)
        assert standings[3].team_id == teams[1].id  # Team B (goal diff: -2, goals for: 0)
    
    def test_incomplete_match_exclusion(self, db: Session, group, teams):
        """Test that incomplete matches are not included in standings calculation."""
        # Add one completed and one incomplete match
        completed_match = Match(
            tournament_id=group.phase.tournament_id,
            phase_id=group.phase_id,
            group_id=group.id,
            home_team_id=teams[0].id,
            away_team_id=teams[1].id,
            home_score=2,
            away_score=0,
            status="completed"
        )
        
        incomplete_match = Match(
            tournament_id=group.phase.tournament_id,
            phase_id=group.phase_id,
            group_id=group.id,
            home_team_id=teams[2].id,
            away_team_id=teams[3].id,
            status="scheduled"
        )
        
        db.add(completed_match)
        db.add(incomplete_match)
        db.commit()
        
        standings = calculate_group_standings(db, group.id)
        
        # Teams from incomplete match should have no points or matches played
        for team_id in [teams[2].id, teams[3].id]:
            standing = next(s for s in standings if s.team_id == team_id)
            assert standing.matches_played == 0
            assert standing.points == 0 
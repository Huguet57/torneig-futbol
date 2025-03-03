from datetime import date
from app.models.tournament import Tournament
from app.models.team import Team
from app.models.phase import Phase
from app.models.group import Group
from app.models.player import Player
from app.models.match import Match


def create_test_tournament(db):
    """Create a test tournament"""
    tournament = Tournament(
        name="Test Tournament",
        edition="I",
        year=2023,
        start_date=date(2023, 6, 1),
        end_date=date(2023, 6, 30),
        description="Test tournament for unit tests",
        logo_url=None,
    )
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament


def create_test_team(db):
    """Create a test team"""
    team = Team(
        name="Test Team",
        short_name="TEST",
        logo_url=None,
        city="Test City",
        colors="Red/White",
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def create_test_phase(db, tournament_id):
    """Create a test phase"""
    phase = Phase(
        tournament_id=tournament_id, name="Group Phase", order=1, type="group"
    )
    db.add(phase)
    db.commit()
    db.refresh(phase)
    return phase


def create_test_group(db, phase_id):
    """Create a test group"""
    group = Group(phase_id=phase_id, name="Group A")
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def create_test_player(db, team_id):
    """Create a test player"""
    player = Player(
        team_id=team_id,
        name="John Doe",
        number=10,
        position="Forward",
        is_goalkeeper=False,
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def add_team_to_group(db, team, group):
    """Add a team to a group"""
    group.teams.append(team)
    db.commit()
    db.refresh(group)
    return group


def create_test_match(db, tournament_id, phase_id, group_id=None, home_team_id=None, away_team_id=None):
    """Create a test match"""
    # If team IDs are not provided, create teams
    if home_team_id is None:
        home_team = create_test_team(db)
        home_team_id = home_team.id
    
    if away_team_id is None:
        away_team = create_test_team(db)
        away_team_id = away_team.id
    
    match = Match(
        tournament_id=tournament_id,
        phase_id=phase_id,
        group_id=group_id,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        date=date(2023, 6, 15),
        location="Test Stadium",
        status="scheduled"
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

#!/usr/bin/env python
"""
Database initialization script for torneig-futbol.

This script populates the database with initial test data:
- 1 tournament
- 2 phases (group and knockout)
- 2 groups in the group phase
- 8 teams (4 per group)
- Players for each team
- Matches between teams in each group
"""
import os
import sys
from datetime import date, timedelta
from typing import List, NoReturn
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models import (
    Tournament, Phase, Group, Team, Player, Match,
    Goal, TeamStats
)

def init_db() -> None:
    """Initialize the database with test data."""
    print("Initializing database with test data...")
    
    # Create a database session
    db: Session = SessionLocal()
    
    try:
        # Create a tournament
        tournament = Tournament(
            name="Test Tournament",
            edition="I",
            year=2023,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            description="A test tournament for the Soccer Tournament Management System"
        )
        db.add(tournament)
        db.commit()
        db.refresh(tournament)
        print(f"Created tournament: {tournament.name} (ID: {tournament.id})")
        
        # Create phases
        group_phase = Phase(
            tournament_id=tournament.id,
            name="Group Phase",
            order=1,
            type="group"
        )
        knockout_phase = Phase(
            tournament_id=tournament.id,
            name="Knockout Phase",
            order=2,
            type="elimination"
        )
        db.add_all([group_phase, knockout_phase])
        db.commit()
        db.refresh(group_phase)
        db.refresh(knockout_phase)
        print(f"Created phases: {group_phase.name}, {knockout_phase.name}")
        
        # Create groups
        group_a = Group(phase_id=group_phase.id, name="Group A")
        group_b = Group(phase_id=group_phase.id, name="Group B")
        db.add_all([group_a, group_b])
        db.commit()
        db.refresh(group_a)
        db.refresh(group_b)
        print(f"Created groups: {group_a.name}, {group_b.name}")
        
        # Create teams
        teams: List[Team] = []
        for i in range(1, 9):
            team = Team(
                name=f"Team {i}",
                short_name=f"T{i}",
                city=f"City {i}",
                colors=f"Color {i}"
            )
            teams.append(team)
        
        db.add_all(teams)
        db.commit()
        for team in teams:
            db.refresh(team)
        print(f"Created {len(teams)} teams")
        
        # Assign teams to groups
        for i, team in enumerate(teams):
            if i < 4:
                group_a.teams.append(team)
            else:
                group_b.teams.append(team)
        db.commit()
        print("Assigned teams to groups")
        
        # Create players for each team
        for team in teams:
            for j in range(1, 12):
                player = Player(
                    team_id=team.id,
                    name=f"Player {j} of {team.name}",
                    number=j,
                    position="Forward" if j <= 3 else "Midfielder" if j <= 6 else "Defender" if j <= 10 else "Goalkeeper",
                    is_goalkeeper=j == 11
                )
                db.add(player)
        db.commit()
        print("Created players for each team")
        
        # Create matches within each group
        today = date.today()
        matches: List[Match] = []
        
        # Group A matches
        group_a_teams = teams[:4]
        for i, home_team in enumerate(group_a_teams):
            for j, away_team in enumerate(group_a_teams):
                if i != j:  # Teams can't play against themselves
                    match = Match(
                        tournament_id=tournament.id,
                        phase_id=group_phase.id,
                        group_id=group_a.id,
                        home_team_id=home_team.id,
                        away_team_id=away_team.id,
                        date=today + timedelta(days=(i+j)),
                        location=f"Field {i+j}",
                        status="scheduled"
                    )
                    matches.append(match)
        
        # Group B matches
        group_b_teams = teams[4:]
        for i, home_team in enumerate(group_b_teams):
            for j, away_team in enumerate(group_b_teams):
                if i != j:  # Teams can't play against themselves
                    match = Match(
                        tournament_id=tournament.id,
                        phase_id=group_phase.id,
                        group_id=group_b.id,
                        home_team_id=home_team.id,
                        away_team_id=away_team.id,
                        date=today + timedelta(days=(i+j)),
                        location=f"Field {i+j}",
                        status="scheduled"
                    )
                    matches.append(match)
        
        db.add_all(matches)
        db.commit()
        print(f"Created {len(matches)} matches")
        
        # Simulate some played matches with results
        for i, match in enumerate(matches[:6]):  # First 6 matches are "played"
            match.status = "completed"
            match.home_score = i % 3 + 1  # 1, 2, 3, 1, 2, 3
            match.away_score = (i + 1) % 3  # 1, 2, 0, 1, 2, 0
            
            # Create some goals for the match
            home_goals = match.home_score
            away_goals = match.away_score
            
            # Get players from both teams
            home_players = db.query(Player).filter(Player.team_id == match.home_team_id).all()
            away_players = db.query(Player).filter(Player.team_id == match.away_team_id).all()
            
            # Create goals for home team
            for g in range(home_goals):
                player = home_players[g % len(home_players)]
                goal = Goal(
                    match_id=match.id,
                    player_id=player.id,
                    team_id=match.home_team_id,
                    minute=15 + g * 15,
                    type="regular"
                )
                db.add(goal)
            
            # Create goals for away team
            for g in range(away_goals):
                player = away_players[g % len(away_players)]
                goal = Goal(
                    match_id=match.id,
                    player_id=player.id,
                    team_id=match.away_team_id,
                    minute=20 + g * 15,
                    type="regular"
                )
                db.add(goal)
                
        db.commit()
        print("Updated match results and created goals")
        
        # Initialize team stats for all teams
        for team in teams:
            team_stats = TeamStats(
                team_id=team.id,
                tournament_id=tournament.id
            )
            db.add(team_stats)
            
        db.commit()
        print("Initialized team stats for all teams")
            
        print("\nDatabase initialization complete!")
        
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_db() 
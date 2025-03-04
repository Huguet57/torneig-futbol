"""Module for calculating standings from match results."""
from typing import Any

from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.match import Match
from app.schemas.team_standing import TeamStanding


def calculate_group_standings(db: Session, group_id: int) -> list[TeamStanding]:
    """
    Calculate standings for teams in a group based on match results.
    
    Args:
        db: Database session
        group_id: ID of the group to calculate standings for
        
    Returns:
        List of TeamStanding objects ordered by points (descending) and goal difference
    """
    # Get all teams in the group
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group or not group.teams:
        return []
    
    # Initialize standings dictionary
    standings: dict[int, dict[str, Any]] = {}
    for team in group.teams:
        standings[team.id] = {
            "team_id": team.id,
            "team_name": team.name,
            "team_short_name": team.short_name,
            "team_logo_url": team.logo_url,
            "matches_played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }
    
    # Get all completed matches in the group
    matches = db.query(Match).filter(
        Match.group_id == group_id,
        Match.status == "completed",
        Match.home_score.isnot(None),
        Match.away_score.isnot(None)
    ).all()
    
    # Calculate standings from match results
    for match in matches:
        # Skip if either team is not in the group
        if match.home_team_id not in standings or match.away_team_id not in standings:
            continue
        
        home_id = match.home_team_id
        away_id = match.away_team_id
        
        # Update matches played
        standings[home_id]["matches_played"] += 1
        standings[away_id]["matches_played"] += 1
        
        # Update goals
        standings[home_id]["goals_for"] += match.home_score
        standings[home_id]["goals_against"] += match.away_score
        standings[away_id]["goals_for"] += match.away_score
        standings[away_id]["goals_against"] += match.home_score
        
        # Update results based on match outcome
        if match.home_score > match.away_score:
            # Home team win
            standings[home_id]["wins"] += 1
            standings[home_id]["points"] += 3
            standings[away_id]["losses"] += 1
        elif match.home_score < match.away_score:
            # Away team win
            standings[away_id]["wins"] += 1
            standings[away_id]["points"] += 3
            standings[home_id]["losses"] += 1
        else:
            # Draw
            standings[home_id]["draws"] += 1
            standings[away_id]["draws"] += 1
            standings[home_id]["points"] += 1
            standings[away_id]["points"] += 1
    
    # Calculate goal difference
    for team_id in standings:
        standings[team_id]["goal_difference"] = (
            standings[team_id]["goals_for"] - standings[team_id]["goals_against"]
        )
    
    # Convert to list of TeamStanding objects and sort
    standings_list = [TeamStanding(**data) for data in standings.values()]
    standings_list.sort(
        key=lambda x: (x.points, x.goal_difference, x.goals_for),
        reverse=True
    )
    
    return standings_list 
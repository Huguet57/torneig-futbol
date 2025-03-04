from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.models.team_stats import TeamStats
from app.schemas.team_stats import TeamStatsCreate, TeamStatsUpdate


class CRUDTeamStats(CRUDBase[TeamStats, TeamStatsCreate, TeamStatsUpdate]):
    """CRUD operations for team statistics."""
    
    def get_by_team_id(self, db: Session, team_id: int) -> Optional[TeamStats]:
        """Get team statistics by team ID."""
        return db.query(TeamStats).filter(TeamStats.team_id == team_id).first()
    
    def get_by_team_tournament(
        self, db: Session, *, team_id: int, tournament_id: int
    ) -> Optional[TeamStats]:
        """Get team statistics for a specific tournament."""
        return db.query(TeamStats).filter(
            TeamStats.team_id == team_id,
            TeamStats.tournament_id == tournament_id
        ).first()
    
    def get_by_tournament(
        self, db: Session, *, tournament_id: int, skip: int = 0, limit: int = 100
    ) -> List[TeamStats]:
        """Get all team statistics for a tournament."""
        return db.query(TeamStats).filter(
            TeamStats.tournament_id == tournament_id
        ).offset(skip).limit(limit).all()
    
    def create_for_team(
        self, db: Session, *, team_id: int, tournament_id: int
    ) -> TeamStats:
        """Create initial statistics for a team."""
        stats_data = {
            "team_id": team_id,
            "tournament_id": tournament_id,
            "matches_played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "clean_sheets": 0,
            "points": 0
        }
        
        stats = TeamStats(**stats_data)
        db.add(stats)
        db.commit()
        db.refresh(stats)
        return stats
    
    def update_stats_from_matches(
        self, db: Session, *, team_id: int, tournament_id: int
    ) -> Optional[TeamStats]:
        """Update team stats based on match results in the tournament."""
        from app.crud.match import match
        
        # Get or create team stats
        db_obj = self.get_by_team_tournament(
            db=db, team_id=team_id, tournament_id=tournament_id
        )
        
        if not db_obj:
            db_obj = self.create_for_team(
                db=db, team_id=team_id, tournament_id=tournament_id
            )
        
        # Get completed matches where the team participated
        home_matches = match.get_all_by_fields(
            db=db,
            fields={
                "home_team_id": team_id,
                "tournament_id": tournament_id,
                "status": "completed"
            }
        )
        
        away_matches = match.get_all_by_fields(
            db=db,
            fields={
                "away_team_id": team_id,
                "tournament_id": tournament_id,
                "status": "completed"
            }
        )
        
        # Reset stats before recalculation
        db_obj.matches_played = 0
        db_obj.wins = 0
        db_obj.draws = 0
        db_obj.losses = 0
        db_obj.goals_for = 0
        db_obj.goals_against = 0
        db_obj.clean_sheets = 0
        db_obj.points = 0
        
        # Calculate stats from home matches
        for match in home_matches:
            db_obj.matches_played += 1
            db_obj.goals_for += match.home_score
            db_obj.goals_against += match.away_score
            
            if match.home_score > match.away_score:
                # Win
                db_obj.wins += 1
                db_obj.points += 3
            elif match.home_score == match.away_score:
                # Draw
                db_obj.draws += 1
                db_obj.points += 1
            else:
                # Loss
                db_obj.losses += 1
            
            if match.away_score == 0:
                db_obj.clean_sheets += 1
        
        # Calculate stats from away matches
        for match in away_matches:
            db_obj.matches_played += 1
            db_obj.goals_for += match.away_score
            db_obj.goals_against += match.home_score
            
            if match.away_score > match.home_score:
                # Win
                db_obj.wins += 1
                db_obj.points += 3
            elif match.away_score == match.home_score:
                # Draw
                db_obj.draws += 1
                db_obj.points += 1
            else:
                # Loss
                db_obj.losses += 1
            
            if match.home_score == 0:
                db_obj.clean_sheets += 1
        
        # Update calculated stats
        db_obj.update_calculated_stats()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj
    
    def get_tournament_teams_ranked(
        self, db: Session, *, tournament_id: int, limit: int = 100
    ) -> List[TeamStats]:
        """Get teams in a tournament ranked by points and goal difference."""
        return db.query(TeamStats).filter(
            TeamStats.tournament_id == tournament_id
        ).order_by(
            TeamStats.points.desc(),
            TeamStats.goal_difference.desc(),
            TeamStats.goals_for.desc()
        ).limit(limit).all()


team_stats = CRUDTeamStats(TeamStats) 
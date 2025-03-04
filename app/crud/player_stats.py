from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.models.player_stats import PlayerStats
from app.schemas.player_stats import PlayerStatsCreate, PlayerStatsBase


class CRUDPlayerStats(CRUDBase[PlayerStats, PlayerStatsBase, PlayerStatsBase]):
    """CRUD operations for player statistics."""
    
    def get_by_player_id(self, db: Session, player_id: int) -> Optional[PlayerStats]:
        """Get player statistics by player ID."""
        return db.query(PlayerStats).filter(PlayerStats.player_id == player_id).first()
    
    def create_for_player(self, db: Session, player_id: int, tournament_id: int = None) -> PlayerStats:
        """Create initial statistics for a player."""
        stats_data = {
            "player_id": player_id,
            "matches_played": 0,
            "goals_scored": 0,
            "minutes_played": 0,
            "goals_per_match": 0.0,
            "minutes_per_goal": 0.0
        }
        
        # Add tournament_id if provided
        if tournament_id is not None:
            stats_data["tournament_id"] = tournament_id
        
        stats = PlayerStats(**stats_data)
        db.add(stats)
        db.commit()
        db.refresh(stats)
        return stats
    
    def remove(self, db: Session, *, id: int) -> PlayerStats:
        """Delete player statistics."""
        return self.delete(db=db, id=id)
    
    def update_stats_from_match(
        self,
        db: Session,
        player_id: int,
        minutes_played: int,
        goals_scored: int = 0
    ) -> PlayerStats:
        """Update player statistics after a match."""
        stats = self.get_by_player_id(db, player_id)
        if not stats:
            stats = self.create_for_player(db, player_id)
        
        stats.matches_played += 1
        stats.minutes_played += minutes_played
        stats.goals_scored += goals_scored
        stats.update_calculated_stats()
        
        db.commit()
        db.refresh(stats)
        return stats
    
    def get_tournament_top_scorers(
        self,
        db: Session,
        tournament_id: int,
        limit: int = 5
    ) -> List[PlayerStats]:
        """Get top scorers for a tournament."""
        from app.models.goal import Goal
        from app.models.match import Match
        from sqlalchemy import func, desc
        
        # Count goals by player in matches of the tournament
        goals_by_player = (
            db.query(
                Goal.player_id,
                func.count(Goal.id).label("goal_count")
            )
            .join(Match, Goal.match_id == Match.id)
            .filter(Match.tournament_id == tournament_id)
            .group_by(Goal.player_id)
            .order_by(desc("goal_count"))
            .limit(limit)
            .all()
        )
        
        # Create or update player stats for each top scorer
        top_scorers = []
        for player_id, goal_count in goals_by_player:
            # Get or create stats for this player in this tournament
            stats = self.get_by_player_tournament(db, player_id=player_id, tournament_id=tournament_id)
            if not stats:
                stats = self.create_for_player(db, player_id=player_id, tournament_id=tournament_id)
                
            # Update with goal count
            stats.goals_scored = goal_count
            stats.update_calculated_stats()
            
            top_scorers.append(stats)
            
        return top_scorers
    
    def get_by_player_tournament(
        self, db: Session, *, player_id: int, tournament_id: int
    ) -> Optional[PlayerStats]:
        """Get player stats for a specific player in a specific tournament."""
        return db.query(self.model).filter(
            self.model.player_id == player_id,
            self.model.tournament_id == tournament_id
        ).first()
    
    def get_by_tournament(
        self, db: Session, *, tournament_id: int, skip: int = 0, limit: int = 100
    ) -> List[PlayerStats]:
        """Get all player stats for a specific tournament."""
        return db.query(self.model).filter(
            self.model.tournament_id == tournament_id
        ).offset(skip).limit(limit).all()
    
    def get_by_player(
        self, db: Session, *, player_id: int, skip: int = 0, limit: int = 100
    ) -> List[PlayerStats]:
        """Get all stats for a specific player across tournaments."""
        return db.query(self.model).filter(
            self.model.player_id == player_id
        ).offset(skip).limit(limit).all()
    
    def create_or_update(
        self, db: Session, *, obj_in: Union[PlayerStatsCreate, Dict[str, Any]]
    ) -> PlayerStats:
        """Create or update player stats for a tournament."""
        if isinstance(obj_in, dict):
            player_id = obj_in.get("player_id")
            tournament_id = obj_in.get("tournament_id")
        else:
            player_id = obj_in.player_id
            tournament_id = obj_in.tournament_id
            
        db_obj = self.get_by_player_tournament(
            db=db, player_id=player_id, tournament_id=tournament_id
        )
        
        if db_obj:
            return self.update(db=db, db_obj=db_obj, obj_in=obj_in)
        return self.create(db=db, obj_in=obj_in)
    
    def update_stats_from_goals(
        self, db: Session, *, player_id: int, tournament_id: int
    ) -> Optional[PlayerStats]:
        """Update player stats based on goals scored in the tournament."""
        from app.crud.goal import goal
        from app.crud.match import match
        
        # Get or create player stats
        db_obj = self.get_by_player_tournament(
            db=db, player_id=player_id, tournament_id=tournament_id
        )
        
        if not db_obj:
            db_obj = self.create(
                db=db, 
                obj_in=PlayerStatsCreate(
                    player_id=player_id,
                    tournament_id=tournament_id
                )
            )
        
        # Get all matches in the tournament
        tournament_matches = match.get_by_tournament(
            db=db, tournament_id=tournament_id
        )
        match_ids = [m.id for m in tournament_matches]
        
        # Get all goals by the player in these matches
        player_goals = goal.get_by_player_in_matches(
            db=db, player_id=player_id, match_ids=match_ids
        )
        
        # Update stats
        db_obj.goals_scored = len(player_goals)
        
        # Count matches played (matches where the player scored)
        matches_with_goals = set(g.match_id for g in player_goals)
        db_obj.matches_played = len(matches_with_goals)
        
        # Estimate minutes played (90 minutes per match)
        db_obj.minutes_played = db_obj.matches_played * 90
        
        # Update calculated stats
        db_obj.update_calculated_stats()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj


player_stats = CRUDPlayerStats(PlayerStats) 
from typing import List, Optional, Dict, Any, Union

from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.models.player_stats import PlayerStats
from app.schemas.player_stats import PlayerStatsCreate, PlayerStatsUpdate


class CRUDPlayerStats(CRUDBase[PlayerStats, PlayerStatsCreate, PlayerStatsUpdate]):
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
        db_obj.goals = len(player_goals)
        
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
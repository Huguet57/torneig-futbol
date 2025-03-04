
from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


class CRUDGoal(CRUDBase[Goal, GoalCreate, GoalUpdate]):
    def get_by_match(
        self, db: Session, *, match_id: int, skip: int = 0, limit: int = 100
    ) -> list[Goal]:
        """Get all goals for a specific match."""
        return db.query(self.model).filter(
            self.model.match_id == match_id
        ).order_by(self.model.minute).offset(skip).limit(limit).all()
    
    def get_by_player(
        self, db: Session, *, player_id: int, skip: int = 0, limit: int = 100
    ) -> list[Goal]:
        """Get all goals scored by a specific player."""
        return db.query(self.model).filter(
            self.model.player_id == player_id
        ).order_by(self.model.match_id, self.model.minute).offset(skip).limit(limit).all()
    
    def get_by_team(
        self, db: Session, *, team_id: int, skip: int = 0, limit: int = 100
    ) -> list[Goal]:
        """Get all goals scored by a specific team."""
        return db.query(self.model).filter(
            self.model.team_id == team_id
        ).order_by(self.model.match_id, self.model.minute).offset(skip).limit(limit).all()
    
    def get_by_player_in_matches(
        self, db: Session, *, player_id: int, match_ids: list[int]
    ) -> list[Goal]:
        """Get all goals scored by a player in specific matches."""
        return db.query(self.model).filter(
            self.model.player_id == player_id,
            self.model.match_id.in_(match_ids)
        ).order_by(self.model.match_id, self.model.minute).all()
    
    def get_by_team_in_matches(
        self, db: Session, *, team_id: int, match_ids: list[int]
    ) -> list[Goal]:
        """Get all goals scored by a team in specific matches."""
        return db.query(self.model).filter(
            self.model.team_id == team_id,
            self.model.match_id.in_(match_ids)
        ).order_by(self.model.match_id, self.model.minute).all()
    
    def count_by_player(self, db: Session, *, player_id: int) -> int:
        """Count goals scored by a player."""
        return db.query(self.model).filter(
            self.model.player_id == player_id
        ).count()
    
    def count_by_team(self, db: Session, *, team_id: int) -> int:
        """Count goals scored by a team."""
        return db.query(self.model).filter(
            self.model.team_id == team_id
        ).count()


goal = CRUDGoal(Goal) 
from typing import List

from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.models.match import Match
from app.schemas.match import MatchCreate, MatchUpdate


class CRUDMatch(CRUDBase[Match, MatchCreate, MatchUpdate]):
    def get_by_tournament(
        self, db: Session, *, tournament_id: int, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        """Get all matches for a specific tournament."""
        return db.query(self.model).filter(
            self.model.tournament_id == tournament_id
        ).order_by(self.model.date, self.model.id).offset(skip).limit(limit).all()
    
    def get_by_phase(
        self, db: Session, *, phase_id: int, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        """Get all matches for a specific phase."""
        return db.query(self.model).filter(
            self.model.phase_id == phase_id
        ).order_by(self.model.date, self.model.id).offset(skip).limit(limit).all()
    
    def get_by_group(
        self, db: Session, *, group_id: int, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        """Get all matches for a specific group."""
        return db.query(self.model).filter(
            self.model.group_id == group_id
        ).order_by(self.model.date, self.model.id).offset(skip).limit(limit).all()
    
    def get_by_team(
        self, db: Session, *, team_id: int, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        """Get all matches for a specific team."""
        return db.query(self.model).filter(
            (self.model.home_team_id == team_id) | (self.model.away_team_id == team_id)
        ).order_by(self.model.date, self.model.id).offset(skip).limit(limit).all()
    
    def get_completed_matches(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        """Get all completed matches."""
        return db.query(self.model).filter(
            self.model.is_completed == True
        ).order_by(self.model.date, self.model.id).offset(skip).limit(limit).all()
    
    def get_upcoming_matches(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        """Get all upcoming matches."""
        return db.query(self.model).filter(
            self.model.is_completed == False
        ).order_by(self.model.date, self.model.id).offset(skip).limit(limit).all()


match = CRUDMatch(Match) 
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class PlayerStats(Base):
    """Model for player statistics."""
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    matches_played = Column(Integer, default=0)
    goals_scored = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    goals_per_match = Column(Float, default=0.0)
    minutes_per_goal = Column(Float, default=0.0)

    # Relationships
    player = relationship("Player", back_populates="stats")
    tournament = relationship("Tournament", back_populates="player_stats")

    def update_calculated_stats(self):
        """Update calculated statistics based on raw data."""
        if self.matches_played > 0:
            self.goals_per_match = self.goals_scored / self.matches_played
        else:
            self.goals_per_match = 0.0
            
        if self.goals_scored > 0:
            self.minutes_per_goal = self.minutes_played / self.goals_scored
        else:
            self.minutes_per_goal = 0.0 
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.database import Base


class PlayerStats(Base):
    """Model for tracking player statistics across matches and tournaments."""
    
    __tablename__ = "player_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    
    # Match participation
    matches_played = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    
    # Goal statistics
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    penalty_goals = Column(Integer, default=0)
    own_goals = Column(Integer, default=0)
    
    # Advanced statistics
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    
    # Calculated statistics
    goals_per_match = Column(Float, default=0.0)
    minutes_per_goal = Column(Float, default=0.0)
    
    # Relationships
    player = relationship("Player", back_populates="stats")
    tournament = relationship("Tournament", back_populates="player_stats")
    
    def update_calculated_stats(self):
        """Update calculated statistics based on raw data."""
        if self.matches_played > 0:
            self.goals_per_match = self.goals / self.matches_played
        else:
            self.goals_per_match = 0.0
            
        if self.goals > 0:
            self.minutes_per_goal = self.minutes_played / self.goals
        else:
            self.minutes_per_goal = 0.0 
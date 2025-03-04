from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class TeamStats(Base):
    """Model for team statistics."""
    __tablename__ = "team_stats"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    
    # Match statistics
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # Goal statistics
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    goal_difference = Column(Integer, default=0)
    clean_sheets = Column(Integer, default=0)
    
    # Tournament statistics
    points = Column(Integer, default=0)
    position = Column(Integer, nullable=True)
    
    # Performance metrics
    win_percentage = Column(Float, default=0.0)
    goals_per_match = Column(Float, default=0.0)
    points_per_match = Column(Float, default=0.0)
    
    # Relationships
    team = relationship("Team", back_populates="stats")
    tournament = relationship("Tournament", back_populates="team_stats")
    
    def update_calculated_stats(self):
        """Update all calculated statistics fields based on raw data."""
        # Calculate goal difference
        self.goal_difference = self.goals_for - self.goals_against
        
        # Calculate performance metrics
        if self.matches_played > 0:
            self.win_percentage = round(self.wins / self.matches_played * 100, 2)
            self.goals_per_match = round(self.goals_for / self.matches_played, 2)
            self.points_per_match = round(self.points / self.matches_played, 2)
        else:
            self.win_percentage = 0.0
            self.goals_per_match = 0.0
            self.points_per_match = 0.0 
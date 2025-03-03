from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    minute = Column(Integer)
    type = Column(
        Enum("regular", "penalty", "own_goal", name="goal_type"),
        default="regular",
    )

    # Relationships
    match = relationship("Match", back_populates="goals")
    player = relationship("Player", back_populates="goals")
    team = relationship("Team", back_populates="goals") 
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    name = Column(String, index=True)
    number = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    is_goalkeeper = Column(Boolean, default=False)

    # Relationships
    team = relationship("Team", back_populates="players")
    goals = relationship("Goal", back_populates="player")
    stats = relationship("PlayerStats", back_populates="player", cascade="all, delete-orphan")

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from app.db.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    phase_id = Column(Integer, ForeignKey("phases.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    date = Column(Date)
    time = Column(Time, nullable=True)
    location = Column(String, nullable=True)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    status = Column(
        Enum("scheduled", "in-progress", "completed", name="match_status"),
        default="scheduled",
    )

    # Relationships
    tournament = relationship("Tournament", back_populates="matches")
    phase = relationship("Phase", back_populates="matches")
    group = relationship("Group", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    goals = relationship("Goal", back_populates="match", cascade="all, delete-orphan")

from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    edition = Column(String)
    year = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)

    # Relationships
    phases = relationship(
        "Phase", back_populates="tournament", cascade="all, delete-orphan"
    )
    matches = relationship(
        "Match", back_populates="tournament", cascade="all, delete-orphan"
    )
    player_stats = relationship(
        "PlayerStats", back_populates="tournament", cascade="all, delete-orphan"
    )
    team_stats = relationship(
        "TeamStats", back_populates="tournament", cascade="all, delete-orphan"
    )

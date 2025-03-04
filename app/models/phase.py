from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    name = Column(String, index=True)
    order = Column(Integer)
    type = Column(Enum("group", "elimination", name="phase_type"))

    # Relationships
    tournament = relationship("Tournament", back_populates="phases")
    groups = relationship("Group", back_populates="phase", cascade="all, delete-orphan")
    matches = relationship(
        "Match", back_populates="phase", cascade="all, delete-orphan"
    )

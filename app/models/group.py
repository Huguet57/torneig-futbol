from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.database import Base


# Association table for many-to-many relationship between teams and groups
team_group = Table(
    "team_group",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    phase_id = Column(Integer, ForeignKey("phases.id"))
    name = Column(String, index=True)

    # Relationships
    phase = relationship("Phase", back_populates="groups")
    teams = relationship("Team", secondary=team_group, back_populates="groups")
    matches = relationship(
        "Match", back_populates="group", cascade="all, delete-orphan"
    )

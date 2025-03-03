from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    short_name = Column(String)
    logo_url = Column(String, nullable=True)
    city = Column(String, nullable=True)
    colors = Column(String, nullable=True)

    # Relationships
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    # For many-to-many relationship with groups through team_group association table
    groups = relationship(
        "Group",
        secondary="team_group",
        back_populates="teams"
    ) 
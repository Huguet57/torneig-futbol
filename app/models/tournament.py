from sqlalchemy import Column, Integer, String, Date, Text
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

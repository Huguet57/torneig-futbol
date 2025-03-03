from datetime import date
from typing import Optional, List

from pydantic import BaseModel


# Base model with common attributes
class TournamentBase(BaseModel):
    name: str
    edition: str
    year: int
    start_date: date
    end_date: date
    description: Optional[str] = None
    logo_url: Optional[str] = None


# Model for creating a tournament
class TournamentCreate(TournamentBase):
    pass


# Model for updating a tournament
class TournamentUpdate(TournamentBase):
    name: Optional[str] = None
    edition: Optional[str] = None
    year: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# Model for tournament in database (includes ID)
class Tournament(TournamentBase):
    id: int

    class Config:
        from_attributes = True  # For SQLAlchemy models compatibility 
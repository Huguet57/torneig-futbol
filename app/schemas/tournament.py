from datetime import date

from pydantic import BaseModel


# Base model with common attributes
class TournamentBase(BaseModel):
    name: str
    edition: str
    year: int
    start_date: date
    end_date: date
    description: str | None = None
    logo_url: str | None = None


# Model for creating a tournament
class TournamentCreate(TournamentBase):
    pass


# Model for updating a tournament
class TournamentUpdate(TournamentBase):
    name: str | None = None
    edition: str | None = None
    year: int | None = None
    start_date: date | None = None
    end_date: date | None = None


# Model for tournament in database (includes ID)
class Tournament(TournamentBase):
    id: int

    model_config = {"from_attributes": True}  # For SQLAlchemy models compatibility

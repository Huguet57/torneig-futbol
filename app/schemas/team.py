from typing import Optional

from pydantic import BaseModel


# Base model with common attributes
class TeamBase(BaseModel):
    name: str
    short_name: str
    logo_url: Optional[str] = None
    city: Optional[str] = None
    colors: Optional[str] = None


# Model for creating a team
class TeamCreate(TeamBase):
    pass


# Model for updating a team
class TeamUpdate(TeamBase):
    name: Optional[str] = None
    short_name: Optional[str] = None


# Model for team in database (includes ID)
class Team(TeamBase):
    id: int

    class Config:
        from_attributes = True  # For SQLAlchemy models compatibility

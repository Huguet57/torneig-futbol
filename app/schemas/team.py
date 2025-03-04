
from pydantic import BaseModel


# Base model with common attributes
class TeamBase(BaseModel):
    name: str
    short_name: str
    logo_url: str | None = None
    city: str | None = None
    colors: str | None = None


# Model for creating a team
class TeamCreate(TeamBase):
    pass


# Model for updating a team
class TeamUpdate(TeamBase):
    name: str | None = None
    short_name: str | None = None


# Model for team in database (includes ID)
class Team(TeamBase):
    id: int

    model_config = {"from_attributes": True}  # For SQLAlchemy models compatibility

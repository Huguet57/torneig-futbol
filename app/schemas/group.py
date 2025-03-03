from typing import Optional, List

from pydantic import BaseModel


# Base model with common attributes
class GroupBase(BaseModel):
    name: str


# Model for creating a group
class GroupCreate(GroupBase):
    phase_id: int


# Model for updating a group
class GroupUpdate(BaseModel):
    name: Optional[str] = None


# Model for team data in group response
class TeamInGroup(BaseModel):
    id: int
    name: str
    short_name: str

    class Config:
        from_attributes = True


# Model for group in database (includes ID)
class Group(GroupBase):
    id: int
    phase_id: int
    teams: List[TeamInGroup] = []

    class Config:
        from_attributes = True  # For SQLAlchemy models compatibility


# Model for group with teams and phase information
class GroupWithTeams(Group):
    phase_name: str
    tournament_id: int
    tournament_name: str

    class Config:
        from_attributes = True


# Model for adding a team to a group
class TeamToGroup(BaseModel):
    team_id: int

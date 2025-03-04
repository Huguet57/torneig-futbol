
from pydantic import BaseModel, Field


class TeamStatsBase(BaseModel):
    """Base schema for team statistics."""
    matches_played: int = Field(default=0)
    wins: int = Field(default=0)
    draws: int = Field(default=0)
    losses: int = Field(default=0)
    goals_for: int = Field(default=0)
    goals_against: int = Field(default=0)
    goal_difference: int = Field(default=0)
    clean_sheets: int = Field(default=0)
    points: int = Field(default=0)
    position: int | None = None
    win_percentage: float = Field(default=0.0)
    goals_per_match: float = Field(default=0.0)
    points_per_match: float = Field(default=0.0)


class TeamStats(TeamStatsBase):
    """Schema for team statistics."""
    id: int
    team_id: int
    tournament_id: int
    
    model_config = {"from_attributes": True}


# Properties to receive on creation
class TeamStatsCreate(TeamStatsBase):
    """Schema for creating team statistics."""
    team_id: int
    tournament_id: int


# Properties to receive on update
class TeamStatsUpdate(BaseModel):
    """Schema for updating team statistics."""
    matches_played: int | None = None
    wins: int | None = None
    draws: int | None = None
    losses: int | None = None
    goals_for: int | None = None
    goals_against: int | None = None
    clean_sheets: int | None = None
    points: int | None = None
    position: int | None = None 
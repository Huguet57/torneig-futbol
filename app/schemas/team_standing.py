from typing import Optional
from pydantic import BaseModel, Field


class TeamStanding(BaseModel):
    team_id: int
    team_name: str
    team_short_name: Optional[str] = None
    team_logo_url: Optional[str] = None
    matches_played: int = Field(default=0, ge=0)
    wins: int = Field(default=0, ge=0)
    draws: int = Field(default=0, ge=0)
    losses: int = Field(default=0, ge=0)
    goals_for: int = Field(default=0, ge=0)
    goals_against: int = Field(default=0, ge=0)
    goal_difference: int = Field(default=0)
    points: int = Field(default=0, ge=0)

    model_config = {"from_attributes": True} 
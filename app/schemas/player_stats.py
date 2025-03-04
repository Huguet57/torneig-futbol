from typing import Optional

from pydantic import BaseModel, Field


class PlayerStatsBase(BaseModel):
    """Base schema for player statistics."""
    matches_played: int = Field(default=0)
    goals_scored: int = Field(default=0)
    minutes_played: int = Field(default=0)
    goals_per_match: float = Field(default=0.0)
    minutes_per_goal: float = Field(default=0.0)


class PlayerStats(PlayerStatsBase):
    """Schema for player statistics."""
    id: int
    player_id: Optional[int] = None
    tournament_id: int

    model_config = {"from_attributes": True}


# Properties to receive on creation
class PlayerStatsCreate(PlayerStatsBase):
    """Schema for creating player statistics."""
    player_id: int
    tournament_id: int


# Properties to receive on update
class PlayerStatsUpdate(BaseModel):
    """Schema for updating player statistics."""
    matches_played: Optional[int] = None
    goals_scored: Optional[int] = None
    minutes_played: Optional[int] = None 
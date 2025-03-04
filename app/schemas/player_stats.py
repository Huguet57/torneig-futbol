
from pydantic import BaseModel, Field

from app.schemas.player import Player
from app.schemas.tournament import Tournament


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
    player_id: int | None = None
    tournament_id: int
    player: Player | None = None
    tournament: Tournament | None = None

    model_config = {"from_attributes": True}


# Properties to receive on creation
class PlayerStatsCreate(PlayerStatsBase):
    """Schema for creating player statistics."""
    player_id: int
    tournament_id: int


# Properties to receive on update
class PlayerStatsUpdate(BaseModel):
    """Schema for updating player statistics."""
    matches_played: int | None = None
    goals_scored: int | None = None
    minutes_played: int | None = None 
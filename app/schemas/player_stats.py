from typing import Optional
from pydantic import BaseModel, Field


# Shared properties
class PlayerStatsBase(BaseModel):
    player_id: int
    tournament_id: int
    matches_played: Optional[int] = Field(default=0)
    minutes_played: Optional[int] = Field(default=0)
    goals: Optional[int] = Field(default=0)
    assists: Optional[int] = Field(default=0)
    penalty_goals: Optional[int] = Field(default=0)
    own_goals: Optional[int] = Field(default=0)
    yellow_cards: Optional[int] = Field(default=0)
    red_cards: Optional[int] = Field(default=0)


# Properties to receive on creation
class PlayerStatsCreate(PlayerStatsBase):
    pass


# Properties to receive on update
class PlayerStatsUpdate(BaseModel):
    matches_played: Optional[int] = None
    minutes_played: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    penalty_goals: Optional[int] = None
    own_goals: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None


# Properties shared by models stored in DB
class PlayerStatsInDBBase(PlayerStatsBase):
    id: int
    goals_per_match: float
    minutes_per_goal: float

    class Config:
        orm_mode = True


# Properties to return to client
class PlayerStats(PlayerStatsInDBBase):
    pass


# Properties stored in DB
class PlayerStatsInDB(PlayerStatsInDBBase):
    pass 
from enum import Enum

from pydantic import BaseModel, Field


class GoalType(str, Enum):
    REGULAR = "regular"
    PENALTY = "penalty"
    OWN_GOAL = "own_goal"


class GoalBase(BaseModel):
    match_id: int
    player_id: int | None = None
    team_id: int
    minute: int = Field(..., ge=0, le=120)
    type: GoalType = GoalType.REGULAR


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    player_id: int | None = None
    team_id: int | None = None
    minute: int | None = Field(None, ge=0, le=120)
    type: GoalType | None = None


class PlayerBase(BaseModel):
    id: int
    name: str
    number: int | None = None
    
    model_config = {"from_attributes": True}


class TeamBase(BaseModel):
    id: int
    name: str
    short_name: str | None = None
    
    model_config = {"from_attributes": True}


class Goal(GoalBase):
    id: int
    player: PlayerBase | None = None
    team: TeamBase | None = None
    
    model_config = {"from_attributes": True} 
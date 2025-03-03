from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GoalType(str, Enum):
    REGULAR = "regular"
    PENALTY = "penalty"
    OWN_GOAL = "own_goal"


class GoalBase(BaseModel):
    match_id: int
    player_id: int
    team_id: int
    minute: int = Field(..., ge=0, le=120)
    type: GoalType = GoalType.REGULAR


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    player_id: Optional[int] = None
    team_id: Optional[int] = None
    minute: Optional[int] = Field(None, ge=0, le=120)
    type: Optional[GoalType] = None


class PlayerBase(BaseModel):
    id: int
    name: str
    number: Optional[int] = None
    
    model_config = {"from_attributes": True}


class TeamBase(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    
    model_config = {"from_attributes": True}


class Goal(GoalBase):
    id: int
    player: Optional[PlayerBase] = None
    team: Optional[TeamBase] = None
    
    model_config = {"from_attributes": True} 
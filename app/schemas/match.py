from datetime import date, time
from typing import Optional
from enum import Enum

from pydantic import BaseModel, field_validator, Field


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class MatchBase(BaseModel):
    tournament_id: int
    phase_id: int
    group_id: Optional[int] = None
    home_team_id: int
    away_team_id: int
    date: date
    time: Optional[time] = None
    location: Optional[str] = None


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    phase_id: Optional[int] = None
    group_id: Optional[int] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    date: Optional[date] = None
    time: Optional[time] = None
    location: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: Optional[MatchStatus] = None


class MatchResult(BaseModel):
    home_score: int = Field(..., ge=0)
    away_score: int = Field(..., ge=0)
    status: MatchStatus = MatchStatus.COMPLETED

    @field_validator("status")
    def status_must_be_completed(cls, v):
        if v != MatchStatus.COMPLETED:
            raise ValueError("Match result can only be updated with status COMPLETED")
        return v


class TeamBase(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True


class Match(MatchBase):
    id: int
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    status: MatchStatus = MatchStatus.SCHEDULED
    home_team: Optional[TeamBase] = None
    away_team: Optional[TeamBase] = None

    class Config:
        from_attributes = True 
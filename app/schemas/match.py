from datetime import date, time
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class MatchBase(BaseModel):
    tournament_id: int
    phase_id: int
    group_id: int | None = None
    home_team_id: int
    away_team_id: int
    date: date
    time: time | None = None
    location: str | None = None


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    phase_id: int | None = None
    group_id: int | None = None
    home_team_id: int | None = None
    away_team_id: int | None = None
    date: date | None = None
    time: time | None = None
    location: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    status: MatchStatus | None = None


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
    short_name: str | None = None
    logo_url: str | None = None

    model_config = {"from_attributes": True}


class Match(MatchBase):
    id: int
    home_score: int | None = None
    away_score: int | None = None
    status: MatchStatus = MatchStatus.SCHEDULED
    home_team: TeamBase | None = None
    away_team: TeamBase | None = None

    model_config = {"from_attributes": True} 
from typing import Optional, List, Literal

from pydantic import BaseModel


# Phase types
PhaseType = Literal["group", "elimination"]


# Base model with common attributes
class PhaseBase(BaseModel):
    name: str
    order: int
    type: PhaseType


# Model for creating a phase
class PhaseCreate(PhaseBase):
    tournament_id: int


# Model for updating a phase
class PhaseUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    type: Optional[PhaseType] = None


# Model for phase in database (includes ID)
class Phase(PhaseBase):
    id: int
    tournament_id: int

    class Config:
        from_attributes = True  # For SQLAlchemy models compatibility 
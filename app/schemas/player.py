from typing import Optional
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    number: Optional[int] = None
    position: Optional[str] = None
    is_goalkeeper: bool = False


class PlayerCreate(PlayerBase):
    team_id: int


class PlayerUpdate(PlayerBase):
    name: Optional[str] = None
    team_id: Optional[int] = None


class Player(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True 
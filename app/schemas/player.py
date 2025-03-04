
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    number: int | None = None
    position: str | None = None
    is_goalkeeper: bool = False


class PlayerCreate(PlayerBase):
    team_id: int


class PlayerUpdate(PlayerBase):
    name: str | None = None
    team_id: int | None = None


class Player(PlayerBase):
    id: int
    team_id: int

    model_config = {"from_attributes": True} 
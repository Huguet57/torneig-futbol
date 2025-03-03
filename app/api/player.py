from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.player import Player as PlayerModel
from app.schemas.player import Player, PlayerCreate, PlayerUpdate
from app.api.crud_base import CRUDBase

router = APIRouter()
crud = CRUDBase[PlayerModel, PlayerCreate, PlayerUpdate](PlayerModel)


@router.get("/", response_model=List[Player])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all players.
    """
    return crud.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Create a new player.
    """
    return crud.create(db, obj_in=player)


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Get a specific player by ID.
    """
    db_player = crud.get(db, id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@router.put("/{player_id}", response_model=Player)
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Update a player.
    """
    db_player = crud.get(db, id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.update(db, db_obj=db_player, obj_in=player)


@router.delete("/{player_id}", response_model=Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Delete a player.
    """
    return crud.delete(db, id=player_id)


@router.get("/team/{team_id}", response_model=List[Player])
def get_players_by_team(team_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all players for a specific team.
    """
    players = db.query(PlayerModel).filter(PlayerModel.team_id == team_id).offset(skip).limit(limit).all()
    return players 
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.player import player as crud_player
from app.crud.player_stats import player_stats as crud_player_stats
from app.schemas.player import Player, PlayerCreate, PlayerUpdate
from app.schemas.player_stats import PlayerStats

router = APIRouter()


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get a player by ID."""
    player = crud_player.get(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/{player_id}/stats", response_model=PlayerStats)
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    """Get statistics for a player."""
    player = crud_player.get(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    stats = crud_player_stats.get_by_player_id(db, player_id)
    if not stats:
        # Create initial stats if they don't exist
        stats = crud_player_stats.create_for_player(db, player_id)
    
    return stats


@router.get("/", response_model=List[Player])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all players."""
    players = crud_player.get_multi(db, skip=skip, limit=limit)
    return players


@router.post("/", response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """Create a new player."""
    return crud_player.create(db, obj_in=player)


@router.put("/{player_id}", response_model=Player)
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    """Update a player."""
    db_player = crud_player.get(db, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud_player.update(db, db_obj=db_player, obj_in=player) 
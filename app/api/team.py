from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.team import Team as TeamModel
from app.models.player import Player as PlayerModel
from app.schemas.team import Team, TeamCreate, TeamUpdate
from app.schemas.player import Player, PlayerCreate
from app.api.crud_base import CRUDBase

router = APIRouter()
crud = CRUDBase[TeamModel, TeamCreate, TeamUpdate](TeamModel)


@router.get("/", response_model=List[Team])
def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all teams.
    """
    return crud.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Team)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    """
    Create a new team.
    """
    return crud.create(db, obj_in=team)


@router.get("/{team_id}", response_model=Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """
    Get a specific team by ID.
    """
    db_team = crud.get(db, id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.put("/{team_id}", response_model=Team)
def update_team(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    """
    Update a team.
    """
    db_team = crud.get(db, id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.update(db, db_obj=db_team, obj_in=team)


@router.delete("/{team_id}", response_model=Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """
    Delete a team.
    """
    return crud.delete(db, id=team_id)


@router.post("/{team_id}/players/", response_model=Player)
def create_team_player(team_id: int, player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Create a new player for a specific team.
    """
    db_team = crud.get(db, id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Create player with the team_id
    db_player = PlayerModel(
        team_id=team_id,
        name=player.name,
        number=player.number,
        position=player.position,
        is_goalkeeper=player.is_goalkeeper
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@router.get("/{team_id}/players/", response_model=List[Player])
def get_team_players(team_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all players for a specific team.
    """
    db_team = crud.get(db, id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    
    players = db.query(PlayerModel).filter(PlayerModel.team_id == team_id).offset(skip).limit(limit).all()
    return players

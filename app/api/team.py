from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.team import Team as TeamModel
from app.schemas.team import Team, TeamCreate, TeamUpdate
from app.api.crud_base import CRUDBase

router = APIRouter()
crud = CRUDBase[TeamModel, TeamCreate, TeamUpdate](TeamModel)


@router.get("/", response_model=List[Team])
def get_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all teams.
    """
    return crud.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Team)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new team.
    """
    return crud.create(db, obj_in=team)


@router.get("/{team_id}", response_model=Team)
def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific team by ID.
    """
    db_team = crud.get(db, id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@router.put("/{team_id}", response_model=Team)
def update_team(
    team_id: int,
    team: TeamUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a team.
    """
    db_team = crud.get(db, id=team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.update(db, db_obj=db_team, obj_in=team)


@router.delete("/{team_id}", response_model=Team)
def delete_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a team.
    """
    return crud.delete(db, id=team_id) 
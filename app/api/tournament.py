from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.tournament import Tournament as TournamentModel
from app.schemas.tournament import Tournament, TournamentCreate, TournamentUpdate
from app.api.crud_base import CRUDBase

router = APIRouter()
crud = CRUDBase[TournamentModel, TournamentCreate, TournamentUpdate](TournamentModel)


@router.get("/", response_model=List[Tournament])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all tournaments.
    """
    return crud.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Tournament)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    """
    Create a new tournament.
    """
    return crud.create(db, obj_in=tournament)


@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Get a specific tournament by ID.
    """
    db_tournament = crud.get(db, id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return db_tournament


@router.put("/{tournament_id}", response_model=Tournament)
def update_tournament(
    tournament_id: int, tournament: TournamentUpdate, db: Session = Depends(get_db)
):
    """
    Update a tournament.
    """
    db_tournament = crud.get(db, id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return crud.update(db, db_obj=db_tournament, obj_in=tournament)


@router.delete("/{tournament_id}", response_model=Tournament)
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Delete a tournament.
    """
    return crud.delete(db, id=tournament_id)

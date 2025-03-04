
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.crud import player_stats as crud_player_stats
from app.db.database import get_db
from app.models.tournament import Tournament as TournamentModel
from app.schemas.player_stats import PlayerStats
from app.schemas.tournament import Tournament, TournamentCreate, TournamentUpdate

router = APIRouter()
crud_tournament = CRUDBase[TournamentModel, TournamentCreate, TournamentUpdate](TournamentModel)


@router.get("/", response_model=list[Tournament])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all tournaments.
    """
    return crud_tournament.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Tournament)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    """
    Create a new tournament.
    """
    return crud_tournament.create(db, obj_in=tournament)


@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Get a specific tournament by ID.
    """
    db_tournament = crud_tournament.get(db, id=tournament_id)
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
    db_tournament = crud_tournament.get(db, id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return crud_tournament.update(db, db_obj=db_tournament, obj_in=tournament)


@router.delete("/{tournament_id}", response_model=Tournament)
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Delete a tournament.
    """
    return crud_tournament.delete(db, id=tournament_id)


@router.get("/{tournament_id}/top-scorers", response_model=list[PlayerStats])
def get_tournament_top_scorers(
    tournament_id: int, 
    limit: int = Query(5, ge=1, le=50, description="Number of top scorers to return"),
    db: Session = Depends(get_db)
):
    """
    Get top scorers for a tournament.
    """
    # Check if tournament exists
    db_tournament = crud_tournament.get(db, id=tournament_id)
    if db_tournament is None:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    # Get top scorers
    return crud_player_stats.get_tournament_top_scorers(
        db=db, tournament_id=tournament_id, limit=limit
    )

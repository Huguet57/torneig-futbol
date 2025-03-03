from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.tournament import tournament as crud_tournament
from app.crud.player_stats import player_stats as crud_player_stats
from app.schemas.tournament import Tournament, TournamentCreate, TournamentUpdate
from app.schemas.player_stats import PlayerStats

router = APIRouter()


@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Get a tournament by ID."""
    tournament = crud_tournament.get(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament


@router.get("/{tournament_id}/top-scorers", response_model=List[PlayerStats])
def get_tournament_top_scorers(
    tournament_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get top scorers for a tournament."""
    tournament = crud_tournament.get(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    return crud_player_stats.get_tournament_top_scorers(db, tournament_id, limit)


@router.get("/", response_model=List[Tournament])
def get_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tournaments."""
    tournaments = crud_tournament.get_multi(db, skip=skip, limit=limit)
    return tournaments


@router.post("/", response_model=Tournament)
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db)):
    """Create a new tournament."""
    return crud_tournament.create(db, obj_in=tournament)


@router.put("/{tournament_id}", response_model=Tournament)
def update_tournament(tournament_id: int, tournament: TournamentUpdate, db: Session = Depends(get_db)):
    """Update a tournament."""
    db_tournament = crud_tournament.get(db, tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return crud_tournament.update(db, db_obj=db_tournament, obj_in=tournament) 
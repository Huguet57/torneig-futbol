from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import crud
from app.db.database import get_db
from app.schemas.team_stats import TeamStats

router = APIRouter()


@router.get("/", response_model=list[TeamStats])
def get_team_stats(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tournament_id: int | None = None,
    team_id: int | None = None,
) -> Any:
    """
    Retrieve team statistics.
    
    Filter by tournament_id or team_id if provided.
    """
    if tournament_id and team_id:
        # Get stats for a specific team in a specific tournament
        stats = crud.team_stats.get_by_team_tournament(
            db=db, team_id=team_id, tournament_id=tournament_id
        )
        return [stats] if stats else []
    elif tournament_id:
        # Get all team stats for a specific tournament
        return crud.team_stats.get_by_tournament(
            db=db, tournament_id=tournament_id, skip=skip, limit=limit
        )
    elif team_id:
        # Get all stats for a specific team across tournaments
        return db.query(crud.team_stats.model).filter(
            crud.team_stats.model.team_id == team_id
        ).offset(skip).limit(limit).all()
    
    # Get all team stats
    return crud.team_stats.get_multi(db=db, skip=skip, limit=limit)


@router.get("/tournament/{tournament_id}", response_model=list[TeamStats])
def get_tournament_team_stats(
    tournament_id: int = Path(...),
    limit: int = 100,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all team statistics for a tournament, ranked by points.
    """
    return crud.team_stats.get_tournament_teams_ranked(
        db=db, tournament_id=tournament_id, limit=limit
    )


@router.get("/team/{team_id}", response_model=list[TeamStats])
def get_team_tournament_stats(
    team_id: int = Path(...),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get team statistics across all tournaments.
    """
    return db.query(crud.team_stats.model).filter(
        crud.team_stats.model.team_id == team_id
    ).offset(skip).limit(limit).all()


@router.post("/update/{team_id}/{tournament_id}", response_model=TeamStats)
def update_team_stats(
    team_id: int = Path(...),
    tournament_id: int = Path(...),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update statistics for a team in a tournament.
    
    Recalculates statistics based on match results.
    """
    stats = crud.team_stats.update_stats_from_matches(
        db=db, team_id=team_id, tournament_id=tournament_id
    )
    
    if not stats:
        raise HTTPException(status_code=404, detail="Team or tournament not found")
    
    return stats 
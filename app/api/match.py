from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.match import Match
from app.schemas.match import Match as MatchSchema
from app.schemas.match import MatchCreate, MatchUpdate, MatchResult
from app.api.crud_base import CRUDBase


router = APIRouter()
crud = CRUDBase(Match)


@router.post("/", response_model=MatchSchema)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    """Create a new match."""
    try:
        db_match = crud.create(db, obj_in=match)
        return db_match
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data for match creation")


@router.get("/{match_id}", response_model=MatchSchema)
def read_match(match_id: int = Path(...), db: Session = Depends(get_db)):
    """Get a match by ID."""
    db_match = db.query(Match).options(
        joinedload(Match.home_team),
        joinedload(Match.away_team)
    ).filter(Match.id == match_id).first()
    
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@router.put("/{match_id}", response_model=MatchSchema)
def update_match(
    match_id: int = Path(...),
    match: MatchUpdate = None,
    db: Session = Depends(get_db),
):
    """Update a match."""
    db_match = crud.get(db, id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    try:
        db_match = crud.update(db, db_obj=db_match, obj_in=match)
        return db_match
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data for match update")


@router.delete("/{match_id}")
def delete_match(match_id: int = Path(...), db: Session = Depends(get_db)):
    """Delete a match."""
    db_match = crud.get(db, id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    crud.delete(db, id=match_id)
    return {"message": "Match deleted successfully"}


@router.put("/{match_id}/result", response_model=MatchSchema)
def update_match_result(
    match_result: MatchResult,
    match_id: int = Path(...),
    db: Session = Depends(get_db),
):
    """Update a match result."""
    db_match = crud.get(db, id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    try:
        db_match = crud.update(db, db_obj=db_match, obj_in=match_result)
        return db_match
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data for match result update")


@router.get("/tournament/{tournament_id}", response_model=List[MatchSchema])
def list_matches_by_tournament(
    tournament_id: int = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all matches for a tournament."""
    matches = db.query(Match).options(
        joinedload(Match.home_team),
        joinedload(Match.away_team)
    ).filter(
        Match.tournament_id == tournament_id
    ).offset(skip).limit(limit).all()
    
    return matches


@router.get("/phase/{phase_id}", response_model=List[MatchSchema])
def list_matches_by_phase(
    phase_id: int = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all matches for a phase."""
    matches = db.query(Match).options(
        joinedload(Match.home_team),
        joinedload(Match.away_team)
    ).filter(
        Match.phase_id == phase_id
    ).offset(skip).limit(limit).all()
    
    return matches


@router.get("/group/{group_id}", response_model=List[MatchSchema])
def list_matches_by_group(
    group_id: int = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all matches for a group."""
    matches = db.query(Match).options(
        joinedload(Match.home_team),
        joinedload(Match.away_team)
    ).filter(
        Match.group_id == group_id
    ).offset(skip).limit(limit).all()
    
    return matches 
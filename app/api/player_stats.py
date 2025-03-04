from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.db.database import get_db
from app.schemas.player_stats import PlayerStats, PlayerStatsCreate, PlayerStatsUpdate
from app.api.tournament import crud_tournament
from app.api.player import crud_player

router = APIRouter()


@router.get("/", response_model=List[PlayerStats])
def get_player_stats(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tournament_id: Optional[int] = None,
    player_id: Optional[int] = None,
) -> Any:
    """
    Retrieve player statistics.
    
    Filter by tournament_id or player_id if provided.
    """
    if tournament_id and player_id:
        # Get stats for a specific player in a specific tournament
        stats = crud.player_stats.get_by_player_tournament(
            db=db, player_id=player_id, tournament_id=tournament_id
        )
        return [stats] if stats else []
    elif tournament_id:
        # Get all player stats for a specific tournament
        return crud.player_stats.get_by_tournament(
            db=db, tournament_id=tournament_id, skip=skip, limit=limit
        )
    elif player_id:
        # Get all stats for a specific player across tournaments
        return crud.player_stats.get_by_player(
            db=db, player_id=player_id, skip=skip, limit=limit
        )
    # Get all player stats
    return crud.player_stats.get_multi(db=db, skip=skip, limit=limit)


@router.post("/", response_model=PlayerStats)
def create_player_stats(
    *,
    db: Session = Depends(get_db),
    player_stats_in: PlayerStatsCreate,
) -> Any:
    """
    Create new player statistics.
    """
    # Check if player exists
    player = crud_player.get(db=db, id=player_stats_in.player_id)
    if not player:
        raise HTTPException(
            status_code=404,
            detail=f"Player with ID {player_stats_in.player_id} not found",
        )
    
    # Check if tournament exists
    tournament = crud_tournament.get(db=db, id=player_stats_in.tournament_id)
    if not tournament:
        raise HTTPException(
            status_code=404,
            detail=f"Tournament with ID {player_stats_in.tournament_id} not found",
        )
    
    # Check if stats already exist for this player in this tournament
    existing_stats = crud.player_stats.get_by_player_tournament(
        db=db, player_id=player_stats_in.player_id, tournament_id=player_stats_in.tournament_id
    )
    if existing_stats:
        raise HTTPException(
            status_code=400,
            detail=f"Statistics already exist for player {player_stats_in.player_id} in tournament {player_stats_in.tournament_id}",
        )
    
    return crud.player_stats.create(db=db, obj_in=player_stats_in)


@router.put("/{stats_id}", response_model=PlayerStats)
def update_player_stats(
    *,
    db: Session = Depends(get_db),
    stats_id: int,
    player_stats_in: PlayerStatsUpdate,
) -> Any:
    """
    Update player statistics.
    """
    stats = crud.player_stats.get(db=db, id=stats_id)
    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"Player statistics with ID {stats_id} not found",
        )
    
    stats = crud.player_stats.update(db=db, db_obj=stats, obj_in=player_stats_in)
    
    # Update calculated statistics
    stats.update_calculated_stats()
    db.add(stats)
    db.commit()
    db.refresh(stats)
    
    return stats


@router.get("/{stats_id}", response_model=PlayerStats)
def get_player_stats_by_id(
    *,
    db: Session = Depends(get_db),
    stats_id: int,
) -> Any:
    """
    Get player statistics by ID.
    """
    stats = crud.player_stats.get(db=db, id=stats_id)
    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"Player statistics with ID {stats_id} not found",
        )
    return stats


@router.delete("/{stats_id}", response_model=PlayerStats)
def delete_player_stats(
    *,
    db: Session = Depends(get_db),
    stats_id: int,
) -> Any:
    """
    Delete player statistics.
    """
    stats = crud.player_stats.get(db=db, id=stats_id)
    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"Player statistics with ID {stats_id} not found",
        )
    return crud.player_stats.remove(db=db, id=stats_id)


@router.post("/update-from-goals/", response_model=List[PlayerStats])
def update_stats_from_goals(
    *,
    db: Session = Depends(get_db),
    tournament_id: int = Query(..., description="Tournament ID to update stats for"),
    player_id: Optional[int] = Query(None, description="Optional player ID to update stats for"),
) -> Any:
    """
    Update player statistics based on goals scored in the tournament.
    
    If player_id is provided, only update stats for that player.
    Otherwise, update stats for all players who scored in the tournament.
    """
    # Check if tournament exists
    tournament = crud_tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(
            status_code=404,
            detail=f"Tournament with ID {tournament_id} not found",
        )
    
    updated_stats = []
    
    if player_id:
        # Update stats for a specific player
        player = crud_player.get(db=db, id=player_id)
        if not player:
            raise HTTPException(
                status_code=404,
                detail=f"Player with ID {player_id} not found",
            )
        
        stats = crud.player_stats.update_stats_from_goals(
            db=db, player_id=player_id, tournament_id=tournament_id
        )
        if stats:
            updated_stats.append(stats)
    else:
        # Get all matches in the tournament
        tournament_matches = crud.match.get_by_tournament(
            db=db, tournament_id=tournament_id
        )
        match_ids = [m.id for m in tournament_matches]
        
        # Get all goals in these matches
        all_goals = []
        for match_id in match_ids:
            match_goals = crud.goal.get_by_match(db=db, match_id=match_id)
            all_goals.extend(match_goals)
        
        # Get unique player IDs from goals
        player_ids = set(goal.player_id for goal in all_goals)
        
        # Update stats for each player
        for pid in player_ids:
            stats = crud.player_stats.update_stats_from_goals(
                db=db, player_id=pid, tournament_id=tournament_id
            )
            if stats:
                updated_stats.append(stats)
    
    return updated_stats 
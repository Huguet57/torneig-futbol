from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.player import Player as PlayerModel
from app.models.tournament import Tournament as TournamentModel
from app.schemas.player import Player, PlayerCreate, PlayerUpdate
from app.schemas.player_stats import PlayerStats
from app.api.crud_base import CRUDBase
from app import crud

router = APIRouter()
crud_player = CRUDBase[PlayerModel, PlayerCreate, PlayerUpdate](PlayerModel)
crud_tournament = CRUDBase[TournamentModel, TournamentModel, TournamentModel](TournamentModel)


@router.get("/", response_model=List[Player])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all players.
    """
    return crud_player.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    """
    Create a new player.
    """
    return crud_player.create(db, obj_in=player)


@router.get("/{player_id}", response_model=Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Get a specific player by ID.
    """
    db_player = crud_player.get(db, id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@router.put("/{player_id}", response_model=Player)
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    """
    Update a player.
    """
    db_player = crud_player.get(db, id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud_player.update(db, db_obj=db_player, obj_in=player)


@router.delete("/{player_id}", response_model=Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Delete a player.
    """
    return crud_player.delete(db, id=player_id)


@router.get("/team/{team_id}", response_model=List[Player])
def get_players_by_team(team_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all players for a specific team.
    """
    return db.query(PlayerModel).filter(PlayerModel.team_id == team_id).offset(skip).limit(limit).all()


@router.get("/{player_id}/stats", response_model=PlayerStats)
def get_player_stats(
    player_id: int, 
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific player.
    
    If tournament_id is provided, return stats for that specific tournament.
    Otherwise, return stats for the first tournament associated with the player.
    """
    # Check if player exists
    player = crud_player.get(db, id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    
    if tournament_id:
        # Get player stats for the specific tournament
        stats = crud.player_stats.get_by_player_tournament(
            db=db, player_id=player_id, tournament_id=tournament_id
        )
        if stats is None:
            # Create initial stats if they don't exist
            stats = crud.player_stats.create_for_player(
                db=db, player_id=player_id, tournament_id=tournament_id
            )
    else:
        # Try to find a tournament where this player has participated
        # First, check if the player has any goals
        from app.crud.goal import goal
        player_goals = goal.get_by_player(db=db, player_id=player_id, limit=1)
        
        if player_goals:
            # Use the tournament from the first match where the player scored
            match = crud.match.get(db=db, id=player_goals[0].match_id)
            tournament_id = match.tournament_id
        else:
            # If no goals, check for matches where the player's team participated
            team_id = player.team_id
            if team_id:
                matches = crud.match.get_by_team(db=db, team_id=team_id, limit=1)
                if matches:
                    tournament_id = matches[0].tournament_id
                else:
                    # If no matches found, use the first tournament as fallback
                    tournaments = crud_tournament.get_all(db=db, limit=1)
                    if not tournaments:
                        raise HTTPException(
                            status_code=404, 
                            detail="No tournaments found to associate with player stats"
                        )
                    tournament_id = tournaments[0].id
            else:
                # If player has no team, use the first tournament as fallback
                tournaments = crud_tournament.get_all(db=db, limit=1)
                if not tournaments:
                    raise HTTPException(
                        status_code=404, 
                        detail="No tournaments found to associate with player stats"
                    )
                tournament_id = tournaments[0].id
        
        # Now get or create the stats with the determined tournament_id
        stats = crud.player_stats.get_by_player_tournament(
            db=db, player_id=player_id, tournament_id=tournament_id
        )
        if stats is None:
            # Create initial stats if they don't exist
            stats = crud.player_stats.create_for_player(
                db=db, player_id=player_id, tournament_id=tournament_id
            )
    
    # Update statistics based on goals and matches
    stats = crud.player_stats.update_stats_from_goals(
        db=db, player_id=player_id, tournament_id=tournament_id
    )
    
    return stats 
"""API endpoints for team standings."""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.core.standings import calculate_group_standings
from app.db.database import get_db
from app.models.group import Group
from app.schemas.team_standing import TeamStanding

router = APIRouter()


@router.get("/group/{group_id}", response_model=list[TeamStanding])
def get_group_standings(group_id: int = Path(...), db: Session = Depends(get_db)):
    """
    Get standings for all teams in a group.
    
    Args:
        group_id: ID of the group
        db: Database session
        
    Returns:
        List of TeamStanding objects sorted by points and goal difference
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    standings = calculate_group_standings(db, group_id)
    return standings 
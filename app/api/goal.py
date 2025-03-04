
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.api.crud_base import CRUDBase
from app.db.database import get_db
from app.models.goal import Goal
from app.schemas.goal import Goal as GoalSchema
from app.schemas.goal import GoalCreate, GoalUpdate

router = APIRouter()
crud = CRUDBase(Goal)


@router.get("/", response_model=list[GoalSchema])
def get_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all goals."""
    goals = db.query(Goal).options(
        joinedload(Goal.player),
        joinedload(Goal.team)
    ).offset(skip).limit(limit).all()
    return goals


@router.post("/", response_model=GoalSchema)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    """Create a new goal entry."""
    try:
        db_goal = crud.create(db, obj_in=goal)
        return db_goal
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data for goal creation")


@router.get("/{goal_id}", response_model=GoalSchema)
def read_goal(goal_id: int = Path(...), db: Session = Depends(get_db)):
    """Get a goal by ID."""
    db_goal = db.query(Goal).options(
        joinedload(Goal.player),
        joinedload(Goal.team)
    ).filter(Goal.id == goal_id).first()
    
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal


@router.put("/{goal_id}", response_model=GoalSchema)
def update_goal(
    goal_id: int = Path(...),
    goal: GoalUpdate = None,
    db: Session = Depends(get_db),
):
    """Update a goal."""
    db_goal = crud.get(db, id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return crud.update(db, db_obj=db_goal, obj_in=goal)


@router.delete("/{goal_id}")
def delete_goal(goal_id: int = Path(...), db: Session = Depends(get_db)):
    """Delete a goal."""
    try:
        crud.delete(db, id=goal_id)
        return {"detail": "Goal deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/match/{match_id}", response_model=list[GoalSchema])
def list_goals_by_match(
    match_id: int = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all goals for a specific match."""
    goals = db.query(Goal).options(
        joinedload(Goal.player),
        joinedload(Goal.team)
    ).filter(Goal.match_id == match_id).offset(skip).limit(limit).all()
    
    return goals


@router.get("/player/{player_id}", response_model=list[GoalSchema])
def list_goals_by_player(
    player_id: int = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all goals scored by a specific player."""
    goals = db.query(Goal).options(
        joinedload(Goal.match),
        joinedload(Goal.team)
    ).filter(Goal.player_id == player_id).offset(skip).limit(limit).all()
    
    return goals


@router.get("/team/{team_id}", response_model=list[GoalSchema])
def list_goals_by_team(
    team_id: int = Path(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all goals scored by a specific team."""
    goals = db.query(Goal).options(
        joinedload(Goal.player),
        joinedload(Goal.match)
    ).filter(Goal.team_id == team_id).offset(skip).limit(limit).all()
    
    return goals 
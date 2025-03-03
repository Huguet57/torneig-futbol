from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.models.group import Group as GroupModel
from app.models.team import Team as TeamModel
from app.schemas.group import Group, GroupCreate, GroupUpdate, TeamToGroup
from app.api.crud_base import CRUDBase

router = APIRouter()
crud = CRUDBase[GroupModel, GroupCreate, GroupUpdate](GroupModel)


@router.get("/", response_model=List[Group])
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all groups.
    """
    return crud.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    """
    Create a new group.
    """
    return crud.create(db, obj_in=group)


@router.get("/{group_id}", response_model=Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    """
    Get a specific group by ID.
    """
    db_group = (
        db.query(GroupModel)
        .filter(GroupModel.id == group_id)
        .options(
            # Include the teams relationship
            joinedload(GroupModel.teams)
        )
        .first()
    )

    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@router.put("/{group_id}", response_model=Group)
def update_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    """
    Update a group.
    """
    db_group = crud.get(db, id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.update(db, db_obj=db_group, obj_in=group)


@router.delete("/{group_id}", response_model=Group)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """
    Delete a group.
    """
    return crud.delete(db, id=group_id)


@router.post("/{group_id}/teams", response_model=Group)
def add_team_to_group(
    group_id: int, team_data: TeamToGroup, db: Session = Depends(get_db)
):
    """
    Add a team to a group.
    """
    db_group = (
        db.query(GroupModel)
        .filter(GroupModel.id == group_id)
        .options(joinedload(GroupModel.teams))
        .first()
    )
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    db_team = db.query(TeamModel).filter(TeamModel.id == team_data.team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    db_group.teams.append(db_team)
    db.commit()
    db.refresh(db_group)
    return db_group


@router.delete("/{group_id}/teams/{team_id}", response_model=Group)
def remove_team_from_group(group_id: int, team_id: int, db: Session = Depends(get_db)):
    """
    Remove a team from a group.
    """
    db_group = (
        db.query(GroupModel)
        .filter(GroupModel.id == group_id)
        .options(joinedload(GroupModel.teams))
        .first()
    )
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    if db_team not in db_group.teams:
        raise HTTPException(status_code=400, detail="Team is not in this group")

    db_group.teams.remove(db_team)
    db.commit()
    db.refresh(db_group)
    return db_group

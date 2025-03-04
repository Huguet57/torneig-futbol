
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.db.database import get_db
from app.models.phase import Phase as PhaseModel
from app.schemas.phase import Phase, PhaseCreate, PhaseUpdate

router = APIRouter()
crud = CRUDBase[PhaseModel, PhaseCreate, PhaseUpdate](PhaseModel)


@router.get("/", response_model=list[Phase])
def get_phases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all phases.
    """
    return crud.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=Phase)
def create_phase(phase: PhaseCreate, db: Session = Depends(get_db)):
    """
    Create a new phase.
    """
    return crud.create(db, obj_in=phase)


@router.get("/{phase_id}", response_model=Phase)
def get_phase(phase_id: int, db: Session = Depends(get_db)):
    """
    Get a specific phase by ID.
    """
    db_phase = crud.get(db, id=phase_id)
    if db_phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    return db_phase


@router.put("/{phase_id}", response_model=Phase)
def update_phase(phase_id: int, phase: PhaseUpdate, db: Session = Depends(get_db)):
    """
    Update a phase.
    """
    db_phase = crud.get(db, id=phase_id)
    if db_phase is None:
        raise HTTPException(status_code=404, detail="Phase not found")
    return crud.update(db, db_obj=db_phase, obj_in=phase)


@router.delete("/{phase_id}", response_model=Phase)
def delete_phase(phase_id: int, db: Session = Depends(get_db)):
    """
    Delete a phase.
    """
    return crud.delete(db, id=phase_id)

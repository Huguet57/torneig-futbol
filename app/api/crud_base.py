from typing import Generic, TypeVar, Type, List, Optional, Dict, Any, Union
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get multiple records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = obj_in.model_dump()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        try:
            if isinstance(obj_in, dict):
                obj_data = obj_in
            else:
                obj_data = obj_in.model_dump(exclude_unset=True)
                
            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.get(self.model, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        try:
            db.delete(obj)
            db.commit()
            return obj
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    def get_all_by_fields(self, db: Session, *, fields: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records that match the given field values."""
        query = db.query(self.model)
        for field, value in fields.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()
        
    def get_one_by_fields(self, db: Session, *, fields: Dict[str, Any]) -> Optional[ModelType]:
        """Get a single record that matches the given field values."""
        query = db.query(self.model)
        for field, value in fields.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.first()

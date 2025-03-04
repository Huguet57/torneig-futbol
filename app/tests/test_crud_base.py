from sqlalchemy.orm import Session

from app.api.crud_base import CRUDBase
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


class TestCRUDBase:
    """Test the generic CRUD base class functionality."""
    
    def test_get(self, db: Session):
        """Test getting a single object by ID."""
        # Create a test team to use with CRUD operations
        team = Team(name="Test Team CRUD", short_name="TTC", city="Test City")
        db.add(team)
        db.commit()
        db.refresh(team)
        
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Test get operation
        retrieved_team = crud.get(db, id=team.id)
        assert retrieved_team is not None
        assert retrieved_team.id == team.id
        assert retrieved_team.name == "Test Team CRUD"
        
        # Test get with non-existent ID
        non_existent = crud.get(db, id=999999)
        assert non_existent is None
    
    def test_get_multi(self, db: Session):
        """Test getting multiple objects with pagination."""
        # Create test teams
        teams = [
            Team(name=f"Test Team {i}", short_name=f"TT{i}", city="Test City")
            for i in range(1, 6)  # Create 5 teams
        ]
        db.add_all(teams)
        db.commit()
        
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Test get_multi with default parameters
        all_teams = crud.get_multi(db)
        assert len(all_teams) >= 5  # Should include at least our 5 teams
        
        # Test get_multi with skip
        skipped_teams = crud.get_multi(db, skip=2)
        assert len(skipped_teams) >= 3  # Should include at least 3 teams (5 - 2)
        
        # Test get_multi with limit
        limited_teams = crud.get_multi(db, limit=3)
        assert len(limited_teams) == 3
    
    def test_create(self, db: Session):
        """Test creating a new object."""
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Create team data
        team_data = TeamCreate(
            name="New Team via CRUD",
            short_name="NTVC",
            city="CRUD City"
        )
        
        # Test create operation
        new_team = crud.create(db, obj_in=team_data)
        assert new_team is not None
        assert new_team.name == "New Team via CRUD"
        assert new_team.short_name == "NTVC"
        assert new_team.city == "CRUD City"
        
        # Verify team was created in the database
        db_team = db.query(Team).filter(Team.id == new_team.id).first()
        assert db_team is not None
        assert db_team.name == "New Team via CRUD"
    
    def test_update(self, db: Session):
        """Test updating an existing object."""
        # Create a test team
        team = Team(name="Update Test Team", short_name="UTT", city="Original City")
        db.add(team)
        db.commit()
        db.refresh(team)
        
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Test update with Pydantic model
        update_data = TeamUpdate(name="Updated Team Name", short_name="UTT")
        updated_team = crud.update(db, db_obj=team, obj_in=update_data)
        
        assert updated_team is not None
        assert updated_team.id == team.id
        assert updated_team.name == "Updated Team Name"
        assert updated_team.city == "Original City"  # Should not be changed
        
        # Test update with dict
        dict_update = {"city": "Updated City"}
        dict_updated_team = crud.update(db, db_obj=updated_team, obj_in=dict_update)
        
        assert dict_updated_team is not None
        assert dict_updated_team.name == "Updated Team Name"  # Should not be changed
        assert dict_updated_team.city == "Updated City"
    
    def test_delete(self, db: Session):
        """Test deleting an object."""
        # Create a test team
        team = Team(name="Delete Test Team", short_name="DTT", city="Delete City")
        db.add(team)
        db.commit()
        db.refresh(team)
        
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Get the team ID
        team_id = team.id
        
        # Test delete operation
        deleted_team = crud.delete(db, id=team_id)
        
        assert deleted_team is not None
        assert deleted_team.id == team_id
        assert deleted_team.name == "Delete Test Team"
        
        # Verify team was deleted from the database
        db_team = db.query(Team).filter(Team.id == team_id).first()
        assert db_team is None
    
    def test_get_all_by_fields(self, db: Session):
        """Test getting objects by field values."""
        # Create test teams with different cities
        teams = [
            Team(name="Team A", short_name="TA", city="City X"),
            Team(name="Team B", short_name="TB", city="City X"),
            Team(name="Team C", short_name="TC", city="City Y"),
            Team(name="Team D", short_name="TD", city="City Y"),
            Team(name="Team E", short_name="TE", city="City Z"),
        ]
        db.add_all(teams)
        db.commit()
        
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Test get_all_by_fields with single field
        x_teams = crud.get_all_by_fields(db, fields={"city": "City X"})
        assert len(x_teams) == 2
        assert all(team.city == "City X" for team in x_teams)
        
        # Test get_all_by_fields with multiple fields
        specific_team = crud.get_all_by_fields(
            db, fields={"name": "Team E", "city": "City Z"}
        )
        assert len(specific_team) == 1
        assert specific_team[0].name == "Team E"
        assert specific_team[0].city == "City Z"
        
        # Test get_all_by_fields with non-existent value
        no_teams = crud.get_all_by_fields(db, fields={"city": "Non-existent City"})
        assert len(no_teams) == 0
    
    def test_get_one_by_fields(self, db: Session):
        """Test getting a single object by field values."""
        # Create test teams
        teams = [
            Team(name="Unique Team", short_name="UT", city="City A"),
            Team(name="Duplicate Name", short_name="DN1", city="City B"),
            Team(name="Duplicate Name", short_name="DN2", city="City C"),
        ]
        db.add_all(teams)
        db.commit()
        
        # Create a CRUD object for Team
        crud = CRUDBase[Team, TeamCreate, TeamUpdate](Team)
        
        # Test get_one_by_fields with unique result
        unique_team = crud.get_one_by_fields(db, fields={"name": "Unique Team"})
        assert unique_team is not None
        assert unique_team.name == "Unique Team"
        assert unique_team.city == "City A"
        
        # Test get_one_by_fields with multiple fields
        specific_team = crud.get_one_by_fields(
            db, fields={"name": "Duplicate Name", "city": "City B"}
        )
        assert specific_team is not None
        assert specific_team.name == "Duplicate Name"
        assert specific_team.city == "City B"
        
        # Test get_one_by_fields with non-existent value
        no_team = crud.get_one_by_fields(db, fields={"name": "Non-existent Team"})
        assert no_team is None

    def test_create_with_integrity_error(self, db: Session):
        """Test creating an object that violates database integrity."""
        # Create a test model with a unique constraint
        from sqlalchemy import Column, Integer, String

        from app.db.database import Base
        
        class TestModel(Base):
            __tablename__ = "test_model"
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String, unique=True)
        
        # Create the table
        Base.metadata.create_all(bind=db.get_bind())
        
        # Create CRUD instance
        from pydantic import BaseModel

        from app.api.crud_base import CRUDBase
        
        class TestSchema(BaseModel):
            name: str
        
        crud = CRUDBase[TestModel, TestSchema, TestSchema](TestModel)
        
        # Create first object
        obj1 = crud.create(db, obj_in=TestSchema(name="test"))
        assert obj1.name == "test"
        
        # Try to create another object with the same name
        import pytest
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            crud.create(db, obj_in=TestSchema(name="test"))
        assert exc_info.value.status_code == 400

    def test_update_with_integrity_error(self, db: Session):
        """Test updating an object that would violate database integrity."""
        # Create a test model with a unique constraint
        from sqlalchemy import Column, Integer, String

        from app.db.database import Base
        
        class TestModel(Base):
            __tablename__ = "test_model_update"
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String, unique=True)
        
        # Create the table
        Base.metadata.create_all(bind=db.get_bind())
        
        # Create CRUD instance
        from pydantic import BaseModel

        from app.api.crud_base import CRUDBase
        
        class TestSchema(BaseModel):
            name: str
        
        crud = CRUDBase[TestModel, TestSchema, TestSchema](TestModel)
        
        # Create two objects
        obj1 = crud.create(db, obj_in=TestSchema(name="test1"))
        obj2 = crud.create(db, obj_in=TestSchema(name="test2"))
        
        # Try to update obj2 with obj1's name
        import pytest
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            crud.update(db, db_obj=obj2, obj_in=TestSchema(name="test1"))
        assert exc_info.value.status_code == 400

    def test_delete_with_integrity_error(self, db: Session):
        """Test deleting an object that would violate database integrity."""
        # Enable foreign key support in SQLite
        from sqlalchemy import text
        db.execute(text("PRAGMA foreign_keys = ON"))
        db.commit()
        
        # Create test models with foreign key constraint
        from sqlalchemy import Column, ForeignKey, Integer, String

        from app.db.database import Base
        
        class ParentModel(Base):
            __tablename__ = "parent_model"
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String)
        
        class ChildModel(Base):
            __tablename__ = "child_model"
            id = Column(Integer, primary_key=True, index=True)
            parent_id = Column(Integer, ForeignKey("parent_model.id", ondelete="RESTRICT"))
        
        # Create the tables
        Base.metadata.create_all(bind=db.get_bind())
        
        # Create CRUD instance
        from pydantic import BaseModel

        from app.api.crud_base import CRUDBase
        
        class ParentSchema(BaseModel):
            name: str
        
        crud = CRUDBase[ParentModel, ParentSchema, ParentSchema](ParentModel)
        
        # Create parent and child
        parent = crud.create(db, obj_in=ParentSchema(name="parent"))
        child = ChildModel(parent_id=parent.id)
        db.add(child)
        db.commit()
        
        # Try to delete parent with existing child
        import pytest
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            crud.delete(db, id=parent.id)
        assert exc_info.value.status_code == 400
        assert "Cannot delete item due to existing references" in str(exc_info.value.detail)

    def test_get_all_by_fields_with_invalid_field(self, db: Session):
        """Test get_all_by_fields with a non-existent field."""
        from sqlalchemy import Column, Integer, String

        from app.db.database import Base
        
        class TestModel(Base):
            __tablename__ = "test_model_fields"
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String)
        
        # Create the table
        Base.metadata.create_all(bind=db.get_bind())
        
        # Create CRUD instance
        from pydantic import BaseModel

        from app.api.crud_base import CRUDBase
        
        class TestSchema(BaseModel):
            name: str
        
        crud = CRUDBase[TestModel, TestSchema, TestSchema](TestModel)
        
        # Try to filter by non-existent field
        import pytest
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            crud.get_all_by_fields(db, fields={"nonexistent": "value"})
        assert exc_info.value.status_code == 400 
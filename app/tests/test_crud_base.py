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
from app.models.group import Group
from app.tests.fixtures import (
    create_test_group,
    create_test_phase,
    create_test_tournament,
)


def test_get_groups(client, db):
    """Test listing all groups with pagination."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group1 = create_test_group(db, phase.id)
    group2 = create_test_group(db, phase.id)

    # Test default pagination
    response = client.get("/api/groups/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Should have at least our 2 groups
    group_ids = [g["id"] for g in data]
    assert group1.id in group_ids
    assert group2.id in group_ids

    # Test pagination with limit
    response = client.get("/api/groups/?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    first_group_id = data[0]["id"]

    # Test pagination with skip
    response = client.get("/api/groups/?skip=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] != first_group_id  # Should be different from first group


def test_get_group(client, db):
    """Test getting a specific group by ID."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)

    # Test getting existing group
    response = client.get(f"/api/groups/{group.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == group.id
    assert data["name"] == group.name
    assert data["phase_id"] == phase.id
    assert "teams" in data  # Should include teams relationship

    # Test getting non-existent group
    response = client.get("/api/groups/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"


def test_update_group(client, db):
    """Test updating a group's details."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)

    # Update group name
    new_name = "Updated Group Name"
    response = client.put(
        f"/api/groups/{group.id}",
        json={"name": new_name, "phase_id": phase.id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name
    assert data["phase_id"] == phase.id

    # Verify update in database
    db_group = db.query(Group).filter(Group.id == group.id).first()
    assert db_group.name == new_name

    # Test updating non-existent group
    response = client.put(
        "/api/groups/99999",
        json={"name": "Non-existent Group", "phase_id": phase.id}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Group not found"


def test_delete_group(client, db):
    """Test deleting a group."""
    # Create test data
    tournament = create_test_tournament(db)
    phase = create_test_phase(db, tournament.id)
    group = create_test_group(db, phase.id)

    # Delete group
    response = client.delete(f"/api/groups/{group.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == group.id

    # Verify deletion in database
    db_group = db.query(Group).filter(Group.id == group.id).first()
    assert db_group is None

    # Test deleting non-existent group
    response = client.delete("/api/groups/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found" 
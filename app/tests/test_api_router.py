from fastapi.testclient import TestClient

from app.main import app


def test_api_router_endpoints():
    """Test that all main API endpoints are correctly registered and accessible."""
    client = TestClient(app)
    
    # Test that core endpoints return 200 status code with proper request parameters
    # Test tournaments API
    response = client.get("/api/tournaments/")
    assert response.status_code == 200
    
    # Test teams API
    response = client.get("/api/teams/")
    assert response.status_code == 200
    
    # Test phases API
    response = client.get("/api/phases/")
    assert response.status_code == 200
    
    # Test groups API
    response = client.get("/api/groups/")
    assert response.status_code == 200
    
    # Test matches API 
    response = client.get("/api/matches/")
    assert response.status_code == 200
    
    # Test goals API
    response = client.get("/api/goals/")
    assert response.status_code == 200
    
    # Test players API
    response = client.get("/api/players/")
    assert response.status_code == 200

    # Test player-stats API
    response = client.get("/api/player-stats/")
    assert response.status_code == 200


def test_api_documentation():
    """Test that the API documentation endpoints are accessible."""
    client = TestClient(app)
    
    # Test OpenAPI documentation
    response = client.get("/docs")
    assert response.status_code == 200
    
    # Test ReDoc documentation
    response = client.get("/redoc")
    assert response.status_code == 200
    
    # Test OpenAPI JSON schema
    response = client.get("/openapi.json")
    assert response.status_code == 200 
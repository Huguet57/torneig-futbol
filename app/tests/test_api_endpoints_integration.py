import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPIEndpointsIntegration:
    """Test the API endpoints integration to ensure all routes are registered correctly."""
    
    @pytest.mark.parametrize(
        "endpoint,expected_status_code", 
        [
            ("/api/tournaments/", 200),
            ("/api/teams/", 200),
            ("/api/phases/", 200),
            ("/api/groups/", 200),
            ("/api/matches/", 200),
            ("/api/goals/", 200),
            ("/api/players/", 200),
            ("/api/player-stats/", 200),
            ("/api/team-stats/", 200),
            # Non-existent endpoint should return 404
            ("/api/non-existent/", 404),
        ]
    )
    def test_api_endpoints_exist(self, endpoint, expected_status_code):
        """Test that all API endpoints are correctly registered and respond."""
        response = client.get(endpoint)
        assert response.status_code == expected_status_code, \
            f"Endpoint {endpoint} returned status {response.status_code}, expected {expected_status_code}"
    
    def test_get_documentation(self):
        """Test the API documentation is available."""
        # Test the docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
        # Test the redoc endpoint
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_root_endpoint(self):
        """Test the root endpoint returns expected welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        # Check if it's HTML content (since UI is mounted on root)
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.parametrize("route,expected_status", [
        ("/api/tournaments/1", 404),
        ("/api/teams/1", 404),
        ("/api/players/1", 404),
        ("/api/matches/1", 404),
        ("/api/groups/1", 404),
        ("/api/phases/1", 404),
    ])
    def test_dynamic_routes_nonexistent_id(self, route, expected_status):
        """
        Test dynamic routes with non-existent IDs.
        
        Note: All endpoints now return 404 for non-existent IDs, which is the
        standard RESTful behavior. This is an improvement over the previous
        implementation that returned 200 with empty data.
        """
        response = client.get(route)
        assert response.status_code == expected_status
    
    def test_api_swagger_json(self):
        """Test the OpenAPI specification is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
        
        # Verify it has basic structure
        api_schema = response.json()
        assert "info" in api_schema
        assert "title" in api_schema["info"]
        assert "Soccer Tournament Management System" in api_schema["info"]["title"]
        assert "paths" in api_schema 
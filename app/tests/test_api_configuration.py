"""Test module for API router configuration."""
from fastapi import APIRouter

from app.api.api import api_router


def test_api_router_configuration():
    """Test that the API router is correctly configured with all endpoints."""
    assert isinstance(api_router, APIRouter), "api_router should be an instance of APIRouter"
    
    # Check that all expected routes are registered
    routes = {}
    for route in api_router.routes:
        # Extract prefix from path pattern
        path = str(route.path)
        prefix = "/" + path.split("/")[1]
        if prefix not in routes and hasattr(route, "tags"):
            routes[prefix] = route.tags[0]
    
    expected_routes = {
        "/tournaments": "tournaments",
        "/teams": "teams",
        "/phases": "phases",
        "/groups": "groups",
        "/matches": "matches",
        "/goals": "goals",
        "/players": "players",
        "/player-stats": "player-stats",
        "/team-stats": "team-stats"
    }
    
    # Verify all expected routes are present
    for prefix, tag in expected_routes.items():
        assert prefix in routes, f"Route {prefix} is not registered"
        assert routes[prefix] == tag, f"Route {prefix} has incorrect tag {routes[prefix]}, expected {tag}"
    
    # Verify no unexpected routes are present
    assert len(routes) == len(expected_routes), "Unexpected routes are registered"


def test_api_router_methods():
    """Test that the API router has all necessary HTTP methods for each endpoint."""
    # Get all routes and their methods
    route_methods = {}
    for route in api_router.routes:
        # Extract prefix from path pattern
        path = str(route.path)
        prefix = "/" + path.split("/")[1]
        if prefix not in route_methods:
            route_methods[prefix] = set()
        route_methods[prefix].add(route.methods.pop())  # FastAPI routes have one method per route
    
    # Each endpoint should support at least GET and POST
    for prefix, methods in route_methods.items():
        assert "GET" in methods, f"Route {prefix} does not support GET method"
        assert "POST" in methods, f"Route {prefix} does not support POST method"
        # Most endpoints should also support PUT and DELETE for CRUD operations
        if prefix not in ["/player-stats", "/team-stats"]:  # Exceptions for non-CRUD endpoints
            assert "PUT" in methods, f"Route {prefix} does not support PUT method"
            assert "DELETE" in methods, f"Route {prefix} does not support DELETE method" 
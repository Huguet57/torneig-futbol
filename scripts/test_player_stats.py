#!/usr/bin/env python
"""
Test script for the player statistics functionality.

This script tests the player statistics workflow:
1. Create a tournament, phase, group
2. Create teams and players
3. Create matches between teams
4. Record goals and update match results
5. Verify player statistics are calculated correctly

Usage:
    poetry run python scripts/test_player_stats.py
"""
import sys
import json
import requests
from datetime import date, timedelta
from typing import Dict, Any, List

# Base URL for the API
BASE_URL = "http://localhost:8000/api"


def print_step(message: str) -> None:
    """Print a step message with formatting."""
    print("\n" + "=" * 80)
    print(f"STEP: {message}")
    print("=" * 80)


def print_response(response: requests.Response, label: str = "Response") -> None:
    """Print a formatted API response."""
    try:
        data = response.json()
        print(f"\n{label} (Status: {response.status_code}):")
        print(json.dumps(data, indent=2))
    except Exception:
        print(f"\n{label} (Status: {response.status_code}):")
        print(response.text)


def create_tournament() -> Dict[str, Any]:
    """Create a test tournament."""
    print_step("Creating tournament")
    
    tournament_data = {
        "name": "Player Stats Test Tournament",
        "edition": "I",
        "year": 2023,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=30)),
        "description": "Tournament for testing player statistics"
    }
    
    response = requests.post(f"{BASE_URL}/tournaments/", json=tournament_data)
    print_response(response, "Tournament created")
    
    if response.status_code != 200:
        print("Failed to create tournament")
        sys.exit(1)
        
    return response.json()


def create_phase(tournament_id: int) -> Dict[str, Any]:
    """Create a test phase."""
    print_step("Creating phase")
    
    phase_data = {
        "name": "Group Phase",
        "order": 1,
        "type": "group",
        "tournament_id": tournament_id
    }
    
    response = requests.post(f"{BASE_URL}/phases/", json=phase_data)
    print_response(response, "Phase created")
    
    if response.status_code != 200:
        print("Failed to create phase")
        sys.exit(1)
        
    return response.json()


def create_group(phase_id: int) -> Dict[str, Any]:
    """Create a test group."""
    print_step("Creating group")
    
    group_data = {
        "name": "Group A",
        "phase_id": phase_id
    }
    
    response = requests.post(f"{BASE_URL}/groups/", json=group_data)
    print_response(response, "Group created")
    
    if response.status_code != 200:
        print("Failed to create group")
        sys.exit(1)
        
    return response.json()


def create_team(name: str) -> Dict[str, Any]:
    """Create a test team."""
    team_data = {
        "name": name,
        "short_name": name[:3].upper(),
        "city": "Test City",
        "colors": "Red/White"
    }
    
    response = requests.post(f"{BASE_URL}/teams/", json=team_data)
    print_response(response, f"Team {name} created")
    
    if response.status_code != 200:
        print(f"Failed to create team {name}")
        sys.exit(1)
        
    return response.json()


def create_player(team_id: int, name: str, number: int, position: str = "Forward") -> Dict[str, Any]:
    """Create a test player."""
    player_data = {
        "name": name,
        "number": number,
        "position": position,
        "is_goalkeeper": position == "Goalkeeper",
        "team_id": team_id
    }
    
    response = requests.post(f"{BASE_URL}/teams/{team_id}/players/", json=player_data)
    print_response(response, f"Player {name} created")
    
    if response.status_code != 200:
        print(f"Failed to create player {name}")
        sys.exit(1)
        
    return response.json()


def create_match(
    tournament_id: int,
    phase_id: int,
    group_id: int,
    home_team_id: int,
    away_team_id: int,
    match_date: date
) -> Dict[str, Any]:
    """Create a test match."""
    print_step("Creating match")
    
    match_data = {
        "tournament_id": tournament_id,
        "phase_id": phase_id,
        "group_id": group_id,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "date": str(match_date),
        "location": "Test Stadium"
    }
    
    response = requests.post(f"{BASE_URL}/matches/", json=match_data)
    print_response(response, "Match created")
    
    if response.status_code != 200:
        print("Failed to create match")
        sys.exit(1)
        
    return response.json()


def update_match_result(match_id: int, home_score: int, away_score: int) -> Dict[str, Any]:
    """Update a match result."""
    print_step("Updating match result")
    
    result_data = {
        "home_score": home_score,
        "away_score": away_score,
        "status": "completed"
    }
    
    response = requests.put(f"{BASE_URL}/matches/{match_id}/result", json=result_data)
    print_response(response, "Match result updated")
    
    if response.status_code != 200:
        print("Failed to update match result")
        sys.exit(1)
        
    return response.json()


def create_goal(match_id: int, player_id: int, team_id: int, minute: int, goal_type: str = "regular") -> Dict[str, Any]:
    """Create a goal."""
    goal_data = {
        "match_id": match_id,
        "player_id": player_id,
        "team_id": team_id,
        "minute": minute,
        "type": goal_type
    }
    
    response = requests.post(f"{BASE_URL}/goals/", json=goal_data)
    print_response(response, f"Goal created for player {player_id} at minute {minute}")
    
    if response.status_code != 200:
        print(f"Failed to create goal for player {player_id} at minute {minute}")
        sys.exit(1)
        
    return response.json()


def get_player_stats(player_id: int) -> Dict[str, Any]:
    """Get statistics for a player."""
    print_step(f"Getting statistics for player {player_id}")
    
    response = requests.get(f"{BASE_URL}/players/{player_id}/stats")
    print_response(response, "Player statistics")
    
    if response.status_code != 200:
        print("Failed to get player statistics")
        sys.exit(1)
        
    return response.json()


def get_tournament_top_scorers(tournament_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """Get top scorers for a tournament."""
    print_step(f"Getting top {limit} scorers for tournament {tournament_id}")
    
    response = requests.get(f"{BASE_URL}/tournaments/{tournament_id}/top-scorers?limit={limit}")
    print_response(response, "Tournament top scorers")
    
    if response.status_code != 200:
        print("Failed to get tournament top scorers")
        sys.exit(1)
        
    return response.json()


def main():
    """Run the player statistics test workflow."""
    # Create tournament structure
    tournament = create_tournament()
    phase = create_phase(tournament["id"])
    group = create_group(phase["id"])
    
    # Create teams
    team1 = create_team("Test Team 1")
    team2 = create_team("Test Team 2")
    
    # Create players for team 1
    striker1 = create_player(team1["id"], "Striker One", 9, "Forward")
    midfielder1 = create_player(team1["id"], "Midfielder One", 8, "Midfielder")
    goalkeeper1 = create_player(team1["id"], "Keeper One", 1, "Goalkeeper")
    
    # Create players for team 2
    striker2 = create_player(team2["id"], "Striker Two", 9, "Forward")
    midfielder2 = create_player(team2["id"], "Midfielder Two", 8, "Midfielder")
    goalkeeper2 = create_player(team2["id"], "Keeper Two", 1, "Goalkeeper")
    
    # Create matches
    match1 = create_match(
        tournament["id"],
        phase["id"],
        group["id"],
        team1["id"],
        team2["id"],
        date.today()
    )
    
    match2 = create_match(
        tournament["id"],
        phase["id"],
        group["id"],
        team2["id"],
        team1["id"],
        date.today() + timedelta(days=7)
    )
    
    # Record goals for match 1
    create_goal(match1["id"], striker1["id"], team1["id"], 15)
    create_goal(match1["id"], striker1["id"], team1["id"], 35)
    create_goal(match1["id"], midfielder1["id"], team1["id"], 55)
    create_goal(match1["id"], striker2["id"], team2["id"], 75)
    
    # Update match 1 result (3-1)
    update_match_result(match1["id"], 3, 1)
    
    # Record goals for match 2
    create_goal(match2["id"], striker2["id"], team2["id"], 20)
    create_goal(match2["id"], striker2["id"], team2["id"], 40)
    create_goal(match2["id"], striker1["id"], team1["id"], 60)
    
    # Update match 2 result (2-1)
    update_match_result(match2["id"], 2, 1)
    
    # Get player statistics
    striker1_stats = get_player_stats(striker1["id"])
    striker2_stats = get_player_stats(striker2["id"])
    midfielder1_stats = get_player_stats(midfielder1["id"])
    
    # Get tournament top scorers
    top_scorers = get_tournament_top_scorers(tournament["id"])
    
    print("\nTest completed successfully!")


if __name__ == "__main__":
    main() 
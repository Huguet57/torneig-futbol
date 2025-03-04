#!/usr/bin/env python
"""
Test script for the goal tracking functionality.

This script tests the goal tracking workflow:
1. Create a tournament, phase, group
2. Create teams and players
3. Create a match between teams
4. Record goals for the match
5. Retrieve goals by match, player, and team

Usage:
    poetry run python scripts/test_goal_tracking.py
"""
import json
import sys
from datetime import date, timedelta
from typing import Any

import requests

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


def create_tournament() -> dict[str, Any]:
    """Create a test tournament."""
    print_step("Creating tournament")
    
    tournament_data = {
        "name": "Goal Tracking Test Tournament",
        "edition": "I",
        "year": 2023,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=30)),
        "description": "Tournament for testing goal tracking"
    }
    
    response = requests.post(f"{BASE_URL}/tournaments/", json=tournament_data)
    print_response(response, "Tournament created")
    
    if response.status_code != 200:
        print("Failed to create tournament")
        sys.exit(1)
        
    return response.json()


def create_phase(tournament_id: int) -> dict[str, Any]:
    """Create a test phase."""
    print_step("Creating phase")
    
    phase_data = {
        "name": "Group Phase",
        "order": 1,
        "type": "group",
        "tournament_id": tournament_id
    }
    
    response = requests.post(
        f"{BASE_URL}/phases/", 
        json=phase_data
    )
    print_response(response, "Phase created")
    
    if response.status_code != 200:
        print("Failed to create phase")
        sys.exit(1)
        
    return response.json()


def create_group(phase_id: int) -> dict[str, Any]:
    """Create a test group."""
    print_step("Creating group")
    
    group_data = {
        "name": "Group A",
        "phase_id": phase_id
    }
    
    response = requests.post(
        f"{BASE_URL}/groups/", 
        json=group_data
    )
    print_response(response, "Group created")
    
    if response.status_code != 200:
        print("Failed to create group")
        sys.exit(1)
        
    return response.json()


def create_team(name: str) -> dict[str, Any]:
    """Create a test team."""
    team_data = {
        "name": name,
        "short_name": name[:3].upper(),
        "city": "Test City",
        "colors": "Red/White"
    }
    
    response = requests.post(f"{BASE_URL}/teams/", json=team_data)
    
    if response.status_code != 200:
        print(f"Failed to create team {name}")
        sys.exit(1)
        
    return response.json()


def create_player(team_id: int, name: str, number: int, is_goalkeeper: bool = False) -> dict[str, Any]:
    """Create a test player."""
    player_data = {
        "name": name,
        "number": number,
        "position": "Goalkeeper" if is_goalkeeper else "Forward",
        "is_goalkeeper": is_goalkeeper,
        "team_id": team_id
    }
    
    # Note: This endpoint is assumed to exist based on the API documentation
    response = requests.post(f"{BASE_URL}/teams/{team_id}/players/", json=player_data)
    
    if response.status_code != 200:
        print(f"Failed to create player {name}")
        sys.exit(1)
        
    return response.json()


def create_match(
    tournament_id: int,
    phase_id: int,
    group_id: int,
    home_team_id: int,
    away_team_id: int
) -> dict[str, Any]:
    """Create a test match."""
    print_step("Creating match")
    
    match_data = {
        "tournament_id": tournament_id,
        "phase_id": phase_id,
        "group_id": group_id,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "date": str(date.today()),
        "location": "Test Stadium"
    }
    
    response = requests.post(f"{BASE_URL}/matches/", json=match_data)
    print_response(response, "Match created")
    
    if response.status_code != 200:
        print("Failed to create match")
        sys.exit(1)
        
    return response.json()


def update_match_result(match_id: int, home_score: int, away_score: int) -> dict[str, Any]:
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


def create_goal(match_id: int, player_id: int, team_id: int, minute: int, goal_type: str = "regular") -> dict[str, Any]:
    """Create a goal."""
    goal_data = {
        "match_id": match_id,
        "player_id": player_id,
        "team_id": team_id,
        "minute": minute,
        "type": goal_type
    }
    
    response = requests.post(f"{BASE_URL}/goals/", json=goal_data)
    
    if response.status_code != 200:
        print(f"Failed to create goal for player {player_id} at minute {minute}")
        sys.exit(1)
        
    return response.json()


def get_goals_by_match(match_id: int) -> list[dict[str, Any]]:
    """Get all goals for a match."""
    print_step("Getting goals by match")
    
    response = requests.get(f"{BASE_URL}/goals/match/{match_id}")
    print_response(response, "Goals for match")
    
    if response.status_code != 200:
        print("Failed to get goals by match")
        sys.exit(1)
        
    return response.json()


def get_goals_by_player(player_id: int) -> list[dict[str, Any]]:
    """Get all goals for a player."""
    print_step("Getting goals by player")
    
    response = requests.get(f"{BASE_URL}/goals/player/{player_id}")
    print_response(response, "Goals for player")
    
    if response.status_code != 200:
        print("Failed to get goals by player")
        sys.exit(1)
        
    return response.json()


def get_goals_by_team(team_id: int) -> list[dict[str, Any]]:
    """Get all goals for a team."""
    print_step("Getting goals by team")
    
    response = requests.get(f"{BASE_URL}/goals/team/{team_id}")
    print_response(response, "Goals for team")
    
    if response.status_code != 200:
        print("Failed to get goals by team")
        sys.exit(1)
        
    return response.json()


def main():
    """Run the goal tracking test workflow."""
    print("\nStarting goal tracking test workflow...\n")
    
    # Step 1: Create tournament structure
    tournament = create_tournament()
    phase = create_phase(tournament["id"])
    group = create_group(phase["id"])
    
    # Step 2: Create teams
    print_step("Creating teams")
    team1 = create_team("Goal Team 1")
    team2 = create_team("Goal Team 2")
    print(f"Created teams: {team1['name']} and {team2['name']}")
    
    # Step 3: Create players
    print_step("Creating players")
    player1_1 = create_player(team1["id"], "Player 1-1", 9)
    player1_2 = create_player(team1["id"], "Player 1-2", 10)
    player2_1 = create_player(team2["id"], "Player 2-1", 7)
    player2_2 = create_player(team2["id"], "Player 2-2", 11)
    print("Created 4 players (2 for each team)")
    
    # Step 4: Create a match
    match = create_match(
        tournament["id"],
        phase["id"],
        group["id"],
        team1["id"],
        team2["id"]
    )
    
    # Step 5: Update match result
    match = update_match_result(match["id"], 3, 2)
    
    # Step 6: Record goals
    print_step("Recording goals")
    
    # Goals for team 1
    goal1 = create_goal(match["id"], player1_1["id"], team1["id"], 15)
    goal2 = create_goal(match["id"], player1_2["id"], team1["id"], 35)
    goal3 = create_goal(match["id"], player1_1["id"], team1["id"], 75)
    
    # Goals for team 2
    goal4 = create_goal(match["id"], player2_1["id"], team2["id"], 25)
    goal5 = create_goal(match["id"], player2_2["id"], team2["id"], 85)
    
    print("Recorded 5 goals (3 for team 1, 2 for team 2)")
    
    # Step 7: Retrieve goals by different criteria
    match_goals = get_goals_by_match(match["id"])
    player_goals = get_goals_by_player(player1_1["id"])
    team_goals = get_goals_by_team(team1["id"])
    
    # Print summary
    print("\n" + "=" * 80)
    print("GOAL TRACKING TEST SUMMARY")
    print("=" * 80)
    print(f"Total goals in match: {len(match_goals)}")
    print(f"Goals by {player1_1['name']}: {len(player_goals)}")
    print(f"Goals by {team1['name']}: {len(team_goals)}")
    print("\nGoal tracking test workflow completed successfully!")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python
"""
Test script for the complete match management workflow.

This script tests the entire match management workflow:
1. Create a tournament
2. Create phases and groups
3. Create teams and assign to groups
4. Create matches between teams
5. Update match results
6. View group standings

Usage:
    poetry run python scripts/test_match_workflow.py
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
        "name": "Test Tournament",
        "edition": "I",
        "year": 2023,
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=30)),
        "description": "Tournament for testing match workflow"
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
        "city": "Test City"
    }
    
    response = requests.post(f"{BASE_URL}/teams/", json=team_data)
    
    if response.status_code != 200:
        print(f"Failed to create team {name}")
        sys.exit(1)
        
    return response.json()


def create_teams() -> List[Dict[str, Any]]:
    """Create multiple test teams."""
    print_step("Creating teams")
    
    teams = []
    for i in range(1, 5):
        team = create_team(f"Team {i}")
        teams.append(team)
        print(f"Created team: {team['name']} (ID: {team['id']})")
    
    return teams


def assign_teams_to_group(group_id: int, team_ids: List[int]) -> None:
    """Assign teams to a group."""
    print_step("Assigning teams to group")
    
    for team_id in team_ids:
        response = requests.post(
            f"{BASE_URL}/groups/{group_id}/teams",
            json={"team_id": team_id}
        )
        
        if response.status_code != 200:
            print(f"Failed to assign team {team_id} to group {group_id}")
            sys.exit(1)
            
        print(f"Assigned team ID {team_id} to group ID {group_id}")


def create_match(
    tournament_id: int,
    phase_id: int,
    group_id: int,
    home_team_id: int,
    away_team_id: int,
    match_date: date
) -> Dict[str, Any]:
    """Create a test match."""
    match_data = {
        "tournament_id": tournament_id,
        "phase_id": phase_id,
        "group_id": group_id,
        "home_team_id": home_team_id,
        "away_team_id": away_team_id,
        "date": str(match_date),
        "location": "Test Field"
    }
    
    response = requests.post(f"{BASE_URL}/matches/", json=match_data)
    
    if response.status_code != 200:
        print(f"Failed to create match between teams {home_team_id} and {away_team_id}")
        print_response(response, "Error")
        sys.exit(1)
        
    return response.json()


def create_matches(tournament_id: int, phase_id: int, group_id: int, team_ids: List[int]) -> List[Dict[str, Any]]:
    """Create matches between all teams in the group."""
    print_step("Creating matches")
    
    matches = []
    match_date = date.today() + timedelta(days=7)
    
    # Create matches for all team combinations
    for i, home_team_id in enumerate(team_ids):
        for away_team_id in team_ids[i+1:]:
            match = create_match(
                tournament_id,
                phase_id,
                group_id,
                home_team_id,
                away_team_id,
                match_date
            )
            matches.append(match)
            print(f"Created match: {match['home_team']['name']} vs {match['away_team']['name']} (ID: {match['id']})")
            match_date += timedelta(days=1)
    
    return matches


def update_match_result(match_id: int, home_score: int, away_score: int) -> Dict[str, Any]:
    """Update a match result."""
    result_data = {
        "home_score": home_score,
        "away_score": away_score,
        "status": "completed"
    }
    
    response = requests.put(f"{BASE_URL}/matches/{match_id}/result", json=result_data)
    
    if response.status_code != 200:
        print(f"Failed to update result for match {match_id}")
        print_response(response, "Error")
        sys.exit(1)
        
    return response.json()


def update_match_results(matches: List[Dict[str, Any]]) -> None:
    """Update results for all matches."""
    print_step("Updating match results")
    
    # Set some sample results
    results = [
        (3, 1),  # Team 1 vs Team 2: 3-1
        (2, 2),  # Team 1 vs Team 3: 2-2
        (1, 0),  # Team 1 vs Team 4: 1-0
        (0, 2),  # Team 2 vs Team 3: 0-2
        (2, 1),  # Team 2 vs Team 4: 2-1
        (3, 3),  # Team 3 vs Team 4: 3-3
    ]
    
    for match, (home_score, away_score) in zip(matches, results):
        updated_match = update_match_result(match["id"], home_score, away_score)
        print(f"Updated match {updated_match['id']}: {updated_match['home_team']['name']} {home_score}-{away_score} {updated_match['away_team']['name']}")


def get_group_standings(group_id: int) -> List[Dict[str, Any]]:
    """Get standings for a group."""
    print_step("Getting group standings")
    
    response = requests.get(f"{BASE_URL}/standings/group/{group_id}")
    
    if response.status_code != 200:
        print(f"Failed to get standings for group {group_id}")
        sys.exit(1)
        
    standings = response.json()
    print_response(response, "Group standings")
    
    # Print standings in a more readable format
    print("\nStandings Table:")
    print(f"{'Team':<20} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GF':>3} {'GA':>3} {'GD':>3} {'Pts':>3}")
    print("-" * 50)
    
    for standing in standings:
        print(
            f"{standing['team_name']:<20} "
            f"{standing['matches_played']:>3} "
            f"{standing['wins']:>3} "
            f"{standing['draws']:>3} "
            f"{standing['losses']:>3} "
            f"{standing['goals_for']:>3} "
            f"{standing['goals_against']:>3} "
            f"{standing['goal_difference']:>3} "
            f"{standing['points']:>3}"
        )
    
    return standings


def main():
    """Run the complete match management workflow test."""
    print("Starting match management workflow test...")
    
    # Step 1: Create tournament structure
    tournament = create_tournament()
    phase = create_phase(tournament["id"])
    group = create_group(phase["id"])
    
    # Step 2: Create teams and assign to group
    teams = create_teams()
    team_ids = [team["id"] for team in teams]
    assign_teams_to_group(group["id"], team_ids)
    
    # Step 3: Create matches
    matches = create_matches(tournament["id"], phase["id"], group["id"], team_ids)
    
    # Step 4: Update match results
    update_match_results(matches)
    
    # Step 5: View standings
    standings = get_group_standings(group["id"])
    
    print("\nMatch management workflow test completed successfully!")


if __name__ == "__main__":
    main() 
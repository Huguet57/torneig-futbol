"""
Test script for team statistics functionality.

This script tests:
1. Retrieving team statistics
2. Updating team statistics based on match results
3. Getting tournament team rankings
"""
import os
import sys
import requests
from pprint import pprint

# Get base URL from environment or use default
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api")


def main():
    """Run team statistics test scenarios."""
    print("\n=== Team Statistics Test Script ===\n")
    
    # Get all tournaments to select one for testing
    print("Getting tournaments...")
    response = requests.get(f"{BASE_URL}/tournaments/")
    response.raise_for_status()
    tournaments = response.json()
    
    if not tournaments:
        print("No tournaments found. Please create a tournament first.")
        sys.exit(1)
    
    # Select the first tournament for testing
    tournament = tournaments[0]
    tournament_id = tournament["id"]
    print(f"Selected tournament: {tournament['name']} (ID: {tournament_id})")
    
    # Get teams in the tournament
    print("\nGetting teams...")
    response = requests.get(f"{BASE_URL}/teams/")
    response.raise_for_status()
    teams = response.json()
    
    if not teams:
        print("No teams found. Please create teams first.")
        sys.exit(1)
    
    print(f"Found {len(teams)} teams")
    
    # Test 1: Update team statistics for each team
    print("\n--- Test 1: Update Team Statistics ---")
    for team in teams:
        team_id = team["id"]
        print(f"Updating statistics for team {team['name']} (ID: {team_id})...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/team-stats/update/{team_id}/{tournament_id}"
            )
            response.raise_for_status()
            stats = response.json()
            print(f"  - Matches: {stats['matches_played']}")
            print(f"  - Record: {stats['wins']}-{stats['draws']}-{stats['losses']}")
            print(f"  - Goals: {stats['goals_for']}-{stats['goals_against']} (Diff: {stats['goal_difference']})")
            print(f"  - Points: {stats['points']}")
        except requests.RequestException as e:
            print(f"Error updating team stats: {e}")
    
    # Test 2: Get tournament team rankings
    print("\n--- Test 2: Get Tournament Team Rankings ---")
    try:
        response = requests.get(
            f"{BASE_URL}/team-stats/tournament/{tournament_id}"
        )
        response.raise_for_status()
        ranked_teams = response.json()
        
        print("\nTeam Rankings:")
        print("-" * 50)
        print(f"{'Pos':>3} | {'Team':<20} | {'P':>3} | {'W':>3}-{'D':>3}-{'L':>3} | {'GF':>3}-{'GA':>3} | {'GD':>3} | {'Pts':>3}")
        print("-" * 50)
        
        for i, team in enumerate(ranked_teams, 1):
            # Get the team name
            team_id = team["team_id"]
            team_name = next((t["name"] for t in teams if t["id"] == team_id), "Unknown")
            
            print(
                f"{i:3} | {team_name:<20} | {team['matches_played']:>3} | "
                f"{team['wins']:>3}-{team['draws']:>3}-{team['losses']:>3} | "
                f"{team['goals_for']:>3}-{team['goals_against']:>3} | "
                f"{team['goal_difference']:>3} | {team['points']:>3}"
            )
    except requests.RequestException as e:
        print(f"Error getting tournament rankings: {e}")
    
    # Test 3: Get team statistics for a specific team
    print("\n--- Test 3: Get Team Statistics for a Specific Team ---")
    if teams:
        selected_team = teams[0]
        team_id = selected_team["id"]
        team_name = selected_team["name"]
        
        try:
            response = requests.get(
                f"{BASE_URL}/team-stats",
                params={"team_id": team_id, "tournament_id": tournament_id}
            )
            response.raise_for_status()
            stats = response.json()
            
            print(f"\nStatistics for {team_name} in tournament {tournament['name']}:")
            if stats:
                pprint(stats[0])
            else:
                print("No statistics found.")
        except requests.RequestException as e:
            print(f"Error getting team stats: {e}")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    main() 
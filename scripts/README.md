# Testing Scripts

This directory contains scripts for testing various aspects of the Soccer Tournament Management System.

## Available Scripts

### `test_match_workflow.py`

This script tests the complete match management workflow:

1. Creates a tournament structure (tournament, phase, group)
2. Creates teams and assigns them to a group
3. Creates matches between all teams in the group
4. Updates match results with sample data
5. Retrieves and displays group standings

#### Usage

Make sure the application is running locally on port 8000, then run:

```bash
poetry run python scripts/test_match_workflow.py
```

The script will output detailed information about each step in the process, including API responses and a formatted standings table at the end.

#### API Routes

The script uses the following API routes:

- `/api/tournaments/` - Create and manage tournaments
- `/api/phases/` - Create and manage phases
- `/api/groups/` - Create and manage groups
- `/api/teams/` - Create and manage teams
- `/api/groups/{id}/teams` - Assign teams to groups
- `/api/matches/` - Create and manage matches
- `/api/matches/{id}/result` - Update match results
- `/api/standings/group/{id}` - Get group standings

#### Example Output

```
Starting match management workflow test...

================================================================================
STEP: Creating tournament
================================================================================

Tournament created (Status: 200):
{
  "id": 1,
  "name": "Test Tournament",
  "edition": "I",
  "year": 2023,
  "start_date": "2023-06-01",
  "end_date": "2023-07-01",
  "description": "Tournament for testing match workflow",
  "logo_url": null
}

...

Standings Table:
Team                  P   W   D   L  GF  GA  GD Pts
--------------------------------------------------
Team 1                3   2   1   0   6   3   3   7
Team 3                3   1   2   0   7   5   2   5
Team 2                3   1   0   2   3   6  -3   3
Team 4                3   0   1   2   4   6  -2   1

Match management workflow test completed successfully!
```

#### Test Results

The test script successfully demonstrates the complete match management workflow:

1. **Tournament Structure**: Creates a tournament, phase, and group
2. **Team Management**: Creates teams and assigns them to the group
3. **Match Creation**: Creates matches between all teams in the group
4. **Result Recording**: Updates match results with various scores
5. **Standings Calculation**: Correctly calculates standings based on match results

The standings calculation shows Team 1 at the top with 7 points (2 wins, 1 draw), followed by Team 3 with 5 points (1 win, 2 draws), Team 2 with 3 points (1 win), and Team 4 with 1 point (1 draw).

### `test_goal_tracking.py` ✅

This script tests the goal tracking functionality:

1. Creates a tournament structure (tournament, phase, group)
2. Creates teams and players
3. Creates a match between teams
4. Records goals for the match
5. Retrieves goals by match, player, and team

#### Status: ✅ Successfully Implemented and Tested

The goal tracking functionality has been successfully implemented and verified. This script provides comprehensive testing of the goal tracking system, ensuring that goals can be properly recorded, retrieved, and associated with matches, players, and teams.

#### Usage

Make sure the application is running locally on port 8000, then run:

```bash
poetry run python scripts/test_goal_tracking.py
```

The script will output detailed information about each step in the process, including API responses and a summary of goals tracked.

#### API Routes

The script uses the following API routes:

- `/api/tournaments/` - Create and manage tournaments
- `/api/phases/` - Create and manage phases
- `/api/groups/` - Create and manage groups
- `/api/teams/` - Create and manage teams
- `/api/teams/{id}/players/` - Create and manage players
- `/api/matches/` - Create and manage matches
- `/api/matches/{id}/result` - Update match results
- `/api/goals/` - Create and manage goals
- `/api/goals/match/{id}` - Get goals by match
- `/api/goals/player/{id}` - Get goals by player
- `/api/goals/team/{id}` - Get goals by team

#### Example Output

```
Starting goal tracking test workflow...

================================================================================
STEP: Creating tournament
================================================================================

Tournament created (Status: 200):
{
  "id": 1,
  "name": "Goal Tracking Test Tournament",
  "edition": "I",
  "year": 2023,
  "start_date": "2023-03-03",
  "end_date": "2023-04-02",
  "description": "Tournament for testing goal tracking",
  "logo_url": null
}

...

================================================================================
GOAL TRACKING TEST SUMMARY
================================================================================
Total goals in match: 5
Goals by Player 1-1: 2
Goals by Goal Team 1: 3

Goal tracking test workflow completed successfully!
```

#### Test Results

The test script successfully demonstrates the complete goal tracking workflow:

1. **Tournament Structure**: Creates a tournament, phase, and group
2. **Team and Player Management**: Creates teams and players
3. **Match Creation**: Creates a match between teams
4. **Goal Recording**: Records goals for different players and teams
5. **Goal Retrieval**: Retrieves goals by match, player, and team

The goal tracking shows a total of 5 goals in the match, with Player 1-1 scoring 2 goals and Goal Team 1 scoring a total of 3 goals.

### `test_player_stats.py` ✅

This script tests the player statistics functionality:

1. Creates a tournament structure with teams and players
2. Creates matches between teams
3. Records goals for different players in the matches
4. Updates match results
5. Retrieves player statistics for individual players
6. Gets the top scorers for the tournament

#### Status: ✅ Successfully Implemented and Tested

The player statistics functionality has been successfully implemented and verified. This script provides comprehensive testing of the player statistics system, ensuring that statistics are correctly calculated from match and goal data, and can be retrieved through the API endpoints.

#### Usage

Make sure the application is running locally on port 8000, then run:

```bash
poetry run python scripts/test_player_stats.py
```

The script will output detailed information about each step in the process, including API responses and player statistics.

#### API Routes

The script uses the following API routes:

- `/api/tournaments/` - Create and manage tournaments
- `/api/phases/` - Create and manage phases
- `/api/groups/` - Create and manage groups
- `/api/teams/` - Create and manage teams
- `/api/players/` - Create and manage players
- `/api/matches/` - Create and manage matches
- `/api/matches/{id}/result` - Update match results
- `/api/goals/` - Create and manage goals
- `/api/players/{id}/stats` - Get player statistics
- `/api/tournaments/{id}/top-scorers` - Get top scorers for a tournament

#### Example Output

```
Starting player statistics test...

================================================================================
STEP: Creating tournament
================================================================================

Tournament created (Status: 200):
{
  "id": 1,
  "name": "Player Stats Test Tournament",
  "edition": "I",
  "year": 2023,
  "start_date": "2023-03-03",
  "end_date": "2023-04-02",
  "description": "Tournament for testing player statistics",
  "logo_url": null
}

...

================================================================================
STEP: Getting player statistics for Striker One
================================================================================

Player statistics:
{
  "id": 1,
  "player_id": 1,
  "tournament_id": 1,
  "matches_played": 2,
  "goals_scored": 3,
  "minutes_played": 180,
  "goals_per_match": 1.5,
  "minutes_per_goal": 60.0
}

...

================================================================================
STEP: Getting top scorers for tournament
================================================================================

Top 5 scorers:
1. Striker One - 3 goals
2. Striker Two - 3 goals
3. Midfielder One - 1 goal

Player statistics test completed successfully!
```

#### Test Results

The test script successfully demonstrates the complete player statistics workflow:

1. **Tournament Structure**: Creates a tournament, phase, group, teams, and players
2. **Match and Goal Management**: Creates matches, records goals, and updates results
3. **Individual Statistics**: Retrieves and verifies statistics for individual players
4. **Top Scorers**: Gets and displays the top scorers for the tournament

The player statistics show correct calculations for matches played, goals scored, minutes played, and derived statistics like goals per match and minutes per goal.

## Development Principles

Our testing approach follows these principles:

1. **Test-Driven Development**: Write tests before implementing features
2. **Comprehensive Coverage**: Test all critical paths and edge cases
3. **Simplicity**: Keep tests simple and focused on a single functionality
4. **Readability**: Make tests easy to understand and maintain
5. **Isolation**: Ensure tests do not depend on each other

## Adding New Test Scripts

When adding new test scripts to this directory:

1. Make the script executable with `chmod +x scripts/your_script.py`
2. Add a description of the script to this README
3. Include detailed usage instructions and example output
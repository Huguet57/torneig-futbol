# Match Management

This document provides detailed information about the match management functionality in the Soccer Tournament Management System.

## Overview

The match management module allows tournament organizers to:
- Create and schedule matches between teams
- Update match details (date, time, location)
- Record match results
- View match listings filtered by tournament, phase, or group
- Calculate team standings based on match results

## Data Models

### Match

The core match entity contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique identifier |
| tournament_id | Integer | Reference to Tournament |
| phase_id | Integer | Reference to Phase |
| group_id | Integer (optional) | Reference to Group (nullable for knockout matches) |
| home_team_id | Integer | Reference to Team (home) |
| away_team_id | Integer | Reference to Team (away) |
| date | Date | Match date |
| time | Time (optional) | Match time |
| location | String (optional) | Match location/field |
| home_score | Integer (optional) | Home team's score |
| away_score | Integer (optional) | Away team's score |
| status | Enum | Match status: "scheduled", "in-progress", "completed" |

### Match Status

Matches can have one of the following statuses:
- `scheduled`: Default status for newly created matches
- `in-progress`: Match is currently being played
- `completed`: Match has finished and has a final result

## API Endpoints

### Creating a Match

```http
POST /matches/
Content-Type: application/json

{
  "tournament_id": 1,
  "phase_id": 2,
  "group_id": 3,
  "home_team_id": 4,
  "away_team_id": 5,
  "date": "2023-06-15",
  "time": "18:00:00",
  "location": "Field 1"
}
```

Response:
```json
{
  "id": 1,
  "tournament_id": 1,
  "phase_id": 2,
  "group_id": 3,
  "home_team_id": 4,
  "away_team_id": 5,
  "date": "2023-06-15",
  "time": "18:00:00",
  "location": "Field 1",
  "home_score": null,
  "away_score": null,
  "status": "scheduled",
  "home_team": {
    "id": 4,
    "name": "Team A",
    "short_name": "TA",
    "logo_url": "https://example.com/logo_a.png"
  },
  "away_team": {
    "id": 5,
    "name": "Team B",
    "short_name": "TB",
    "logo_url": "https://example.com/logo_b.png"
  }
}
```

### Updating Match Results

```http
PUT /matches/1/result
Content-Type: application/json

{
  "home_score": 2,
  "away_score": 1
}
```

Response:
```json
{
  "id": 1,
  "tournament_id": 1,
  "phase_id": 2,
  "group_id": 3,
  "home_team_id": 4,
  "away_team_id": 5,
  "date": "2023-06-15",
  "time": "18:00:00",
  "location": "Field 1",
  "home_score": 2,
  "away_score": 1,
  "status": "completed",
  "home_team": {
    "id": 4,
    "name": "Team A",
    "short_name": "TA",
    "logo_url": "https://example.com/logo_a.png"
  },
  "away_team": {
    "id": 5,
    "name": "Team B",
    "short_name": "TB",
    "logo_url": "https://example.com/logo_b.png"
  }
}
```

## Team Standings

When match results are recorded, the system automatically calculates team standings for the group. Standings include:

- Matches played
- Wins, draws, and losses
- Goals scored and conceded
- Goal difference
- Total points (3 for a win, 1 for a draw)

### Retrieving Group Standings

```http
GET /standings/group/3
```

Response:
```json
[
  {
    "team_id": 4,
    "team_name": "Team A",
    "team_short_name": "TA",
    "team_logo_url": "https://example.com/logo_a.png",
    "matches_played": 1,
    "wins": 1,
    "draws": 0,
    "losses": 0,
    "goals_for": 2,
    "goals_against": 1,
    "goal_difference": 1,
    "points": 3
  },
  {
    "team_id": 5,
    "team_name": "Team B",
    "team_short_name": "TB",
    "team_logo_url": "https://example.com/logo_b.png",
    "matches_played": 1,
    "wins": 0,
    "draws": 0,
    "losses": 1,
    "goals_for": 1,
    "goals_against": 2,
    "goal_difference": -1,
    "points": 0
  }
]
```

## Match Management Workflow

1. **Create Tournament Structure**
   - Create tournament
   - Add phases (e.g., group phase, knockout phase)
   - Create groups within phases
   - Assign teams to groups

2. **Schedule Matches**
   - Create matches between teams in the same group
   - Set date, time, and location for each match

3. **Record Results**
   - Update match results as games are played
   - System automatically calculates standings

4. **View Standings**
   - Check group standings to see team rankings
   - Standings are sorted by points and goal difference

## Implementation Notes

- Match creation validates that teams exist and belong to the specified group
- Teams cannot play against themselves (home_team_id must be different from away_team_id)
- Match results can only be updated with non-negative scores
- When a match result is updated, the status is automatically set to "completed"
- Standings are calculated dynamically based on all completed matches in a group 
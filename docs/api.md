# API Documentation

This document outlines the API endpoints for the Soccer Tournament Management System.

## Tournament Management
- `GET /tournaments`: List all tournaments
- `GET /tournaments/{id}`: Get tournament details
- `POST /tournaments`: Create new tournament
- `PUT /tournaments/{id}`: Update tournament
- `DELETE /tournaments/{id}`: Delete tournament

## Phase Management
- `GET /tournaments/{id}/phases`: List all phases for a tournament
- `GET /phases/{id}`: Get phase details
- `POST /tournaments/{id}/phases`: Create new phase
- `PUT /phases/{id}`: Update phase
- `DELETE /phases/{id}`: Delete phase

## Group Management
- `GET /phases/{id}/groups`: List all groups for a phase
- `GET /groups/{id}`: Get group details
- `POST /phases/{id}/groups`: Create new group
- `PUT /groups/{id}`: Update group
- `DELETE /groups/{id}`: Delete group

## Team Management
- `GET /teams`: List all teams
- `GET /teams/{id}`: Get team details
- `POST /teams`: Create new team
- `PUT /teams/{id}`: Update team
- `DELETE /teams/{id}`: Delete team
- `POST /groups/{id}/teams`: Add team to group

## Player Management
- `GET /teams/{id}/players`: List all players for a team
- `GET /players/{id}`: Get player details
- `POST /teams/{id}/players`: Create new player
- `PUT /players/{id}`: Update player
- `DELETE /players/{id}`: Delete player

## Match Management

### Match CRUD Operations
- `GET /matches/{id}`: Get match details by ID
  - Returns complete match information including related teams
  - Response includes match status, scores, and location

- `POST /matches/`: Create a new match
  - Requires tournament_id, phase_id, home_team_id, away_team_id, and date
  - Optional fields: group_id, time, location

- `PUT /matches/{id}`: Update match details
  - Can update any match field except ID
  - Partial updates are supported (only include fields to be updated)

- `DELETE /matches/{id}`: Delete a match
  - Permanently removes the match from the database

### Match Filtering
- `GET /matches/tournament/{id}`: List all matches for a tournament
  - Returns matches filtered by tournament ID
  - Supports pagination with skip and limit parameters

- `GET /matches/phase/{id}`: List all matches for a phase
  - Returns matches filtered by phase ID
  - Supports pagination with skip and limit parameters

- `GET /matches/group/{id}`: List all matches for a group
  - Returns matches filtered by group ID
  - Supports pagination with skip and limit parameters

### Match Results
- `PUT /matches/{id}/result`: Update match result
  - Updates home_score, away_score, and sets status to "completed"
  - Automatically triggers standings recalculation for the group

## Statistics
- `GET /standings/group/{id}`: Get group standings
  - Returns calculated standings for all teams in a group
  - Includes matches played, wins, draws, losses, goals, and points
  - Sorted by points (descending) and goal difference

- `GET /tournaments/{id}/players/stats`: Get player statistics for tournament
- `GET /tournaments/{id}/teams/stats`: Get team statistics for tournament 
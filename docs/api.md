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

## Goal Management

### Goal CRUD Operations
- `GET /goals/{id}`: Get goal details by ID
  - Returns complete goal information including player and team
  - Response includes minute, type, and related entities

- `POST /goals/`: Create a new goal
  - Requires match_id, player_id, team_id, and minute
  - Optional fields: type (regular, penalty, own_goal)

- `PUT /goals/{id}`: Update goal details
  - Can update any goal field except ID
  - Partial updates are supported (only include fields to be updated)

- `DELETE /goals/{id}`: Delete a goal
  - Permanently removes the goal from the database

### Goal Filtering
- `GET /goals/match/{id}`: List all goals for a match
  - Returns goals filtered by match ID
  - Supports pagination with skip and limit parameters

- `GET /goals/player/{id}`: List all goals for a player
  - Returns goals filtered by player ID
  - Supports pagination with skip and limit parameters

- `GET /goals/team/{id}`: List all goals for a team
  - Returns goals filtered by team ID
  - Supports pagination with skip and limit parameters

## Statistics

### Team Statistics
- `GET /standings/group/{id}`: Get group standings
  - Returns calculated standings for all teams in a group
  - Includes matches played, wins, draws, losses, goals, and points
  - Sorted by points (descending) and goal difference

### Player Statistics (In Development)
The following endpoints for player statistics are currently under development:

- `GET /player-stats/{id}`: Get player statistics by player ID
  - Returns complete statistics for a specific player
  - Includes matches played, goals scored, minutes played

- `GET /player-stats/tournament/{id}`: Get all player statistics for a tournament
  - Returns statistics for all players in a tournament
  - Supports filtering by top scorers, position, and team
  - Includes pagination with skip and limit parameters

- `GET /player-stats/team/{id}`: Get player statistics for a team
  - Returns statistics for all players in a specific team
  - Useful for team performance analysis
  - Supports pagination and sorting options

- `GET /player-stats/match/{id}`: Get player statistics for a specific match
  - Returns statistics for all players who participated in a match
  - Shows players who scored goals with goal details

- `POST /player-stats/recalculate/{player_id}`: Recalculate statistics for a player
  - Triggers recalculation of statistics based on recorded goals and matches
  - Admin-only endpoint for data maintenance

## Implementation Philosophy

The API implementation follows these principles:

1. **Simplicity First**: Endpoints are designed to be straightforward and intuitive
2. **Consistent Response Format**: All endpoints return data in a consistent JSON structure
3. **Error Handling**: Clear error messages with appropriate HTTP status codes
4. **Pagination**: List endpoints support pagination for efficient data retrieval
5. **Filtering**: Support for filtering data to retrieve only what's needed
6. **Performance**: Optimized queries to ensure fast response times 
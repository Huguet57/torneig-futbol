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
- `GET /tournaments/{id}/matches`: List all matches for a tournament
- `GET /phases/{id}/matches`: List all matches for a phase
- `GET /groups/{id}/matches`: List all matches for a group
- `GET /matches/{id}`: Get match details
- `POST /tournaments/{id}/matches`: Create new match
- `PUT /matches/{id}`: Update match
- `DELETE /matches/{id}`: Delete match
- `PUT /matches/{id}/result`: Update match result

## Statistics
- `GET /tournaments/{id}/standings`: Get tournament standings
- `GET /groups/{id}/standings`: Get group standings
- `GET /tournaments/{id}/players/stats`: Get player statistics for tournament
- `GET /tournaments/{id}/teams/stats`: Get team statistics for tournament 
# API Examples

This document provides detailed examples for using the Soccer Tournament Management System API.

## Authentication

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Refresh Token
```http
POST /auth/refresh
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Tournament Management

### Create Tournament
```http
POST /tournaments/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "Summer Cup 2024",
  "start_date": "2024-06-01",
  "end_date": "2024-06-30",
  "description": "Annual summer soccer tournament"
}
```

Response:
```json
{
  "id": 1,
  "name": "Summer Cup 2024",
  "start_date": "2024-06-01",
  "end_date": "2024-06-30",
  "description": "Annual summer soccer tournament",
  "created_at": "2024-03-04T12:00:00Z",
  "updated_at": "2024-03-04T12:00:00Z"
}
```

### Get Tournament Details
```http
GET /tournaments/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "id": 1,
  "name": "Summer Cup 2024",
  "start_date": "2024-06-01",
  "end_date": "2024-06-30",
  "description": "Annual summer soccer tournament",
  "created_at": "2024-03-04T12:00:00Z",
  "updated_at": "2024-03-04T12:00:00Z",
  "phases": [
    {
      "id": 1,
      "name": "Group Stage",
      "type": "group",
      "groups": [
        {
          "id": 1,
          "name": "Group A",
          "teams": []
        }
      ]
    }
  ]
}
```

### List Tournaments with Pagination
```http
GET /tournaments/?skip=0&limit=10
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "items": [
    {
      "id": 1,
      "name": "Summer Cup 2024",
      "start_date": "2024-06-01",
      "end_date": "2024-06-30"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

## Team Management

### Create Team
```http
POST /teams/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "Red Dragons",
  "city": "Barcelona",
  "description": "Local amateur team"
}
```

Response:
```json
{
  "id": 1,
  "name": "Red Dragons",
  "city": "Barcelona",
  "description": "Local amateur team",
  "created_at": "2024-03-04T12:00:00Z",
  "updated_at": "2024-03-04T12:00:00Z"
}
```

### Add Team to Group
```http
POST /groups/1/teams
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "team_id": 1
}
```

Response:
```json
{
  "id": 1,
  "group_id": 1,
  "team_id": 1,
  "points": 0,
  "matches_played": 0,
  "wins": 0,
  "draws": 0,
  "losses": 0,
  "goals_for": 0,
  "goals_against": 0
}
```

## Match Management

### Create Match
```http
POST /matches/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "tournament_id": 1,
  "phase_id": 1,
  "group_id": 1,
  "home_team_id": 1,
  "away_team_id": 2,
  "date": "2024-06-01T15:00:00Z",
  "location": "Main Stadium"
}
```

Response:
```json
{
  "id": 1,
  "tournament_id": 1,
  "phase_id": 1,
  "group_id": 1,
  "home_team_id": 1,
  "away_team_id": 2,
  "home_score": null,
  "away_score": null,
  "date": "2024-06-01T15:00:00Z",
  "location": "Main Stadium",
  "status": "scheduled",
  "created_at": "2024-03-04T12:00:00Z",
  "updated_at": "2024-03-04T12:00:00Z"
}
```

### Update Match Result
```http
PUT /matches/1/result
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "home_score": 2,
  "away_score": 1,
  "status": "completed"
}
```

Response:
```json
{
  "id": 1,
  "tournament_id": 1,
  "phase_id": 1,
  "group_id": 1,
  "home_team_id": 1,
  "away_team_id": 2,
  "home_score": 2,
  "away_score": 1,
  "date": "2024-06-01T15:00:00Z",
  "location": "Main Stadium",
  "status": "completed",
  "updated_at": "2024-03-04T12:30:00Z"
}
```

## Goal Management

### Record Goal
```http
POST /goals/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "match_id": 1,
  "player_id": 1,
  "team_id": 1,
  "minute": 35,
  "type": "regular"
}
```

Response:
```json
{
  "id": 1,
  "match_id": 1,
  "player_id": 1,
  "team_id": 1,
  "minute": 35,
  "type": "regular",
  "created_at": "2024-03-04T12:35:00Z"
}
```

## Statistics

### Get Team Statistics
```http
GET /team-stats/tournament/1/team/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "team_id": 1,
  "tournament_id": 1,
  "matches_played": 1,
  "wins": 1,
  "draws": 0,
  "losses": 0,
  "goals_for": 2,
  "goals_against": 1,
  "points": 3,
  "goal_difference": 1,
  "win_percentage": 100.0
}
```

### Get Player Statistics
```http
GET /player-stats/tournament/1/player/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "player_id": 1,
  "tournament_id": 1,
  "matches_played": 1,
  "goals_scored": 1,
  "assists": 0,
  "minutes_played": 90,
  "goals_per_match": 1.0
}
```

### Get Tournament Top Scorers
```http
GET /tournaments/1/top-scorers?limit=5
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "items": [
    {
      "player_id": 1,
      "name": "John Doe",
      "team_name": "Red Dragons",
      "goals_scored": 1,
      "matches_played": 1,
      "goals_per_match": 1.0
    }
  ],
  "total": 1,
  "limit": 5
}
```

## Error Responses

### Resource Not Found
```http
GET /tournaments/999
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "detail": {
    "message": "Tournament not found",
    "code": "NOT_FOUND",
    "params": {
      "id": 999
    }
  }
}
```

### Validation Error
```http
POST /tournaments/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "",
  "start_date": "invalid-date"
}
```

Response:
```json
{
  "detail": {
    "message": "Validation error",
    "code": "VALIDATION_ERROR",
    "params": {
      "name": ["Field required"],
      "start_date": ["Invalid date format"]
    }
  }
}
```

### Rate Limit Exceeded
```http
GET /tournaments/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

Response:
```json
{
  "detail": {
    "message": "Rate limit exceeded",
    "code": "RATE_LIMIT_EXCEEDED",
    "params": {
      "retry_after": 60
    }
  }
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- Authenticated requests: 1000 requests per hour
- Unauthenticated requests: 100 requests per hour

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1709561400
```

## Pagination

List endpoints support pagination using `skip` and `limit` parameters:

```http
GET /tournaments/?skip=0&limit=10
GET /matches/?skip=20&limit=20
GET /teams/?skip=40&limit=10
```

Response format:
```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 10
}
``` 
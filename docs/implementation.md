# Implementation Details

This document outlines the implementation details for the Soccer Tournament Management System, including database design and technology choices.

## Database Design

### Core Entities

#### Tournament
- `id`: Unique identifier
- `name`: Tournament name
- `edition`: Tournament edition (e.g., "XXI")
- `year`: Year of the tournament
- `start_date`: Start date
- `end_date`: End date
- `description`: Tournament description
- `logo_url`: Tournament logo URL

#### Phase
- `id`: Unique identifier
- `tournament_id`: Reference to Tournament
- `name`: Phase name (e.g., "Group Phase", "Gold Phase", "Silver Phase")
- `order`: Order in which phases occur
- `type`: Type of phase (e.g., "group", "elimination")

#### Group
- `id`: Unique identifier
- `phase_id`: Reference to Phase
- `name`: Group name (e.g., "Group A", "Group B")

#### Team
- `id`: Unique identifier
- `name`: Team name
- `short_name`: Abbreviated team name
- `logo_url`: Team logo URL
- `city`: Team's city
- `colors`: Team colors

#### Player
- `id`: Unique identifier
- `team_id`: Reference to Team
- `name`: Player's name
- `number`: Jersey number
- `position`: Playing position
- `is_goalkeeper`: Boolean indicating if player is a goalkeeper

#### Match
- `id`: Unique identifier
- `tournament_id`: Reference to Tournament
- `phase_id`: Reference to Phase
- `group_id`: Reference to Group (nullable for knockout matches)
- `home_team_id`: Reference to Team (home)
- `away_team_id`: Reference to Team (away)
- `date`: Match date
- `time`: Match time
- `location`: Match location/field
- `home_score`: Home team's score
- `away_score`: Away team's score
- `status`: Match status (scheduled, in-progress, completed)

#### Goal
- `id`: Unique identifier
- `match_id`: Reference to Match
- `player_id`: Reference to Player who scored
- `team_id`: Reference to Team
- `minute`: Minute when goal was scored
- `type`: Type of goal (regular, penalty, own goal)

### Derived Entities (For Calculations)

#### TeamStanding
- `id`: Unique identifier
- `tournament_id`: Reference to Tournament
- `phase_id`: Reference to Phase
- `group_id`: Reference to Group
- `team_id`: Reference to Team
- `matches_played`: Number of matches played
- `wins`: Number of wins
- `draws`: Number of draws
- `losses`: Number of losses
- `goals_for`: Goals scored
- `goals_against`: Goals conceded
- `goal_difference`: Goal difference
- `points`: Total points

#### PlayerStats
- `id`: Unique identifier
- `tournament_id`: Reference to Tournament
- `phase_id`: Reference to Phase (nullable)
- `player_id`: Reference to Player
- `team_id`: Reference to Team
- `matches_played`: Number of matches played
- `goals`: Number of goals scored
- `minutes_played`: Minutes played

## Technology Stack

### Backend
- **Programming Language**: Python
- **Web Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **API Documentation**: Swagger/OpenAPI

### Optional Frontend
- **Framework**: React
- **State Management**: Redux
- **UI Components**: Material-UI or Bootstrap
- **Charts**: Chart.js or D3.js 
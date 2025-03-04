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
- `type`: Type of goal (regular, penalty, own_goal)
- Implementation Status: ✅ Completed

### Derived Entities (For Calculations)

#### TeamStats
- `id`: Unique identifier
- `tournament_id`: Reference to Tournament
- `team_id`: Reference to Team
- `matches_played`: Number of matches played
- `wins`: Number of wins
- `draws`: Number of draws
- `losses`: Number of losses
- `goals_for`: Goals scored
- `goals_against`: Goals conceded
- `goal_difference`: Goal difference (calculated)
- `clean_sheets`: Number of matches without conceding goals
- `points`: Total points
- `position`: Team position in tournament (nullable)
- `win_percentage`: Percentage of matches won (calculated)
- `goals_per_match`: Average goals per match (calculated)
- `points_per_match`: Average points per match (calculated)
- Implementation Status: ✅ Completed

#### PlayerStats
- `id`: Unique identifier
- `player_id`: Reference to Player
- `tournament_id`: Reference to Tournament
- `matches_played`: Number of matches played
- `goals_scored`: Number of goals scored (calculated from Goal records)
- `minutes_played`: Minutes played
- `goals_per_match`: Calculated ratio of goals per match
- `minutes_per_goal`: Calculated ratio of minutes per goal
- Implementation Status: ✅ Completed

## Technology Stack

### Backend
- **Programming Language**: Python
- **Web Framework**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **API Documentation**: Swagger/OpenAPI

### Optional Frontend
- **Framework**: React
- **State Management**: Redux
- **UI Components**: Material-UI or Bootstrap
- **Charts**: Chart.js or D3.js 

## Implementation Progress

### Completed Components
- ✅ Base database models and configuration
- ✅ Tournament, Team, Phase, Group, Player management
- ✅ Match scheduling and result tracking
- ✅ Team standings calculation
- ✅ Goal tracking system
- ✅ Player statistics tracking and calculations
- ✅ Tournament top scorers functionality
- ✅ Enhanced team statistics with performance metrics

### Upcoming Work for MVP 4
- Phase progression rules
- Tournament templates
- Automatic scheduling
- UI improvements for statistics visualization
- Advanced reporting capabilities

### Development Philosophy
- Focus on simplicity and core functionality
- Implement features incrementally with thorough testing
- Prioritize stability and performance over feature abundance
- Ensure comprehensive error handling and validation 
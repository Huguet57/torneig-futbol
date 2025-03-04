# System Architecture

This document outlines the architecture of the Soccer Tournament Management System.

## System Overview

```mermaid
graph TB
    subgraph Client Layer
        UI[Web UI]
        API_Client[API Client]
    end

    subgraph API Layer
        FastAPI[FastAPI Application]
        Middleware[Middleware]
        Router[API Routers]
    end

    subgraph Service Layer
        TournamentService[Tournament Service]
        MatchService[Match Service]
        StatsService[Statistics Service]
    end

    subgraph Data Layer
        DB[(SQLite Database)]
        Models[SQLAlchemy Models]
        Schemas[Pydantic Schemas]
    end

    UI --> API_Client
    API_Client --> FastAPI
    FastAPI --> Middleware
    Middleware --> Router
    Router --> TournamentService
    Router --> MatchService
    Router --> StatsService
    TournamentService --> Models
    MatchService --> Models
    StatsService --> Models
    Models --> DB
    Models <--> Schemas
```

## Database Schema

```mermaid
erDiagram
    Tournament ||--o{ Phase : contains
    Phase ||--o{ Group : contains
    Group ||--o{ TeamGroup : contains
    Team ||--o{ TeamGroup : belongs_to
    Team ||--o{ Player : has
    Match }|--|| Group : belongs_to
    Match ||--o{ Goal : has
    Goal }|--|| Player : scored_by
    Player ||--o{ PlayerStats : has
    Tournament ||--o{ PlayerStats : tracks

    Tournament {
        int id PK
        string name
        date start_date
        date end_date
    }

    Phase {
        int id PK
        int tournament_id FK
        string name
        string type
    }

    Group {
        int id PK
        int phase_id FK
        string name
    }

    Team {
        int id PK
        string name
        string city
    }

    TeamGroup {
        int id PK
        int team_id FK
        int group_id FK
        int points
    }

    Player {
        int id PK
        int team_id FK
        string name
        string position
    }

    Match {
        int id PK
        int group_id FK
        int home_team_id FK
        int away_team_id FK
        int home_score
        int away_score
        datetime date
        string status
    }

    Goal {
        int id PK
        int match_id FK
        int player_id FK
        int team_id FK
        int minute
        string type
    }

    PlayerStats {
        int id PK
        int player_id FK
        int tournament_id FK
        int matches_played
        int goals_scored
        int assists
    }
```

## Component Interaction

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant S as Service
    participant D as Database

    C->>A: HTTP Request
    A->>A: Validate Request
    A->>S: Process Request
    S->>D: Query Data
    D-->>S: Return Data
    S->>S: Process Data
    S-->>A: Return Result
    A-->>C: HTTP Response
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth Service
    participant API as API
    participant D as Database

    C->>A: Login Request
    A->>D: Validate Credentials
    D-->>A: User Data
    A->>A: Generate JWT
    A-->>C: Return Token
    C->>API: API Request + Token
    API->>API: Validate Token
    API->>D: Process Request
    D-->>API: Return Data
    API-->>C: Return Response
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Production
        LB[Load Balancer]
        subgraph App Servers
            API1[API Server 1]
            API2[API Server 2]
        end
        DB[(Database)]
        Cache[(Cache)]
    end

    subgraph Monitoring
        Logs[Log Aggregator]
        Metrics[Metrics Server]
        Alerts[Alert Manager]
    end

    Client-->LB
    LB-->API1
    LB-->API2
    API1-->DB
    API2-->DB
    API1-->Cache
    API2-->Cache
    API1-->Logs
    API2-->Logs
    Logs-->Metrics
    Metrics-->Alerts
```

## Design Decisions

### 1. Database Choice
- SQLite for development simplicity
- Easy migration path to PostgreSQL for production
- Built-in support in SQLAlchemy

### 2. API Design
- RESTful architecture for simplicity and familiarity
- FastAPI for automatic OpenAPI documentation
- Pydantic for request/response validation

### 3. Authentication
- JWT-based authentication
- Token refresh mechanism
- Role-based access control

### 4. Performance Considerations
- Database indexing on frequently queried fields
- Caching for static data
- Pagination for large result sets

### 5. Scalability
- Stateless API design
- Horizontal scaling capability
- Database connection pooling

## Technology Stack

1. **Backend Framework**
   - FastAPI (ASGI)
   - Uvicorn server

2. **Database**
   - SQLite (Development)
   - SQLAlchemy ORM
   - Alembic migrations

3. **API Documentation**
   - OpenAPI (Swagger)
   - ReDoc

4. **Testing**
   - Pytest
   - Coverage.py
   - Factory Boy

5. **Code Quality**
   - Ruff
   - Mypy
   - Pre-commit hooks

6. **Monitoring**
   - Structured logging
   - Sentry error tracking
   - Health check endpoints

## Security Measures

1. **API Security**
   - HTTPS only
   - CORS configuration
   - Rate limiting
   - Input validation

2. **Data Security**
   - Parameterized queries
   - Input sanitization
   - Secure password storage

3. **Authentication**
   - JWT with expiration
   - Secure token storage
   - Role-based access

## Future Considerations

1. **Scalability**
   - Migration to PostgreSQL
   - Redis caching
   - Load balancing

2. **Features**
   - Real-time updates
   - Advanced statistics
   - Mobile app support

3. **Integration**
   - External APIs
   - Notification system
   - Data export/import 
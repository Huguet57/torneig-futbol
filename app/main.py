from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api import tournament, team, phase, group, match, standings, goal, player, player_stats, team_stats
from app.ui import ui_router

app = FastAPI(
    title="Soccer Tournament Management System",
    description="API for managing soccer tournaments, teams, and matches",
    version="0.1.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include routers
app.include_router(tournament.router, prefix="/api/tournaments", tags=["tournaments"])
app.include_router(team.router, prefix="/api/teams", tags=["teams"])
app.include_router(phase.router, prefix="/api/phases", tags=["phases"])
app.include_router(group.router, prefix="/api/groups", tags=["groups"])
app.include_router(match.router, prefix="/api/matches", tags=["matches"])
app.include_router(standings.router, prefix="/api/standings", tags=["standings"])
app.include_router(goal.router, prefix="/api/goals", tags=["goals"])
app.include_router(player.router, prefix="/api/players", tags=["players"])
app.include_router(player_stats.router, prefix="/api/player-stats", tags=["player-stats"])
app.include_router(team_stats.router, prefix="/api/team-stats", tags=["team-stats"])

# Include UI router
app.include_router(ui_router.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Soccer Tournament Management System API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }

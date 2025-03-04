from fastapi import APIRouter

from app.api.endpoints import (
    tournaments,
    teams,
    phases,
    groups,
    matches,
    goals,
    players
)
from app.api import player_stats

api_router = APIRouter()

api_router.include_router(tournaments.router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(phases.router, prefix="/phases", tags=["phases"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(player_stats.router, prefix="/player-stats", tags=["player-stats"]) 
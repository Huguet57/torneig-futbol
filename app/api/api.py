from fastapi import APIRouter

from app.api import (
    tournament,
    team,
    phase,
    group,
    match,
    goal,
    player,
    player_stats,
    team_stats
)

api_router = APIRouter()

api_router.include_router(tournament.router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(team.router, prefix="/teams", tags=["teams"])
api_router.include_router(phase.router, prefix="/phases", tags=["phases"])
api_router.include_router(group.router, prefix="/groups", tags=["groups"])
api_router.include_router(match.router, prefix="/matches", tags=["matches"])
api_router.include_router(goal.router, prefix="/goals", tags=["goals"])
api_router.include_router(player.router, prefix="/players", tags=["players"])
api_router.include_router(player_stats.router, prefix="/player-stats", tags=["player-stats"])
api_router.include_router(team_stats.router, prefix="/team-stats", tags=["team-stats"]) 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import structlog
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.api import tournament, team, phase, group, match, standings, goal, player, player_stats, team_stats
from app.ui import ui_router
from app.db.database import engine, Base

# Configure structured logging
logger = structlog.get_logger()
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(structlog.get_logger().level),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

# Initialize Sentry
sentry_sdk.init(
    dsn="your-sentry-dsn",  # Replace with your Sentry DSN
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title="Soccer Tournament Management System",
    description="API for managing soccer tournaments, teams, matches, and statistics",
    version="1.0.0",
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

# Create database tables
Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with structured logging."""
    logger.info(
        "request_started",
        path=request.url.path,
        method=request.method,
        client=request.client.host if request.client else None,
    )
    response = await call_next(request)
    logger.info(
        "request_completed",
        path=request.url.path,
        method=request.method,
        status_code=response.status_code,
    )
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",  # We could add actual DB health check here
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint that redirects to the UI home page."""
    return {"message": "Welcome to the Soccer Tournament Management System API"}

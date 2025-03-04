from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from datetime import date, time
from pathlib import Path
from typing import Optional

from app.db.database import get_db
from app.models import Tournament, Team, Phase, Group, Match, Player, Goal, PlayerStats, TeamStats
from app.core.standings import calculate_group_standings

# Initialize templates
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # Get system statistics
    stats = {
        "tournaments": db.query(Tournament).count(),
        "teams": db.query(Team).count(),
        "phases": db.query(Phase).count(),
        "groups": db.query(Group).count(),
        "matches": db.query(Match).count(),
    }

    return templates.TemplateResponse(
        request,
        "index.html", 
        {"stats": stats}
    )


# Match routes
@router.get("/matches", response_class=HTMLResponse)
async def list_matches(
    request: Request,
    tournament_id: Optional[int] = None,
    phase_id: Optional[int] = None,
    group_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Match).options(
        joinedload(Match.tournament),
        joinedload(Match.phase),
        joinedload(Match.group),
        joinedload(Match.home_team),
        joinedload(Match.away_team),
    )
    
    if tournament_id:
        query = query.filter(Match.tournament_id == tournament_id)
    if phase_id:
        query = query.filter(Match.phase_id == phase_id)
    if group_id:
        query = query.filter(Match.group_id == group_id)
    
    matches = query.order_by(Match.date, Match.time).all()
    tournaments = db.query(Tournament).all()
    phases = db.query(Phase).all() if tournament_id else []
    groups = db.query(Group).all() if phase_id else []
    
    return templates.TemplateResponse(
        request,
        "matches/list.html",
        {
            "matches": matches,
            "tournaments": tournaments,
            "phases": phases,
            "groups": groups,
            "selected_tournament_id": tournament_id,
            "selected_phase_id": phase_id,
            "selected_group_id": group_id,
        },
    )


@router.get("/matches/create", response_class=HTMLResponse)
async def create_match_form(
    request: Request,
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    tournaments = db.query(Tournament).all()
    phases = []
    groups = []
    teams = db.query(Team).all()
    
    if tournament_id:
        phases = db.query(Phase).filter(Phase.tournament_id == tournament_id).all()
    
    return templates.TemplateResponse(
        request,
        "matches/create.html",
        {
            "tournaments": tournaments,
            "teams": teams,
            "phases": phases,
            "groups": groups,
            "selected_tournament_id": tournament_id,
        },
    )


@router.post("/matches/create")
async def create_match(
    request: Request,
    tournament_id: int = Form(...),
    phase_id: int = Form(...),
    group_id: Optional[int] = Form(None),
    home_team_id: int = Form(...),
    away_team_id: int = Form(...),
    date: date = Form(...),
    time: Optional[time] = Form(None),
    location: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    match = Match(
        tournament_id=tournament_id,
        phase_id=phase_id,
        group_id=group_id,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        date=date,
        time=time,
        location=location,
        status="scheduled",
    )
    db.add(match)
    db.commit()
    
    return RedirectResponse(url=f"/matches/{match.id}", status_code=303)


@router.get("/matches/{match_id}", response_class=HTMLResponse)
async def view_match(
    request: Request,
    match_id: int,
    db: Session = Depends(get_db),
):
    match = db.query(Match).options(
        joinedload(Match.tournament),
        joinedload(Match.phase),
        joinedload(Match.group),
        joinedload(Match.home_team),
        joinedload(Match.away_team),
    ).filter(Match.id == match_id).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Get goals for this match
    goals = db.query(Goal).options(
        joinedload(Goal.player),
        joinedload(Goal.team)
    ).filter(Goal.match_id == match_id).order_by(Goal.minute).all()
    
    # Get previous and next matches in the same group/phase
    prev_match = None
    next_match = None
    
    if match.group_id:
        prev_match = db.query(Match).filter(
            Match.group_id == match.group_id,
            Match.id < match_id
        ).order_by(Match.id.desc()).first()
        
        next_match = db.query(Match).filter(
            Match.group_id == match.group_id,
            Match.id > match_id
        ).order_by(Match.id).first()
    else:
        prev_match = db.query(Match).filter(
            Match.phase_id == match.phase_id,
            Match.id < match_id
        ).order_by(Match.id.desc()).first()
        
        next_match = db.query(Match).filter(
            Match.phase_id == match.phase_id,
            Match.id > match_id
        ).order_by(Match.id).first()
    
    # Get standings if match is in a group
    standings = []
    if match.group_id and match.status == "completed":
        standings = calculate_group_standings(db, match.group_id)
    
    return templates.TemplateResponse(
        request,
        "matches/view.html",
        {
            "match": match,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "tournament": match.tournament,
            "phase": match.phase,
            "group": match.group,
            "goals": goals,
            "prev_match": prev_match,
            "next_match": next_match,
            "standings": standings,
        },
    )


@router.get("/matches/{match_id}/result", response_class=HTMLResponse)
async def update_match_result_form(
    request: Request,
    match_id: int,
    db: Session = Depends(get_db),
):
    match = db.query(Match).options(
        joinedload(Match.tournament),
        joinedload(Match.phase),
        joinedload(Match.group),
        joinedload(Match.home_team),
        joinedload(Match.away_team),
    ).filter(Match.id == match_id).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return templates.TemplateResponse(
        request,
        "matches/result.html",
        {"match": match},
    )


@router.post("/matches/{match_id}/result")
async def update_match_result(
    request: Request,
    match_id: int,
    home_score: int = Form(...),
    away_score: int = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    match.home_score = home_score
    match.away_score = away_score
    match.status = status
    db.commit()
    
    return RedirectResponse(url=f"/matches/{match_id}", status_code=303)


# Tournament routes
@router.get("/tournaments", response_class=HTMLResponse)
async def list_tournaments(request: Request, db: Session = Depends(get_db)):
    tournaments = db.query(Tournament).all()

    return templates.TemplateResponse(
        request,
        "tournaments/list.html", 
        {"tournaments": tournaments}
    )


@router.get("/tournaments/create", response_class=HTMLResponse)
async def create_tournament_form(request: Request):
    return templates.TemplateResponse(request, "tournaments/create.html", {})


@router.post("/tournaments/create")
async def create_tournament(
    request: Request,
    name: str = Form(...),
    edition: str = Form(...),
    year: int = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    description: Optional[str] = Form(None),
    logo_url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    tournament_data = {
        "name": name,
        "edition": edition,
        "year": year,
        "start_date": start_date,
        "end_date": end_date,
        "description": description,
        "logo_url": logo_url,
    }

    tournament = Tournament(**tournament_data)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)

    return RedirectResponse(url="/tournaments", status_code=303)


@router.get("/tournaments/{tournament_id}", response_class=HTMLResponse)
async def view_tournament(
    request: Request, tournament_id: int, db: Session = Depends(get_db)
):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    phases = db.query(Phase).filter(Phase.tournament_id == tournament_id).all()

    return templates.TemplateResponse(
        request,
        "tournaments/view.html",
        {
            "tournament": tournament,
            "phases": phases,
            "groups": groups,
            "teams": teams,
            "matches": matches,
            "standings": standings,
        },
    )


# Player routes
@router.get("/players", response_class=HTMLResponse)
async def list_players(
    request: Request,
    team_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Player).options(
        joinedload(Player.team),
        joinedload(Player.goals),
    )
    
    if team_id:
        query = query.filter(Player.team_id == team_id)
    
    players = query.all()
    teams = db.query(Team).all()
    
    return templates.TemplateResponse(
        request,
        "players/index.html",
        {
            "players": players,
            "teams": teams,
            "selected_team_id": team_id,
        },
    )


@router.get("/players/{player_id}", response_class=HTMLResponse)
async def view_player(
    request: Request,
    player_id: int,
    db: Session = Depends(get_db),
):
    player = db.query(Player).options(
        joinedload(Player.team),
        joinedload(Player.goals).joinedload(Goal.match).joinedload(Match.home_team),
        joinedload(Player.goals).joinedload(Goal.match).joinedload(Match.away_team),
    ).filter(Player.id == player_id).first()
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    goals = db.query(Goal).filter(Goal.player_id == player_id).all()
    
    # Calculate basic statistics
    matches_played = len(set(goal.match_id for goal in goals))
    total_goals = len(goals)
    goals_per_match = round(total_goals / matches_played, 2) if matches_played > 0 else 0
    
    stats = {
        "matches_played": matches_played,
        "goals": total_goals,
        "goals_per_match": goals_per_match,
    }
    
    return templates.TemplateResponse(
        request,
        "players/view.html",
        {
            "player": player,
            "team": player.team,
            "stats": stats,
            "goals": goals,
        },
    )


# Goal routes
@router.get("/goals", response_class=HTMLResponse)
async def goals_page(
    request: Request,
    tournament_id: Optional[int] = None,
    team_id: Optional[int] = None,
    player_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Goals page."""
    # Build query with optional filters
    query = db.query(Goal).options(
        joinedload(Goal.match).joinedload(Match.tournament),
        joinedload(Goal.player),
        joinedload(Goal.team),
    )

    if tournament_id:
        query = query.join(Match).filter(Match.tournament_id == tournament_id)

    if team_id:
        query = query.filter(Goal.team_id == team_id)

    if player_id:
        query = query.filter(Goal.player_id == player_id)

    goals = query.order_by(Goal.match_id, Goal.minute).all()

    # Get filter options
    tournaments = db.query(Tournament).all()
    teams = db.query(Team).all()
    players = db.query(Player).options(joinedload(Player.team)).all()
    
    return templates.TemplateResponse(
        request,
        "goals/index.html",
        {
            "goals": goals,
            "tournaments": tournaments,
            "teams": teams,
            "players": players,
            "selected_tournament_id": tournament_id,
            "selected_team_id": team_id,
            "selected_player_id": player_id,
        },
    )


@router.get("/player-stats", response_class=HTMLResponse)
async def list_player_stats(
    request: Request,
    tournament_id: Optional[int] = None,
    team_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List all player statistics with optional filtering."""
    # Get tournaments and teams for filtering
    tournaments = db.query(Tournament).all()
    teams = db.query(Team).all()
    
    # Build query with eager loading of related entities
    query = db.query(PlayerStats).options(
        joinedload(PlayerStats.player),
        joinedload(PlayerStats.tournament),
        joinedload(PlayerStats.player).joinedload(Player.team)
    ).order_by(PlayerStats.goals_scored.desc())
    
    # Apply filters if provided
    if tournament_id:
        query = query.filter(PlayerStats.tournament_id == tournament_id)
    
    if team_id:
        query = query.join(Player).filter(Player.team_id == team_id)
    
    player_stats = query.all()
    
    return templates.TemplateResponse(
        request,
        "player_stats/list.html",
        {
            "player_stats": player_stats,
            "tournaments": tournaments,
            "teams": teams,
            "selected_tournament_id": tournament_id,
            "selected_team_id": team_id,
        },
    )


# Add similar routes for teams, phases, and groups
# For brevity, we'll implement just the tournament and match routes for now

@router.get("/teams", response_class=HTMLResponse)
async def list_teams(
    request: Request,
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List all teams or teams in a specific tournament."""
    query = db.query(Team)
    
    if tournament_id:
        # If tournament_id is provided, filter teams that have participated in that tournament
        query = query.join(Match, (Team.id == Match.home_team_id) | (Team.id == Match.away_team_id))\
                    .filter(Match.tournament_id == tournament_id)\
                    .distinct()
    
    teams = query.order_by(Team.name).all()
    tournaments = db.query(Tournament).all()
    
    return templates.TemplateResponse(
        request,
        "teams/list.html",
        {
            "teams": teams,
            "tournaments": tournaments,
            "selected_tournament_id": tournament_id,
        },
    )

@router.get("/teams/{team_id}", response_class=HTMLResponse)
async def view_team(
    request: Request,
    team_id: int,
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """View team details and statistics."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Get team statistics
    query = db.query(TeamStats).filter(TeamStats.team_id == team_id)
    if tournament_id:
        query = query.filter(TeamStats.tournament_id == tournament_id)
    team_stats = query.all()
    
    # Get recent matches
    matches = db.query(Match).options(
        joinedload(Match.tournament),
        joinedload(Match.home_team),
        joinedload(Match.away_team)
    ).filter(
        (Match.home_team_id == team_id) | (Match.away_team_id == team_id)
    ).order_by(Match.date.desc()).limit(5).all()
    
    # Get players
    players = db.query(Player).filter(Player.team_id == team_id).all()
    
    return templates.TemplateResponse(
        request,
        "teams/view.html",
        {
            "team": team,
            "players": players,
            "matches": matches,
            "stats": team_stats,
        },
    )

@router.get("/stats", response_class=HTMLResponse)
async def stats_overview(
    request: Request,
    tournament_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Overview of tournament statistics."""
    # Get tournaments for filtering
    tournaments = db.query(Tournament).all()
    
    # Get top scorers
    top_scorers_query = db.query(PlayerStats).options(
        joinedload(PlayerStats.player),
        joinedload(PlayerStats.tournament),
        joinedload(PlayerStats.player).joinedload(Player.team)
    ).order_by(PlayerStats.goals_scored.desc())
    
    if tournament_id:
        top_scorers_query = top_scorers_query.filter(PlayerStats.tournament_id == tournament_id)
    
    top_scorers = top_scorers_query.limit(10).all()
    
    # Get team rankings
    team_rankings_query = db.query(TeamStats).options(
        joinedload(TeamStats.team),
        joinedload(TeamStats.tournament)
    ).order_by(
        TeamStats.points.desc(),
        TeamStats.goal_difference.desc()
    )
    
    if tournament_id:
        team_rankings_query = team_rankings_query.filter(TeamStats.tournament_id == tournament_id)
    
    team_stats = team_rankings_query.limit(10).all()
    
    # Calculate summary statistics
    total_matches_query = db.query(Match).filter(Match.status == "completed")
    total_goals_query = db.query(Goal)
    
    if tournament_id:
        total_matches_query = total_matches_query.filter(Match.tournament_id == tournament_id)
        total_goals_query = total_goals_query.join(Match).filter(Match.tournament_id == tournament_id)
    
    total_matches = total_matches_query.count()
    total_goals = total_goals_query.count()
    goals_per_match = total_goals / total_matches if total_matches > 0 else 0
    
    # Count clean sheets
    total_clean_sheets = 0
    if tournament_id:
        clean_sheets = db.query(TeamStats).filter(
            TeamStats.tournament_id == tournament_id,
            TeamStats.clean_sheets > 0
        ).all()
        total_clean_sheets = sum(ts.clean_sheets for ts in clean_sheets)
    else:
        clean_sheets = db.query(TeamStats).filter(TeamStats.clean_sheets > 0).all()
        total_clean_sheets = sum(ts.clean_sheets for ts in clean_sheets)
    
    return templates.TemplateResponse(
        request,
        "stats/overview.html",
        {
            "tournaments": tournaments,
            "selected_tournament_id": tournament_id,
            "top_scorers": top_scorers,
            "team_stats": team_stats,
            "total_matches": total_matches,
            "total_goals": total_goals,
            "goals_per_match": goals_per_match,
            "total_clean_sheets": total_clean_sheets
        },
    )

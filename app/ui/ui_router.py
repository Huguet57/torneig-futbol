from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from datetime import date, time
from pathlib import Path
from typing import Optional

from app.db.database import get_db
from app.models import Tournament, Team, Phase, Group, Match
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
        "index.html", {"request": request, "stats": stats}
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
        "matches/list.html",
        {
            "request": request,
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
        "matches/create.html",
        {
            "request": request,
            "tournaments": tournaments,
            "phases": phases,
            "groups": groups,
            "teams": teams,
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
    
    # Get previous and next matches in the same tournament
    prev_match = (
        db.query(Match)
        .filter(
            Match.tournament_id == match.tournament_id,
            Match.date < match.date
        )
        .order_by(Match.date.desc(), Match.time.desc())
        .first()
    )
    
    next_match = (
        db.query(Match)
        .filter(
            Match.tournament_id == match.tournament_id,
            Match.date > match.date
        )
        .order_by(Match.date.asc(), Match.time.asc())
        .first()
    )
    
    # Get group standings if match is part of a group
    standings = []
    if match.group_id:
        standings = calculate_group_standings(db, match.group_id)
    
    return templates.TemplateResponse(
        "matches/view.html",
        {
            "request": request,
            "match": match,
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
        "matches/result.html",
        {"request": request, "match": match},
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
        "tournaments/list.html", {"request": request, "tournaments": tournaments}
    )


@router.get("/tournaments/create", response_class=HTMLResponse)
async def create_tournament_form(request: Request):
    return templates.TemplateResponse("tournaments/create.html", {"request": request})


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
        "tournaments/view.html",
        {"request": request, "tournament": tournament, "phases": phases},
    )


# Add similar routes for teams, phases, and groups
# For brevity, we'll implement just the tournament and match routes for now

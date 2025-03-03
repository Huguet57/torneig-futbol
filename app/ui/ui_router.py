from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import date
from pathlib import Path
from typing import List, Optional

from app.db.database import get_db
from app.models import Tournament, Team, Phase, Group
from app.schemas.tournament import TournamentCreate, TournamentUpdate

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
        "groups": db.query(Group).count()
    }
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "stats": stats}
    )


# Tournament routes
@router.get("/tournaments", response_class=HTMLResponse)
async def list_tournaments(request: Request, db: Session = Depends(get_db)):
    tournaments = db.query(Tournament).all()
    
    return templates.TemplateResponse(
        "tournaments/list.html",
        {"request": request, "tournaments": tournaments}
    )


@router.get("/tournaments/create", response_class=HTMLResponse)
async def create_tournament_form(request: Request):
    return templates.TemplateResponse(
        "tournaments/create.html",
        {"request": request}
    )


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
    db: Session = Depends(get_db)
):
    tournament_data = {
        "name": name,
        "edition": edition,
        "year": year,
        "start_date": start_date,
        "end_date": end_date,
        "description": description,
        "logo_url": logo_url
    }
    
    tournament = Tournament(**tournament_data)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    
    return RedirectResponse(url="/tournaments", status_code=303)


@router.get("/tournaments/{tournament_id}", response_class=HTMLResponse)
async def view_tournament(request: Request, tournament_id: int, db: Session = Depends(get_db)):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    phases = db.query(Phase).filter(Phase.tournament_id == tournament_id).all()
    
    return templates.TemplateResponse(
        "tournaments/view.html",
        {"request": request, "tournament": tournament, "phases": phases}
    )


# Add similar routes for teams, phases, and groups
# For brevity, we'll implement just the tournament routes for now
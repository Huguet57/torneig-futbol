#!/usr/bin/env python
"""
Script to update player statistics based on goals scored in tournaments.
This script can be run periodically to ensure player statistics are up-to-date.
"""

import sys
import os
import argparse
from typing import Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models import Tournament, Player, Goal, Match
from app.models.player_stats import PlayerStats


def update_player_stats(
    db: Session, tournament_id: Optional[int] = None, player_id: Optional[int] = None
) -> None:
    """
    Update player statistics based on goals scored.
    
    Args:
        db: Database session
        tournament_id: Optional tournament ID to filter by
        player_id: Optional player ID to filter by
    """
    # Get tournaments to process
    if tournament_id:
        tournaments = db.query(Tournament).filter(Tournament.id == tournament_id).all()
        if not tournaments:
            print(f"Tournament with ID {tournament_id} not found.")
            return
    else:
        tournaments = db.query(Tournament).all()
        print(f"Processing {len(tournaments)} tournaments...")
    
    # Process each tournament
    for tournament in tournaments:
        print(f"Processing tournament: {tournament.name} ({tournament.edition})")
        
        # Get all matches in the tournament
        matches = db.query(Match).filter(Match.tournament_id == tournament.id).all()
        match_ids = [match.id for match in matches]
        
        if not match_ids:
            print(f"  No matches found for tournament {tournament.name}")
            continue
        
        # Get all goals in these matches
        goals = db.query(Goal).filter(Goal.match_id.in_(match_ids)).all()
        
        if not goals:
            print(f"  No goals found for tournament {tournament.name}")
            continue
        
        # Get unique player IDs from goals
        player_ids = set(goal.player_id for goal in goals)
        
        if player_id:
            # Filter to specific player if requested
            if player_id in player_ids:
                player_ids = {player_id}
            else:
                print(f"  Player with ID {player_id} has no goals in tournament {tournament.name}")
                continue
        
        print(f"  Updating statistics for {len(player_ids)} players...")
        
        # Process each player
        for pid in player_ids:
            player = db.query(Player).filter(Player.id == pid).first()
            if not player:
                print(f"  Warning: Player with ID {pid} not found, skipping...")
                continue
            
            # Get or create player stats for this tournament
            stats = db.query(PlayerStats).filter(
                PlayerStats.player_id == pid,
                PlayerStats.tournament_id == tournament.id
            ).first()
            
            if not stats:
                stats = PlayerStats(
                    player_id=pid,
                    tournament_id=tournament.id,
                    matches_played=0,
                    minutes_played=0,
                    goals=0,
                    assists=0,
                    penalty_goals=0,
                    own_goals=0,
                    yellow_cards=0,
                    red_cards=0,
                    goals_per_match=0.0,
                    minutes_per_goal=0.0
                )
                db.add(stats)
            
            # Get player's goals in this tournament
            player_goals = [g for g in goals if g.player_id == pid]
            
            # Count goals by type
            regular_goals = sum(1 for g in player_goals if g.type == "regular")
            penalty_goals = sum(1 for g in player_goals if g.type == "penalty")
            own_goals = sum(1 for g in player_goals if g.type == "own_goal")
            
            # Count matches played (matches where the player scored)
            matches_with_goals = set(g.match_id for g in player_goals)
            
            # Update stats
            stats.goals = regular_goals + penalty_goals
            stats.penalty_goals = penalty_goals
            stats.own_goals = own_goals
            stats.matches_played = len(matches_with_goals)
            
            # Estimate minutes played (90 minutes per match)
            stats.minutes_played = stats.matches_played * 90
            
            # Update calculated stats
            if stats.matches_played > 0:
                stats.goals_per_match = stats.goals / stats.matches_played
            else:
                stats.goals_per_match = 0.0
                
            if stats.goals > 0:
                stats.minutes_per_goal = stats.minutes_played / stats.goals
            else:
                stats.minutes_per_goal = 0.0
            
            db.commit()
            print(f"  Updated stats for {player.name}: {stats.goals} goals in {stats.matches_played} matches")
    
    print("Player statistics update completed.")


def main():
    """Main function to parse arguments and run the update."""
    parser = argparse.ArgumentParser(description="Update player statistics based on goals.")
    parser.add_argument(
        "--tournament", "-t", type=int, help="Tournament ID to update stats for"
    )
    parser.add_argument(
        "--player", "-p", type=int, help="Player ID to update stats for"
    )
    
    args = parser.parse_args()
    
    # Create database session
    db = SessionLocal()
    try:
        update_player_stats(db, tournament_id=args.tournament, player_id=args.player)
    finally:
        db.close()


if __name__ == "__main__":
    main() 
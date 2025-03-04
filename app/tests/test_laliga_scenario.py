import pytest
from datetime import date, timedelta

from app.tests.fixtures import (
    create_test_team,
    create_test_player
)


@pytest.mark.laliga_scenario
class TestLaLigaScenario:
    """Test the complete tournament workflow using LaLiga teams and players."""

    def test_laliga_tournament_workflow(self, client, db, refresh):
        """
        Test a complete tournament workflow using LaLiga data.
        
        This test creates a mini-tournament with 4 LaLiga teams:
        - Real Madrid
        - Barcelona
        - Atletico Madrid
        - Sevilla
        
        Each team has 3 key players, and we'll simulate matches between them
        with realistic scorelines and goal scorers.
        """
        # Step 1: Create tournament
        tournament_data = {
            "name": "LaLiga Test Tournament",
            "edition": "2024",
            "year": 2024,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=30)),
            "description": "A test tournament featuring LaLiga teams"
        }
        response = client.post("/api/tournaments/", json=tournament_data)
        assert response.status_code == 200
        tournament = response.json()

        # Create group phase
        phase_data = {
            "name": "Group Phase",
            "order": 1,
            "type": "group",
            "tournament_id": tournament["id"]
        }
        response = client.post("/api/phases/", json=phase_data)
        assert response.status_code == 200
        phase = response.json()

        # Create single group
        group_data = {
            "name": "Group A",
            "phase_id": phase["id"]
        }
        response = client.post("/api/groups/", json=group_data)
        assert response.status_code == 200
        group = response.json()

        # Step 2: Create teams with their star players
        teams_data = {
            "Real Madrid": [
                {"name": "Vinicius Jr.", "number": 7, "position": "Forward"},
                {"name": "Jude Bellingham", "number": 5, "position": "Midfielder"},
                {"name": "Toni Kroos", "number": 8, "position": "Midfielder"}
            ],
            "Barcelona": [
                {"name": "Robert Lewandowski", "number": 9, "position": "Forward"},
                {"name": "Pedri", "number": 8, "position": "Midfielder"},
                {"name": "Frenkie de Jong", "number": 21, "position": "Midfielder"}
            ],
            "Atletico Madrid": [
                {"name": "Antoine Griezmann", "number": 7, "position": "Forward"},
                {"name": "Marcos Llorente", "number": 14, "position": "Midfielder"},
                {"name": "Koke", "number": 6, "position": "Midfielder"}
            ],
            "Sevilla": [
                {"name": "Youssef En-Nesyri", "number": 15, "position": "Forward"},
                {"name": "Lucas Ocampos", "number": 5, "position": "Midfielder"},
                {"name": "Ivan Rakitic", "number": 10, "position": "Midfielder"}
            ]
        }

        teams = {}
        players = {}

        for team_name, team_players in teams_data.items():
            # Create team
            team = create_test_team(db)
            team.name = team_name
            team.short_name = team_name[:3].upper()
            db.commit()
            refresh(db, team)
            teams[team_name] = team

            # Add team to group
            response = client.post(
                f"/api/groups/{group['id']}/teams",
                json={"team_id": team.id}
            )
            assert response.status_code == 200

            # Create players for team
            team_players_dict = {}
            for player_data in team_players:
                player = create_test_player(db, team.id)
                player.name = player_data["name"]
                player.number = player_data["number"]
                player.position = player_data["position"]
                db.commit()
                refresh(db, player)
                team_players_dict[player_data["name"]] = player
            players[team_name] = team_players_dict

        # Step 3: Create matches between all teams
        match_results = [
            # Real Madrid vs Barcelona (El Clásico)
            {
                "home": "Real Madrid",
                "away": "Barcelona",
                "score": (3, 2),
                "goals": [
                    ("Vinicius Jr.", 15, "regular"),
                    ("Robert Lewandowski", 25, "regular"),
                    ("Jude Bellingham", 40, "regular"),
                    ("Pedri", 60, "regular"),
                    ("Vinicius Jr.", 85, "regular")
                ]
            },
            # Atletico Madrid vs Sevilla
            {
                "home": "Atletico Madrid",
                "away": "Sevilla",
                "score": (2, 1),
                "goals": [
                    ("Antoine Griezmann", 20, "regular"),
                    ("Youssef En-Nesyri", 55, "regular"),
                    ("Antoine Griezmann", 75, "penalty")
                ]
            },
            # Barcelona vs Atletico Madrid
            {
                "home": "Barcelona",
                "away": "Atletico Madrid",
                "score": (2, 2),
                "goals": [
                    ("Robert Lewandowski", 10, "regular"),
                    ("Antoine Griezmann", 30, "regular"),
                    ("Pedri", 65, "regular"),
                    ("Marcos Llorente", 88, "regular")
                ]
            },
            # Sevilla vs Real Madrid
            {
                "home": "Sevilla",
                "away": "Real Madrid",
                "score": (1, 3),
                "goals": [
                    ("Youssef En-Nesyri", 15, "regular"),
                    ("Vinicius Jr.", 35, "regular"),
                    ("Jude Bellingham", 55, "regular"),
                    ("Toni Kroos", 70, "regular")
                ]
            },
            # Real Madrid vs Atletico Madrid (Madrid Derby)
            {
                "home": "Real Madrid",
                "away": "Atletico Madrid",
                "score": (2, 1),
                "goals": [
                    ("Jude Bellingham", 25, "regular"),
                    ("Antoine Griezmann", 40, "penalty"),
                    ("Vinicius Jr.", 78, "regular")
                ]
            },
            # Barcelona vs Sevilla
            {
                "home": "Barcelona",
                "away": "Sevilla",
                "score": (3, 0),
                "goals": [
                    ("Robert Lewandowski", 22, "regular"),
                    ("Pedri", 44, "regular"),
                    ("Robert Lewandowski", 67, "penalty")
                ]
            }
        ]

        match_date = date.today()
        for match_data in match_results:
            # Create match
            match_request = {
                "tournament_id": tournament["id"],
                "phase_id": phase["id"],
                "group_id": group["id"],
                "home_team_id": teams[match_data["home"]].id,
                "away_team_id": teams[match_data["away"]].id,
                "date": str(match_date),
                "location": "LaLiga Test Stadium"
            }
            response = client.post("/api/matches/", json=match_request)
            assert response.status_code == 200
            match = response.json()

            # Record goals
            for scorer_name, minute, goal_type in match_data["goals"]:
                team_name = match_data["home"] if scorer_name in players[match_data["home"]] else match_data["away"]
                goal_request = {
                    "match_id": match["id"],
                    "player_id": players[team_name][scorer_name].id,
                    "team_id": teams[team_name].id,
                    "minute": minute,
                    "type": goal_type
                }
                response = client.post("/api/goals/", json=goal_request)
                assert response.status_code == 200

            # Update match result
            result_request = {
                "home_score": match_data["score"][0],
                "away_score": match_data["score"][1],
                "status": "completed"
            }
            response = client.put(f"/api/matches/{match['id']}/result", json=result_request)
            assert response.status_code == 200

            match_date += timedelta(days=7)

        # Step 4: Verify final standings
        response = client.get(f"/api/standings/group/{group['id']}")
        assert response.status_code == 200
        standings = response.json()

        # Expected standings:
        # 1. Real Madrid: 3 wins, 0 draws = 9 points
        # 2. Barcelona: 1 win, 1 draw, 1 loss = 4 points
        # 3. Atletico Madrid: 1 win, 1 draw, 1 loss = 4 points
        # 4. Sevilla: 0 wins, 0 draws, 3 losses = 0 points

        # Verify Real Madrid is first
        real_madrid = next(s for s in standings if s["team_name"] == "Real Madrid")
        assert real_madrid["matches_played"] == 3
        assert real_madrid["wins"] == 3
        assert real_madrid["draws"] == 0
        assert real_madrid["losses"] == 0
        assert real_madrid["points"] == 9

        # Verify Barcelona's position
        barcelona = next(s for s in standings if s["team_name"] == "Barcelona")
        assert barcelona["matches_played"] == 3
        assert barcelona["wins"] == 1
        assert barcelona["draws"] == 1
        assert barcelona["losses"] == 1
        assert barcelona["points"] == 4

        # Verify Atletico Madrid's position
        atletico = next(s for s in standings if s["team_name"] == "Atletico Madrid")
        assert atletico["matches_played"] == 3
        assert atletico["wins"] == 1
        assert atletico["draws"] == 1
        assert atletico["losses"] == 1
        assert atletico["points"] == 4

        # Verify Sevilla is last
        sevilla = next(s for s in standings if s["team_name"] == "Sevilla")
        assert sevilla["matches_played"] == 3
        assert sevilla["wins"] == 0
        assert sevilla["draws"] == 0
        assert sevilla["losses"] == 3
        assert sevilla["points"] == 0

        # Step 5: Verify top scorers
        response = client.get(f"/api/tournaments/{tournament['id']}/top-scorers?limit=5")
        assert response.status_code == 200
        top_scorers = response.json()

        # Expected top scorers:
        # 1. Vinicius Jr. (4 goals)
        # 2. Robert Lewandowski (4 goals)
        # 3. Antoine Griezmann (4 goals)
        # 4. Jude Bellingham (3 goals)
        # 5. Pedri (3 goals)

        assert len(top_scorers) == 5
        
        # Verify top scorers have correct goal counts
        vini = next(s for s in top_scorers if s.get("player", {}).get("name") == "Vinicius Jr.")
        assert vini.get("goals_scored") == 4

        lewa = next(s for s in top_scorers if s.get("player", {}).get("name") == "Robert Lewandowski")
        assert lewa.get("goals_scored") == 4

        griezmann = next(s for s in top_scorers if s.get("player", {}).get("name") == "Antoine Griezmann")
        assert griezmann.get("goals_scored") == 4

        bellingham = next(s for s in top_scorers if s.get("player", {}).get("name") == "Jude Bellingham")
        assert bellingham.get("goals_scored") == 3

        pedri = next(s for s in top_scorers if s.get("player", {}).get("name") == "Pedri")
        assert pedri.get("goals_scored") == 3 
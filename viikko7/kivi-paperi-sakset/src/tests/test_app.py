import pytest
from app import app
from flask import session


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret_key"
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_with_session(client):
    """Create a test client with session support"""
    with client.session_transaction() as sess:
        yield client, sess


# NOTE: Game now requires 3 wins to complete instead of manual termination


class TestIndexRoute:
    """Tests for the index route"""

    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Kivi-Paperi-Sakset" in response.text

    def test_index_clears_session(self, client):
        """Test that visiting index clears the session"""
        with client.session_transaction() as sess:
            sess["game_mode"] = "a"
            sess["tuomari"] = {"ekan_pisteet": 1, "tokan_pisteet": 1, "tasapelit": 0}

        response = client.get("/")
        assert response.status_code == 200

        with client.session_transaction() as sess:
            assert "game_mode" not in sess
            assert "tuomari" not in sess


class TestStartGameRoute:
    """Tests for the start_game route"""

    def test_start_game_player_vs_player(self, client):
        """Test starting a player vs player game"""
        response = client.post(
            "/start", data={"game_mode": "a"}, follow_redirects=False
        )
        assert response.status_code == 302
        assert "/play" in response.location

        with client.session_transaction() as sess:
            assert sess["game_mode"] == "a"
            assert sess["tuomari"]["ekan_pisteet"] == 0
            assert sess["tuomari"]["tokan_pisteet"] == 0
            assert sess["tuomari"]["tasapelit"] == 0
            assert sess["siirrot"] == []

    def test_start_game_vs_ai(self, client):
        """Test starting a game vs simple AI"""
        response = client.post(
            "/start", data={"game_mode": "b"}, follow_redirects=False
        )
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["game_mode"] == "b"
            assert "tekoaly_muisti" in sess

    def test_start_game_vs_advanced_ai(self, client):
        """Test starting a game vs advanced AI"""
        response = client.post(
            "/start", data={"game_mode": "c"}, follow_redirects=False
        )
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["game_mode"] == "c"
            assert "tekoaly_muisti" in sess


class TestPlayRoute:
    """Tests for the play route"""

    def test_play_redirects_without_game_mode(self, client):
        """Test that play redirects to index if no game_mode in session"""
        response = client.get("/play")
        assert response.status_code == 302
        assert "/" in response.location

    def test_play_displays_game_page(self, client):
        """Test that play page displays when game is started"""
        # Start a game first
        client.post("/start", data={"game_mode": "a"})

        response = client.get("/play")
        assert response.status_code == 200
        assert "Pelaaja vs Pelaaja" in response.text

    def test_play_player_vs_player_single_round(self, client):
        """Test playing a single round in player vs player mode"""
        # Start game
        client.post("/start", data={"game_mode": "a"})

        # Play a round: rock vs scissors, player 1 wins
        response = client.post(
            "/play", data={"move": "k", "opponent_move": "s"}, follow_redirects=False
        )
        assert response.status_code == 200

        with client.session_transaction() as sess:
            assert sess["tuomari"]["ekan_pisteet"] == 1
            assert sess["tuomari"]["tokan_pisteet"] == 0
            assert len(sess["siirrot"]) == 1
            assert sess["siirrot"][0]["player"] == "k"
            assert sess["siirrot"][0]["opponent"] == "s"

    def test_play_until_player1_wins(self, client):
        """Test playing until player 1 gets 3 wins"""
        client.post("/start", data={"game_mode": "a"})

        # Play 3 rounds where player 1 wins (rock vs scissors)
        for i in range(3):
            response = client.post(
                "/play",
                data={"move": "k", "opponent_move": "s"},
                follow_redirects=False,
            )

            # All responses render the play page (with win notification if won)
            assert response.status_code == 200

        with client.session_transaction() as sess:
            assert sess["tuomari"]["ekan_pisteet"] == 3
            assert len(sess["siirrot"]) == 3

    def test_play_until_player2_wins(self, client):
        """Test playing until player 2 gets 3 wins"""
        client.post("/start", data={"game_mode": "a"})

        # Play 3 rounds where player 2 wins (scissors vs paper)
        for i in range(3):
            response = client.post(
                "/play",
                data={"move": "p", "opponent_move": "s"},
                follow_redirects=False,
            )

            # All responses render the play page (with win notification if won)
            assert response.status_code == 200

        with client.session_transaction() as sess:
            assert sess["tuomari"]["tokan_pisteet"] == 3
            assert len(sess["siirrot"]) == 3

    def test_play_mixed_rounds_until_3_wins(self, client):
        """Test game with mixed results until someone gets 3 wins"""
        client.post("/start", data={"game_mode": "a"})

        # Sequence: p1 wins, p2 wins, p1 wins, tie, p1 wins, p2 wins, p1 wins, p1 wins
        moves = [
            ("k", "s"),  # P1 wins (1-0)
            ("p", "s"),  # P2 wins (1-1)
            ("k", "s"),  # P1 wins (2-1)
            ("k", "k"),  # Tie (2-1, t:1)
            ("k", "s"),  # P1 wins (3-1) - WINNER
        ]

        for idx, (p1_move, p2_move) in enumerate(moves):
            response = client.post(
                "/play",
                data={"move": p1_move, "opponent_move": p2_move},
                follow_redirects=False,
            )

            # All responses render the play page (with win notification if won)
            assert response.status_code == 200

        with client.session_transaction() as sess:
            assert sess["tuomari"]["ekan_pisteet"] == 3
            assert sess["tuomari"]["tokan_pisteet"] == 1
            assert sess["tuomari"]["tasapelit"] == 1
            assert len(sess["siirrot"]) == 5

    def test_play_invalid_move_redirects_to_results(self, client):
        """Test that invalid move redirects to results"""
        client.post("/start", data={"game_mode": "a"})

        response = client.post(
            "/play", data={"move": "x", "opponent_move": "k"}, follow_redirects=False
        )
        assert response.status_code == 302
        assert "/results" in response.location

    def test_play_vs_simple_ai_until_win(self, client):
        """Test playing against simple AI until someone wins"""
        client.post("/start", data={"game_mode": "b"})

        # Play many rounds until someone reaches 3 wins
        # Since AI is random, we need to play until we get a winner
        rounds = 0
        while rounds < 50:  # Safety limit
            response = client.post("/play", data={"move": "k"}, follow_redirects=False)
            rounds += 1

            with client.session_transaction() as sess:
                if (
                    sess["tuomari"]["ekan_pisteet"] == 3
                    or sess["tuomari"]["tokan_pisteet"] == 3
                ):
                    # Game should have ended and displayed win notification
                    assert response.status_code == 200
                    break
                else:
                    # Game continues
                    assert response.status_code == 200

    def test_play_vs_advanced_ai(self, client):
        """Test playing against advanced AI"""
        client.post("/start", data={"game_mode": "c"})

        # Play multiple rounds
        for move in ["k", "p", "s", "k"]:
            client.post("/play", data={"move": move})

        with client.session_transaction() as sess:
            assert len(sess["siirrot"]) == 4
            assert len(sess["tekoaly_muisti"]) == 4

    def test_all_move_combinations(self, client):
        """Test all possible move combinations and their outcomes"""
        test_cases = [
            # (player_move, opponent_move, expected_winner)
            # 'eka' = player 1 wins, 'toka' = player 2 wins, 'tasapeli' = tie
            ("k", "s", "eka"),  # Rock beats scissors
            ("k", "p", "toka"),  # Paper beats rock
            ("k", "k", "tasapeli"),  # Rock ties rock
            ("p", "k", "eka"),  # Paper beats rock
            ("p", "s", "toka"),  # Scissors beats paper
            ("p", "p", "tasapeli"),  # Paper ties paper
            ("s", "p", "eka"),  # Scissors beats paper
            ("s", "k", "toka"),  # Rock beats scissors
            ("s", "s", "tasapeli"),  # Scissors ties scissors
        ]

        for player_move, opponent_move, expected_winner in test_cases:
            # Start fresh game
            client.post("/start", data={"game_mode": "a"})

            # Play the round
            client.post(
                "/play", data={"move": player_move, "opponent_move": opponent_move}
            )

            with client.session_transaction() as sess:
                if expected_winner == "eka":
                    assert sess["tuomari"]["ekan_pisteet"] == 1
                    assert sess["tuomari"]["tokan_pisteet"] == 0
                    assert sess["tuomari"]["tasapelit"] == 0
                elif expected_winner == "toka":
                    assert sess["tuomari"]["ekan_pisteet"] == 0
                    assert sess["tuomari"]["tokan_pisteet"] == 1
                    assert sess["tuomari"]["tasapelit"] == 0
                else:  # tasapeli
                    assert sess["tuomari"]["ekan_pisteet"] == 0
                    assert sess["tuomari"]["tokan_pisteet"] == 0
                    assert sess["tuomari"]["tasapelit"] == 1


class TestResultsRoute:
    """Tests for the results route"""

    def test_results_redirects_without_session(self, client):
        """Test that results redirects to index if no tuomari in session"""
        response = client.get("/results")
        assert response.status_code == 302
        assert "/" in response.location

    def test_results_displays_final_score_after_3_wins(self, client):
        """Test that results page displays the final score after reaching 3 wins"""
        # Start and play a game until player 1 wins
        client.post("/start", data={"game_mode": "a"})
        for _ in range(3):
            client.post("/play", data={"move": "k", "opponent_move": "s"})

        response = client.get("/results")
        assert response.status_code == 200
        assert "Lopputulos" in response.text

    def test_results_shows_player1_victory(self, client):
        """Test results page when player 1 reaches 3 wins"""
        client.post("/start", data={"game_mode": "a"})
        for _ in range(3):
            client.post("/play", data={"move": "k", "opponent_move": "s"})

        response = client.get("/results")
        assert response.status_code == 200
        assert "Pelaaja 1" in response.text

    def test_results_shows_player2_victory(self, client):
        """Test results page when player 2 reaches 3 wins"""
        client.post("/start", data={"game_mode": "a"})
        for _ in range(3):
            client.post("/play", data={"move": "s", "opponent_move": "k"})

        response = client.get("/results")
        assert response.status_code == 200

    def test_results_includes_statistics(self, client):
        """Test that results page includes game statistics"""
        client.post("/start", data={"game_mode": "a"})

        # Play rounds until player 1 wins (3 rounds)
        for _ in range(3):
            client.post("/play", data={"move": "k", "opponent_move": "s"})

        response = client.get("/results")
        assert response.status_code == 200
        assert "Pelitilastot" in response.text

    def test_results_shows_winner_after_mixed_rounds(self, client):
        """Test results page after game with mixed round outcomes"""
        client.post("/start", data={"game_mode": "a"})

        # Mix of wins and ties until someone reaches 3 wins
        moves = [
            ("k", "s"),  # P1 wins
            ("k", "k"),  # Tie
            ("k", "s"),  # P1 wins
            ("k", "k"),  # Tie
            ("k", "s"),  # P1 wins
        ]

        for p1_move, p2_move in moves:
            client.post("/play", data={"move": p1_move, "opponent_move": p2_move})

        response = client.get("/results")
        assert response.status_code == 200


class TestGameFlow:
    """Integration tests for complete game flows"""

    def test_complete_best_of_nine_game_flow(self, client):
        """Test a complete game until someone gets 3 wins"""
        # 1. Visit index
        response = client.get("/")
        assert response.status_code == 200

        # 2. Start a game
        response = client.post("/start", data={"game_mode": "a"}, follow_redirects=True)
        assert response.status_code == 200

        # 3. Play until someone wins (3 wins)
        for i in range(3):
            response = client.post(
                "/play",
                data={"move": "k", "opponent_move": "s"},
                follow_redirects=False,
            )
            # All responses render the play page (with win notification if won)
            assert response.status_code == 200

        # 4. View results (user can navigate from the notification or wait for auto-redirect)
        response = client.get("/results")
        assert response.status_code == 200

        # Verify final state
        with client.session_transaction() as sess:
            assert sess["tuomari"]["ekan_pisteet"] == 3
            assert len(sess["siirrot"]) == 3

    def test_game_flow_with_ai_until_winner(self, client):
        """Test complete game flow against AI until someone wins"""
        # Start game vs AI
        client.post("/start", data={"game_mode": "b"})

        # Play many rounds until someone reaches 3 wins
        rounds = 0
        while rounds < 50:  # Safety limit
            response = client.post("/play", data={"move": "k"}, follow_redirects=False)
            rounds += 1

            with client.session_transaction() as sess:
                if (
                    sess["tuomari"]["ekan_pisteet"] == 3
                    or sess["tuomari"]["tokan_pisteet"] == 3
                ):
                    # Game should have ended and displayed win notification
                    assert response.status_code == 200
                    break

        # Verify the game ended
        with client.session_transaction() as sess:
            assert (
                sess["tuomari"]["ekan_pisteet"] == 3
                or sess["tuomari"]["tokan_pisteet"] == 3
            )

    def test_restart_game_after_completion(self, client):
        """Test restarting a game after it completes"""
        # Play first game until completion
        client.post("/start", data={"game_mode": "a"})
        for _ in range(5):
            client.post("/play", data={"move": "k", "opponent_move": "s"})

        # Go to index to restart
        response = client.get("/")
        assert response.status_code == 200

        with client.session_transaction() as sess:
            assert "game_mode" not in sess

        # Start new game
        client.post("/start", data={"game_mode": "a"})

        with client.session_transaction() as sess:
            assert sess["game_mode"] == "a"
            assert sess["tuomari"]["ekan_pisteet"] == 0
            assert sess["tuomari"]["tokan_pisteet"] == 0
            assert sess["siirrot"] == []

        # Play a single round in the new game
        client.post("/play", data={"move": "k", "opponent_move": "s"})

        with client.session_transaction() as sess:
            assert sess["tuomari"]["ekan_pisteet"] == 1
            assert len(sess["siirrot"]) == 1

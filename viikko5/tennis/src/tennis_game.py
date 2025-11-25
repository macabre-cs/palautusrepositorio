class TennisGame:
    SCORE_NAMES = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}

    def score_name(self, score):
        return self.SCORE_NAMES.get(score, "")

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.score1 = 0
        self.score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.score1 += 1
        elif player_name == self.player2_name:
            self.score2 += 1

    def _equal_score(self):
        if self.score1 < 3:
            return f"{self.score_name(self.score1)}-All"
        return "Deuce"

    def _advantage_or_win(self):
        diff = self.score1 - self.score2
        if diff == 1:
            return "Advantage player1"
        if diff == -1:
            return "Advantage player2"
        if diff >= 2:
            return "Win for player1"
        return "Win for player2"

    def get_score(self):
        if self.score1 == self.score2:
            return self._equal_score()
        if self.score1 >= 4 or self.score2 >= 4:
            return self._advantage_or_win()
        return f"{self.score_name(self.score1)}-{self.score_name(self.score2)}"

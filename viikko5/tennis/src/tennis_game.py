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
        if player_name == "player1":
            self.score1 = self.score1 + 1
        else:
            self.score2 = self.score2 + 1

    def get_score(self):
        score = ""
        current_score = 0

        if self.score1 == self.score2:
            if self.score1 == 0:
                score = "Love-All"
            elif self.score1 == 1:
                score = "Fifteen-All"
            elif self.score1 == 2:
                score = "Thirty-All"
            else:
                score = "Deuce"
        elif self.score1 >= 4 or self.score2 >= 4:
            minus_result = self.score1 - self.score2

            if minus_result == 1:
                score = "Advantage player1"
            elif minus_result == -1:
                score = "Advantage player2"
            elif minus_result >= 2:
                score = "Win for player1"
            else:
                score = "Win for player2"
        else:
            for i in range(1, 3):
                if i == 1:
                    current_score = self.score1
                else:
                    score = score + "-"
                    current_score = self.score2

                score = score + self.score_name(current_score)

        return score

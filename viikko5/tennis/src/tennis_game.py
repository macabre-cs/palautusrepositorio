class TennisGame:
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

                if current_score == 0:
                    score = score + "Love"
                elif current_score == 1:
                    score = score + "Fifteen"
                elif current_score == 2:
                    score = score + "Thirty"
                elif current_score == 3:
                    score = score + "Forty"

        return score

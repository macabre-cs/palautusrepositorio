class Player:
    def __init__(self, data):
        self.name = data['name']
        self.nationality = data['nationality']
        self.team = data['team']
        self.goals = data['goals']
        self.assists = data['assists']

    def points(self):
        return self.goals + self.assists

    def __repr__(self):
        return f"{self.name} {self.team} {self.goals + self.assists} pts"

class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        filtered_players = [p for p in self.players if p.nationality == nationality]
        filtered_players.sort(key=lambda p: p.points(), reverse=True)
        return filtered_players

    def all_players(self):
        return self.players

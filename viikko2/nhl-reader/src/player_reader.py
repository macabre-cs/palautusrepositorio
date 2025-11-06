# pylint: disable=too-few-public-methods

import requests
from player import Player

class PlayerReader:
    def __init__(self, season):
        self.season = season
        self.url = f"https://studies.cs.helsinki.fi/nhlstats/{self.season}/players"

    def get_players(self):
        response = requests.get(self.url, timeout=10)
        players = [Player(player_data) for player_data in response.json()]
        return players

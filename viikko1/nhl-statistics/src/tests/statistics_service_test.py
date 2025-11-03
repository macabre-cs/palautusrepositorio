import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    
    def test_etsi_pelaaja(self):
        player = self.stats.search("Kurri")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Kurri")
    
    def test_etsi_tiimi(self):
        team_players = self.stats.team("EDM")
        self.assertEqual(len(team_players), 3)
        self.assertEqual(team_players[0].name, "Semenko")
        self.assertEqual(team_players[1].name, "Kurri")
        self.assertEqual(team_players[2].name, "Gretzky")
    
    def test_laske_pisteet(self):
        player = self.stats.search("Gretzky")
        self.assertEqual(player.points, 124)
    
    def test_top_pelaajat(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 3)
        self.assertEqual(top_players[0].name, "Gretzky")
        self.assertEqual(top_players[1].name, "Lemieux")
        self.assertEqual(top_players[2].name, "Yzerman")

    def test_etsi_olematon_pelaaja(self):
        player = self.stats.search("Luukkainen")
        self.assertIsNone(player)

    def test_str(self):
        player = self.stats.search("Semenko")
        self.assertEqual(str(player), "Semenko EDM 4 + 12 = 16")
    
    def test_top_goals(self):
        top_players = self.stats.top(2, sort_by=SortBy.GOALS)
        self.assertEqual(len(top_players), 2)
        self.assertEqual(top_players[0].name, "Lemieux")  # 45
        self.assertEqual(top_players[1].name, "Yzerman")  # 42
    
    def test_top_assists(self):
        top_players = self.stats.top(2, sort_by=SortBy.ASSISTS)
        self.assertEqual(len(top_players), 2)
        self.assertEqual(top_players[0].name, "Gretzky")  # 89
        self.assertEqual(top_players[1].name, "Yzerman")  # 56

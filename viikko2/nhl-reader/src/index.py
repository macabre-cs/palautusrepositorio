from player_reader import PlayerReader
from statistic_service import PlayerStats

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationality = input("Minkä maan pelaajat tulostetaan?")
    players = stats.top_scorers_by_nationality(nationality)

    print(f"\nPlayers from {nationality}:\n")
    for player in players:
        print(player)

if __name__ == "__main__":
    main()

import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    nationality = input("Minkä maan pelaajat tulostetaan?")

    players.sort(key=lambda p: p.points(), reverse=True)

    print(f"\nPlayers from {nationality}:\n")
    for player in players:
        if player.nationality == nationality:
            print(player)

if __name__ == "__main__":
    main()

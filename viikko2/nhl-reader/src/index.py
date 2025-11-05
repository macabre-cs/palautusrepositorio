from player_reader import PlayerReader
from statistic_service import PlayerStats
from rich.table import Table
from rich.console import Console

def main():
    season = input("Minkä kauden tilastoja tarkastellaan? (esim. 2024-25) ")
    nationality = input("Minkä maan pelaajat tulostetaan? (esim. FIN, SWE, CAN) ")

    reader = PlayerReader(season)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    console = Console()
    table = Table(title=f"Season {season} players from {nationality}:")

    table.add_column("Released", justify="left", style="cyan")
    table.add_column("Teams", justify="left", style="magenta")
    table.add_column("Goals", justify="right", style="yellow")
    table.add_column("Assists", justify="right", style="yellow")
    table.add_column("Points", justify="right", style="yellow")

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points())
        )

    console.print(table)

if __name__ == "__main__":
    main()

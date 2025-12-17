from nba_api.stats.static import teams
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

nba_teams = teams.get_teams()

# As a simple list of (id, full_name)
def get_teams():
    team_list = [(t["full_name"],t["id"]) for t in nba_teams]
    return team_list

def get_team_player_points(game_id: str, team_id: int):
    """
    Returns a list of dicts with player name and points
    for a specific team in a specific game.

    :param game_id: NBA game ID (e.g. '0022300001')
    :param team_id: NBA team ID (e.g. 1610612747)
    """
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(
        game_id=game_id
    )

    players_df = boxscore.get_data_frames()[0]

    team_players = players_df[
        players_df["TEAM_ID"] == team_id
    ]

    return [
        {
            "player_id": int(row["PLAYER_ID"]),
            "player_name": row["PLAYER_NAME"],
            "points": int(row["PTS"])
        }
        for _, row in team_players.iterrows()
    ]

def get_current_season_games(team_id: int, season: str):
    """
    Returns a DataFrame of games for the specified team and season.

    :param team_id: NBA team ID (e.g. 1610612747)
    :param season: Season string (e.g. '2023-24')
    """
    df = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id,
        season_nullable=season
    ).get_data_frames()[0]

    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    return df.sort_values("GAME_DATE", ascending=False)

def get_game_player_boxscore(game_id: str):
    box = boxscoretraditionalv2.BoxScoreTraditionalV2(
        game_id=game_id
    )
    return box.get_data_frames()[0]
import streamlit as st
import stats
from datetime import datetime

CACHE_TTL = 600

def current_nba_season():
    year = datetime.now().year
    month = datetime.now().month
    # NBA season rolls over around October
    if month >= 10:
        return f"{year}-{str(year + 1)[-2:]}"
    else:
        return f"{year - 1}-{str(year)[-2:]}"

@st.cache_data(ttl=CACHE_TTL)
def get_current_season_games(team_id: int, season: str):
    return stats.get_current_season_games(team_id, season)

@st.cache_data(ttl=CACHE_TTL)
def get_game_player_boxscore(game_id: str):
    return stats.get_game_player_boxscore(game_id)

st.title("Basketball Wager Analytics Notes")
season = current_nba_season()
#team selector dropdown
teams = stats.get_teams()
#show in dropdown
selected_team = st.selectbox("Select an NBA Team", teams, format_func=lambda team: team[0])

st.write(f"Current NBA Season: {season}")
st.write(f"Team: {selected_team[0]}")

games_df = get_current_season_games(selected_team[1], season)
# st.write(games_df)
display_df = games_df[
    ["MATCHUP", "WL", "PTS", "GAME_ID","GAME_DATE"]
]

selection = st.dataframe(
    display_df,
    width='stretch',
    selection_mode="single-row",
    on_select="rerun"
)

if selection.selection.rows:
    selected_row = selection.selection.rows[0]
    selected_game_id = display_df.iloc[selected_row]["GAME_ID"]

    st.write(f"Selected Game ID: {selected_game_id}")

    players_df = get_game_player_boxscore(selected_game_id)

    team_players_df = players_df[
        players_df["TEAM_ID"] == selected_team[1]
    ]

    display_df = team_players_df[
        ["PLAYER_NAME", "MIN", "PTS","FG_PCT","FGA"]
    ].sort_values("PTS", ascending=False)

    st.subheader("Player Scoring (Selected Team)")
    st.dataframe(
        display_df,
        width='stretch'
    )
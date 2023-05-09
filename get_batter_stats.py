from statcast_format_data import get_statcast_data
from strikezone import batter_strikezone, general_strikezone
from pybaseball import statcast_batter, spraychart, cache, team_batting_bref, playerid_lookup
import pandas as pd


cache.enable()

team_batting = team_batting_bref("NYM", 2023)
team_batting = team_batting[team_batting['Pos'] != "P"]
team_batting = team_batting.sort_values(by='OPS', ascending=False)
team_batting_slash = team_batting[['Name', 'BA', 'OBP', 'SLG', 'OPS', 'HR', 'RBI']]

players = team_batting['Name'].tolist()

pitch_type_data = {}
for player_name in players:
    try:
        player = playerid_lookup(player_name.split()[1], player_name.split()[0])

        df = get_statcast_data("2023-01-01",
                                 "2023-12-30",
                                 player["key_mlbam"][0],
                                 statcast_type='batter')

        # df = df[df['Is_Hit'] == 1]
        # df = df[df['home_team'] == 'LAD']

        data = df[df['events'] == 'strikeout']
        data = df[df['Is_Hit'] == 1]
        general_strikezone(data, player_name.split()[0], player_name.split()[1], 'batter')

        pitch_counts = df['pitch_name'].value_counts(normalize=True)
        pitch_type_data.update({player_name: pitch_counts})
        events = df['events'].value_counts(normalize=True)
        pitch_type_data.update({player_name: events})

    except:
        print(f"Failed to get data for {player_name}")

pitch_type_graph = pd.DataFrame(pitch_type_data)
# pitch_type_graph = pitch_type_graph.transpose()

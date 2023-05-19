from statcast_format_data import get_statcast_data
from strikezone import batter_strikezone, general_strikezone
from pybaseball import statcast_batter, spraychart, cache, team_batting_bref, playerid_lookup
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('module://backend_interagg')


# cache.enable()

team = "NYM"
team_nickname = "reds"
year = 2023
start_date = "2023-05-15"
end_date = "2023-05-15"

team_batting = team_batting_bref(team, year)
team_batting = team_batting[team_batting['Pos'] != "P"]
team_batting[["BA", "OBP", "SLG", "OPS", "OPS+", "HR", "RBI", "R", "SB", "SO", "PA"]] = team_batting[["BA", "OBP", "SLG", "OPS", "OPS+", "HR", "RBI", "R", "SB", "SO", "PA"]].apply(pd.to_numeric, errors='coerce', axis=1)
plate_app_threshold = np.percentile(team_batting["PA"], 10)
team_batting = team_batting[team_batting['PA'] >= plate_app_threshold]
team_batting["SO %"] = team_batting["SO"]/team_batting["PA"]
team_batting = team_batting.sort_values(by='OPS+', ascending=False)
team_batting_slash = team_batting[['Name', 'Pos', 'BA', 'OBP', 'SLG', 'OPS', 'OPS+', 'HR', 'RBI', 'SO %', 'R', 'SB']]

players = team_batting['Name'].tolist()

for player in players:
    try:
        player_mlb = playerid_lookup(player.split()[1], player.split()[0])
        df = get_statcast_data(start_date,
                               end_date,
                               player_mlb["key_mlbam"][0],
                               statcast_type='batter')
        if not df.empty:
            # hit_df = df[df['Is_Hit'] == 1]
            # spraychart(df, team_nickname, title=f'{player} Hit Chart ({start_date} - {end_date})',
            #            width=1000,
            #            height=1000,
            #            size=50)
            general_strikezone(df, player.split()[0], player.split()[1], 'batter')
        else:
            del df
    except:
        print(f"Failed to get data for {player}")
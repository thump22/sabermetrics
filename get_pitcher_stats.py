import sys
import time
import os

from get_player_id import get_player_id
from pybaseball import statcast_pitcher
from pybaseball import cache

import pandas as pd
import dataframe_image as dfi
import matplotlib.pyplot as plt
import seaborn as sns

cache.enable()


def get_statcast_data(start_date, end_date, pitcher_name):
    player = get_player_id(pitcher_name[0], pitcher_name[1])
    df = statcast_pitcher(start_date, end_date, player_id=player)
    return df, pitcher_name


def graph_pitch_over_time(df, directory):
    pitcher = df[0]
    pitcher_name = df[1]
    pitcher['year'] = pitcher['game_date'].str[:4]
    pitcher_stats = pitcher.loc[~pitcher['pitch_type'].isna()]
    pitcher_seasons = pitcher_stats.groupby(['year', 'pitch_name']).agg({
      'player_name': 'size',
      'release_speed': 'mean',
      'release_spin_rate': 'mean'
    })
    pitcher_seasons = pitcher_seasons.reset_index()
    pitch_count = pitcher_seasons.groupby('year').sum().reset_index()
    pitch_count = pitch_count.loc[:, ['year', 'player_name']]
    pitcher_seasons = pitcher_seasons.merge(pitch_count, on='year')
    pitcher_seasons['percent_thrown'] = \
        pitcher_seasons['player_name_x']/pitcher_seasons['player_name_y']

    cols_to_graph = [['release_speed', 'Release Speed'],
                     ['percent_thrown', 'Percent Thrown']]

    for graph in cols_to_graph:
        ax = sns.relplot(data=pitcher_seasons, x='year', y=graph[0], kind='line', hue='pitch_name')
        ax.set_xticklabels(rotation=1)
        ax.set(ylabel=f'{graph[1]}', xlabel='Year', title=f'{graph[1]} - {pitcher_name[0]} {pitcher_name[1]}')
        ax.savefig(f"{dir}/{pitcher_name[1]}_{graph[0]}.png")

    time.sleep(5)
    # dfi.export(pitcher_seasons, f'graphs/pitchers/{pitcher_name[1]}_pitch_data.png')


def pitch_totals(df):
    print(df['pitch_type'].value_counts())


mets_pitchers = [
    ['Adam', 'Ottavino'],
    ['Carlos', 'Carrasco'],
    ['David', 'Peterson'],
    ['Edwin', 'Diaz'],
    ['Joey', 'Lucchesi'],
    ['Max', 'Scherzer'],
    ['Tylor', 'Megill'],
    ['Justin', 'Verlander'],
    ['David', 'Robertson'],
    ['Drew', 'Smith'],
    ['Brooks', 'Raley'],
    ['Tommy', 'Hunter'],
    ['José', 'Quintana']
]

dataframes = []
for pitcher in mets_pitchers:
    print(pitcher[1])
    dir = f"graphs/pitchers/by_team/mets/indiv/{pitcher[1]}"
    if not os.path.exists(dir):
        os.makedirs(dir)
    df = get_statcast_data('2016-01-01', '2023-12-01', pitcher)
    graph_pitch_over_time(df, dir)
    dataframes.append(df[0])

all_data = pd.concat(dataframes)

pitch_types = ["FF", "SL", "CU", "CH", "FC"]
pitcher_pitch_velo_df = all_data.groupby(['player_name', 'pitch_type'], as_index=False)['release_speed'].mean()

for ptype in pitch_types:
    data = pitcher_pitch_velo_df[pitcher_pitch_velo_df['pitch_type'] == ptype].sort_values(by='release_speed',
                                                                                         ascending=False)
    dfi.export(data, f'graphs/pitchers/by_team/mets/pitch_type/{ptype}_release_speed.png')

from statcast_format_data import get_statcast_data
from pybaseball import playerid_lookup, statcast_batter, spraychart, cache

cache.enable()
player = playerid_lookup('Cortes', 'Nestor')

df = get_statcast_data("2023-04-01",
                       "2023-12-30",
                       player["key_mlbam"][0],
                       statcast_type='pitcher')

#sub_data = df[(df['home_team'] == 'NYM' ) | (df['away_team'] == "NYM")]

# spraychart(sub_data, 'marlins', title="Scherzer @ MIA ('16-'22)")
df.to_csv('pitchcast-data.csv')


def pitch_count(sub_data):
    sub_data = sub_data[sub_data['game_date'].dt.year == 2023]
    sub_data = sub_data[sub_data['balls'] == 3]
    pitcher = sub_data[sub_data['strikes'] == 2]
    pitcher['year'] = pitcher['game_date'].dt.year
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
    pitcher_seasons['percent_thrown'] = pitcher_seasons['player_name_x'] / pitcher_seasons['player_name_y']
    print(pitcher_seasons)


pitch_count(df)

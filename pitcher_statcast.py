from statcast_format_data import get_statcast_data
from pybaseball import statcast_batter, spraychart, cache

cache.enable()

df = get_statcast_data('2021-01-01', '2022-12-30', ['Sandy', 'Alcantara'], statcast_type='pitcher')
sub_data = df[(df['home_team'] == 'NYM' ) | (df['away_team'] == "NYM")]

# spraychart(sub_data, 'marlins', title="Scherzer @ MIA ('16-'22)")
sub_data.to_csv('pitchcast-data.csv')


def onbase_percentage(sub_data):
    # (OBP) = (hits + walks + hit by pitch) ÷ (at-bats + walks + hit by pitch + sacrifice flies)

    hits = sub_data['Is_Hit'].sum()
    at_bats = sub_data['AB_flag'].sum()
    hit_by_pitches = (sub_data['events'] == 'hit_by_pitch').sum()
    walks = (sub_data['events'] == 'walk').sum()
    sac_flies = (sub_data['events'] == 'sac_fly').sum()
    sac_bunts = (sub_data['events'] == 'sac_bunt').sum()

    obp = (hits + walks + hit_by_pitches) / (at_bats + walks +hit_by_pitches + sac_flies + sac_bunts)
    return obp


def strikeout_rate(sub_data):
    strikeouts = (sub_data['events'] == 'strikeout').sum()
    at_bats = sub_data['AB_flag'].sum()
    return strikeouts / at_bats


print(onbase_percentage(sub_data))
print(strikeout_rate(sub_data))
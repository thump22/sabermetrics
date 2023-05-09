def batting_average(sub_data):
    hits = sub_data['Is_Hit'].sum()
    at_bats = sub_data['AB_flag'].sum()
    return hits/at_bats


def on_base_percentage(sub_data):
    hits = sub_data['Is_Hit'].sum()
    at_bats = sub_data['AB_flag'].sum()
    hit_by_pitches = (sub_data['events'] == 'hit_by_pitch').sum()
    walks = (sub_data['events'] == 'walk').sum()
    sac_flies = (sub_data['events'] == 'sac_fly').sum()
    sac_bunts = (sub_data['events'] == 'sac_bunt').sum()
    obp = (hits + walks + hit_by_pitches) / (at_bats + walks + hit_by_pitches + sac_flies + sac_bunts)
    return obp


def slugging_percentage(sub_data):
    # SLG = (1B + 2*2B + 3*3B + 4*HR)/AB
    singles = sub_data['events'].value_counts()['single'] if 'single' in sub_data['events'].value_counts() else 0
    doubles = sub_data['events'].value_counts()['double'] if 'double' in sub_data['events'].value_counts() else 0
    triples = sub_data['events'].value_counts()['triple'] if 'triple' in sub_data['events'].value_counts() else 0
    homeruns = sub_data['events'].value_counts()['home_run'] if 'home_run' in sub_data['events'].value_counts() else 0
    at_bats = sub_data['AB_flag'].sum()
    slg = (singles + (2*doubles) + (3*triples) + (4*homeruns)) / at_bats
    return slg


def ops_rate(sub_data):
    obp = on_base_percentage(sub_data)
    slg = slugging_percentage(sub_data)
    return obp + slg


def strikeout_rate(sub_data):
    strikeouts = (sub_data['events'] == 'strikeout').sum()
    plate_apps = sub_data['PA_flag'].sum()
    return strikeouts / plate_apps


def home_run_rate(sub_data):
    strikeouts = (sub_data['events'] == 'home_run').sum()
    plate_apps = sub_data['PA_flag'].sum()
    return strikeouts / plate_apps

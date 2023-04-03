from get_player_id import get_player_id
from pybaseball import statcast_pitcher, statcast_batter, spraychart, cache

import numpy as np
import pandas as pd

cache.enable()


# PA Flag Dictionary - This specifies which events constitute a plate appearance ending :: based on events column
pa_flag_dict = {'field_out': 1, 'nan': 0, 'strikeout': 1, 'double': 1, 'strikeout_double_play': 1,
                'single': 1, 'force_out': 1, 'hit_by_pitch': 1, 'grounded_into_double_play': 1,
                'home_run': 1, 'walk': 1, 'caught_stealing_2b': 0, 'sac_bunt': 1, 'triple': 1,
                'sac_fly': 1, 'field_error': 1, 'double_play': 1, 'catcher_interf': 1, 'fielders_choice_out': 1,
                'fielders_choice': 1, 'pickoff_1b': 0, 'other_out': 0, 'caught_stealing_home': 0, 'pickoff_caught_stealing_2b': 0,
                'caught_stealing_3b': 0, 'sac_fly_double_play': 1, 'pickoff_caught_stealing_home': 0, 'pickoff_2b': 0, 'run': 0,
                'triple_play': 1, 'batter_interference': 1, 'pickoff_3b': 0, 'sac_bunt_double_play': 1, 'pickoff_caught_stealing_3b': 0}

# AB Flag Dictionary - This specifies which events constitute an at-bat ending :: based on events column
ab_flag_dict = {'field_out': 1, 'nan': 0, 'strikeout': 1, 'double': 1,
                'strikeout_double_play': 1, 'single': 1, 'force_out': 1, 'hit_by_pitch': 0,
                'grounded_into_double_play': 1, 'home_run': 1, 'walk': 0, 'caught_stealing_2b': 0,
                'sac_bunt': 0, 'triple': 1, 'sac_fly': 0, 'field_error': 1,
                'double_play': 1, 'catcher_interf': 0, 'fielders_choice_out': 1, 'fielders_choice': 1,
                'pickoff_1b': 0, 'other_out': 0, 'caught_stealing_home': 0, 'pickoff_caught_stealing_2b': 0,
                'caught_stealing_3b': 0, 'sac_fly_double_play': 1, 'pickoff_caught_stealing_home': 0, 'pickoff_2b': 0,
                'run': 0, 'triple_play': 1, 'batter_interference': 1, 'pickoff_3b': 0, 'sac_bunt_double_play': 1, 'pickoff_caught_stealing_3b': 0}

# Is Hit Dictionary - This puts a 1 for events that are hits (singles, doubles, triples, homers)
# and a zero for everything else :: based on events column
is_hit_dict = {'field_out': 0, 'nan': 0, 'strikeout': 0, 'double': 1, 'strikeout_double_play': 0,
               'single': 1, 'force_out': 0, 'hit_by_pitch': 0, 'grounded_into_double_play': 0, 'home_run': 1,
               'walk': 0, 'caught_stealing_2b': 0, 'sac_bunt': 0, 'triple': 1, 'sac_fly': 0,
               'field_error': 0, 'double_play': 0, 'catcher_interf': 0, 'fielders_choice_out': 0, 'fielders_choice': 0,
               'pickoff_1,b': 0, 'other_out': 0, 'caught_stealing_home': 0, 'pickoff_caught_stealing_2b': 0, 'caught_stealing_3b': 0,
               'sac_fly_double_play': 0, 'pickoff_caught_stealing_home': 0, 'pickoff_2b': 0, 'run': 0, 'triple_play': 0, 'batter_interference': 0,
               'pickoff_3b': 0, 'sac_bunt_double_play': 0, 'pickoff_caught_stealing_3b': 0}

# Swing Dictionary - This puts a 1 for a row where the batter swung and a 0 for when they didn't
# :: based on the description column
swing_dict = {'ball': 0, 'foul_tip': 1, 'called_strike': 0, 'swinging_strike': 1, 'pitchout':  0, 'bunt_foul_tip':  1,
              'foul': 1, 'hit_into_play_no_out': 1, 'hit_into_play': 1, 'hit_into_play_score': 1, 'missed_bunt':  1,
              'hit_by_pitch': 0, 'blocked_ball': 0, 'swinging_strike_blocked': 1, 'foul_bunt':  1}

# Fair Contact Dict - Puts a 1 for pitches there were put in play (fair) :: based on description column
fair_contact_dict = {'ball': 0, 'foul_tip': 0, 'called_strike': 0, 'swinging_strike': 0, 'pitchout':  0,
                     'foul': 0, 'hit_into_play_no_out': 1, 'hit_into_play': 1, 'missed_bunt':  0,
                     'hit_into_play_score': 1, 'hit_by_pitch': 0, 'bunt_foul_tip':  0,
                     'blocked_ball': 0, 'swinging_strike_blocked': 0, 'foul_bunt':  0}

# Foul or Fair Contact Dict - Puts a 1 for pitches there were put in play (includes foul balls)
# :: based on description column
foul_contact_dict = {'ball': 0, 'foul_tip': 1, 'called_strike': 0, 'swinging_strike': 0, 'pitchout':  0,
                     'foul': 1, 'hit_into_play_no_out': 1, 'hit_into_play': 1, 'missed_bunt':  0,
                     'hit_into_play_score': 1, 'hit_by_pitch': 0, 'bunt_foul_tip':  1,
                     'blocked_ball': 0, 'swinging_strike_blocked': 0, 'foul_bunt':  1}


# OBP = (Hits + Walks + Hit by Pitch) / (At Bats + Walks + Hit by Pitch + Sacrifice Flies)


def addOns(df):
    df['game_date'] = pd.to_datetime(df['game_date'])
    sav = df.sort_values(by='game_date')

    sav['PA_flag'] = sav['events'].map(pa_flag_dict)
    sav['AB_flag'] = sav['events'].map(ab_flag_dict)
    sav['Is_Hit'] = sav['events'].map(is_hit_dict)
    sav['Is_Hit'] = sav['Is_Hit'].fillna(0)
    sav['SwungOn'] = sav['description'].map(swing_dict)
    sav['ContactMade_Fair'] = sav['description'].map(fair_contact_dict)
    sav['ContactMade_Foul'] = sav['description'].map(foul_contact_dict)

    sav['BatterTeam'] = np.where(sav['inning_topbot'] == 'Top', sav['away_team'], sav['home_team'])
    sav['PitcherTeam'] = np.where(sav['inning_topbot'] == 'Top', sav['home_team'], sav['away_team'])
    return sav


def get_statcast_data(start_date, end_date, pitcher_name, statcast_type='batter'):
    if statcast_type == 'batter':
        df = statcast_batter(start_date, end_date,
                             get_player_id(pitcher_name[0], pitcher_name[1]))
    else:
        df = statcast_pitcher(start_date, end_date, player_id=
                              get_player_id(pitcher_name[0], pitcher_name[1]))
    df = addOns(df)
    return df

import time

import statsapi
from statcast_format_data import get_statcast_data
from pybaseball import statcast_pitcher, cache

cache.enable()

def get_player_name(player_id, players):
    # Loop through the players
    for player in players.values():
        # Check if the player's id matches the id we are looking for
        if player['id'] == player_id:
            # If the ids match, return the player's fullName
            return player['fullName']
    return None


def get_latest_pitcher(pitcher_list):
    # Set a variable to keep track of the latest pitcher
    latest_pitcher = None
    # Loop through the list of pitchers
    for pitcher in pitcher_list:
        # Check if the pitcher's personId is not equal to 0
        if pitcher['personId'] != 0:
            # If the personId is not 0, set the latest pitcher to the current pitcher
            latest_pitcher = pitcher
    # Return the latest pitcher
    return latest_pitcher


def get_next_batter(pitcher_stats, batting_order):
    # Get the number of innings pitched from the pitcher stats
    innings_pitched = float(pitcher_stats['ip'])
    # Calculate the number of batters faced
    num_batters_faced = int(innings_pitched * 3) + 1
    print(num_batters_faced)
    print(innings_pitched)
    # Get the next batter from the batting order
    next_batter = batting_order[num_batters_faced % len(batting_order)]
    # Return the next batter
    return next_batter


def run_game_data():
    # https://www.reddit.com/r/Sabermetrics/comments/99yvdc/statsapi_working_documentation/
    sched = statsapi.schedule(start_date='04/27/2023',
                              end_date='04/27/2023',
                              team=121,
                              opponent=120)
    line_score = statsapi.linescore(sched[0]['game_id'])
    box_score = statsapi.boxscore(sched[0]['game_id'])
    box_score_data = statsapi.boxscore_data(sched[0]['game_id'])
    live_game = statsapi.get('game', {'gamePk': sched[0]['game_id']})
    data = live_game['liveData']['plays']['currentPlay']

    print(f"The count is {data['count']['balls']}-{data['count']['strikes']}.  {data['count']['outs']} outs.")
    print(f"B: {data['matchup']['batSide']['code']} {data['matchup']['batter']['fullName']} ({data['matchup']['batter']['id']})")
    print(f"P: {data['matchup']['pitchHand']['code']} {data['matchup']['pitcher']['fullName']} ({data['matchup']['pitcher']['id']})")
    print(f"{data['playEvents']}")

    batter_df = get_statcast_data('2023-01-01', '2023-12-30', data['matchup']['batter']['id'],
                                  statcast_type='batter')
    batter_pitch_counts = batter_df['pitch_name'].value_counts(normalize=True)
    print(batter_pitch_counts[:3])
    pitcher_df = get_statcast_data('2023-01-01', '2023-12-30', data['matchup']['pitcher']['id'],
                                  statcast_type='pitcher')
    pitcher_df = pitcher_df[pitcher_df['balls'] == data['count']['balls']]
    pitcher_df = pitcher_df[pitcher_df['strikes'] == data['count']['strikes']]
    pitcher_pitch_counts = pitcher_df['pitch_name'].value_counts(normalize=True)
    print(pitcher_pitch_counts[:3])
    print('----------------------------------------------')

while True:
    run_game_data()
    time.sleep(20)
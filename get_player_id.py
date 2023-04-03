from pybaseball import playerid_lookup

# Helper: https://docs.google.com/spreadsheets/d/1AP4kH92zCW7Qwh7M1-S-cx2DAzcdYkbzK1Hkp5U1I_k/edit#gid=0
# Above sheet is for 2022 season


def get_player_id(first_name, last_name):
    player = playerid_lookup(last_name, first_name)
    return player.key_mlbam.values[0]


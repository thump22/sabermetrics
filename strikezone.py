from pybaseball import playerid_lookup, cache, statcast_batter, statcast_pitcher
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from statcast_format_data import get_statcast_data

cache.enable()


# Plots strike zone of pitches for a batter
# Time can be a day or a range of dates (ex: batterSZ('2016-05-01', 'david', 'ortiz')
# or batterSZ('2016-04-01 to 2016-05-01', 'david', 'ortiz'))
def batter_strikezone(firstname, lastname, start_date, end_date):
    player = playerid_lookup(lastname, firstname)

    data = get_statcast_data(start_date, end_date, player["key_mlbam"][0],
                             statcast_type='batter')
    if data.size == 0:
        return "Error: Did not find any data. Try again."
    general_strikezone(data, firstname, lastname, 'batter')


# Plots strike zone of pitches for a pitcher
# Time can be a day or a range of dates (ex: pitcherSZ('2017-05-30', 'chris', 'sale')
# or pitcherSZ('2017-05-01 to 2017-06-01', 'chris', 'sale'))
def pitcher_strikezone(firstname, lastname, start_date, end_date):
    player = playerid_lookup(lastname, firstname)

    data = get_statcast_data(start_date, end_date, player["key_mlbam"][0],
                             statcast_type='batter')
    if data.size == 0:
        return "Error: Did not find any data. Try again."
    general_strikezone(data, firstname, lastname, 'pitcher')


# Set labels for graph
def set_labels(exclude):
    if "foul" in exclude:
        exclude.pop(exclude.index("foul"))

    blue = patches.Patch(color='blue', label='Hit Into Play')
    red = patches.Patch(color='red', label='Called Strike')
    brown = patches.Patch(color='brown', label='Foul/Swinging Strike')
    green = patches.Patch(color='green', label='Ball')
    colors = [blue, red, brown, green]
    labels = [patch.get_label() for patch in colors]

    for elm in exclude:
        if elm == "hit":
            colors.pop(labels.index("Hit Into Play"))
        elif elm == "called_strike":
            colors.pop(labels.index("Called Strike"))
        elif elm == "swinging_strike":
            colors.pop(labels.index("Foul/Swinging Strike"))
        elif elm == "ball":
            colors.pop(labels.index("Ball"))
    return colors


# Set color depending on type of outcome on pitch
def set_colors(data):
    colors = []
    for row in data['description']:
        if "hit" in row:
            colors.append("blue")
        elif "called_strike" in row:
            colors.append("red")
        elif "foul" in row or "swinging_strike" in row:
            colors.append("brown")
        else:
            colors.append("green")
    return colors


def general_strikezone(data, firstname, lastname, posid):
    print("Finding strike zone dimensions for player.")
    top = np.round(np.mean(data['sz_top']), 3)  # height from ground to top of strike zone
    bot = np.round(np.mean(data['sz_bot']), 3)  # height from ground to bottom of strike zone

    labels = set_labels(data)

    print("Creating strike zone from player's perspective.")
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111)

    if posid == 'batter': ax.scatter(data['plate_x'], data['plate_z'], c=set_colors(data), marker='o')
    # default is x coords in batter's perspective, so multiply by -1 to reverse direction for pitcher
    elif posid == 'pitcher':
        ax.scatter([x_pos*-1 for x_pos in data['plate_x']], data['plate_z'], c=set_colors(data), marker='o')

    # personalize strike zone per player
    ax.add_patch(patches.Rectangle((-20.14/24, bot), 20.14/12, top-bot, fill=False))
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 6)
    plt.legend(handles=labels)
    plt.xlabel("Horizontal Distance Away from Center of Plate (feet)")
    plt.ylabel("Height of Pitch (feet)")

    if posid == 'batter':
        plt.title("Strike Zone of " + firstname.title() + " " + lastname.title() + " from Umpire's Perspective")
    elif posid == 'pitcher':
        plt.title("Strike Zone of " + firstname.title() + " " + lastname.title() + " from Pitcher's Perspective")

    plt.show()


player = playerid_lookup('Cortes', 'Nestor')

df = get_statcast_data("2023-04-01",
                       "2023-12-30",
                       player["key_mlbam"][0],
                       statcast_type='pitcher')
# df = df[df['Is_Hit'] == 1]
general_strikezone(df, 'Nestor', 'Cortes', 'pitcher')
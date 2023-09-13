import matplotlib.pyplot as plt
import seaborn as sns

from scripts.random.statcast_format_data import *

cache.enable()

first_name = "Kodai"
last_name = "Senga"
start_date = "2023-06-28"
end_date = "2023-06-28"

player_id = get_player_id(first_name, last_name)
pitcher_statcast = get_statcast_data(
    start_date=start_date,
    end_date=end_date,
    player_id=player_id,
    statcast_type="pitcher")
pitcher_statcast = addOns(pitcher_statcast)
inning_descr = pitcher_statcast["inning"].describe()
by_inning = pitcher_statcast.groupby(["inning", "pitch_name"]).agg(
    {
        'release_speed': 'mean',
        'release_spin_rate': 'mean'
    }
)
by_inning = by_inning.reset_index()
cols_to_graph = [
    ['release_speed', 'Release Speed'],
    ['release_spin_rate', 'Spin Rate']
]
for graph in cols_to_graph:
    ax = sns.relplot(data=by_inning, x='inning', y=graph[0], kind='line', hue='pitch_name', linewidth=3)
    ax.set_xticklabels(rotation=1)
    ax.set(ylabel=f'{graph[1]}', xlabel='Inning', title=f'')
    plt.show()
by_inning

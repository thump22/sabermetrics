import numpy as np

from pybaseball import statcast, cache
from scripts.random.statcast_format_data import addOns

cache.enable()

df = statcast('2023-04-01', '2023-12-30', team="NYM")
df = addOns(df)
df['in_scoring_position'] = np.where((df['on_2b'].notnull() & df['on_3b'].notnull()), True, False)
df_risp = df[df['in_scoring_position'] == True]
home_risp = df_risp[df_risp["home_team"] == "NYM"]
away_risp = df_risp[df_risp["away_team"] == "NYM"]
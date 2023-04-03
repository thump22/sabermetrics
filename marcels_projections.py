import pandas as pd
from pybaseball.analysis.projections.marcels import MarcelProjectionsPitching
from pybaseball.analysis.projections.marcels import MarcelProjectionsBatting
from pybaseball.lahman import people

ppl = people()  # for merging player names onto the projections
ppl['Player'] = ppl['nameFirst'].str.cat(ppl['nameLast'], ' ')
marcel_batting = MarcelProjectionsBatting()
marcel_pitching = MarcelProjectionsPitching()

pitchers = marcel_pitching.projections(2023)
batters = marcel_batting.projections(2023)
pitchers = pd.merge(ppl[['playerID', 'Player']], pitchers, on='playerID', how='right')
batters = pd.merge(ppl[['playerID', 'Player']], batters, on='playerID', how='right')

batters = batters.sort_values('HR', ascending=False)
pitchers = pitchers.sort_values('SO', ascending=False)

batters.to_csv('marcel-batters.csv')
pitchers.to_csv('marcel-pitchers.csv')
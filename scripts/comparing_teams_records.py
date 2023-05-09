from pybaseball import schedule_and_record
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

year = 2023

mets_team_data = schedule_and_record(year, "NYM")
atlanta_team_data = schedule_and_record(year, "ATL")
phillies_team_data = schedule_and_record(year, "PHI")
washington_team_data = schedule_and_record(year, "WSN")
miami_team_data = schedule_and_record(year, "MIA")

mets_team_data['win-count'] = np.where(mets_team_data['W/L'] == 'W', 1, 0).cumsum()
atlanta_team_data['win-count'] = np.where(atlanta_team_data['W/L'] == 'W', 1, 0).cumsum()
phillies_team_data['win-count'] = np.where(phillies_team_data['W/L'] == 'W', 1, 0).cumsum()
washington_team_data['win-count'] = np.where(washington_team_data['W/L'] == 'W', 1, 0).cumsum()
miami_team_data['win-count'] = np.where(miami_team_data['W/L'] == 'W', 1, 0).cumsum()

plt.plot(mets_team_data[:50]['win-count'], label="NYM", color="#002D72", linewidth=3)
plt.plot(atlanta_team_data[:50]['win-count'], label="ATL", color="#CE1141")
plt.plot(phillies_team_data[:50]['win-count'], label="PHI", color="#E81828")
plt.plot(washington_team_data[:50]['win-count'], label="WSN", color="#AB0003")
plt.plot(miami_team_data[:50]['win-count'], label="MIA", color="#00A3E0")

plt.legend(loc=4)
plt.xlabel('Games into Season')
plt.ylabel('Win Count')
plt.title('NL East Record Throughout Season')
plt.show()
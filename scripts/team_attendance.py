from pybaseball import schedule_and_record
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

year = 2023
team = "NYM"

team_data = schedule_and_record(year, team)[:68]
team_data = team_data[team_data['Attendance'].notna()]
team_data["Time"] = team_data["Time"].apply(lambda x: float(x.split(':')[0])*60+float(x.split(':')[1]))

team_data_home = team_data[team_data['Home_Away'] == "Home"]

# plt.plot(team_data_home["Attendance"], label="Attendance", color="#002D72", linewidth=3)

bar = team_data_home["Attendance"].plot.bar(color="#002D72")
plt.legend(loc=4)
plt.xlabel('Games into Season')
plt.ylabel('Attendance')
plt.title(f'{team} Attendance ({year}) - {"{0:,.2f}".format(team_data_home["Attendance"].mean())}')
plt.show()

# plt.plot(team_data_home["Time"], label="Attendance", color="#002D72", linewidth=3)
# plt.show()
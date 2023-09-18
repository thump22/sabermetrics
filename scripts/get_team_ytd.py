from pybaseball import schedule_and_record, statcast_pitcher
import pandas as pd
from datetime import datetime, timedelta
#Create a date range with yesterday and today
ts = pd.date_range(end=(datetime.now() + timedelta(-1)), periods=1)
yesterday_date = ts[0].date()

# year = 2023
# team = "NYM"
#
# mets_team_data = schedule_and_record(year, team)
# # mets_team_data["Datetime"] = datetime.datetime.strptime(mets_team_data['Date']}, 2023", "%A, %b %d, %Y").date()
# # mets_team_data['Datea'] = pd.to_datetime(mets_team_data['Date'], format='%A, %b %d')
# #Filter dataframe by yesterday's date
# data = mets_team_data[mets_team_data['Date'] == yesterday_date]
# data

from pybaseball import statcast_batter, spraychart


data = statcast_pitcher('2023-03-25', '2023-07-01', 453286)
sub_data = data[data['home_team'] == 'NYM']
spraychart(sub_data, 'mets', title='Scherzer @ Citi Field (2023)')
data
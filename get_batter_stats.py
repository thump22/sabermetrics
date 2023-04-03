from statcast_format_data import get_statcast_data
from pybaseball import statcast_batter, spraychart




x = get_statcast_data('2022-01-01', '2023-12-30', ['pete', 'alonso'], statcast_type='batter')
df = x[x['Is_Hit'] == 1]
sub_data = df[df['home_team'] == 'NYM']
spraychart(sub_data, 'mets', title='Jose Altuve: May-June 2019')
print(df)

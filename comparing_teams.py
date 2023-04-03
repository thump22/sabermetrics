from pybaseball import schedule_and_record
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mets_2022 = schedule_and_record(2022, 'NYM')
mets_2015 = schedule_and_record(2015, 'NYM')
mets_2006 = schedule_and_record(2006, 'NYM')
mets_2000 = schedule_and_record(2000, 'NYM')
mets_1986 = schedule_and_record(1986, 'NYM')

mets_2022['win-count'] = np.where(mets_2022['W/L'] == 'W', 1, 0).cumsum()
mets_2015['win-count'] = np.where(mets_2015['W/L'] == 'W', 1, 0).cumsum()
mets_2006['win-count'] = np.where(mets_2006['W/L'] == 'W', 1, 0).cumsum()
mets_2000['win-count'] = np.where(mets_2000['W/L'] == 'W', 1, 0).cumsum()
mets_1986['win-count'] = np.where(mets_1986['W/L'] == 'W', 1, 0).cumsum()


# diff = mets['win-count'] - braves['win-count']
# diff.to_csv('mets-braves-win-count-diff')

plt.plot(mets_2022['win-count'], label="2022")
plt.plot(mets_2015['win-count'], label="2015")
plt.plot(mets_2006['win-count'], label="2006")
plt.plot(mets_2000['win-count'], label="2000")
plt.plot(mets_1986['win-count'], label="1986")

plt.legend(loc=4)
plt.xlabel('Games into Season')
plt.ylabel('Win Count')
plt.title('Record Throughout Season')
plt.show()
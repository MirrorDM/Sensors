from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import shutil
import sqlite3
import os
import sys

# Copy file of database.
origin_db = 'air.db'
temp_db = 'air.bak.db'

try:
    shutil.copy2(origin_db, temp_db)
except:
    print("Copy failed.")
    sys.exit(1)

conn = sqlite3.connect(temp_db)

end_dt = datetime.now()
start_dt = end_dt - timedelta(hours=12)

end_ts = datetime.timestamp(end_dt)
start_ts = datetime.timestamp(start_dt)

data = conn.execute('''SELECT * FROM Air WHERE TIME_STAMP>? AND TIME_STAMP<?''', 
    (start_ts, end_ts)).fetchall()

ts_list = [line[0] for line in data]
dt_x = [datetime.fromtimestamp(ts) for ts in ts_list]
co2 = [line[1] for line in data]
pm25us = [line[2] for line in data]
pm25cn = [line[3] for line in data]
pm100us = [line[4] for line in data]

# Plot single
# plt.plot(dt_x, co2)`
# plt.show()

max_len = 300
while len(dt_x) > max_len:
    dt_x = dt_x[::2]
    co2 = co2[::2]
    pm25us = pm25us[::2]
    pm100us = pm100us[::2]
# Plot double
fig, axes = plt.subplots(2, 1, figsize=(8, 8))
fig.suptitle('Air Quality')

axes[0].plot(dt_x, co2, 'b', label='CO2')
axes[0].legend(loc=1)
axes[0].set_ylabel('CO2')
axes[0].set_title('CO2 Level')

axes[1].plot(dt_x, pm25us, 'g', label='PM2.5')
axes[1].plot(dt_x, pm100us, 'b', label='PM10')
axes[1].legend(loc=1)
axes[1].set_ylabel('PM2.5')
axes[1].set_title('PM2.5 Index')

# fig, laxis = plt.subplots()
# laxis.plot(dt_x, co2, 'b', label='CO2')
# laxis.legend(loc='upper left')
# laxis.set_xlabel('Time')
# laxis.set_ylabel('CO2')

# raxis = laxis.twinx()
# raxis.plot(dt_x, pm25us, 'g', label='PM2.5')
# raxis.legend(loc='upper right')
# raxis.set_ylabel('PM2.5')

plt.show()

conn.close()
os.remove(temp_db)
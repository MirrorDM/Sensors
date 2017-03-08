from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import shutil
import sqlite3

try:
    shutil.copy2('air.db', 'air.bak.db')
except:
    print("Copy failed.")

conn = sqlite3.connect('air.bak.db')

end_dt = datetime.now()
start_dt = end_dt - timedelta(hours=24)

end_ts = datetime.timestamp(end_dt)
start_ts = datetime.timestamp(start_dt)

data = conn.execute('''SELECT * FROM Air WHERE TIME_STAMP>? AND TIME_STAMP<?''', 
    (start_ts, end_ts)).fetchall()

ts_list = [line[0] for line in data]
dt_x = [datetime.fromtimestamp(ts) for ts in ts_list]
co2 = [line[1] for line in data]
pm25us = [line[2] for line in data]

# Plot single
plt.plot(dt_x, co2)
plt.show()

# Plot double
fig, laxis = plt.subplots()
raxis = laxis.twinx()
laxis.plot(dt_x, co2)
raxis.plot(dt_x, pm25us)
plt.show()

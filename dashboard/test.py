import pandas as pd
from datetime import datetime

time_range_start = datetime.min
data = pd.read_csv('../data/temperature.csv', parse_dates=True, index_col='date')

data = data[data['date'] >= time_range_start]
data.resample('1H')
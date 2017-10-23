import sys
import os
import pandas as pd
import talib
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# -------------------------------------------------------------
# local import
# -------------------------------------------------------------
path1 = os.path.join(parent_folder, 'data_ploter')
sys.path.append(path1)
path2 = os.path.join(parent_folder, 'simulator')
sys.path.append(path2)
from basic_ploter import BasicPloter
from basic_simulator import BasicSimulator
# -------------------------------------------------------------




# -------------------------------------------------------------
# data
# -------------------------------------------------------------
instrument = 'GBP_USD'
data_file = '{}.csv'.format(instrument)
data_folder = os.path.join(parent_folder, 'data')
date_file_path = os.path.join(data_folder, data_file)
# -------------------------------------------------------------



df = pd.read_csv(date_file_path)
closeMidData = df['closeMid'].values
dateData = df['date'].values
macd, macdsignal, macdhist = talib.MACD(closeMidData, fastperiod=12, slowperiod=26, signalperiod=9)
forex_ploter = BasicPloter()
forex_ploter.plot_basic_trend(dateData, closeMidData, title = instrument)
forex_ploter.plot_MACD(dateData, closeMidData, macd, macdsignal, macdhist, title = instrument)



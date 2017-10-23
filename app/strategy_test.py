import sys
import os
import pandas as pd
import talib

parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ----------------------------------------------------------------------------------------------------------------------
# local import
# ----------------------------------------------------------------------------------------------------------------------
path1 = os.path.join(parent_folder, 'data_ploter')
sys.path.append(path1)
path2 = os.path.join(parent_folder, 'simulator')
sys.path.append(path2)
from basic_ploter import BasicPloter
from basic_simulator import BasicSimulator
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# raw data
# ----------------------------------------------------------------------------------------------------------------------
instrument = 'GBP_USD'
data_file = '{}.csv'.format(instrument)
data_folder = os.path.join(parent_folder, 'data')
date_file_path = os.path.join(data_folder, data_file)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# MACD data
# ----------------------------------------------------------------------------------------------------------------------
df = pd.read_csv(date_file_path)
closeMidData = df['closeMid'].values
dateData = df['date'].values
macd, macdsignal, macdhist = talib.MACD(closeMidData, fastperiod=12, slowperiod=26, signalperiod=9)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# [MACD strategy] test
# ----------------------------------------------------------------------------------------------------------------------
capital = 1
basic_simulator1 = BasicSimulator(capital, closeMidData, dateData)
buy_id_list = []
open_pos_date_list = []
close_pos_date_list = []

for i, day in enumerate(dateData):
    if macd[i] == 'nan':
        continue
    else:
        dif_value = macd[i]
        dea_value = macdsignal[i]
        # --------------------------------------------------------------------
        # MACD jin_cha, open and close (*buy)
        # --------------------------------------------------------------------
        # open pos
        if dif_value >= dea_value and is_dif_line_down:
            action = 'buy'
            capital = basic_simulator1.capital
            if capital <= 0:
                print("capital-{}, you have no more money to open new positions.".format(capital))
            else:
                uid = basic_simulator1.open_pos(day, capital, action=action)
                open_pos_date_list.append(day)
                buy_id_list.append(uid)

        # close pos
        if dif_value < dea_value and not is_dif_line_down:  # dif line up
            for uid in buy_id_list:
                is_closed = basic_simulator1.close_pos(uid, day)
                if is_closed:
                    close_pos_date_list.append(day)
                    buy_id_list.remove(uid)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # update is_dif_line_down
        # --------------------------------------------------------------------
        if dif_value < dea_value:
            is_dif_line_down = True
        else:
            is_dif_line_down = False
            # --------------------------------------------------------------------

final_capital = basic_simulator1.capital
print("final_capital: ", final_capital)

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# PLOT
# ----------------------------------------------------------------------------------------------------------------------
forex_ploter = BasicPloter()
# forex_ploter.plot_basic_trend(dateData, closeMidData, title = instrument)
forex_ploter.plot_MACD(dateData, closeMidData, macd, macdsignal, macdhist, title=instrument,
                       open_pos_date=open_pos_date_list, close_pos_date=close_pos_date_list)
# ----------------------------------------------------------------------------------------------------------------------


#================================================
import json
import os
import sys
import pandas as pd
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------------------
# local import 1
path1 = os.path.join(parent_folder, 'data_reader')
sys.path.append(path1)
from forex_data_reader import ReadForexData
# -------------------------------------------------------------



# =========================================READING UP-TO-DATE-FOREX-DATA================================================
# (1.) read parameters
# update mode to testing
parameter_dict = {}
parameter_dict['mode'] = 'trading'
parameter_dict['instrument'] = 'GBP_USD' #'USD_JPY', 'USD_CAD', 'GBP_USD', 'USD_CHF', 'AUD_USD'
parameter_dict['granularity'] = "D"
parameter_dict['candle_format'] = "midpoint"
parameter_dict['date_range'] = 2000
parameter_dict['alignmentTimezone'] = "America%2FNew_York"
parameter_dict['output_attributors_str'] = "instrument,date,openMid,closeMid,highMid,lowMid,volume"

# data save path
file_save_name = '{}.csv'.format(parameter_dict['instrument'])
file_save_path = os.path.join(parent_folder, 'data', file_save_name)
parameter_dict['file_path'] = file_save_path
#
# =========================================READING UP-TO-DATE-FOREX-DATA================================================
# (2.) read forex data
read_forex_data = ReadForexData(parameter_dict)
read_forex_data.new_read_data_from_onanda()
read_forex_data.write_forex_dict_to_file()

# # --------------------------------------------panda test
# df = pd.read_csv(file_save_path)
# print (df.values)
# print (type(df.values))
# print (type(df['date'].values))
# print (df[0:3])
# # --------------------------------------------

# # ===========================================get the max, min and average of the data
# read_forex_data.get_data_distribution(read_forex_data.file_path)


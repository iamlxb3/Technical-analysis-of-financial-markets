import os
import requests
import collections
import re
import sys
import numpy as np




class ReadForexData:
    """read the up-to-date forex data via oanda API"""
    def __init__(self, parameter_dict):
        self.mode = parameter_dict['mode']
        self.instruments_list = ['EUR_USD', 'USD_JPY', 'USD_CAD', 'GBP_USD', 'USD_CHF','AUD_USD']
        self.instrument = parameter_dict['instrument']
        self.granularity = parameter_dict['granularity']
        self.candle_format = parameter_dict['candle_format']
        self.date_range = parameter_dict['date_range']
        self.time_zone = parameter_dict['alignmentTimezone']
        self.file_path = parameter_dict['file_path']
        self.output_attributors_str = parameter_dict['output_attributors_str']
        # reference:
        # http://developer.oanda.com/docs/timezones.txt
        self.url = "https://api-fxtrade.oanda.com/v1/candles?" \
                   "instrument={instrument}&" \
                   "count={date_range}&" \
                   "candleFormat={candle_format}&" \
                   "granularity={granularity}&" \
                   "dailyAlignment=0&" \
                   "alignmentTimezone={time_zone}".format(instrument = self.instrument,
                                                          date_range = self.date_range,
                                                          candle_format = self.candle_format,
                                                          granularity = self.granularity,
                                                          time_zone = self.time_zone)
        self.forex_data_dict = collections.defaultdict(lambda :[])

    def write_forex_dict_to_file(self):
        path = self.file_path
        #self.forex_data_dict : {'EUR_USD':[('AUD_USD', '2014-9-9', 0.77157, 0.772, 0.767955, 0.76851, 0.76, 0.11, 0.14), ...]}
        with open (path, 'w', encoding = 'utf-8') as f:
            f.write("{}\n".format(self.output_attributors_str))
            for instrument, days_feature_list in self.forex_data_dict.items():
                for i, day_features in enumerate(days_feature_list):
                    day_features = [str(x) for x in day_features]
                    feature_str = ','.join(day_features)
                    if i == len(days_feature_list) - 1:
                        f.write(feature_str)
                    else:
                        f.write(feature_str)
                        f.write('\n')
                    
    #['_', 'AUD_USD', '02/21/2017', '-0.12', '0.1', '-0.2', '0.31', '6162', '26.63',
    # '0.4', '1.8', '1.8', '3.2', '0.48', '0.64', '0.84', '-0.047', '-0.238', '-0.471\
    # n']
    
    def get_data_distribution(self, file_path):
        feature_all_value_dict = collections.defaultdict(lambda:[])
        feature_value_distribution_dict = collections.defaultdict(lambda:[])
        with open(file_path, 'r', encoding = 'utf-8') as f:
            for line in (f):
                feature_list = line.split(',')
                for i, feature in enumerate(feature_list):
                    if i < 3:
                        continue
                    feature_all_value_dict[i].append(float(feature.strip()))
        
        # compute max, min, etc
        for feature_id, feature_value_list in feature_all_value_dict.items():
            max_value = max(feature_value_list)
            min_value = min(feature_value_list)
            zero_list = [0 for x in feature_value_list if x == 0]
            # pos
            pos_feature_value_list = [x for x in feature_value_list if x > 0]
            if len(pos_feature_value_list) > 0:
                pos_average = sum(pos_feature_value_list) / len(pos_feature_value_list)
            else:
                pos_average = 0
            # neg
            neg_feature_value_list = [x for x in feature_value_list if x < 0]
            if len(neg_feature_value_list) > 0:
                neg_average = sum(neg_feature_value_list) / len(neg_feature_value_list)
            else:
                neg_average = 0
            # zero_num
            zero_num = len(zero_list)
            feature_value_distribution_dict[feature_id] = (max_value, min_value, pos_average, neg_average, zero_num)
    
        # write everything to file
        with open ('feature_value_distribution_dict.txt', 'w', encoding = 'utf-8') as f:
            feature_value_distribution_list = list(feature_value_distribution_dict.items())
            for feature_id, value_tuple in feature_value_distribution_list:
                max_value = value_tuple[0]
                min_value = value_tuple[1]
                pos_average = value_tuple[2]
                neg_average = value_tuple[3]
                zero_num = value_tuple[4]
                f.write("Feature_id: {}, max: {}, min: {}, pos_average: {}, neg_average: {}, zero_num: {}"
                .format(feature_id, max_value, min_value, pos_average, neg_average, zero_num))
                f.write('\n')
    
    def read_onanda_data(self):
        def compute_std(day, day_forex_list, feature, i, instrument):
            variance_list = []
            for j in range(day):
                feature_value = day_forex_list[i-j][feature]
                if feature == 'openMid':
                    if instrument == 'USD_JPY':
                        feature_value *= 10
                    else:
                        feature_value *= 1000
                elif feature == 'volume':
                    feature_value /= 1000
                variance_list.append(feature_value)
            std = np.std(variance_list)
            std = float("{:3.1f}".format(std))
            #oanda_logger.debug("instrument: {}, feature :{}, variance: {}".format(instrument, feature, std))
            return std

        '''read oanda data via online api to dict with several features'''
        ignore_date_num = 7
        for instrument in self.instruments_list:
            url = self.url.replace("#instrument", instrument)
            response = requests.get(url)
            response_status_code = response.status_code
            print("response_status_code: ", response_status_code)
            day_forex_list = dict(response.json())['candles']
            #print (day_forex_list)

            for i, day_forex_dict in enumerate(day_forex_list):
                if self.mode == 'testing':
                    if i < ignore_date_num or i > len(day_forex_list) - 1 - ignore_date_num: # -1-7
                        continue
                elif self.mode == 'trading':
                    if i < ignore_date_num:
                        continue

                time = day_forex_dict['time']
                time = re.findall(r'([0-9]+-[0-9]+-[0-9]+)', time)[0]
                time_list = time.split('-')
                # switch year with day, day with month
                time_list[0], time_list[2] = time_list[2], time_list[0]
                time_list[0], time_list[1] = time_list[1], time_list[0]
                time = '/'.join(time_list)
                ## getting features
                # openMid
                openMid = day_forex_dict['openMid']
                openMid_1_day_ago = day_forex_list[i - 1]['openMid']
                openMid_1_day_percent = float("{:2.2f}".format(100*((openMid - openMid_1_day_ago)/ openMid)))
                openMid_3_day_std = compute_std(3, day_forex_list, 'openMid', i, instrument)
                openMid_7_day_std = compute_std(7, day_forex_list, 'openMid', i, instrument)
                # highMid
                highMid = day_forex_dict['highMid']
                highMid_1_day_ago = day_forex_list[i - 1]['highMid']
                highMid_1_day_percent = float("{:2.2f}".format(100*((highMid - highMid_1_day_ago) / highMid)))
                # lowMid
                lowMid = day_forex_dict['lowMid']
                lowMid_1_day_ago = day_forex_list[i - 1]['lowMid']
                lowMid_percent = float("{:2.2f}".format(100*((lowMid - lowMid_1_day_ago)/ lowMid)))
                # closeMid
                if self.mode == 'trading':
                    closeMid = day_forex_dict['closeMid']
                    closeMid_1_day_ago = day_forex_list[i - 1]['closeMid']
                    closeMid_1_day_later = 0.0
                    closeMid_3_day_later = 0.0
                    closeMid_7_day_later = 0.0
                    closeMid_1_day_percent = float("{:2.2f}".format(100*((closeMid - closeMid_1_day_ago)/ closeMid)))
                elif self.mode == 'testing':
                    closeMid = day_forex_dict['closeMid']
                    closeMid_1_day_ago = day_forex_list[i - 1]['closeMid']
                    closeMid_1_day_later = day_forex_list[i + 1]['closeMid']
                    closeMid_3_day_later = day_forex_list[i + 3]['closeMid']
                    closeMid_7_day_later = day_forex_list[i + 7]['closeMid']
                    closeMid_1_day_percent = float("{:2.2f}".format(100*((closeMid - closeMid_1_day_ago)/ closeMid)))
                # volume
                volume = day_forex_dict['volume']
                volume_1_day_ago = day_forex_list[i - 1]['volume']
                volume_1_day_percent = float("{:2.2f}".format(100*((volume - volume_1_day_ago)/ volume)))
                volume_3_day_std = compute_std(3, day_forex_list, 'volume', i, instrument)
                volume_7_day_std = compute_std(7, day_forex_list, 'volume', i, instrument)
                # profit
                if self.mode == 'trading':
                    profit_1_day = 0.0
                    profit_3_day = 0.0
                    profit_7_day = 0.0
                elif self.mode == 'testing':
                    profit_1_day = float("{:2.3f}".format(100*((closeMid_1_day_later - closeMid) / closeMid)))
                    profit_3_day = float("{:2.3f}".format(100*((closeMid_3_day_later - closeMid) / closeMid)))
                    profit_7_day = float("{:2.3f}".format(100*((closeMid_7_day_later - closeMid) / closeMid)))
                # custom feature
                if highMid - lowMid == 0:
                    real_body_percent = 0.0
                    upper_shadow_percent = 0.0
                    lower_shadow_percent = 0.0
                else:
                    real_body_percent = float("{:2.2f}".format(100*abs((openMid - closeMid) / (highMid - lowMid))))
                    upper_shadow_percent = float("{:2.2f}".format(100*abs((highMid - openMid) / (highMid - lowMid))))
                    lower_shadow_percent = float("{:2.2f}".format(100*abs((closeMid - lowMid) / (highMid - lowMid))))
                # 1,AA,1/14/2011,$16.71,$16.71,$15.64,$15.97,242963398,-4.42849,1.380223028,239655616,$16.19,$15.79,
                # -2.47066,19,0.187852
                day_forex_tuple = ('_', instrument, time, openMid_1_day_percent, highMid_1_day_percent, lowMid_percent,
                                   closeMid_1_day_percent, volume, volume_1_day_percent, openMid_3_day_std,
                                   openMid_7_day_std, volume_3_day_std, volume_7_day_std,
                                   real_body_percent, upper_shadow_percent, lower_shadow_percent, profit_1_day,
                                   profit_3_day, profit_7_day, openMid)
                self.forex_data_dict[instrument].append(day_forex_tuple)

    def new_read_data_from_onanda(self):
        def compute_std(day, day_forex_list, feature, i, instrument):
            variance_list = []
            for j in range(day):
                feature_value = day_forex_list[i-j][feature]
                if feature == 'openMid':
                    if instrument == 'USD_JPY':
                        feature_value *= 10
                    else:
                        feature_value *= 1000
                elif feature == 'volume':
                    feature_value /= 1000
                variance_list.append(feature_value)
            std = np.std(variance_list)
            std = float("{:3.1f}".format(std))
            #oanda_logger.debug("instrument: {}, feature :{}, variance: {}".format(instrument, feature, std))
            return std

        '''read oanda data via online api to dict with several features'''
        ignore_date_num = 7
        instrument = self.instrument
        url = self.url
        response = requests.get(url)
        response_status_code = response.status_code
        print("response_status_code: ", response_status_code)
        day_forex_list = dict(response.json())['candles']
        #print (day_forex_list)

        for i, day_forex_dict in enumerate(day_forex_list):
            if self.mode == 'testing':
                if i < ignore_date_num or i > len(day_forex_list) - 1 - ignore_date_num: # -1-7
                    continue
            elif self.mode == 'trading':
                if i < ignore_date_num:
                    continue

            time = day_forex_dict['time']
            time = re.findall(r'([0-9]+-[0-9]+-[0-9]+)', time)[0]
            time_list = time.split('-')
            # switch year with day, day with month
            time_list[0], time_list[2] = time_list[2], time_list[0]
            time_list[0], time_list[1] = time_list[1], time_list[0]
            time = '/'.join(time_list)
            ## getting features
            # openMid
            openMid = day_forex_dict['openMid']
            # highMid
            highMid = day_forex_dict['highMid']
            # lowMid
            lowMid = day_forex_dict['lowMid']
            # closeMid
            closeMid = day_forex_dict['closeMid']
            # volume
            volume = day_forex_dict['volume']

            day_forex_tuple = (instrument, time, openMid, closeMid, highMid, lowMid, volume)
            self.forex_data_dict[instrument].append(day_forex_tuple)



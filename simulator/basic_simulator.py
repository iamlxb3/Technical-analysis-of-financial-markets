import collections
import sys


class BasicSimulator:
    def __init__(self, init_capital, price_data, date_data, transaction_fee=0.0):
        self.capital = init_capital
        self.pos_unique_id = 0
        self.pos_dict = collections.defaultdict(lambda: {})
        self.price_data = list(price_data)
        self.date_data = list(date_data)
        self.transaction_fee = transaction_fee

    def open_pos(self, date, capital, action='buy', is_print=True):
        if capital > self.capital:
            print("Capital {} not sufficient to open position!".format(capital))
            sys.exit()
        pos_detail_dict = {'action': action, 'date': date, 'capital': capital}
        self.pos_dict[self.pos_unique_id] = pos_detail_dict
        placed_uid = self.pos_unique_id
        self.pos_unique_id += 1
        self.capital -= capital
        if is_print:
            print(
                "Uid-{}, Open position({}) sucesfully for {} capital on {}.".format(placed_uid, action, capital, date))
        return placed_uid

    def close_pos(self, uid, close_pos_date, is_print=True):
        # print ("self.pos_dict[uid]: ", self.pos_dict[uid])
        open_pos_date = self.pos_dict[uid]['date']
        capital = self.pos_dict[uid]['capital']
        action = self.pos_dict[uid]['action']

        open_date_price = self.price_data[self.date_data.index(open_pos_date)]
        close_date_price = self.price_data[self.date_data.index(close_pos_date)]

        if action == 'buy':
            price_change = (close_date_price - open_date_price) / open_date_price
        elif action == 'sell':
            price_change = -1 * (close_date_price - open_date_price) / open_date_price
        else:
            print("Action wrong! Action: {}".format(action))
            sys.exit()
        profit = capital * price_change
        capital += profit
        self.capital += capital

        # delete this position
        self.pos_dict.pop(uid)
        if is_print:
            print("Uid-{}, Close position({}) successfully! Profit: {}".format(uid, action, profit))
        return True

import matplotlib.pyplot as plt

class BasicPloter:

    def __init__(self):
        pass

    def plot_basic_trend(self, date, data, label = '', title = '', xlabel = ''):
        f1, (ax1) = plt.subplots(1, sharex=True, sharey=True)
        X = [x for x in range(len(date))]
        # ax1
        ax1.plot(X, data, '-', label=label)
        date[1:-1] = ['' for x in range(len(date)-2)]
        plt.xticks(X, date)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.legend(loc=2)
        #
        plt.show()
        #plt.savefig('{}.png'.format(aaa))

    def _plot_dots(self, dot_ax, date, data, open_pos_date, close_pos_date):
        date_list = list(date)
        data_list = list(data)

        # open pos
        open_pos_index = [date_list.index(date) for date in open_pos_date]
        open_pos_value = [data_list[index] for index in open_pos_index]
        #

        # close pos
        close_pos_index = [date_list.index(date) for date in close_pos_date]
        close_pos_value = [data_list[index] for index in close_pos_index]
        #


        dot_ax.plot(open_pos_index, open_pos_value, 'rx', label='open pos')
        dot_ax.plot(close_pos_index, close_pos_value, 'gx', label='close pos')



    def plot_MACD(self, date, data, macd, macdsignal, macdhist, label = '', title = '', xlabel = '',
                  open_pos_date = None, close_pos_date = None):

        f1, (ax1, ax2) = plt.subplots(2, sharex=True)
        X = [x for x in range(len(date))]
        # ----------------------------------------------------------------------------
        # plot for the basic trend
        # ----------------------------------------------------------------------------
        # ax1
        ax1.plot(X, data, '-', label=label)

        # plot open/close dots
        if open_pos_date and close_pos_date:
            self._plot_dots(ax1, date, data, open_pos_date, close_pos_date)
        #

        date[1:-1] = ['' for x in range(len(date)-2)]
        plt.xticks(X, date)
        ax1.set_title(title)
        ax1.set_xlabel(xlabel)
        ax1.legend(loc=2)
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # plot for MACD
        # ----------------------------------------------------------------------------
        X = [x for x in range(len(date))]
        # ax1
        ax2.plot(X, macd, '-b', label='DIF')
        ax2.plot(X, macdsignal, '-r', label='DEA')
        #ax2.plot(X, macdhist, '-', label='HISTOGRAM')
        # plt.xticks(X, date)
        # ax1.set_title(title)
        # ax1.set_xlabel(xlabel)
        # ax1.legend(loc=2)
        # ----------------------------------------------------------------------------

        #plt.tight_layout()
        plt.show()







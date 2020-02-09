from collections import namedtuple
import datetime
from pandas_datareader import data as pdr
import yfinance as yf
from Data import Intervals
from Utility import *
import Consts
import logger

StockQuote = namedtuple('StockQuote', ['Date', 'Hour', 'Weekday', 'Open', 'Low', 'High', 'Close'])

log = logger.get_logger('DataParser')


class DataParser:
    def __init__(self, tickers, start, stop=None, interval=Intervals._1h):
        self.tickers = tickers if isinstance(tickers, (list, set, tuple)) else tickers.replace(',', ' ').split()
        self.start = start
        self.stop = stop
        self.interval = interval.value if isinstance(interval, Intervals) else interval
        self.deltatime = Intervals(self.interval).to_deltatime()
        self.data = None
        self.week_data = []

        yf.pdr_override()  # <== that's all it takes :-)

    def download_data(self):
        # download dataframe using pandas_datareader
        log.debug('Downloading ...')
        self.data = pdr.get_data_yahoo(self.tickers, start=self.start, end=self.stop, interval=self.interval)
        # d2 = pdr.DataReader(tickers='MSFT', data_source='google', start=self.start, interval=self.interval)
        # print(d2)
        # from pandas_datareader import stooq
        # d3 = stooq.StooqDailyReader(symbols='MSFT', start=self.start).read()
        # # d3 = pdr.get_data_stooq(symbols='MSFT', start=self.start, freq='d')
        # print('-'*30)
        # print(d3)
        # r4 = stooq.StooqDailyReader(symbols='MSFT', start=self.start)
        # r4.freq='1h'
        # d4 = r4.read()
        # print('-' * 30)
        # print(d4

    def parse_to_week_data(self):
        for ticker in self.tickers:
            market_start_hour = get_market_open(get_market(ticker), Intervals(self.interval))

            prev_date = None
            counter = 0

            for i, row in enumerate(self.data.iterrows()):
                date = datetime.datetime.strptime(row[0]._date_repr, Consts.date_format).date()
                if date == prev_date:
                    counter += 1
                else:
                    counter = 0
                prev_date = date
                sq = StockQuote(date, add_time(market_start_hour, self.deltatime * counter),
                                day_of_week(row[0]._date_repr, Consts.date_format),
                                row[1]['Open'], row[1]['Low'], row[1]['High'], row[1]['Close'])
                self.week_data.append(sq)

    def _show(self):
        for v in self.week_data:
            log.info(v)


if __name__ == '__main__':
    dp = DataParser('MSFT', '2019-08-01', interval='1h')
    dp.download_data()

    dp.parse_to_week_data()
    dp._show()

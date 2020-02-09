from collections import namedtuple
from enum import Enum
from datetime import timedelta, datetime
import Consts

MarketData = namedtuple('MarketData', ['Open', 'Close', 'Tickers'])


class Intervals(Enum):
    _1m = '1m'
    _5m = '5m'
    _30m = '30m'
    _1h = '1h'
    _1d = '1d'

    def to_deltatime(self):
        if self == Intervals._1m:
            return timedelta(minutes=1)
        elif self == Intervals._5m:
            return timedelta(minutes=5)
        elif self == Intervals._30m:
            return timedelta(minutes=30)
        elif self == Intervals._1h:
            return timedelta(hours=1)
        elif self == Intervals._1d:
            return timedelta(days=1)


markets = {'NASDAQ': MarketData(Open=datetime.strptime('15:30:00', Consts.time_format).time(),
                                Close=datetime.strptime('22:00:00', Consts.time_format).time(),
                                Tickers=['MSFT', 'APPL'])}

if __name__ == '__main__':
    interval = Intervals._1h;

    print(interval)
    print(interval.to_deltatime())
    print(Intervals('1m'))

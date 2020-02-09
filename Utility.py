import datetime
import Data
from Consts import Weekday


def log_obj(object):
    try:
        log
    except NameError:
        import logger
        log = logger.get_logger('log_obj::Adhoc')

    log.info('-'.center(30, '-'))
    log.info("Type: {}".format(type(object)))
    log.info("dir: {}".format(dir(object)))
    log.info("Object: {}".format(object))
    log.info('-'.center(30, '-'))


def add_time(time, timedelta: datetime.timedelta):
    tmp = datetime.datetime.combine(datetime.date.today(), time) + timedelta
    return tmp.time()


def day_of_week(date, format: str):
    return Weekday(datetime.datetime.strptime(date, format).strftime('%A'))


def get_market(ticker: str):
    ticker = ticker.upper()
    for market, market_data in Data.markets.items():
        if ticker in market_data.Tickers:
            return market

    raise Exception('Nie znaleziono giełdy dla tikera "{}"'.format(ticker))


def get_market_open(market: str, interval: Data.Intervals = None):
    time = Data.markets[market].Open
    if interval:
        if interval == Data.Intervals._1h:
            time = time.replace(minute=0, second=0, microsecond=0)

    return time



if __name__ == '__main__':
    import logger

    log = logger.get_logger('Utility_test')

    format = '%Y-%m-%d'
    test_dates = ['2020-01-08', datetime.date.today().strftime(format)]

    for test_date in test_dates:
        log.info('Date: {}'.format(test_date))
        log.info('Day of week: {}'.format(day_of_week(test_date, format)))

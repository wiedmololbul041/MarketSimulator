import logger
from DataParser import DataParser, StockQuote
import datetime
from Consts import *

log = logger.get_logger('MarketSimulator')

buy_time = datetime.datetime.strptime('19:00:00', time_format).time()
sell_time = datetime.datetime.strptime('21:00:00', time_format).time()


class MarketSimulator:
    def __init__(self, tickets, start='2019-08-01', interval='1h'):
        self.tickets = tickets
        self.start = start
        self.interval = interval

        self.dp = DataParser(tickets, start=self.start, interval=self.interval)

        self.dp.download_data()
        self.dp.parse_to_week_data()

        self.data = self.dp.week_data

        self.budget = 10000.0

        self.start_budget = None
        self.initial_buy_date = None
        self.buy_n = None
        self.sell_n = None
        self.stop_budget = None

        self.market_first_price = None
        self.market_money = None
        self.market_stock_n = None
        self.market_last_price = None
        self.market_stop_budget = None

        self.buy_day = None
        self.sell_day = None

    def buy_day_sell_day(self, buy_day, sell_day, buy_time, sell_time, buy_strategy='max', budget=None):
        money = budget if budget else self.budget
        assets_money = 0
        stock_n = 0
        buy_n = 0
        sell_n = 0

        self.start_budget = money

        for quote in self.data:
            # log.debug(quote)
            assets_money = stock_n * quote.High
            if money + assets_money < quote.High:
                log.info("Jesteś bankrutem!!!")
                break

            # sprzedaż
            if stock_n > 0 and quote.Weekday == sell_day and quote.Hour == sell_time:
                value = stock_n * quote.High
                money += value
                assets_money -= value
                # log.info('[{}] Sprzedano {} po {:.2f} o wartości {:.2f}. Konto: {:.2f}, aktywa: {:.2f}. Razem: {:.2f}'
                #          .format(quote.Date, stock_n, quote.High, stock_n * quote.High, money, assets_money, money + assets_money))
                sell_n += 1
                stock_n = 0

            # kupno
            if money > 0 and quote.Weekday == buy_day and quote.Hour == buy_time:
                n = money // quote.High
                stock_n += n
                value = (quote.High * n)
                money -= value
                assets_money += value
                # log.info('[{}] Kupiono {} po {:.2f} o wartości {:.2f}. Konto: {:.2f}, aktywa: {:.2f}. Razem: {:.2f}'
                #          .format(quote.Date, stock_n, quote.High, stock_n * quote.High, money, assets_money, money + assets_money))

                if buy_n == 0:
                    self.initial_buy_date = quote.Date

                    self.market_first_price = quote.High
                    self.market_stock_n = stock_n
                    self.market_money = money
                buy_n += 1

        self.sell_n = sell_n
        self.buy_n = buy_n
        self.stop_budget = money + assets_money
        self.market_stop_budget = self.market_stock_n * quote.High

        self.buy_day = buy_day
        self.sell_day = sell_day

    def summary(self, brief=True, sh=None):
        if sh:
            log.addHandler(sh)
        log.info('-'.center(30, '-'))
        log.info(' Summary '.center(30, '-'))
        log.info('Początkowa kwota: {:.2f}'.format(self.start_budget))
        log.info('Końcowa kwota: {:.2f}'.format(self.stop_budget))
        if not brief:
            log.info('Ilość zrealizowanych zleceń kupna: {}'.format(self.buy_n))
            log.info('Ilość zrealizowanych zleceń sprzedaży: {}'.format(self.sell_n))
            log.info('Data pierwszego zakupu: {}'.format(self.initial_buy_date))
            log.info('Dzień zakupu: {}'.format(self.buy_day))
            log.info('Dzień sprzedaży: {}'.format(self.sell_day))
        log.info('-'.center(30, '-'))
        log.info(' Rynek '.center(30, '-'))
        if not brief:
            log.info('Początkowa kwota: {:.2f}'.format(self.start_budget))
        log.info('Końcowa kwota: {:.2f}\n'.format(self.market_stop_budget))

        if sh:
            log.removeHandler(sh)


if __name__ == '__main__':
    ms = MarketSimulator('MSFT', start='2019-01-01')

    import logging
    fh = logging.FileHandler('result.txt', mode='a')
    ms.buy_day_sell_day(Weekday.Monday, Weekday.Thursday, buy_time, sell_time)
    ms.summary(fh)

    ms.buy_day_sell_day(Weekday.Tuesday, Weekday.Thursday, buy_time, sell_time)
    ms.summary(fh)

    ms.buy_day_sell_day(Weekday.Wednesday, Weekday.Thursday, buy_time, sell_time)
    ms.summary(fh)

    ms.buy_day_sell_day(Weekday.Thursday, Weekday.Thursday, buy_time, sell_time)
    ms.summary(fh)

    ms.buy_day_sell_day(Weekday.Friday, Weekday.Thursday, buy_time, sell_time)
    ms.summary(fh)

import yfinance as yf
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf
import logger

log = logger.get_logger('StockLog')


if __name__ == "__main__":
    log.debug('Start')

    # yf.pdr_override()  # <== that's all it takes :-)

    # download dataframe using pandas_datareader
    # msft = pdr.get_data_yahoo("MSFT", start="2017-01-01")

    msft = yf.Ticker("MSFT")
    print(msft)

    print(msft.info)

    data = msft.history(start="2019-11-01", end="2020-02-08", interval='1h')
    # log_obj(data)

    # data.hist(column='High',bins=25, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
    log_obj(data['High'])
    high_hist = data['High'].hist(bins=10)
    log_obj(high_hist)
    high_hist.set_title('Czy widać?')
    high_hist.plot()
    # plt.show()

    for x in data['High'].iteritems():
        print(x)


    log.debug('Stop')



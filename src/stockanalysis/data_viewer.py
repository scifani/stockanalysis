import logging
import mplfinance as mpf


class DataViewer:
    def __init__(self):
        logging.debug("DataViewer::__init__")


    def candle_plot(self, df):
        mpf.plot(df, type='candle', volume=True, style='yahoo')  #, figscale=4, figratio=(7.00,3.75)


import pytest
import os
import pandas

from ..data_viewer import DataViewer


def test_candle_plot():

    base_path = os.path.dirname(os.path.realpath(__file__))
    csv_file = os.path.join(base_path, "data/ISP.MI_2020-10-16.csv")

    df = pandas.read_csv(csv_file, parse_dates=True, index_col='Date')

    dv = DataViewer()
    dv.candle_plot(df)
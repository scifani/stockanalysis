import pytest
import os

from ..data_collector import DataCollector

def test_get_history():
    dc = DataCollector()
    data = dc.get_ticker_history("ISP.MI")

    assert data is not None
    assert data.shape[0] > 0
    assert data.shape[1] == 1


def test_load_csv():
    base_path = os.path.dirname(os.path.realpath(__file__))
    csv_file = os.path.join(base_path, "data/ISP.MI_2020-10-16.csv")

    dc = DataCollector()
    data = dc.load_csv(csv_file)

    assert data is not None
    assert data.shape[0] > 0
    assert data.shape[1] == 1


def test_get_info():
    dc = DataCollector()
    info = dc.get_ticker_info("ISP.MI")

    assert info is not None
    assert info["longName"] is not None    

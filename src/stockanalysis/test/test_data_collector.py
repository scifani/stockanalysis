from ..data_collector import DataCollector

def test_data_collector_1():
    dc = DataCollector()
    data = dc.get_ticker_history("ISP.MI")

    assert data is not None
    assert data.shape[0] > 0
    assert data.shape[1] == 1

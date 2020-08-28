from ..data_preprocessor import DataPreprocessor
import numpy as np


def test_data_preprocessor_normalize():

    array = np.array([[0.0],[1.0],[2.0],[3.0],[4.0],[5.0],[6.0],[7.0],[8.0],[9.0],[10.0]])
    array_exp = np.array([[0.0],[0.1],[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9],[1.0]])

    dp = DataPreprocessor()
    array_norm = dp.normalize(array)
    
    assert len(array_norm) == len(array)
    assert np.array_equal(array_norm, array_exp) 

def test_data_preprocessor_norm_denorm():

    array = np.array([[0.0],[1.0],[2.0],[3.0],[4.0],[5.0],[6.0],[7.0],[8.0],[9.0],[10.0]])    

    dump_file = '/tmp/scaler.json'

    dp = DataPreprocessor()
    array_norm = dp.normalize(array, dump_file)
    
    array_denorm = dp.denormalize(array_norm, dump_file)

    assert np.array_equal(array, array_denorm)

def test_data_preprocessor_split():

    array = np.array([[30.0],[30.0],[29.0],[30.0],[29.0],[21.0],[22.0],[23.0],[24.0],[25.0],[15.0],[19.0],[22.0],[30.0],[27.0],[21.0],[25.0],[23.0],[24.0],[25.0],[32.0]])

    look_back = 2
    forward_days = 2
    train_set_ratio = 0.7

    dp = DataPreprocessor()
    array_train, array_test = dp.split(array, train_set_ratio, forward_days, look_back)
    
    assert len(array_train) == 14
    assert len(array_test) == (len(array) - len(array_train) + look_back)
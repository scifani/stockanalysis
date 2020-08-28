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

    dp = DataPreprocessor(look_back=2, forward=2)
    array_train, array_test = dp.split(array, train_set_ratio=0.7)
    
    assert len(array_train) == 14
    assert len(array_test) == (len(array) - len(array_train) + dp.look_back)

def test_data_preprocessor_to_matrices():

    array = np.array([[0.0],[1.0],[2.0],[3.0],[4.0],[5.0],[6.0],[7.0],[8.0],[9.0],[10.0],[11.0],[12.0],[13.0],[14.0],[15.0],[16.0],[17.0],[18.0],[19.0],[20.0]])

    look_back_ = 3
    forward_ = 2
    step_ = 2

    blocks = int((len(array) - (look_back_ + forward_)) / step_) + 1

    dp = DataPreprocessor(look_back=look_back_, forward=forward_)
    X, Y = dp.array_to_matrices(array, step=step_)

    assert X.shape == (blocks, look_back_, 1)
    assert Y.shape == (blocks, forward_)
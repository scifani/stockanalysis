import logging
import json
import numpy as np

class DataPreprocessor:
    def __init__(self):
        logging.debug("DataPreprocessor::__init__")

    def normalize(self, array, dump_file=None):
        '''
            Applies minmax normalization to the input data array

            array: the input numpy array
            dump_file: the file path where the scale factors will be saved          
        '''

        min_value = np.min(array)
        max_value = np.max(array)
         
        array_norm = (array - min_value) / (max_value - min_value)

        if dump_file is not None:
            json.dump({'min_value' : min_value, 'max_value' : max_value}, open(dump_file, 'w'))

        return array_norm


    def denormalize(self, array, dump_file):
        '''
            Rescale an input minmax normalized data array using the provided scale factors

            array: the input numpy array
            dump_file: the json file containing the scale factors - e.g. {'min_value' : 0.01, 'max_value' : 99.9}
        '''

        scl = json.load(open(dump_file, 'rb'))
        min_value = scl['min_value']
        max_value = scl['max_value']

        array_denorm = (array + min_value) * (max_value - min_value)

        return array_denorm

    
    def split(self, array, train_set_ratio, forward_samples, look_back_samples):
        '''
            Splits the input data array in two arrays, one for training and one for testing

            array: the input numpy array
            train_set_ratio: number of training samples w.r.t. data set (eg. 0.7)
            forward_samples: the n samples ahead to predict
            look_back_samples: the m past observed samples            
        '''

        if train_set_ratio < 0 or train_set_ratio > 1:
            raise Exception('train_set_ratio must be comprised between 0 and 1')
        
        num_train_samples = int((len(array) * train_set_ratio) / forward_samples) * forward_samples
        
        array_train = array[:num_train_samples]
        array_test = array[num_train_samples-look_back_samples:]                

        return array_train, array_test




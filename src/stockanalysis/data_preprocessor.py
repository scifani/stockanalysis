import logging
import json
import numpy as np

class DataPreprocessor:
    def __init__(self, look_back=0, forward=0):
        logging.debug("DataPreprocessor::__init__")
        '''
            forward: the n samples ahead to predict
            look_back: the m past observed samples
        '''
        self.look_back = look_back
        self.forward = forward
        self.min_value = 0
        self.max_value = 0

    def normalize(self, array, dump_file=None):
        '''
            Applies minmax normalization to the input data array

            array: the input numpy array
            dump_file: the file path where the scale factors will be saved          
        '''

        self.min_value = np.min(array)
        self.max_value = np.max(array)
         
        array_norm = (array - self.min_value) / (self.max_value - self.min_value)

        if dump_file is not None:
            json.dump({'min_value' : self.min_value, 'max_value' : self.max_value}, open(dump_file, 'w'))

        return array_norm


    def denormalize(self, array, dump_file):
        '''
            Rescale an input minmax normalized data array using the provided scale factors

            array: the input numpy array
            dump_file: the json file containing the scale factors - e.g. {'min_value' : 0.01, 'max_value' : 99.9}
        '''

        if dump_file is not None:
            jsn = json.load(open(dump_file, 'rb'))
            self.min_value = jsn['min_value']
            self.max_value = jsn['max_value']

        array_denorm = (array + self.min_value) * (self.max_value - self.min_value)

        return array_denorm

    
    def split(self, array, train_set_ratio):
        '''
            Splits the input data array in two arrays, one for training and one for testing

            array: the input numpy array
            train_set_ratio: number of training samples w.r.t. data set (eg. 0.7)           
        '''

        if train_set_ratio < 0 or train_set_ratio > 1:
            raise Exception('train_set_ratio must be comprised between 0 and 1')

        num_train_samples = int((len(array) * train_set_ratio) / self.forward) * self.forward
        
        array_train = array[:num_train_samples]
        array_test = array[num_train_samples - self.look_back:]                

        return array_train, array_test


    def array_to_matrices(self, array, step=1):
        '''
            Given an input array returns two matrices, X and Y, 
            where the i-th row of X is the i-th look_back period 
            and the i-th row of Y is the corresponding forward samples

            array: the input numpy array
            step: number of samples to move ahead at each iteration
        '''
                       
        end = len(array) - (self.look_back + self.forward) + 1

        X,Y = [],[]
        for i in range(0, end, step):
            X.append(array[i:(i+self.look_back)])
            Y.append(array[(i+self.look_back):(i+self.look_back+self.forward)])

        X = np.array(X)        
        Y = np.array([list(a.ravel()) for a in Y]) # transform Y from (n, m, 1) to (n, m)

        return X,Y
import logging

from keras.models import Sequential
from keras.layers import LSTM,Dense


class DataModel:
    def __init__(self, num_neurons, look_back, forward):
        logging.debug("DataModel::__init__")
        '''
            num_neurons: list containing the number of neurons for each layer
            look_back: the m past observed samples 
            forward: the n samples ahead to predict
        '''
        self.model = Sequential()

        for i in range(len(num_neurons)):
            if i == 0:
                self.model.add(LSTM(num_neurons[0],input_shape=(1, look_back), return_sequences=True))
            else:
                self.model.add(LSTM(num_neurons[i],input_shape=(num_neurons[i-1],1)))

        self.model.add(Dense(forward))
        self.model.compile(loss='mean_squared_error', optimizer='adam')


    def train(self, epochs, batch_size, X_train, y_train, X_validate=None, y_validate=None, weights_file=None):
        
        history = None
        try:
            valid_data = None
            if X_validate is not None and y_validate is not None:
                valid_data = (X_validate, y_validate)

            history = self.model.fit(X_train,y_train,epochs=epochs,validation_data=valid_data,
                                    shuffle=True,batch_size=batch_size, verbose=2)

            if weights_file is not None:
                self.model.save_weights(weights_file)

            rc = 0
        except Exception as e:
            logging.error(e)
            rc = -1
        
        return rc, history


    def predict(self, X):        

        y_hat = self.model.predict(X)
        #y_hat = y_hat.reshape(-1, 1)

        return y_hat

    
    def load_weights(self, weights_file):
        self.model.load_weights(weights_file)
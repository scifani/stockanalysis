import logging

from keras.models import Sequential
from keras.layers import LSTM,Dense

class DataLstm:
    def __init__(self, layers, num_neurons, X_len, Y_len):
        logging.debug("DataLstm::__init__")
        '''
            layers: the number of Sequential layers which constitutes the LSTM 
                    (excluded the last Dense layer)
            num_neurons: the number of neurons for each layer
            look_back:             
        '''
        self.model = Sequential()

        for i in range(num_neurons):
            if i == 0:
                self.model.add(LSTM(num_neurons[0],input_shape=(X_len,1), return_sequences=True))
            else:
                self.model.add(LSTM(num_neurons[i],input_shape=(num_neurons[i-1],1)))

        self.model.add(Dense(Y_len))
        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def train(self, epochs, X_train, y_train, X_validate, y_validate):
        history = self.model.fit(X_train,y_train,epochs=epochs,validation_data=(X_validate,y_validate),shuffle=True,batch_size=2, verbose=2)
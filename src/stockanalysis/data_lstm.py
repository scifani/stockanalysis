import logging

from keras.models import Sequential
from keras.layers import LSTM,Dense

# The Long Short-Term Memory network, or LSTM network, is a recurrent neural network that is trained 
# using Backpropagation Through Time and overcomes the vanishing gradient problem.
# Instead of neurons, LSTM networks have memory blocks that are connected through layers.
# A block contains gates that manage the block’s state and output.
# A block operates upon an input sequence and each gate within a block uses the sigmoid activation  
# units to control whether they are triggered or not, making the change of state and addition of  
# information flowing through the block conditional.
# There are three types of gates within a unit:
#  - Forget Gate: conditionally decides what information to throw away from the block.
#  - Input Gate: conditionally decides which values from the input to update the memory state.
#  - Output Gate: conditionally decides what to output based on input and the memory of the block.
# Each unit is like a mini-state machine where the gates of the units have weights that are learned 
# during the training procedure.


class DataLstm:
    def __init__(self, num_neurons, look_back, forward):
        logging.debug("DataLstm::__init__")
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

    def train(self, epochs, batch_size, X_train, y_train, X_validate=None, y_validate=None):
        
        valid_data = None
        if X_validate is not None and y_validate is not None:
            valid_data = (X_validate, y_validate)

        history = self.model.fit(X_train,y_train,epochs=epochs,validation_data=valid_data,
                                shuffle=True,batch_size=batch_size, verbose=2)
        
        return history

    def predict(self, x):
        y = self.model.predict(x)
        return y.reshape(-1, 1)

    
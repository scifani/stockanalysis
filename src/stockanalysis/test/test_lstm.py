
# References:
# - https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/


import os
import numpy
import matplotlib.pyplot as plt
import pandas
import math
from sklearn.metrics import mean_squared_error

from ..data_preprocessor import DataPreprocessor
from ..data_lstm import DataLstm

base_path = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(base_path,'data/airline-passengers.csv')

# Dataset sample:
#---------------------
# "Month","Passengers"
# "1949-01",112
# "1949-02",118
# "1949-03",132

def test_lstm():
    df = pandas.read_csv(data_file)

    dataset = df['Passengers'].values
    dataset = dataset.astype('float32')

    # fix random seed for reproducibility
    numpy.random.seed(7)

    look_back = 1
    forward = 1

    # normalize the data set
    data_preprocessor = DataPreprocessor(look_back, forward)
    dataset = data_preprocessor.normalize(dataset)

    # split into train and test sets    
    train, test = data_preprocessor.split(dataset, train_set_ratio=0.67)

    trainX, trainY = data_preprocessor.create_dataset(train)
    testX, testY = data_preprocessor.create_dataset(test)

    data_lstm = DataLstm(num_neurons=[4], look_back=look_back, forward=forward)
    hist = data_lstm.train(epochs=100, batch_size=1, X_train=trainX, y_train=trainY)
    print(hist)

    trainPredict = data_lstm.predict(trainX)
    testPredict = data_lstm.predict(testX)
    # invert predictions
    trainPredict = data_preprocessor.denormalize(trainPredict)
    trainY = data_preprocessor.denormalize(trainY)
    testPredict = data_preprocessor.denormalize(testPredict)
    testY = data_preprocessor.denormalize(testY)
    # calculate root mean squared error    
    trainScore = math.sqrt(mean_squared_error(trainY, trainPredict[:,0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY, testPredict[:,0]))
    print('Test Score: %.2f RMSE' % (testScore))

    assert trainScore < 25
    assert testScore < 55

    # Because of how the dataset was prepared, we must shift the predictions so that they 
    # align on the x-axis with the original dataset. Once prepared, the data is plotted, 
    # showing the original dataset in blue, the predictions for the training dataset in 
    # green, and the predictions on the unseen test dataset in red.
    #
    # shift train predictions for plotting
    trainPredictPlot = numpy.empty_like(dataset.reshape(-1, 1))
    trainPredictPlot[:] = numpy.nan
    trainPredictPlot[look_back:len(trainPredict)+look_back] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = numpy.empty_like(dataset.reshape(-1, 1))
    testPredictPlot[:] = numpy.nan
    testPredictPlot[len(trainPredict)+1:len(dataset)] = testPredict
    # plot baseline and predictions
    plt.plot(data_preprocessor.denormalize(dataset))
    plt.plot(trainPredictPlot)
    plt.plot(testPredictPlot)
    plt.show()
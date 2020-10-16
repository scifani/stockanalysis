#
# References:
# - https://medium.com/neuronio/predicting-stock-prices-with-lstm-349f5a0974d4


import pytest
import os
import numpy as np
import sklearn.model_selection
from datetime import datetime
from ..data_collector import DataCollector
from ..data_preprocessor import DataPreprocessor
from ..data_model import DataModel
import matplotlib.pyplot as plt

def test_single_ticker_prediction():

    base_path = os.path.dirname(os.path.realpath(__file__))
    csv_file = os.path.join(base_path, "data/ISP.MI_2020-10-16.csv")
    weights_file = os.path.join(base_path,"data/ISP.MI_2020-10-16.h5")

    look_back = 40         # the m past observed days (input)
    forward = 10           # the n days ahead to predict (output)
    train_set_ratio = 0.8  # data set is split in train and test set. Train set will take the 80% of total data
    valid_set_ratio = 0.2  # train set is split in train and validation set.
    neurons = [50, 30]
    epochs = 50
    
    dc = DataCollector()
    data = dc.load_csv(csv_file)

    dp = DataPreprocessor(look_back, forward)
    data_norm = dp.normalize(data)
    array_train, array_test = dp.split(data_norm, train_set_ratio)
    X_train, y_train = dp.create_dataset(array_train)
    X_test,  y_test  = dp.create_dataset(array_test)

    X_train, X_validate, y_train, y_validate = sklearn.model_selection.train_test_split(X_train, y_train, test_size=valid_set_ratio, random_state=42)

    print(f"X_train.shape    = {X_train.shape}")
    print(f"X_validate.shape = {X_validate.shape}")
    print(f"X_test.shape     = {X_test.shape}")
    print(f"y_train.shape    = {y_train.shape}")
    print(f"y_validate.shape = {y_validate.shape}")
    print(f"y_test.shape     = {y_test.shape}")

    model = DataModel(neurons, look_back, forward)
    #rc, _ = model.train(epochs=epochs, batch_size=2, X_train=X_train, y_train=y_train, X_validate=X_validate, y_validate=y_validate, weights_file=weights_file)
    # assert rc == 0
    model.load_weights(weights_file)
    Y_test_pred = model.predict(X_test)


    fig1, ax1 = plt.subplots()
    ax1.plot(data)

    fig2, ax2 = plt.subplots()
    yyy=[]
    for i in range(len(Y_test_pred)):        
        y_tmp = dp.denormalize(Y_test_pred[i].reshape(-1,1))    
        yyy.append(np.mean(y_tmp))
        
    ax2.plot(yyy, color='r', label='Prediction')    
    y_ref = dp.denormalize(array_test.reshape(-1,1))
    ax2.plot(y_ref[look_back:], label='Target')
    ax2.legend(loc='best')

    plt.show()

#
# References:
# - https://medium.com/neuronio/predicting-stock-prices-with-lstm-349f5a0974d4

import matplotlib.pyplot as plt
import numpy as np
from data_collector import DataCollector
from data_preprocessor import DataPreprocessor

ticker_name = "ISP.MI"

dc = DataCollector()
data = dc.get_ticker_history(ticker_name)

#plt.plot(data)
#plt.show()


# We want to predict the n days ahead (foward) having as input the m past observed days (look_back).
dp = DataPreprocessor(look_back=40, forward=10)
data_norm = dp.normalize(data, 'scaler.json')

# We will split the data in Train and Test. Train set will take the 80% of total data.
array_train, array_test = dp.split(data_norm, train_set_ratio=0.8)

# Split arrays in matrices to be fed to tensorflow
X, y = dp.array_to_matrices(array_train)
X_test, y_test = dp.array_to_matrices(array_test)

from sklearn.model_selection import train_test_split
X_train, X_validate, y_train, y_validate = train_test_split(X, y, test_size=0.20, random_state=42)

print(f"X_train.shape    = {X_train.shape}")
print(f"X_validate.shape = {X_validate.shape}")
print(f"X_test.shape     = {X_test.shape}")
print(f"y_train.shape    = {y_train.shape}")
print(f"y_validate.shape = {y_validate.shape}")
print(f"y_test.shape     = {y_test.shape}")

NUM_NEURONS_FirstLayer = 50
NUM_NEURONS_SecondLayer = 30
EPOCHS = 50

#Build the model
model = Sequential()
model.add(LSTM(NUM_NEURONS_FirstLayer,input_shape=(look_back,1), return_sequences=True))
model.add(LSTM(NUM_NEURONS_SecondLayer,input_shape=(NUM_NEURONS_FirstLayer,1)))
model.add(Dense(forward_days))
model.compile(loss='mean_squared_error', optimizer='adam')

history = model.fit(X_train,y_train,epochs=EPOCHS,validation_data=(X_validate,y_validate),shuffle=True,batch_size=2, verbose=2)

Xt = model.predict(X_test)

plt.figure(figsize = (15,10))

for i in range(0,len(Xt)):
    plt.plot([x + i*forward_days for x in range(len(Xt[i]))], scl.inverse_transform(Xt[i].reshape(-1,1)), color='r')
    
plt.plot(0, scl.inverse_transform(Xt[i].reshape(-1,1))[0], color='r', label='Prediction') #only to place the label
    
plt.plot(scl.inverse_transform(y_test.reshape(-1,1)), label='Target')
plt.legend(loc='best')
plt.show()
# The Recurring Neural Network Model to predict expected gear bearing temperature is developed
#The data used in the training, testing and validating is from the turbine data collected with no failures.

# Import necessary libraries
import random
random.seed(123)
import numpy as np  
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler

#import tensorflow as tf
from keras.layers import Dense,LSTM,Dropout,GRU,Masking,BatchNormalization, Activation
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import losses, optimizers, metrics

#Converting csv to dataframe for using it in neural network model
import pandas as pd
import io
path = r'C:\SEP Project'
df = pd.read_csv(path+'\m1_clean.csv')
#df = pd.DataFrame(df)
data = df.copy()
data = data.rename(columns={'GearBearingTemperature':'GearOilTemperature'})

df.shape

# Changing datatypes
for col in data.columns[~data.columns.isin(['Time'])]:
    data[col] = data[col].astype('float32')

# Delete rows which contain all 0's
data = data.loc[~(data==0).all(axis=1)]

# Split data into train and test set

train_size = 0.8 # Use 80 % of the data as the train set
val_size = 0.1 #10% of the data for validation
test_size = 0.1 #10% of the data for testing
# Split train & test
split_index_val = int((data.shape[0]*train_size)) # the index at which to split df into train and validation
split_index_test = int((data.shape[0]*train_size+val_size)) # the index at which to split df into validation and testing
X = data.drop(['Time','GearOilTemperature'],axis=1)
y = data[['GearOilTemperature']]

X.max()

y.max()

# The DataFrame data is converted to a NumPy array by doing data.values.
X_train = X.values[:split_index_val]
X_val = X.values[split_index_val:split_index_test]
X_test = X.values[split_index_test:]

y_train = y.values[:split_index_val]
y_val = y.values[split_index_val:split_index_test]
y_test = y.values[split_index_test:]


# Feature Scaling 
scalerX = MaxAbsScaler().fit(X_train)
scalery = MaxAbsScaler().fit(y_train)
X_train = scalerX.transform(X_train)
y_train = scalery.transform(y_train)
X_val = scalerX.transform(X_val)
y_val = scalery.transform(y_val)

# horizontally stack columns of training set
dataset = np.hstack((X_train,y_train))
#dataset = dataset[:-57, :]
dataset.shape

# horizontally stack columns of validation set
val_dataset = np.hstack((X_val,y_val))
#val_dataset = val_dataset[:-87, :]
val_dataset.shape

X_val

X_train.shape

X_val.shape

y_train.shape

y_val.shape

# Convert into supervised learning problem
def split_sequences(sequences, n_steps):
	X, y = list(), list()
	for i in range(len(sequences)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the dataset
		if end_ix > len(sequences):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, [5]]
		X.append(seq_x)
		y.append(seq_y)
	return np.array(X),np.array(y)
print(X.shape, y.shape)

# Network Optimizer (Lookbacks and batch size)
n_steps = 1
n_features = 5
batch_size  = 144
# convert into input/output of training set
X_train, y_train = split_sequences(dataset, n_steps)
# Change the length of X_train and y_train to be divisible by the batch_size
X_train = X_train[0:int(np.floor(len(X_train)/batch_size)*batch_size)]
y_train = y_train[0:int(np.floor(len(y_train)/batch_size)*batch_size)]


print(X_train.shape, y_train.shape)

# convert into input/output of validation set
X_val, y_val = split_sequences(val_dataset, n_steps)
# Change the length of X_val and y_val to be divisible by the batch_size
X_val = X_val[0:int(np.floor(len(X_val)/batch_size)*batch_size)]
y_val = y_val[0:int(np.floor(len(y_val)/batch_size)*batch_size)]
print(X_val.shape, y_val.shape)

# Priniting input/output sequence for RNN training
for i in range(len(X_train)):
	print(X_train[i], y_train[i])

# Priniting input/output sequence for RNN validation
for i in range(len(X_val)):
  print(X_val[i], y_val[i])

"""# Model Architecture and Training"""

# Define Recurring Neural Network model - baseline model
model = Sequential()
#model.add(Masking(mask_value=0., input_shape=(n_steps, n_features),
                 # batch_input_shape=(batch_size, n_steps, n_features)))

model.add(GRU(10, input_shape=(n_steps, n_features), return_sequences=True,
              kernel_initializer='glorot_uniform', recurrent_dropout=0.3, 
              stateful=True, batch_input_shape=(batch_size, n_steps, n_features)))
model.add(Activation('relu'))

model.add(GRU(5, kernel_initializer='glorot_uniform', recurrent_dropout=0.1, stateful=True)) 
model.add(Activation('relu'))

model.add(Dense(1))
model.add(Activation('linear'))

optimizer = optimizers.adam(lr=0.001)
model.compile(loss=losses.mean_squared_error, optimizer=optimizer,
              metrics=['mae'])
earlystopping=EarlyStopping(monitor='val_loss', patience=5, verbose=2,
                            mode='auto')

model.summary()

# Model Training
history = model.fit(X_train, y_train, batch_size=batch_size, epochs=1000, validation_data=(X_val, y_val), callbacks=[earlystopping],
          shuffle=False, verbose=2)
model.reset_states()

plt.figure(figsize=(16,10))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss', fontsize=18)
plt.ylabel('Mean Squared Error (Loss)', fontsize=18)
plt.xlabel('Epoch', fontsize=18)
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()

# Model Predict on test set

y_pred = model.predict(X_test, batch_size=batch_size)
y_pred.shape

y_pred

y_new_inverse = scalery.inverse_transform(y_pred)

y_new_inverse

y_real = scalery.inverse_transform(y_test)
y_real

for i in range(len(y_pred)):
	print(y_new_inverse[i])

for i in range(len(y_val)):
	print(y_real[i])

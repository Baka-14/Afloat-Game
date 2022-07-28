import tensorflow as tf
from tensorflow import keras 

model = keras.Sequential([
    keras.layers.Reshape(target_shape=(1*2), input_shape=(1,6)),
    keras.layers.Dense(units=256, activation='relu'),
    keras.layers.Dense(units=192, activation='relu'),
    keras.layers.Dense(units=10, activation='softmax')
])  


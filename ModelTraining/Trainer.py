import pickle
import keras
import os
import pandas as pd
import numpy as np
import tensorflow as tf
import keras.backend as kback
import keras.backend.tensorflow_backend as tfback
from keras.models import Model, Sequential
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from DataLoader import DataLoader

# backend.set_image_dim_ordering('th')

class Trainer:
	_DATA_FILENAME = 'data.csv'

	def __init__(self, epochs=10, batch_size=200, shuffle=True, verbose=1):
		tfback._get_available_gpus = self._get_available_gpus
		self.epochs = epochs
		self.batch_size = batch_size
		self.shuffle = shuffle
		self.verbose = verbose
		
		self.data = self._load_data()
		self.labels = self.data[['784']]
		self.data.drop(self.data.columns[[784]], axis = 1, inplace = True)

		#backend.set_image_dim_ordering('th')
		self.labels = np.array(self.labels)
		self.categorical = np_utils.to_categorical(self.labels)

		self._initialize_model()

	def _load_data(self) -> pd.DataFrame:
		if not os.path.exists(self._DATA_FILENAME):
			dataLoader = DataLoader('..\Dataset')
			return dataLoader.get_training_data(self._DATA_FILENAME)
		else:
			return pd.read_csv(self._DATA_FILENAME, index_col = False)

	def _get_available_gpus(self):
		"""Get a list of available gpu devices (formatted as strings).

		# Returns
			A list of available GPU devices.
		"""
		#global _LOCAL_DEVICES
		if tfback._LOCAL_DEVICES is None:
			devices = tf.config.list_logical_devices()
			tfback._LOCAL_DEVICES = [x.name for x in devices]
		return [x for x in tfback._LOCAL_DEVICES if 'device:gpu' in x.lower()]

	def _initialize_model(self):
		self.model = Sequential()
		#self.model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
		self.model.add(Conv2D(30, (3, 3), activation='relu', input_shape=(1,28,28), data_format='channels_first'))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Conv2D(15, (3,3), activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Dropout(0.2))
		self.model.add(Flatten())
		self.model.add(Dense(128, activation='relu'))
		self.model.add(Dense(50, activation='relu'))
		self.model.add(Dense(22, activation='softmax'))

		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	def train(self):
		l = []
		
		for i in range(0, 233913):
			l.append(np.array(self.data[i:i+1]).reshape(1, 28, 28))

		self.model.fit(np.array(l), self.categorical, epochs=self.epochs, batch_size=self.batch_size, shuffle=self.shuffle, verbose=self.verbose)

	def save_model(self, filename):
		model_json = self.model.to_json()
		with open(filename + ".json", "w") as json_file:
			json_file.write(model_json)
		self.model.save_weights(filename + ".h5")
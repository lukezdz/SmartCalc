import pickle
import os
import pandas as pd
import numpy as np
import tensorflow as tf
from DataLoader import DataLoader

# backend.set_image_dim_ordering('th')

class Trainer:
	_TRAINDATA_FILENAME = 'trainData.csv'
	_TESTDATA_FILENAME = 'testData.csv'

	def __init__(self, epochs=100, batch_size=200, shuffle=True, verbose=1):
		# tfback._get_available_gpus = self._get_available_gpus
		self.epochs = epochs
		self.batch_size = batch_size
		self.shuffle = shuffle
		self.verbose = verbose
		
		self._prepare_data()
		self._initialize_model()

	def _prepare_data(self):
		dataLoader = DataLoader('..\Dataset')

		self.train_data = dataLoader.get_training_data(self._TRAINDATA_FILENAME)
		self.train_labels = self.train_data[['784']]
		self.train_data.drop(self.train_data.columns[[784]], axis = 1, inplace = True)
		self.train_labels = np.array(self.train_labels)
		self.train_categories = tf.keras.utils.to_categorical(self.train_labels)
		
		self.test_data = dataLoader.get_test_data(self._TESTDATA_FILENAME)
		self.test_labels = self.test_data[['784']]
		self.test_data.drop(self.test_data.columns[[784]], axis = 1, inplace = True)
		self.test_labels = np.array(self.test_labels)
		self.test_categories = tf.keras.utils.to_categorical(self.test_labels)

	# fixes a bug in keras and tf 2.1
	def _get_available_gpus(self):
		"""Get a list of available gpu devices (formatted as strings).

		# Returns
			A list of available GPU devices.
		"""
		#global _LOCAL_DEVICES
		if tf.keras.backend._LOCAL_DEVICES is None:
			devices = tf.config.list_logical_devices()
			tfback._LOCAL_DEVICES = [x.name for x in devices]
		return [x for x in tf.keras.backend._LOCAL_DEVICES if 'device:gpu' in x.lower()]

	def _initialize_model(self):
		self.model = tf.keras.models.Sequential()
		self.model.add(tf.keras.layers.Conv2D(30, (3, 3), activation='relu', input_shape=(1,28,28), data_format='channels_first'))
		self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
		self.model.add(tf.keras.layers.Conv2D(15, (3,3), activation='relu'))
		self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
		self.model.add(tf.keras.layers.Dropout(0.2))
		self.model.add(tf.keras.layers.Flatten())
		self.model.add(tf.keras.layers.Dense(128, activation='relu'))
		self.model.add(tf.keras.layers.Dense(50, activation='relu'))
		self.model.add(tf.keras.layers.Dense(22, activation='softmax'))

		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	def train(self):
		l = []
		
		for i in range(0, self.train_data.shape[0]):
			l.append(np.array(self.train_data[i:i+1]).reshape(1, 28, 28))

		self.model.fit(
			np.array(l), 
			self.train_categories, 
			epochs=self.epochs, 
			batch_size=self.batch_size, 
			shuffle=self.shuffle, 
			verbose=self.verbose,
			validation_split=0.02,
			callbacks=[
				tf.keras.callbacks.EarlyStopping(patience=10),
				tf.keras.callbacks.ModelCheckpoint('model.hdf5', save_best_only=True)
			]
		)
		self.model = tf.keras.models.load_model('model.hdf5')

	def evaluate(self):
		l = []

		for i in range(0, self.test_data.shape[0]):
			l.append(np.array(self.test_data[i:i+1]).reshape(1, 28, 28))

		print("")
		print("Evaluating model with test data")
		loss_value, accuracy_value = self.model.evaluate(
			np.array(l),
			self.test_categories,
			batch_size=self.batch_size,
			verbose=self.verbose
		)

		print("Loss value: " + str(loss_value) + "; Accuracy: " + str(accuracy_value))
		return accuracy_value

	def save_model(self, filename):
		model_json = self.model.to_json()
		with open(filename + ".json", "w") as json_file:
			json_file.write(model_json)
		tf.keras.models.save_model(self.model, "model.hdf5")
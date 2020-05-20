import cv2
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot
from os import listdir
from os.path import isfile, join

class DataLoader:
	def __init__(self, dataset_root):
		self.dataset_root = dataset_root

	def load_images_from_folder(self, folder):
		folder_path = self.dataset_root + "\\" + folder
		train_data = []
		for filename in os.listdir(folder_path):
			image = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_GRAYSCALE)
			image = ~image
			if image is not None:
				ret, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
				contours, ret = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
				count = sorted(contours, key = lambda contour: cv2.boundingRect(contour)[0])
				width = 28
				height = 28
				maxi = 0

				for c in count:
					x, y, width, height = cv2.boundingRect(c)
					maxi = max(width*height, maxi)
					if maxi == width * height:
						x_max = x
						y_max = y
						width_max = width
						height_max = height
				im_crop = threshold[y_max : y_max + height_max + 10, x_max : x_max + width_max + 10]
				im_resize = cv2.resize(im_crop, (28, 28))
				im_resize = np.reshape(im_resize, (784, 1))
				train_data.append(im_resize)
		return train_data


	def get_training_data(self, filename) -> pd.DataFrame:
		output_configuration = [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9'], ['10'], ['11'], ['12'], ['13'], ['14'], ['15'], ['16'], ['17'], ['18'], ['19'], ['20'], ['21']]
		input_configuration = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', '+', '-', 'times', 'div', '=', '(', ')']

		print("Loading data from: " + input_configuration[0])
		data = self.load_images_from_folder(input_configuration[0])
		for i in range(0, len(data)):
			data[i] = np.append(data[i], output_configuration[0])

		for i in range(1, len(output_configuration)):
			print("Loading data from: " + input_configuration[i])
			temp_data = self.load_images_from_folder(input_configuration[i])
			for j in range(0, len(temp_data)):
				temp_data[j] = np.append(temp_data[j], output_configuration[i])
			data = np.concatenate((data, temp_data))

		dataFrame = pd.DataFrame(data, index=None)
		dataFrame.to_csv(filename, index=False)
		return dataFrame

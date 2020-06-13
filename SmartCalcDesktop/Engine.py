import keras
import keras.backend.tensorflow_backend as tfback
import tensorflow as tf
import numpy as np
import cv2
import random as rng

class Engine:
	def __init__(self):
		tfback._get_available_gpus = self._get_available_gpus
		self.model: keras.models.Sequential = keras.models.load_model("model.hdf5")
		self.character_map = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "+", "-", "*", "/", "=", "(", ")"]

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

	def handle_processing(self):
		if self.testing:
			src = cv2.imread("temp.jpg")
			if src is None:
				print('Could not open or find the image: temp.jpg')
				exit(0)
			# Convert image to gray and blur it
			src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
			self.src_gray = cv2.blur(src_gray, (3,3))
			source_window = 'Source'
			cv2.namedWindow(source_window)
			cv2.imshow(source_window, src)
			max_thresh = 255
			thresh = 100 # initial threshold
			cv2.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, self.thresh_callback)
			self.thresh_callback(thresh)
		else:
			image = cv2.imread("temp.jpg", cv2.IMREAD_GRAYSCALE)
			equation = self.get_equation(image)
			print(equation)

	def thresh_callback(self, val):
		threshold = val
		
		canny_output = cv2.Canny(self.src_gray, threshold, threshold * 2)
		
		
		contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		
		contours_poly = [None]*len(contours)
		boundRect = [None]*len(contours)
		centers = [None]*len(contours)
		radius = [None]*len(contours)
		for i, c in enumerate(contours):
			contours_poly[i] = cv2.approxPolyDP(c, 3, True)
			boundRect[i] = cv2.boundingRect(contours_poly[i])
			centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
		
		
		drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
		
		
		for i in range(len(contours)):
			color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
			cv2.drawContours(drawing, contours_poly, i, color)
			cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
			(int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
			cv2.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
		
		
		cv2.imshow('Contours', drawing)
		cv2.waitKey()

	def get_equation(self, image) -> str:
		image = ~image
		if image is None:
			return "error"
		
		ret, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
		contours, ret = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		# count = sorted(contours, key = lambda contour: cv2.boundingRect(contour)[0])
		rects = []
		for c in contours:
			rects.append(cv2.boundingRect(c))
		width = 28
		height = 28
		maxi = 0

		selected = []
		for r in rects:
			x, y, width, height = cv2.boundingRect(r)
			maxi = max(width*height, maxi)
			if maxi == width * height:
				x_max = x
				y_max = y
				width_max = width
				height_max = height
			im_crop = threshold[y_max : y_max + height_max + 10, x_max : x_max + width_max + 10]
			im_resize = cv2.resize(im_crop, (28, 28))	
			im_resize = np.reshape(im_resize, (784, 1))
			selected.append(im_resize)
		
		ans = ""
		for s in selected:
			ans += self.get_character(s)
		return ans
	
	def get_character(self, pixels_array) -> str:
		ans = self.model.predict(pixels_array)
		return self.character_map[ans]
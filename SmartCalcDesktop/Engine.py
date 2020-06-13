import keras
import keras.backend.tensorflow_backend as tfback
import tensorflow as tf
import numpy as np
import cv2
import random as rng

class Engine:
	def __init__(self):
		tfback._get_available_gpus = self._get_available_gpus
		self.testing = False
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
		image = cv2.imread("test_g.jpg", cv2.IMREAD_GRAYSCALE)
		equation = self.get_equation(image)
		print(equation)

	def get_equation(self):
		img = cv2.imread('testtest.png', cv2.IMREAD_GRAYSCALE)
		cv2.imshow('wo', img)
		cv2.waitKey()
		cv2.destroyAllWindows()

		if img is not None:
			img = ~img
			ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
			ctrs, ret = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
			w = 28
			h = 28
			train_data = []
			rects = []
			for c in cnt:
				x,y,w,h = cv2.boundingRect(c)
				rect = [x,y,w,h]
				rects.append(rect)
			bool_rect = []
			for r in rects:
				l = []
				for rec in rects:
					flag=0
					if rec!=r:
						if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
							flag=1
						l.append(flag)
					if rec == r:
						l.append(0)
				bool_rect.append(l)
			dump_rect = []
			for i in range(0, len(cnt)):
				for j in range(0, len(cnt)):
					if bool_rect[i][j] == 1:
						area1 = rects[i][2]*rects[i][3]
						area2 = rects[j][2]*rects[j][3]
						if (area1 == min(area1, area2)):
							dump_rect.append(rects[i])
			final_rect = [i for i in rects if i not in dump_rect]

			for r in final_rect:
				x=r[0]
				y=r[1]
				w=r[2]
				h=r[3]
				im_crop = thresh[y:y+h+10, x:x+w+10]

				im_resize = cv2.resize(im_crop, (28, 28))
				cv2.imshow('work', im_resize)
				cv2.waitKey()
				cv2.destroyAllWindows()

				im_resize = np.reshape(im_resize, (1,28,28))
				train_data.append(im_resize)

			ans = ""
			for i in range(len(train_data)):
				train_data[i] = np.array(train_data[i])
				train_data[i] = train_data[i].reshape(1,1,28,28)
				result = self.model.predict_classes(train_data[i])
				ans += self.character_map[result[0]]
			print(ans)


	# def get_equation(self, image) -> str:
	# 	image = ~image
	# 	if image is None:
	# 		return "error"
		
	# 	ret, thresholded = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
	# 	contours, ret = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	# 	#count = sorted(contours, key = lambda contour: cv2.boundingRect(contour)[0])
	# 	rects = []
	# 	for c in contours:
	# 		approximated = cv2.approxPolyDP(c, 3, False)
	# 		rects.append(cv2.boundingRect(c))
	# 	width = 28
	# 	height = 28
	# 	maxi = 0

	# 	selected = []
	# 	for r in rects:
	# 		# x, y, width, height = cv2.boundingRect(r)
	# 		x, y, width, height = r
	# 		maxi = max(width*height, maxi)
	# 		if maxi == width * height:
	# 			x_max = x
	# 			y_max = y
	# 			width_max = width
	# 			height_max = height
	# 		im_crop = thresholded[y_max : y_max + height_max + 10, x_max : x_max + width_max + 10]
	# 		im_resize = cv2.resize(im_crop, (28, 28))	
	# 		im_resize = np.reshape(im_resize, (784, 1))
	# 		im_resize = np.reshape(im_resize, (1, 28, 28))
	# 		selected.append(im_resize)
		
	# 	ans = ""
	# 	for s in selected:
	# 		ans += self.get_character(s)
	# 	return ans
	
	# def get_character(self, pixels_array) -> str:
	# 	ans = self.model.predict_classes(pixels_array)
	# 	return self.character_map[ans]
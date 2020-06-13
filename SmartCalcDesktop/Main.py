import cv2
import keras
import threading
from Engine import Engine
from Calc import Calc

engine = Engine()
equation = engine.get_equation()

cv2.waitKey()

# cv2.namedWindow("SmartCalcDesktop")
# vc = cv2.VideoCapture(0)

# if vc.isOpened(): # try to get the first frame
# 	rval, frame = vc.read()
# 	engine = Engine()
# else:
#     rval = False

# while rval:
#     cv2.imshow("SmartCalcDesktop", frame)
#     rval, frame = vc.read()
#     key = cv2.waitKey(20)
#     if key == 27:
#         break
#     if key == 32:
#         print("Starting processing")
#         cv2.imwrite("temp.jpg", frame)
#         processing_thread = threading.Thread(target=engine.handle_processing)
#         processing_thread.start()

# vc.release()
# cv2.destroyWindow("SmartCalcDesktop")
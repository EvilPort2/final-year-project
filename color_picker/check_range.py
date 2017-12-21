import cv2
import pickle
import numpy as np


def check_range():
	with open("range.pickle", "rb") as f:
		t = pickle.load(f)

	lower = np.array([t[0], t[1], t[2]])                       # HSV green lower
	upper = np.array([t[3], t[4], t[5]])                    # HSV green upper
	cam = cv2.VideoCapture(0)
	while True:
		img = cam.read()[1]
		img = cv2.flip(img, 1)
		imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(imgHSV, lower, upper)

		cv2.imshow("img", img)
		cv2.imshow("mask", mask)

		if cv2.waitKey(1) == ord('q'):
			break

	cam.release()
	cv2.destroyAllWindows()


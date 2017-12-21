import cv2
import pickle
import numpy as np
from .check_range import check_range

def color_picker():
	cam = cv2.VideoCapture(0)
	width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)	
	height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
	center = (int(width/2), int(height/2))
	point1 = (center[0]-30, center[1]-30)
	point2 = (center[0], center[1]-30)
	point3 = (center[0]+30, center[1]-30)
	point4 = (center[0]-30, center[1])
	point5 = (center[0]+30, center[1])
	point6 = (center[0]-30, center[1]+30)
	point7 = (center[0], center[1]+30)
	point8 = (center[0]+30, center[1]+30)

	countTotalFrames = 0
	countColorPickerFrames = 0
	flagCapturingColor = False
	flagDotDisplayed = False

	while True:
		img = cam.read()[1]
		img = cv2.flip(img, 1)
		imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		#imgHSV = cv2.medianBlur(imgHSV, 15)
		#imgHSV = cv2.GaussianBlur(imgHSV , (5,5), 0)

		colorHSV1 = np.int0(imgHSV[center])
		colorHSV2 = np.int0(imgHSV[point1])
		colorHSV3 = np.int0(imgHSV[point2])
		colorHSV4 = np.int0(imgHSV[point3])
		colorHSV5 = np.int0(imgHSV[point4])
		colorHSV6 = np.int0(imgHSV[point5])
		colorHSV7 = np.int0(imgHSV[point6])
		colorHSV8 = np.int0(imgHSV[point7])
		colorHSV9 = np.int0(imgHSV[point8])

		HSVColor = []

		if countTotalFrames >= 30 or flagDotDisplayed == True:
			cv2.circle(img, center, 2, (0, 255, 0), 2)
			cv2.circle(img, point1, 2, (0, 255, 0), 2)
			cv2.circle(img, point2, 2, (0, 255, 0), 2)
			cv2.circle(img, point3, 2, (0, 255, 0), 2)
			cv2.circle(img, point4, 2, (0, 255, 0), 2)
			cv2.circle(img, point5, 2, (0, 255, 0), 2)
			cv2.circle(img, point6, 2, (0, 255, 0), 2)
			cv2.circle(img, point7, 2, (0, 255, 0), 2)
			cv2.circle(img, point8, 2, (0, 255, 0), 2)
			countTotalFrames = 0
			flagDotDisplayed = True

		if cv2.waitKey(1) == ord('q'):
			break

		if cv2.waitKey(1) == ord('c') or flagCapturingColor == True:
			print(countColorPickerFrames)
			if countColorPickerFrames >= 50:
				HSVColor.append((colorHSV1 + colorHSV2 + colorHSV3 + colorHSV4 + colorHSV5 + colorHSV6 + colorHSV7 + colorHSV8 + colorHSV9) / 9 )
				avgHSVColor = sum(HSVColor)/len(HSVColor)
				avgBGRColor = cv2.cvtColor(np.uint8([[avgHSVColor]]), cv2.COLOR_HSV2BGR)
				avgBGRColor = (float(avgBGRColor[0][0][0]), float(avgBGRColor[0][0][1]), float(avgBGRColor[0][0][2]))
				print(avgBGRColor, avgHSVColor)
				cv2.circle(img, center, 2, avgBGRColor, 2)
				cv2.circle(img, point1, 2, avgBGRColor, 2)
				cv2.circle(img, point2, 2, avgBGRColor, 2)
				cv2.circle(img, point3, 2, avgBGRColor, 2)
				cv2.circle(img, point4, 2, avgBGRColor, 2)
				cv2.circle(img, point5, 2, avgBGRColor, 2)
				cv2.circle(img, point6, 2, avgBGRColor, 2)
				cv2.circle(img, point7, 2, avgBGRColor, 2)
				cv2.circle(img, point8, 2, avgBGRColor, 2)

				print(countColorPickerFrames)
			if countColorPickerFrames == 200:
				avgHSVColor = sum(HSVColor)/len(HSVColor)
				print(avgHSVColor, countColorPickerFrames)
			elif countColorPickerFrames > 200:
				print(avgHSVColor)
				colorRange = [avgHSVColor[0]-30, avgHSVColor[1]-50, avgHSVColor[2]-50, avgHSVColor[0]+30, avgHSVColor[1]+50, avgHSVColor[2]+50]
				for color in colorRange:
					if color < 0:
						colorRange[colorRange.index(color)] = 0
				with open("range.pickle", "wb") as f:
					pickle.dump(colorRange,f)
				break
			countColorPickerFrames += 1
			flagCapturingColor = True

		countTotalFrames += 1

		#cv2.imshow("imgHSV", imgHSV)
		cv2.imshow("img", img)
	cam.release()
	cv2.destroyAllWindows()

	check_range()
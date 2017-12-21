import cv2
import sqlite3
from face_recognition.py.database import getProfileDataById

def match_face(unlockFaceId):
	faceCascPath = "face_recognition/haarcascade_frontalface_default.xml"
	eyeCascadePath = "face_recognition/haarcascade_eye.xml"
	faceCascade = cv2.CascadeClassifier(faceCascPath)
	eyeCascade = cv2.CascadeClassifier(eyeCascadePath)

	cam = cv2.VideoCapture(0)
	recog = cv2.face.LBPHFaceRecognizer_create()
	recog.read('face_recognition/recognized/training.yml')

	faceId = 0
	matchFrameCount = 0
	flagFaceMatched = False

	while True:
		img = cam.read()[1]
		img = cv2.flip(img,1)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, 1.1, 5, flags = cv2.CASCADE_SCALE_IMAGE)
		for (x, y, w, h) in faces:
			face = gray[y:y+h, x:x+w]
			eyes = eyeCascade.detectMultiScale(face, 1.1, 5, flags = cv2.CASCADE_SCALE_IMAGE)
			if len(eyes) == 2:
				faceId, confidence = recog.predict(face)
				if confidence < 60:
					profile = getProfileDataById(str(faceId))
					name = profile[1]
					if unlockFaceId == faceId:
						matchFrameCount += 0.5
					else:
						matchFrameCount = 0
				else:
					name = "Unknown"
					matchFrameCount = 0
				cv2.rectangle(img, (x, y), (x + w, y + h), 2)
				cv2.putText(img, "Name- " + name, (x, y + h), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)

				matchFrameCountPercentage = int(matchFrameCount*100/10)
				if matchFrameCountPercentage <= 10:
					cv2.putText(img, "Matching... " + str(matchFrameCountPercentage) + "%", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)		#red
				elif matchFrameCountPercentage <= 20:
					cv2.putText(img, "Matching... " + str(matchFrameCountPercentage) + "%", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 165, 255), 2)	#orange
				elif matchFrameCountPercentage <= 60:
					cv2.putText(img, "Matching... " + str(matchFrameCountPercentage) + "%", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)	#yellow
				elif matchFrameCountPercentage <= 99:
					cv2.putText(img, "Matching... " + str(matchFrameCountPercentage) + "%", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (50, 205, 154), 2)	#lime green
				else:
					cv2.putText(img, "Matched " + str(matchFrameCountPercentage) + "%", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
					flagFaceMatched = True
					with open("match_face_result", "w") as f:
						f.write("True")
					break
				#print ("id = " + str(faceId) + " , confidence = " + str(confidence))
		
		if flagFaceMatched == True:
			break
		cv2.imshow("Face Recognition Running", img)
		cv2.waitKey(10)
	cam.release()
	cv2.destroyAllWindows()

	return flagFaceMatched
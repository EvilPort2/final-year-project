import os
from face_recognition.py.trainer import trainDetector
from face_recognition.py.recognize import faceRecognize
from face_recognition.py.datasetCreator import createDataset
from face_recognition.py.database import displayDbContent

def face_recognition_main():
	while True:
		if os.name == 'nt':
			os.system("cls")
		else:
			os.system("clear")

		print ("\t\tTrain Face Recognizer\n\t\t-------------\n")
		print ("CHOICES:\n\n1. Save a new face or Update an old face\n2. Train detector\n3. Detect and recognize "
			   "faces\n4. Display ID and other information of all the stored faces\n5. Clear "
			   "screen\n6. Back\n\n")
		while True:
			try:
				choice = int(input("Enter your choice: "))
			except KeyboardInterrupt:
				print("Exiting...")
				break
			except:
				continue
			if choice >= 1 and choice <= 6:
				break

		if choice == 1:
			createDataset()
			input("Dataset created successfully. Press ENTER to continue...")
		elif choice == 2:
			trainDetector()
			input("Detector is trained and is ready to detect and recognize stored faces. Press ENTER to continue...")
		elif choice == 3:
			print ("Press \'q\' to stop face recognition...")
			faceRecognize()
			input("Press ENTER to continue...")
		elif choice == 4:
			displayDbContent()
			input("Press ENTER to continue...")
		elif choice == 5:
			if os.name != 'nt':
				os.system("clear")
			else:
				os.system("cls")
		else:
			print ("Exiting...")
			break

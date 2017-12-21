import os
import sys
from gesture_recognition.gesture_action import gesture_action 
from color_picker.color_picker import color_picker
from face_recognition.faceRecognizeMain import face_recognition_main

def clear_screen():
	os.system("cls")

def show_settings():
	while True:
		clear_screen()
		print("\t\t\tSettings")
		print("\t\t\t--------")
		print("1. Set Color range (Automatic)")
		print("2. Set Color range (Manual)")
		print("3. Train the face recognizer")
		print("4. Back\n")
		choice = input("Choice: ")

		try:
			choice = int(choice)
		except KeyboardInterrupt:
			print("Exiting...")
			sys.exit()
		except:
			continue

		if choice < 1 or choice > 4:
			continue

		if choice == 1:
			# automatted color detection
			color_picker()
		elif choice == 2:
			os.system("python range-detector.py -f HSV -w")
		elif choice == 3:
			face_recognition_main()
		else:
			return




def main():
	while True:
		clear_screen()
		print("\t\t\tMAIN MENU")
		print("\t\t\t---------")
		print("1. Start")
		print("2. Settings")
		print("3. Exit\n")
		choice = input("Choice: ")

		try:
			choice = int(choice)
		except KeyboardInterrupt:
			print("Exiting...")
			sys.exit()
		except:
			continue

		if choice < 1 or choice > 3:
			continue

		# Start the gesture recognizer
		if choice == 1:
			gesture_action()

		elif choice == 2:
			show_settings()
			
		else:
			sys.exit()



main()
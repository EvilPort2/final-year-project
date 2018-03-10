import pyautogui as gui
import os
import time
import datetime
import cv2
import thread
from threading import Thread

class TakePhoto(Thread):
	def __init__(self, cam):
		Thread.__init__(self)
		self.cam = cam
		self.start()

	def run(self):
		cam = self.cam
		time.sleep(5)
		img1 = cam.read()[1]
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d %H_%M_%S')
		cv2.imwrite("photos/"+st + ".png", img1)

		
def take_photo(cam):
	cam.release()
	cam = cv2.VideoCapture(1)
	if cam.read()[0]==False:
		cam=cv2.VideoCapture(0)
	count_frames = 0
	while count_frames != 50:
		img = cam.read()[1]
		img = cv2.flip(img, 1)
		count_frames += 1
		cv2.waitKey(1)
		cv2.imshow("Taking a photo", img)
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d %H_%M_%S')
	cv2.imwrite("photos/"+st + ".png", img)
	cv2.destroyAllWindows()
	return cam

def screenshot(x = None):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d %H_%M_%S')
	gui.screenshot("screenshots/" + st + ".png")

def text_editor(x = None):
	Thread(target=os.system, args=("notepad", )).atart()

def start_menu(x = None):
	gui.press('winleft')

def new_file(x = None):
	gui.hotkey('ctrlleft', 'n')

def select_all(x = None):
	gui.hotkey('ctrlleft', 'a')

def close(x = None):
	gui.hotkey('altleft', 'f4')

def copy(x = None):
	gui.hotkey('ctrlleft', 'c')
	
def paste(x = None):
	gui.hotkey('ctrlleft', 'v')

def cut(x = None):
	gui.hotkey('ctrlleft', 'x')

def next_window(x = None):
	gui.hotkey('altleft', 'tab')

def prev_window(x = None):
	gui.hotkey('altleft', 'shiftleft', 'tab')

def maximize(x = None):
	gui.hotkey('winleft', 'up')

def minimize(x = None):
	gui.hotkey('winleft', 'down')

def lockscreen(cam):
	cam.release()
	os.system("python modules/face_lock_unlock/unlock_using_face.py")
	cam = cv2.VideoCapture(1)
	if cam.read()[0]==False:
		cam=cv2.VideoCapture(0)
	return cam

def start_keyboard(cam):
	from modules.virtual_keyboard.virtual_keyboard import start_keyboard
	cam.release()
	start_keyboard()
	cam = cv2.VideoCapture(1)
	if cam.read()[0]==False:
		cam=cv2.VideoCapture(0)
	return cam

def task_manager(x = None):
	gui.hotkey('ctrlleft', 'shiftleft', 'esc')

GEST_START = ("N", "E", "S", "W")
GEST_KEYBOARD = ("E", "S", "W", "N")
GEST_CLOSE = ("SE", "N", "SW")
GEST_COPY = ("W", "S", "E")
GEST_PASTE = ("SE", "NE")
GEST_CUT = ("SW", "N", "SE")
GEST_ALT_TAB = ("SE", "SW")
GEST_ALT_SHIFT_TAB = ("SW", "SE")
GEST_MAXIMIZE = ("N",)
GEST_MINIMIZE = ("S",)
GEST_LOCK = ("S", "E")
GEST_TASK_MANAGER = ("E", "W", "S")
GEST_NEW_FILE = ("N", "SE", "N")
GEST_SELECT_ALL = ("NE", "SE", "NW", "W")

GESTURES_ONE_HAND = \
{GEST_START: start_menu, 
GEST_CLOSE: close,
GEST_COPY: copy,
GEST_PASTE: paste,
GEST_CUT: cut,
GEST_ALT_TAB: next_window,
GEST_ALT_SHIFT_TAB: prev_window,
GEST_MAXIMIZE: maximize,
GEST_MINIMIZE: minimize,
GEST_LOCK: lockscreen,
GEST_TASK_MANAGER: task_manager,
GEST_NEW_FILE: new_file,
GEST_SELECT_ALL: select_all,
GEST_KEYBOARD: start_keyboard}


GEST_SCREENSHOT = (("W", "S", "E"), ("E", "S", "W"))
GEST_CAMERA = (("SW", "SE"), ("SE", "SW"))
GEST_TEXT_EDITOR = (("N", "E", "S", "W"), ("S",))

GESTURES_TWO_HAND = \
{GEST_SCREENSHOT: screenshot,
GEST_CAMERA: take_photo,
GEST_TEXT_EDITOR: text_editor}

def do_gesture_action(cam, gesture1, gesture2 = None):
	ret = None
	if gesture2 == None:
		if gesture1 in GESTURES_ONE_HAND.keys():
			ret = GESTURES_ONE_HAND[gesture1](cam)
	else:
		if (gesture1, gesture2) in GESTURES_TWO_HAND.keys():
			ret = GESTURES_TWO_HAND[(gesture1, gesture2)](cam)

	if ret != None:
		cam = ret

	return cam
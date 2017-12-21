import pygame, PyHook3, os
import time

def KeyboardMouseDisable(event):
	print("Keyboard and Mouse is disabled")
	return False

def KeyboardMouseEnable(event):
	print(event.Message)
	return True

hm = PyHook3.HookManager()
hm.KeyAll = KeyboardMouseDisable
hm.MouseAll = KeyboardMouseDisable
hm.HookKeyboard()
hm.HookMouse()
pygame.init()
while True:
	pygame.event.pump()
	try:
		with open("match_face_result") as f:
			result = f.read()
	except:
		time.sleep(0.01)
		continue

	if result:
		os.remove("match_face_result")
		hm.KeyAll = KeyboardMouseEnable
		hm.MouseAll = KeyboardMouseEnable
		hm.UnhookKeyboard()
		hm.UnhookMouse()
		break


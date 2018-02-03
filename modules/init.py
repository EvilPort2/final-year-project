import os
import sqlite3

def create_folders():
	if not os.path.exists("photos"):
		os.mkdir("photos")
	if not os.path.exists("screenshots"):
		os.mkdir("screenshots")

def create_databases():
	if not os.path.exists("modules/face_lock_unlock/face_recognition/faceDetectDatabase.db"):
		conn = sqlite3.connect("modules/face_lock_unlock/face_recognition/faceDetectDatabase.db")
		cmd1 = "CREATE TABLE People ( id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name varchar ( 50 ), occupation varchar ( 100 ), gender varchar ( 10 ), lastPictureNumber varchar ( 10 ), is_password INTEGER DEFAULT 0 )"
		conn.execute(cmd1)


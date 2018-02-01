import os

def create_folders():
	if not os.path.exists("photos"):
		os.mkdir("photos")
	if not os.path.exists("screenshots"):
		os.mkdir("screenshots")

create_folders()
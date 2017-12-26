from cx_Freeze import setup, Executable
import sys
import modules

build_exe_options = {"packages": ["os", "sys", "glob", "cv2", "win32api",], "includes": [modules] } # <-- Include easy_gui


base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "Final-year-Project" ,
      version = "0.1" ,
      description = "" ,
      options = {"build_exe": build_exe_options},
      executables = [Executable("main.py", base=base)])
from threading import Thread
import tkinter, win32api, win32con, pywintypes
from face_matching import match_face
import os

def KeyboardMouseDisable(event):
    print("Keyboard and Mouse are disabled")
    return False

def KeyboardMouseEnable(event):
    print(event.Message)
    return True


class DisplayFaceRecognizer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        if not os.path.exists("modules/face_lock_unlock/face_recognition/faceDetectDatabase.db"):
            print("Database does not exist. Create a database first from Settings>>Train the face recognizer")
            with open("match_face_result", "w") as f:
                f.write("True")
            return

        conn = sqlite3.connect("modules/face_lock_unlock/face_recognition/faceDetectDatabase.db")
        try:
            cmd = "SELECT MIN(id) FROM People"
            cursor = conn.execute(cmd)
        except sqlite3.OperationalError:
            print("Table does not exist. Create a table first from Settings>>Train the face recognizer")
            with open("match_face_result", "w") as f:
                f.write("True")
            return
        for row in cursor:
            unlockFaceId = row[0]
        self.is_matched = match_face(unlockFaceId)

class DisplayLockscreenText(Thread):
    def callback(self):
        self.root.quit()

    def __init__(self):
        Thread.__init__(self)
        self.start()
            
    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        label = tkinter.Label(self.root, text='Computer is Locked', font=('Times New Roman','80'), fg='green', bg='white')
        label.master.overrideredirect(True)
        label.master.geometry("+250+250")
        label.master.lift()
        label.master.wm_attributes("-topmost", True)
        label.master.wm_attributes("-disabled", True)
        label.master.wm_attributes("-transparentcolor", "white")
        hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        label.pack()
        while True:
            self.root.update()
            try:
                with open("match_face_result") as f:
                    result = f.read()
            except:
                continue
            if result:
                break


displayLockscreenText = DisplayLockscreenText()
displayFaceRecognizer = DisplayFaceRecognizer()
os.system("python modules/face_lock_unlock/keyboard_mouse_disable.py")

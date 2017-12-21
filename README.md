# The Applications of Facial Recognition, Gesture Recognition and Motion Detection and Tracking
This is my B.Tech Final Year project. The aim of this project is to reduce the number of input devices to one which is the webcam.

### Disclaimer
This project is not yet complete. Some modules are yet to be added and the added ones need refining. So use this if you like fixing and playing with broken or incomplete things. Also this is not a complete documentation.

### Applications
1. <b>Facial Recognition</b> - Using facial recognition I decided to create a lockscreen that can be unlocked only using my face. When the screen is locked, both the keyboard and the mouse get disabled and a gren text saying "Computer is Locked" is displayed on the screen.<br>
2. <b>Gesture Recognition</b> - Using this every others module can be controlled. I can also give keyboard shortcut inputs to the computer. Other than that I can take screenshots and photos from the webcam itself using 2 hand gestures. For this module the user needs to wear a yellow (actually the user can wear any coloured paper except black and white, I prefer yellow) paper on his finger.<br>
3. <b>Motion Detection and Tracking</b> - I created a virtual keyboard and a mouse. Using the motion of your fingers you can control your keyboard and mouse. The keyboard has only 27 keys (26 alphabets + 1 space bar).

As you might have probably noticed the above said applications are something that I have already made. Yeah you are right I am just slapping all of them into one giant project. Haha.

### Requirements
1. Python 3
2. OpenCV 3
3. OpenCV contrib library
4. pygame or pythoncom
5. pywin32
6. tkinter
7. imutils

Hope that I have pretty much listed everything.

### Usage
	python3 main.py
Then goto option 2 to set the color mask for the paper that you are going to wear in your finger for gesture recognition and also set your face for unlocking the lockscreen. If that is done you can go back and choose option 1 to start the gesture recognition program.<br>
If you liked the facial unlock program you can directly start it using<br>
    
    python3 unlock_using_face.py

# Virtual Keyboard
A simple virtual keyboard created using OpenCV and Python which has 26 alphabets and a space bar.

# Outcome
Look for yourself in this <a href = "https://lh3.googleusercontent.com/-BE99T5RPcL4/WdNYbPeHOpI/AAAAAAAAAxE/v_ZXXGv6y9MqSgfwcVTH4b7y2BCERvvBACJoC/w663-h373-rw/video41.gif">video</a>

# What have I done
The secret here is the area of the yellow paper I am wearing on my fingers. When I bring the paper near to the camera, the area of the paper as seen by the camera increases. When it is moved back the, the area of the paper as seen by the camera decreases. This is the simple idea that I have used to detect the click. The position of the click determines the key press that is to be simulated.<br>
The keyboard creation is a bit complicated process. I hope that the code will be able to explain it.

# Requirements
1. PyAutoGui<br>
2. OpenCV 3<br>

# Usage
First run the range-detector.py to set the range for the mask for colour segmentation. No need to change anything in the virtual_keyboard.py file

    python3 range-detector.py -f HSV -w
    python3 virtual_keyboard.py

# Got a question?
If you have any questions that are bothering you please contact me on my <a href = "facebook.com/dibakar.saha.750">facebook profile</a>. Just do not ask me questions like where do I live, who do I work for etc. Also no questions like what does this line do. If you think a line is redundant or can be removed to make the program better then you can obviously ask me or make a pull request.

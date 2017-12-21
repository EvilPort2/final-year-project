import cv2
import numpy as np
import pyautogui as gui
import time
from imutils import contours
from .gesture_api import do_gesture_action
from collections import deque
import datetime
import pickle
import os, thread
import pyHook, pythoncom

def contour_area_sort(contours, area_threshold):
    contours.sort(key = cv2.contourArea, reverse = True)
    cnts = [c for c in contours if cv2.contourArea(c) > area_threshold]
    return cnts

def determine_direction(diff):
    diffx, diffy = diff[0], diff[1]
    if abs(diffx) <=10 and abs(diffy) <= 10:
        return "St"
    elif diffx > 15 and abs(diffy) <= 15:
        return "E"
    elif diffx < -15 and abs(diffy) <= 15:
        return "W"
    elif abs(diffx) <= 15 and diffy < -15:
        return "N"
    elif abs(diffx) <= 15 and diffy > 15:
        return "S"
    elif diffx > 25 and diffy > 25:
        return "SE"
    elif diffx < -25 and diffy > 25:
        return "SW"
    elif diffx > 25 and diffy < -25:
        return "NE"
    elif diffx < -25 and diffy < -25:
        return "NW"

def process_created_gesture(created_gesture):
    """
    function to remove all the St direction and removes duplicate direction if they
    occur consecutively.
    """
    if created_gesture != []:
        for i in range(created_gesture.count("St")):
            created_gesture.remove("St")
        for i in range(created_gesture.count(None)):
            created_gesture.remove(None)

        for j in range(len(created_gesture)):
            for i in range(len(created_gesture) - 1):
                if created_gesture[i] == created_gesture[i+1]:
                    del created_gesture[i+1]
                    break
    return created_gesture

def gesture_action():
    cam = cv2.VideoCapture(0)
    with open("range.pickle", "rb") as f:
        t = pickle.load(f)
    print(t)
    yellow_lower = np.array([t[0], t[1], t[2]])                          # HSV yellow lower
    yellow_upper = np.array([t[3], t[4], t[5]])                      # HSV yellow upper
    screen_width, screen_height = gui.size()
    camx, camy = 480, 360

    c2, c1 = 0, 0
    flag_do_gesture = 0
    flags = [False, False, False]                                               # flags for number of coloured objects found (flag0, flag1, flag2)
    buff = 64
    line_pts = deque(maxlen = buff)
    line_pts1 = deque(maxlen = buff)
    line_pts2 = deque(maxlen = buff)
    created_gesture_hand = []
    created_gesture_hand_left = []
    created_gesture_hand_right = []
    old_center_left, old_center_right, old_center, center_left, center_right, center = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]

    while True:
        _, img = cam.read()

        # Resize for faster processing. Flipping for better orientation
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (camx, camy))

        # Convert to HSV for better color segmentation
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Mask for yellow color
        mask = cv2.inRange(imgHSV, yellow_lower, yellow_upper)

        # Bluring to reduce noises
        blur = cv2.medianBlur(mask, 15)
        blur = cv2.GaussianBlur(blur , (5,5), 0)

        # Thresholding
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        cv2.imshow("Thresh Yellow", thresh)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
        cnts = contour_area_sort(cnts, 350)

        # 2 hand gesture
        if len(cnts) >= 2:
            flag_do_gesture = 0
            line_pts = deque(maxlen = buff)

            cnt = cnts[:2]                                                          # take the top 2 contours
            cnt = contours.sort_contours(cnt, method = "left-to-right")[0]          # sort the contours from left to right

            contour_left = cnt[0]
            contour_right = cnt[1]

            rect_left = cv2.minAreaRect(contour_left)
            center_left = list(rect_left[0])
            box = cv2.boxPoints(rect_left)
            box = np.int0(box)
            cv2.circle(img, tuple(np.int0(center_left)), 2, (0, 255, 0), 2)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            line_pts1.appendleft(tuple(np.int0(center_left)))

            rect_right = cv2.minAreaRect(contour_right)
            center_right = list(rect_right[0])
            box = cv2.boxPoints(rect_right)
            box = np.int0(box)
            cv2.circle(img, tuple(np.int0(center_right)), 2, (0, 255, 0), 2)
            cv2.drawContours(img,[box],0,(0,255,255),2)
            line_pts2.appendleft(tuple(np.int0(center_right)))

            if c2 == 0:
                old_center_left = center_left
                old_center_right = center_right
            c2 += 1

            diff_left = np.array([0,0])
            diff_right = np.array([0,0])
            if c2 > 4:
                diff_left = np.array(center_left) - np.array(old_center_left)
                diff_right = np.array(center_right) - np.array(old_center_right)
                c2 = 0

            created_gesture_hand_left.append(determine_direction(diff_left))
            created_gesture_hand_right.append(determine_direction(diff_right))

            for i in range(1, len(line_pts1)):
                if line_pts1[i - 1] is None or line_pts1[i] is None:
                    continue
                cv2.line(img, line_pts1[i-1], line_pts1[i], (0, 255, 0), 2)

            for i in range(1, len(line_pts2)):
                if line_pts2[i - 1] is None or line_pts2[i] is None:
                    continue
                cv2.line(img, line_pts2[i-1], line_pts2[i], (0, 0, 255), 2)

            flags = [False, False, True]

        # 1 hand gestures
        elif len(cnts) >= 1:
            flag_do_gesture = 0
            line_pts1 = deque(maxlen = buff)
            line_pts2 = deque(maxlen = buff)

            contour = cnts[0]
            rect = cv2.minAreaRect(contour)
            center = list(rect[0])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.circle(img, tuple(np.int0(center)), 2, (0, 255, 0), 2)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            line_pts.appendleft(tuple(np.int0(center)))

            if c1 == 0:
                old_center = center
            c1 += 1

            diff = np.array([0,0])
            
            if c1 > 4:
                diff = np.array(center) - np.array(old_center)
                c1 = 0

            created_gesture_hand.append(determine_direction(diff))

            for i in range(1, len(line_pts)):
                if line_pts[i - 1] is None or line_pts[i] is None:
                    continue
                cv2.line(img, line_pts[i-1], line_pts[i], (0, 255, 0), 2)

            flags = [False, True, False]


        #completion of a gesture
        else:
            line_pts = deque(maxlen = buff)
            line_pts1 = deque(maxlen = buff)
            line_pts2 = deque(maxlen = buff)

            processed_gesture, processed_gesture_left, processed_gesture_right = (), (), ()

            if flags == [False, False, True]:                                       # completion of a 2 hand gesture
                processed_gesture_left = tuple(process_created_gesture(created_gesture_hand_left))
                processed_gesture_right = tuple(process_created_gesture(created_gesture_hand_right))
                if flag_do_gesture == 0:
                    if processed_gesture_right != () or processed_gesture_left != ():
                        # camera click
                        if processed_gesture_left == ("SW", "SE") and processed_gesture_right == ("SE", "SW"):
                            img1 = cam.read()[1]
                            ts = time.time()
                            st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d %H_%M_%S')
                            cv2.imwrite("photos/"+st + ".png", img1)
                        else:
                            do_gesture_action(processed_gesture_left, processed_gesture_right)
                    flag_do_gesture = 1

                print(processed_gesture_left, processed_gesture_right)
                created_gesture_hand_left.clear()
                created_gesture_hand_right.clear()

            elif flags == [False, True, False]:                                     # completion of a 1 hand gesture
                processed_gesture = tuple(process_created_gesture(created_gesture_hand))
                if flag_do_gesture == 0:
                    if processed_gesture != ():
                        if processed_gesture == ('S', 'E'):
                            # Lock the computer
                            cam.release()
                            os.system("python unlock_using_face.py")
                            
                            cam = cv2.VideoCapture(0)
                        else:
                            do_gesture_action(processed_gesture)
                    flag_do_gesture = 1

                print(processed_gesture)
                created_gesture_hand.clear()
                
            flags = [True, False, False]


        cv2.imshow("IMG", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()


#gesture_action()
import cv2
import numpy as np
import pyautogui as gui
import pickle




def top(collection, key, n):
    collection = sorted(collection, key = key, reverse = True)
    returnable = []
    for i in range(n):
        returnable.append(collection[i])
    return returnable

def start_mouse():
    #kernelopen = np.ones((5, 5), np.uint8)
    #kernelclose = np.ones((15, 15), np.uint8)
    with open("range.pickle", "rb") as f:
        t = pickle.load(f)

    cam = cv2.VideoCapture(1)
    lower = np.array([t[0], t[1], t[2]])                       # HSV green lower
    upper = np.array([t[3], t[4], t[5]])                    # HSV green upper
    screen_width, screen_height = gui.size()
    frame_width, frame_height = 640, 480
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    center = (0, 0)
    area1 = area2 = area3 = 0
    damping = 3
    sx, sy = (screen_width/frame_width)/damping, (screen_height/frame_height)/damping

    flag3 = False
    flag2 = False
    flag1 = False
    flag0 = True

    while True:
        _, img = cam.read()

        #  Flipping for better orientation
        img = cv2.flip(img, 1)

        # Convert to HSV for better color segmentation
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Mask for blue color
        mask = cv2.inRange(imgHSV, lower, upper)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelopen)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelclose)
        #cv2.imshow("mask", mask)

        # Bluring to reduce noises
        blur = cv2.medianBlur(mask, 15)
        blur = cv2.GaussianBlur(blur , (5,5), 0)
        #cv2.imshow("Blur", blur)

        # Thresholding
        _,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow("Thresh", thresh)

        image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        mposx, mposy = gui.position()

        if len(contours) >= 3:
            old_center = center

            if flag2 == True:
                damping = 3
            else:
                damping = 1.3
            sx, sy = (screen_width/frame_width)/damping, (screen_height/frame_height)/damping

            gui.mouseUp()

            flag3 = True
            flag2 = False
            flag1 = False

            c1, c2, c3 = top(contours, cv2.contourArea, 3)

            rect1 = cv2.minAreaRect(c1)
            (w, h) = rect1[1]
            area1 = cv2.contourArea(c1)
            center1 = list(rect1[0])
            box = cv2.boxPoints(rect1)
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)

            rect2 = cv2.minAreaRect(c2)
            (w, h) = rect2[1]
            area2 = cv2.contourArea(c2)
            center2 = list(rect2[0])
            box = cv2.boxPoints(rect2)
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)

            rect3 = cv2.minAreaRect(c3)
            (w, h) = rect3[1]
            area3 = cv2.contourArea(c3)
            center3 = list(rect3[0])
            box = cv2.boxPoints(rect3)
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)

            center = (int((center1[0]+center2[0]+center3[0])/3), int((center1[1]+center2[1]+center3[1])/3))

            center1[0] = int(center1[0])
            center1[1] = int(center1[1])
            center2[0] = int(center2[0])
            center2[1] = int(center2[1])
            center3[0] = int(center3[0])
            center3[1] = int(center3[1])

            cv2.line(img, tuple(center1), center, (255, 0, 0), 2)
            cv2.line(img, tuple(center2), center, (255, 0, 0), 2)
            cv2.line(img, tuple(center3), center, (255, 0, 0), 2)
            cv2.circle(img, center, 2, (0, 0, 255), 3)

            if not flag0:
                if abs(center[0]-old_center[0]) > 5 or abs(center[1]-old_center[1]) > 5 or damping == 1.3:
                    gui.moveTo(mposx+(center[0]-old_center[0])*sx, mposy + (center[1]-old_center[1])*sy)
            else:
                #gui.moveTo(mposx, mposy)
                flag0 = False

        elif len(contours) >= 2:
            c1, c2 = top(contours, cv2.contourArea, 2)

            (x, y), radius = cv2.minEnclosingCircle(c1)
            area = cv2.contourArea(c1)
            cv2.circle(img,(int(x), int(y)), int(radius), (0, 255, 0), 2)

            rect2 = cv2.minAreaRect(c2)
            (w, h) = rect2[1]
            area4 = cv2.contourArea(c2)
            center2 = list(rect2[0])
            box = cv2.boxPoints(rect2)
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

            try:
                error1 = int(abs(area - area1 - area2)/area * 100)
                error2 = int(abs(area - area1 - area3)/area * 100)
                error3 = int(abs(area - area2 - area3)/area * 100)
                error4 = int(abs(area4 - area1)/area4 * 100)
                error5 = int(abs(area4 - area2)/area4 * 100)
                error6 = int(abs(area4 - area3)/area4 * 100)
            except ZeroDivisionError:
                error1 = error2 = error3 = error4 = error5 = error6 = 100

            if (error1 <= 50 and error6 < 20) or (error2 <= 50 and error5 < 20) or (error3 <= 50 and error4 < 20):
                if flag3 == True and radius > 20:
                    gui.rightClick()
                    flag3 = False
                    flag2 = True
                    flag1 = False

        elif len(contours) >= 1:
            damping = 3
            sx, sy = (screen_width/frame_width)/damping, (screen_height/frame_height)/damping

            old_center = center
            c1 = max(contours, key = cv2.contourArea)

            center, radius = cv2.minEnclosingCircle(c1)
            area = cv2.contourArea(c1)
            cv2.circle(img,(int(center[0]), int(center[1])), int(radius), (255, 0, 0), 2)

            try:
                error = int(abs(area - area1 - area2 - area3)/area * 100)
            except:
                error = 100
            if error < 40:
                if (flag3 == True or flag2 == True) and radius > 20:
                    gui.mouseDown()
                    flag3 = False
                    flag2 = False
                    flag1 = True
                gui.moveTo(mposx+(center[0]-old_center[0])*sx, mposy + (center[1]-old_center[1])*sy)
            else:
                # start the virtual keyboard
                pass

        elif len(contours) == 0:
            flag0 = True
            gui.mouseUp()

        cv2.imshow("IMG", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    gui.mouseUp()


'This program should be executed first'
import cv2
import os
import sqlite3
import glob
from .database import getProfileDataById

def createDataset():
    faceCascPath = "modules/face_lock_unlock/face_recognition/haarcascade_frontalface_default.xml"
    eyeCascadePath = "modules/face_lock_unlock/face_recognition/haarcascade_eye.xml"
    faceCascade = cv2.CascadeClassifier(faceCascPath)
    eyeCascade = cv2.CascadeClassifier(eyeCascadePath)

    while True:
        user_id = (input("\nEnter the user id: "))
        if user_id.strip() == '':
            break
        try:
            user_id = int(user_id)
            break
        except KeyboardInterrupt:
            print("Exiting...")
            exit(1)
        except:
            continue

    i = 0
    j = 100

    flag = 1  # if flag is 1 then id does not exist in database else id exists
    conn = sqlite3.connect("modules/face_lock_unlock/face_recognition/faceDetectDatabase.db")
    if user_id != "":
        cmd = "SELECT * FROM People WHERE ID = " + str(user_id)
        cursor = conn.execute(cmd) 
        for row in cursor:
            flag = 0
            break

    # ID not in Database
    if flag == 1:
        name = input("Enter new name: ")
        occupation = input("Enter new occupation: ")
        gender = input("Enter new gender: ")
        while True:
            is_password = input("Set this face as password (0 for no and 1 for yes): ")
            if is_password == "0" or is_password == "1":
                break
        if user_id != "":
            cmd = "INSERT INTO People VALUES(" + str(user_id) + ",\"" + str(name) + "\",\"" + str(occupation) + "\",\"" + str(gender) + "\",100, "+is_password+" )"
        else:
            cmd = "INSERT INTO People (name, occupation, gender, lastPictureNumber, is_password) VALUES(\"" + str(name) + "\",\"" + str(occupation) + "\",\"" + str(gender) + "\",100, "+is_password+" )"
        conn.execute(cmd)
        conn.commit()
        cmd = "SELECT MAX(id) from People"
        cursor = conn.execute(cmd)
        for row in cursor:
            user_id = str(row[0])
            break
        conn.close()

    # ID is in database
    if flag == 0:
        print ("ID already exists in database. What would you like to do?\n\n1. Delete the old face and add a new face " \
              "with new info to the same ID\n2. " \
              "Update an old face\n ")
        while True:
            try:
                choice = int(input("Choice: "))
            except:
                continue
            if choice >= 1 and choice <= 2:
                break

        if choice == 1:
            cmd = "DELETE FROM People WHERE ID=" + str(user_id)
            conn.execute(cmd)
            conn.commit()
            name = input("Enter new name: ")
            occupation = input("Enter new occupation: ")
            gender = input("Enter new gender: ")
            while True:
                is_password = input("Set this face as password (0 for no and 1 for yes): ")
                if is_password != "0" or is_password != "1":
                    continue
            for f in glob.glob("modules/face_lock_unlock/face_recognition/dataset/user." + str(user_id) + "*.jpg"):
                os.remove(f)
            cmd = "INSERT INTO People VALUES(" + str(user_id) + ",\"" + name + "\",\"" + occupation + "\",\"" + gender + "\",\"" + str(j)+ "\", "+ is_password + ")"
            conn.execute(cmd)
            conn.commit()
            conn.close()

        else:
            profile = getProfileDataById(user_id)
            i = int(profile[4])
            j = i + 100
            cmd = "UPDATE People SET lastPictureNumber="+str(j)+" WHERE ID="+str(user_id)
            conn.execute(cmd)
            conn.commit()
            conn.close()

    cam = cv2.VideoCapture(1)
    while True:
        ret, img = cam.read() 
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 5, flags = cv2.CASCADE_SCALE_IMAGE)
        if len(faces) == 1:
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                eyes = eyeCascade.detectMultiScale(face, 1.1, 5, flags = cv2.CASCADE_SCALE_IMAGE)
                if len(eyes) == 2:
                    cv2.imwrite("modules/face_lock_unlock/face_recognition/dataset/user." + str(user_id) + "." + str(i) + ".jpg", face)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    i = i + 1
        cv2.imshow("Webcam Face Detection", img)
        cv2.waitKey(1)
        if i > j:
            break

    cam.release()
    cv2.destroyAllWindows()

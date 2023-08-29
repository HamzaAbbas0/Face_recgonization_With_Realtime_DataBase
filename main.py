from datetime import datetime
import os
import pickle
import numpy as np
import cv2
import os
import cvzone
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import numpy as np

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancerealtime-19687-default-rtdb.firebaseio.com/',
    'storageBucket': "faceattendancerealtime-19687.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
imageBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
imgModelList = []
modePathList = os.listdir(folderModePath)

for path in modePathList:
    imgModelList.append(cv2.imread(os.path.join(folderModePath, path)))

print("Loading Encoding File ......")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()

encodeListKnown, studentIds = encodeListKnownWithIds
print('Encode File Loaded!!!')

modeType = 0
counter = 0
studentinfo = {}
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imageBackground[162:162 + 480, 55:55 + 640] = img
    imageBackground[44:44 + 633, 808:808 + 414] = imgModelList[modeType]

    if not faceCurFrame:
        # If no faces detected, reset modeType and related variables
        modeType = 0
        counter = 0
        studentinfo = {}
        imgStudent = []

    else:
        for encodeFace, facLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = facLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imageBackground = cvzone.cornerRect(imageBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imageBackground, "Loading", (275, 400),1.5,)

                    cv2.imshow("Face Attendance", imageBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
                    imageBackground[44:44 + 633, 808:808 + 414] = imgModelList[modeType]

        if counter != 0:
            if counter == 1:
                modeType = 1
                imageBackground[44:44 + 633, 808:808 + 414] = imgModelList[modeType]
                # Get the data from firebase
                studentinfo = db.reference(f'students/{id}').get()
                print(studentinfo)

                if not isinstance(studentinfo, dict) or not studentinfo or 'total_attendence' not in studentinfo:
                    # If studentinfo is not a dictionary, is empty, or 'total_attendence' key is missing, reset the variables
                    modeType = 0
                    counter = 0
                    studentinfo = {}
                    imgStudent = []

                else:
                    # Get the Images from firebase
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    # Update the Attendance
                    datetimeObject = datetime.strptime(studentinfo["Last_attendance_time"], "%Y-%m-%d %H:%M:%S")
                    secondElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondElapsed)
                    if secondElapsed > 30:
                        ref = db.reference(f'students/{id}')
                        studentinfo['total_attendence'] += 1
                        ref.child('total_attendence').set(studentinfo['total_attendence'])
                        ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imageBackground[44:44 + 633, 808:808 + 414] = imgModelList[modeType]

        if modeType != 3:
            if 10 < counter < 20:
                modeType = 2
            imageBackground[44:44 + 633, 808:808 + 414] = imgModelList[modeType]

            if counter <= 10 and studentinfo:
                cv2.putText(imageBackground, str(studentinfo['total_attendence']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(imageBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imageBackground, str(studentinfo['major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imageBackground, str(studentinfo['standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imageBackground, str(studentinfo['year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imageBackground, str(studentinfo['starting_year']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (w, h), _ = cv2.getTextSize(studentinfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2
                cv2.putText(imageBackground, str(studentinfo['name']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                if imgStudent.any():
                    imageBackground[175:175 + 216, 909:909 + 216] = imgStudent

            counter += 1
            print("counter is", counter)

            if counter >= 20:
                counter = 0
                modeType = 0
                studentinfo = {}
                imgStudent = []
                imageBackground[44:44 + 633, 808:808 + 414] = imgModelList[modeType]

    cv2.imshow("Face Attendance", imageBackground)
    cv2.waitKey(1)

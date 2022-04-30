import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv

#AUTO LOAD IMAGES FROM FOLDER
path = 'imageAttendance'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)

# find encodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

 # save encodings
def sendEncodings():
    with open('encoding.csv','w') as f:
        write = csv.writer(f)
        write.writerows(encodeListKnown1)

# read saved encodings
def readEncoding():
    with open('encoding.csv', newline='' ) as f:
        reader = csv.reader(f)
        data = list(reader)
        return (list(filter(lambda x:x,data)))

# mark attencance      
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        #print(myDataList)
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

#markAttendance('Elon')

# main code
encodeListKnown1 = findEncodings(images)
encodeListKnown = readEncoding()
#sendEncodings()
print('Encoding Complete')
#print(encodeListKnown)

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    print(encodeListKnown1)

    for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
        #print(encodeFace)
        #print('')
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        #print(matches)
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDist)
        matchIndex = np.argmin(faceDist)
        #Box
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 *4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            #y1,x2,y2,x1 = faceLoc
            #y1, x2, y2, x1 =y1*4, x2*4, y2*4, x1*4
            #cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('webcam',img)
    cv2.waitKey(1)

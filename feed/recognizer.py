from cv2 import cv2
import numpy as np
import face_recognition
import os
import datetime

from numpy.lib.function_base import append
from student.models import Student


def define(allStudents):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "media"))
    data = []
    Names = []
    # item.rollNo for item in allStudents
    # myList = os.listdir(path)  # name of the data

    # myList.remove('.DS_Store')
    for each in allStudents:

        currimg = face_recognition.load_image_file(
            f"{path}/{each.photo}"
        )  # reading the image with the help of path of image
        data.append(currimg)
        Names.append(each.rollNo)  # names of all the data
    # print(data)
    return data, Names


def encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if len(encode) > 0:
            biden_encoding = encode[0]
        else:
            # print("No faces found in the image!")
            pass
        encodeList.append(biden_encoding)
    # print(encodeList)
    return encodeList


def gen_frames():  # generate frame by frame from camerapipe
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    all_data = Student.objects.all()
    if len(all_data) > 0:

        images, Names = define(all_data)
        encodeListKnown = encodings(images)
        names = []
        while True:
            # Capture frame-by-frame
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                #  We can find multiple face so to give face locations and send it to encoding fucntion
                #  Encoding the capured image
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                faceCurr = face_recognition.face_locations(imgS)
                encodeCurr = face_recognition.face_encodings(imgS, faceCurr)
                face_names = []

                # Finding matches
                for encodeFace, faceLoc in zip(encodeCurr, faceCurr):
                    # matches gives bollean output if which of the face is matching
                    matches = face_recognition.compare_faces(
                        encodeListKnown, encodeFace
                    )
                    # the lower the face disatnce the better the match is
                    faceDis = face_recognition.face_distance(
                        encodeListKnown, encodeFace
                    )
                    # as we are giving list as input to faceDis we will get list as output
                    # We will get 3 output as we have given 3 input and the lowest will be the match
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = Names[matchIndex].upper()
                        print("name", name)
                        face_names.append(name)
                        if name not in names:
                            names.append(name)
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = (
                            y1 * 4,
                            x2 * 4,
                            y2 * 4,
                            x1 * 4,
                        )  # since we resized it we are incrasing the size
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(
                            frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED
                        )
                        cv2.putText(
                            frame,
                            name,
                            (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1,
                            (255, 255, 255),
                            2,
                        )

            cv2.imshow("Video Capture", frame)
            if cv2.waitKey(1) == ord("s"):
                break
    camera.release()
    cv2.destroyAllWindows()
    print(names, "nammmm")
    return names
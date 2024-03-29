from cv2 import cv2
import numpy as np
import face_recognition
import os


def define(allStudents):
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media'))
    data = []
    Names = []
    # item.rollNo for item in allStudents
    # myList = os.listdir(path)  # name of the data

    # myList.remove('.DS_Store')
    for each in allStudents:

        currimg = face_recognition.load_image_file(f'{path}/{each.photo}')  # reading the image with the help of path of image
        data.append(currimg)
        Names.append(each.name)  # names of all the data
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
            print("No faces found in the image!")
        encodeList.append(biden_encoding)
    # print(encodeList)
    return encodeList

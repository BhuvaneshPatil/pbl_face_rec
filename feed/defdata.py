from cv2 import cv2
import numpy as np
import face_recognition
import os


def define():
    path = 'data'
    data = []
    Names = []
    myList = os.listdir(path)  # name of the data
    myList.remove('.DS_Store')
    for each in myList:
        currimg = cv2.imread(f'{path}/{each}')  # reading the image with the help of path of image
        data.append(currimg)
        Names.append(os.path.splitext(each)[0])  # names of all the data
    return data, Names


def encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import io
from student.models import Student
from django.core.files.images import ImageFile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from . import defdata
import face_recognition

# import face_detection
import numpy as np

# Create your views here.


def gen_frames():  # generate frame by frame from camerapipe
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    all_data = Student.objects.all()
    print(len(all_data))
    if len(all_data) > 0:

        images, Names = defdata.define(all_data)
        print(Names)
        encodeListKnown = defdata.encodings(images)
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
                        print(name)
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

            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


def feedView(request):
    cv2.destroyAllWindows()
    try:
        return StreamingHttpResponse(
            gen_frames(), content_type="multipart/x-mixed-replace; boundary=frame"
        )
    except:
        return HttpResponse("heh")


# @csrf_exempt
# def index(request):
#     # all_data = Student.objects.all()

#     # print(all_data[0].photo)
#     if request.method == "POST":
#         data = request.POST
#         success, image = camera.read()
#         # Saves the frames with frame-count
#         is_success, buffer = cv2.imencode(".jpg", image)

#         s = Student(rollNo=data["roll"])
#         s.photo = ImageFile(io.BytesIO(buffer.tobytes()), name="temp.jpg")
#         s.save()
#         pass
#     return render(request, "feed/index.html")


#
# def addView(request):
#     if request.method == "POST":
#         current_image = cv2.imwrite('opencv.png', gen_frames)
#         print(current_image)
#

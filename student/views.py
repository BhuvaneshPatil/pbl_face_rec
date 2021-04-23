from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.core.files.images import ImageFile
from django.views.decorators.csrf import csrf_exempt
import cv2
import io
import face_recognition
from .models import Student

camera = cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camerapipe
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


# Create your views here.
def demoShowFeed(request):
    return StreamingHttpResponse(
        gen_frames(), content_type="multipart/x-mixed-replace; boundary=frame"
    )


@csrf_exempt
def addView(request):
    if request.method == "POST":
        data = request.POST
        success, image = camera.read()
        # Saves the frames with frame-count
        is_success, buffer = cv2.imencode(".jpg", image)
        s = Student(rollNo=data["roll"], name=data["name"])
        s.photo = ImageFile(io.BytesIO(buffer.tobytes()), name="temp.jpg")
        s.save()
        return redirect("student:addView")
    return render(request, template_name="student/index.html")

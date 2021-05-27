from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.http import StreamingHttpResponse, HttpResponse
from django.core.files.images import ImageFile
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
import cv2
import io
import face_recognition
from .models import Student


def gen_frames():  # generate frame by frame from camerapipe
    camera = cv2.VideoCapture(0)
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
    cv2.destroyAllWindows()
    return StreamingHttpResponse(
        gen_frames(), content_type="multipart/x-mixed-replace; boundary=frame"
    )


@csrf_exempt
def addView(request):
    camera = cv2.VideoCapture(0)

    if request.method == "POST":
        data = request.POST
        success, image = camera.read()
        # Saves the frames with frame-count
        is_success, buffer = cv2.imencode(".jpg", image)
        s = Student(rollNo=data["roll"], name=data["name"])
        s.photo = ImageFile(io.BytesIO(buffer.tobytes()), name="temp.jpg")
        try:
            s.save()
            messages.success(request, "Successfully Added New Student")
        except IntegrityError:
            messages.error(
                request, f"Student with roll no {data['roll']} already exist"
            )

        # camera.clear()
        return redirect("student:addView")
    return render(request, template_name="student/index.html")


def updateView(request, id):
    curr_student = Student.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        s = Student.objects.get(pk=id)

    return render(
        request, template_name="student/update.html", context={"student": curr_student}
    )


def detailView(request, id):
    curr_student = Student.objects.get(id=id)
    return render(
        request,
        template_name="student/detailView.html",
        context={"student": curr_student},
    )


class StudentListView(ListView):
    template_name = "student/list.html"
    queryset = Student.objects.all()
    context_object_name = "students"
    print()
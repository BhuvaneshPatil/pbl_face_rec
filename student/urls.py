from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path("add/", views.addView, name="addView"),
    path("feed/", views.demoShowFeed, name="demoFeed"),
    path("list/", views.StudentListView.as_view(), name="studentList")
]

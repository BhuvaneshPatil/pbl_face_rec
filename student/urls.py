from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path("", views.addView, name="addView"),
    path("feed/", views.demoShowFeed, name="demoFeed"),
]

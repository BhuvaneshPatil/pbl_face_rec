from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "feed"

urlpatterns = [
    # path("", views.index, name="base"),
    # path('',views.addView,name=""),
    path("video", views.feedView, name="video"),
    # path("", views.feedView, name="video"),
]
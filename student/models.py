from django.db import models
from django.utils import timezone

import os


def path_and_rename(instance, filename):
    upload_to = "photos"
    filename = "{}.{}".format(instance.rollNo, "jpg")
    return os.path.join(upload_to, filename)


# # Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    rollNo = models.CharField(max_length=10, unique=True)
    photo = models.ImageField(upload_to=path_and_rename, blank=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-added_at"]

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone
import os
import os
def path_and_rename(instance, filename):
    upload_to = 'photos'
    # ext = filename.split('.')[-1]
    # get filename
    # if instance.rollNo:
    filename = '{}.{}'.format(instance.rollNo,"jpg")
    # else:
    #     # set filename as random string
    #     filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
# Create your models here.
class Student(models.Model):
    rollNo = models.CharField(max_length=12,unique=True)
    photo = models.ImageField(upload_to=path_and_rename,blank=True)

    def __str__(self):
        return self.rollNo
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     S = Student(rollNo=self.rollNo,photo=f'{self.rollNo}.jpg')
    #     S.save()


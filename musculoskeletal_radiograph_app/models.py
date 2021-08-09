import datetime
import os
from django.db import models



#File Path
def filepath_patient(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('patient/', filename)

def filepath_radiograph(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('radiograph/', filename)


# Create your models here.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    sur_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to=filepath_patient,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Radiograph(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField(upload_to=filepath_radiograph,null=False,blank=False)
    prediction = models.CharField(max_length=255)
    accuracy = models.CharField(max_length=255)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    objects = models.Manager()
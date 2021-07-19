from django.db import models

class IpScan(models.Model):
    taskid = models.IntegerField(default=1)
    ip = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    isShown = models.BooleanField(default=False)



# Create your models here.

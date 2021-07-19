import datetime

from django.db import models
from django.utils.timezone import now


class Poc(models.Model):
    poc_name = models.CharField(max_length=50, default="")
    real_name = models.CharField(max_length=50, default="")
    type = models.CharField(max_length=50, default="")
    risk = models.CharField(max_length=50, default="high")     # high, medium, low
    hasExp = models.BooleanField(default=False)
    isUse = models.BooleanField(default=True)
    cmd = models.CharField(max_length=50, default="")


# Create your models here.

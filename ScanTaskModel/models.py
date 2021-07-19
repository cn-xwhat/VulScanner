import datetime

from django.db import models
from django.utils.timezone import now


class ScanTask(models.Model):
    start_time = models.DateField(default=now)
    ip_range = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=50, default="")
    task_count = models.IntegerField(default=0)
    vuln_count = models.IntegerField(default=0)
    service_process = models.FloatField(default=0)
    vuln_process = models.FloatField(default=0)
    isPause = models.BooleanField(default=False)
    isStart = models.BooleanField(default=False)
    mode = models.CharField(max_length=50, default="")

# Create your models here.

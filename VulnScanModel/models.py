from django.db import models


class VulnScan(models.Model):
    taskid = models.IntegerField(default=1)
    ip = models.CharField(max_length=50)
    port = models.IntegerField(default=0)
    url = models.CharField(max_length=50, default="")
    vulnerability = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200, default="")
    risk = models.CharField(max_length=10, default="danger")
    isShown = models.BooleanField(default=False)
    module = models.CharField(max_length=50, default="")
    specify = models.CharField(max_length=50, default="")  # 需单独保存的特殊结果

# Create your models here.

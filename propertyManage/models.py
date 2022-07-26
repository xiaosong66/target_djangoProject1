from django.db import models


# Create your models here.
class individual_property(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)
    type = models.CharField(max_length=30, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    describe = models.CharField(max_length=500, null=True)
    backup = models.BooleanField(null=True)
    encryption = models.BooleanField(null=True)
    fileName = models.CharField(max_length=128, null=True)
    filePath = models.CharField(max_length=128, null=True)

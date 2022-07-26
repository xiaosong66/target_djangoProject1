from django.db import models
from propertyManage.models import *


# Create your models here.
# 位置信息数据库
class position(models.Model):
    user = models.CharField(max_length=128)
    log_time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    location = models.CharField(max_length=500, null=True)
    logInfo = models.CharField(max_length=500, default=None, null=True)
    if_log_success = models.BooleanField(null=True)
    if_solve = models.BooleanField(null=True)
    solve_method = models.CharField(max_length=20, null=True)


# 资产授权信息数据库
class property_auth(models.Model):
    individualProperty = models.ForeignKey(individual_property, on_delete=models.CASCADE)
    original_user = models.CharField(max_length=20)
    share_users = models.CharField(max_length=100, null=True)
    share_start_time = models.DateTimeField(null=True)
    share_end_time = models.DateTimeField(null=True)
    fileDescribe = models.CharField(max_length=200, null=True)


# 授权用户可登录ip
class Login_location_auth(models.Model):
    username = models.CharField(max_length=20)
    auth_first_time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    if_auth_login = models.BooleanField(null=True)
    auth_start_time = models.DateTimeField(null=True)
    auth_end_time = models.DateTimeField(null=True)

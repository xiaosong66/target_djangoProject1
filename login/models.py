from django.db import models


# Create your models here.
# 扩展用户信息
class userInfo(models.Model):
    username = models.CharField(max_length=128)
    uid = models.CharField(max_length=128, null=True)
    second_password = models.CharField(max_length=128, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=12, null=True)
    last_login = models.DateTimeField(null=True)
    common_login_location = models.CharField(max_length=100, null=True)
    common_login_ip = models.GenericIPAddressField(null=True)
    common_login_time = models.CharField(max_length=30, null=True)
    login_failure_num = models.IntegerField(default=0, null=True)
    loginFailure_days = models.IntegerField(default=0, null=True)
    loginFailure_days_Tag = models.BooleanField(default=False, null=True)
    if_auth_login = models.BooleanField(default=True, null=True)

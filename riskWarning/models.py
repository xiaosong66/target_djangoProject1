from django.db import models


# Create your models here.
class accessLogs(models.Model):
    time = models.DateTimeField(null=True)
    level = models.CharField(max_length=8, null=True)
    method = models.CharField(max_length=4, null=True)
    username = models.CharField(max_length=128, null=True)
    sip = models.GenericIPAddressField(null=True)
    dip = models.GenericIPAddressField(null=True)
    path = models.CharField(max_length=100, null=True)
    status_code = models.CharField(max_length=3, null=True)
    reason_phrase = models.CharField(max_length=30, null=True)
    body = models.CharField(max_length=200, null=True)


# 用户分享模块，记录用户的登录锁定风险，密码修改等，资产授权等
class userRisk(models.Model):
    username = models.CharField(max_length=128, null=True)
    time = models.DateTimeField(null=True)
    level = models.CharField(max_length=8, null=True)
    riskDescribe = models.CharField(max_length=100, null=True)


# 记录用户风险评分
class riskValue(models.Model):
    username = models.CharField(max_length=128, null=True)
    riskType = models.CharField(max_length=20, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    riskDescribe = models.CharField(max_length=200, null=True)
    if_solve = models.BooleanField(default=False, null=True)
    securityScore = models.CharField(default=0, null=True, max_length=10)


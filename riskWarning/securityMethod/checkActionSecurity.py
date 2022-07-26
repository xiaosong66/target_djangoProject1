# -*- coding: utf-8 -*-
# @Time    : 2022/4/27 19:53
# @Author  : xiaosong
# @File    : checkActionSecurity.py
# @Software: PyCharm
from authorizationManage.models import position
from login.models import userInfo
from riskWarning.models import riskValue


def checkActionSecurity(username):
    risk = ''
    score = 0
    # 常用登陆地
    obj = userInfo.objects.filter(username=username).first()
    common_login_location = obj.common_login_location
    common_login_ip = obj.common_login_ip
    # print(common_login_location)
    firstLoginLocation = position.objects.filter(user=username, if_log_success=True).order_by("-log_time").first()
    # print(firstLoginLocation.location)
    if common_login_location != firstLoginLocation.location:
        risk = '不在常用地登录，登录地为' + firstLoginLocation.location
        score = 5
        # 保存风险信息
    else:
        score = 20
        risk = ''

    riskObj = riskValue.objects.filter(username=username, riskType="行为安全评分")
    if riskObj.count() == 0:
        riskValue(username=username, riskType="行为安全评分", riskDescribe=risk, securityScore=score).save()
    else:
        riskObj.update(riskDescribe=risk, securityScore=score)

    return common_login_location, common_login_ip

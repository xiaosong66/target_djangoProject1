# -*- coding: utf-8 -*-
# @Time    : 2022/4/26 20:31
# @Author  : xiaosong
# @File    : checkAccoutSecurity.py
# @Software: PyCharm
from riskWarning.models import riskValue
from login.models import userInfo


def checkAccountSecurity(username):
    '''
    检测是否设置了邮箱和手机号
    '''
    risk = []
    score = 0
    myInfo = userInfo.objects.filter(username=username).first()
    if myInfo.email == '' or myInfo.email == "None":
        risk.append("邮箱未设置")
    else:
        score += 10

    if myInfo.phone_number == '' or myInfo.phone_number is None:
        risk.append("手机号未设置")
    else:
        score += 10

    riskObj = riskValue.objects.filter(username=username, riskType="账户安全评分")
    if len(risk) == 0:
        risk = ''
    if riskObj.count() == 0:
        riskValue(username=username, riskType="账户安全评分", riskDescribe=risk, securityScore=score).save()
    else:
        riskObj.update(riskDescribe=risk, securityScore=score)


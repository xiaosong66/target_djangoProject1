# -*- coding: utf-8 -*-
# @Time    : 2022/4/30 16:01
# @Author  : xiaosong
# @File    : otherSecurity.py
# @Software: PyCharm
import datetime

from riskWarning.models import userRisk, riskValue


# 判断账户是否有登录锁定的记录是否被处理
def otherSecurity(username=None):
    score = 20
    risk = []
    loginLock = userRisk.objects.filter(username=username, riskDescribe='账户锁定登录一天')
    loginLockRisk = []
    if loginLock.count() != 0:
        for i in loginLock:
            score -= 5
            if score <= 0:
                score = 0
            loginLockRisk.append(datetime.datetime.strftime(i.time, '%Y-%m-%d %H:%M') + ' ' + i.riskDescribe)
        # print(loginLockRisk)

    risk.append(loginLockRisk)
    riskObj = riskValue.objects.filter(username=username, riskType="其他安全评分")
    if riskObj.count() == 0:
        riskValue(username=username, riskType="其他安全评分", riskDescribe=risk, securityScore=score).save()
    else:
        riskObj.update(riskDescribe=risk, securityScore=score)

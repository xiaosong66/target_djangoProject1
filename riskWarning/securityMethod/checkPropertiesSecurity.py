# -*- coding: utf-8 -*-
# @Time    : 2022/4/26 20:07
# @Author  : xiaosong
# @File    : checkPropertiesSecurity.py
# @Software: PyCharm
from propertyManage.models import individual_property
from riskWarning.models import riskValue


def checkPropertiesSecurity(username):
    risk = []
    score = 20
    allData = individual_property.objects.filter(user=username).all()
    for obj in allData:
        if (not obj.backup) or (not obj.encryption):
            score -= 1
            if score <= 0:
                score = 0
            risk.append(obj.fileName)

    if len(risk) == 0:
        score = 20
        risk = ''

    riskObj = riskValue.objects.filter(username=username, riskType="资产安全评分")
    if riskObj.count() == 0:
        riskValue(username=username, riskType="资产安全评分", riskDescribe=risk, securityScore=score).save()
    else:
        riskObj.update(riskDescribe=risk, securityScore=score)



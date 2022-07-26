# -*- coding: utf-8 -*-
# @Time    : 2022/4/25 21:54
# @Author  : xiaosong
# @File    : checkPdStrength.py
# @Software: PyCharm
from riskWarning.models import riskValue


# 登录成功后检测密码强度
def checkPdStrength(password, username=None):
    notions = []
    score = 0
    uppercase, lowercase, letters = set(), set(), set()
    digits, special = set(), set()

    for character in password:
        if character.isupper():  # 大写
            uppercase.add(character)
            letters.add(character)
        elif character.islower():  # 小写
            lowercase.add(character)
            letters.add(character)
        elif character.isdigit():  # 数字
            digits.add(character)
        elif not character.isspace():  # 特殊字符，最后判断，不是字母和数字，则只能符号，除去空格就是特殊符号
            special.add(character)

    if len(uppercase) == 0:
        notions.append("缺少大写字母")
    else:
        score += 4
    if len(lowercase) == 0:
        notions.append("缺少小写字母")
    else:
        score += 4
    if len(digits) == 0:
        notions.append("缺少数字")
    else:
        score += 2
    if len(special) == 0:
        notions.append("缺少特殊符号")
    else:
        score += 4
    if len(password) < 8:
        notions.append("密码长度不足八位")
    else:
        score += 6

    # return notions
    if len(notions) == 0:
        notions = ''

    data = riskValue.objects.filter(username=username, riskType="密码安全评分")
    if data.count() != 0:
        data.update(riskDescribe=notions, securityScore=score)
    else:
        data = riskValue(username=username, riskType="密码安全评分", riskDescribe=notions, securityScore=score)
        data.save()


# checkPdStrength(password='aa!12345')

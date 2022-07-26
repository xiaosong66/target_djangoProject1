import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from riskWarning.models import userRisk, riskValue
from riskWarning.securityMethod.checkPropertiesSecurity import checkPropertiesSecurity
from riskWarning.securityMethod.checkAccoutSecurity import checkAccountSecurity
from riskWarning.securityMethod.checkActionSecurity import checkActionSecurity
from riskWarning.securityMethod.otherSecurity import otherSecurity


# 返回登录锁定信息
@csrf_exempt
def get_loginFailure_info(request):
    if request.method == 'POST':
        inquireUser = request.user
        response = userRisk.objects.filter(username=inquireUser)

        if response is not None:
            return render(request, 'riskWarning.html', {'loginFailureData': response})
        else:
            # jsonData = serializers.serialize('json', response)
            # request.session['queryResult'] = jsonData
            return HttpResponse("无查询结果！")
    return HttpResponseRedirect('/PM/property/')


""" 
----------------------- 登录安全评分 ----------------------
"""


# 获取密码强度信息
@csrf_exempt
def getPdStrengthSecurityInfo(request):
    if request.method == 'POST':
        username = request.user
        data = riskValue.objects.filter(username=username, riskType="密码安全评分").first()
        riskDescribe = data.riskDescribe
        score = data.securityScore
        return render(request, 'riskWarning.html', {'pdSecurityData': riskDescribe, 'pdScore': score})
    return HttpResponse('0')


# 获得资产安全信息
@csrf_exempt
def getPropertySecurityInfo(request):
    if request.method == 'POST':
        username = request.user
        checkPropertiesSecurity(username)
        data = riskValue.objects.filter(username=username, riskType="资产安全评分").first()
        riskDescribe = data.riskDescribe
        score = data.securityScore
        return render(request, 'riskWarning.html', {'propertySecurityData': riskDescribe, 'propertyScore': score})
    return HttpResponse('0')


# 获得账户安全信息
@csrf_exempt
def getAccountSecurityInfo(request):
    if request.method == 'POST':
        username = request.user
        checkAccountSecurity(username)
        data = riskValue.objects.filter(username=username, riskType="账户安全评分").first()
        riskDescribe = data.riskDescribe
        score = data.securityScore
        return render(request, 'riskWarning.html', {'accountSecurityData': riskDescribe, 'accountScore': score})
    return HttpResponse('0')


# 获得行为安全信息
# 常用登录地、常用登录设备、常用登录IP
@csrf_exempt
def getActionSecurityInfo(request):
    if request.method == 'POST':
        username = request.user

        common_login_location, common_login_ip = checkActionSecurity(username)
        data = riskValue.objects.filter(username=username, riskType="行为安全评分").first()
        riskDescribe = data.riskDescribe
        score = data.securityScore
        return render(request, 'riskWarning.html', {
            'actionSecurityData': riskDescribe,
            'common_login_location': common_login_location,
            'common_login_ip': common_login_ip,
            'actionScore': score
        })
    return HttpResponse('0')


# 获得其他安全信息
@csrf_exempt
def getOtherSecurityInfo(request):
    if request.method == 'POST':
        username = request.user
        otherSecurity(username)
        data = riskValue.objects.filter(username=username, riskType="其他安全评分").first()
        riskDescribe = data.riskDescribe
        score = data.securityScore
        return render(request, 'riskWarning.html', {'otherSecurityData': riskDescribe, 'otherScore': score})
    return HttpResponse('0')


# 获取总体安全评分
@csrf_exempt
def getSecurityScore(request):
    if request.method == 'POST':
        score = 0
        username = request.user
        objs = riskValue.objects.filter(username=username).all()
        eachScore = []
        for obj in objs:
            score += int(obj.securityScore)
            eachScore.append([obj.riskType, obj.securityScore])
        eachScore.append(['score', score])
        # print(eachScore)
        return HttpResponse(json.dumps(eachScore, ensure_ascii=False))
    return HttpResponse('0')

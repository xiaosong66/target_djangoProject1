import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from login.views import statistics_log_info
from authorizationManage.models import position, Login_location_auth
from login.models import userInfo
from django.core.cache import cache


# Create your views here.
# 保存用户登录信息在 login app
# 获取登录信息,统计成功和失败次数
def log_success_failure(request):
    if request.method == 'POST':
        logInfo = []
        log_data, before, now = statistics_log_info(request, False)
        before = datetime.datetime(before.year, before.month, before.day)
        now = datetime.datetime(now.year, now.month, now.day)
        ipList = []

        for i in log_data:
            if i.ip not in ipList:
                ipList.append(i.ip)

        ipListLen = len(ipList)
        log_all = [0] * ipListLen  # 总次数
        log_success = [0] * ipListLen  # 成功次数
        log_failure = [0] * ipListLen  # 成功次数

        for obj in log_data:
            index = ipList.index(obj.ip)
            log_all[index] += 1
            if obj.if_log_success == 1:
                log_success[index] += 1
            else:
                log_failure[index] += 1

        logInfo.append(ipList)
        logInfo.append(log_all)
        logInfo.append(log_success)
        logInfo.append(log_failure)
        logInfo.append([str(before) + '~' + str(now)])
        return HttpResponse(json.dumps(logInfo))

    return HttpResponse('获取地址信息失败')


# 处理登录失败和异地登录的信息
def solve_log_failure(request):
    if request.method == 'POST':
        username = request.user
        ip = request.POST.get('ip')
        logType = request.POST.get('type')
        if logType == '失败次数':
            obj = position.objects.filter(ip=ip, user=username, if_log_success=False)
        elif logType == '成功次数':
            obj = position.objects.filter(ip=ip, user=username, if_log_success=True)
        else:
            obj = position.objects.filter(ip=ip, user=username)
        return render(request, 'loginLocationMana.html', {'allData': obj})
    return HttpResponse('登录信息请求失败')


# 加载最近的数据
def get_now_info(request):
    if request.method == 'POST':
        username = request.user
        request.session['common_log_location'] = userInfo.objects.filter(
            username=username).first().common_login_location
        obj = position.objects.filter(user=username).order_by('-log_time')
        return render(request, 'loginLocationMana.html', {'allData': obj[0:10]})

    return HttpResponse('加载失败')


# 管理登录信息，信任登录
def verify_logLocation(request):
    if request.method == 'POST':
        username = request.user
        trustVal = request.POST.get('trustVal')
        # print(type(trustVal))
        positionID = request.POST.get('id')
        if trustVal == '1':  # 信任此次登录
            position.objects.filter(id=positionID).update(solve_method='信任', if_solve=True)
        else:  # 不信任
            position.objects.filter(id=positionID).update(solve_method='不信任', if_solve=True)

        data = position.objects.filter(user=username).all()
        return render(request, 'loginLocationMana.html', {'allData': data})
    return HttpResponse('0')


# 登录信息点击修改密码，所有的置为不信任，且处理为1
def verify_loc_modifyPD(request):
    if request.method == 'POST':
        username = request.user
        obj = position.objects.filter(user=username).exclude(if_solve=True)
        obj.update(if_solve=True, solve_method='修改密码')

        return HttpResponse('1')

    return HttpResponse('0')


# 查询功能
@login_required(login_url='/lg/login/')
@csrf_exempt
def searchLoginInfo(request):
    if request.method == 'POST':
        username = request.user
        searchContent = request.POST['searchContent']
        data = position.objects.filter(user=username).filter(Q(ip=searchContent) | Q(location__contains=searchContent))
        return render(request, 'loginLocationMana.html', {'allData': data})
    return HttpResponse(0)


# 修改密码
@login_required(login_url='/lg/login/')
@csrf_exempt
def modifyPD(request):
    if request.method == 'POST':
        new_password = request.POST["new_password"]
        repeat_new_password = request.POST["repeat_new_password"]
        authCode = request.POST["authCode"]
        myCode = cache.get("verifyCode")
        username = request.user

        if (new_password == '') or (repeat_new_password == ''):
            return HttpResponse("密码不能为空")
        if new_password != repeat_new_password:
            return HttpResponse("两次密码不相同")
        if myCode != authCode:
            return HttpResponse("验证码错误")

        cache.delete("verifyCode")

        User.objects.filter(username=username).update(password=make_password(new_password))
        return HttpResponse("密码修改成功")
    return HttpResponse(0)


@login_required(login_url='/lg/login/')
@csrf_exempt
def sendMessage(request):
    if request.method == 'POST':
        # 生成验证码
        import random
        str1 = '0123456789'
        verifyCode = ''
        for i in range(0, 6):
            verifyCode += str1[random.randrange(0, len(str1))]
        # 发送邮件：
        # 记录验证码,缓存记录, 10分钟有效
        cache.set("verifyCode", verifyCode, 600)
        # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        message = "您的验证码是" + verifyCode + "，10分钟内有效，请尽快填写"
        to_email = request.POST.get('myEmail')
        emailBox = [to_email]
        username = request.user
        if to_email != '':
            if to_email == userInfo.objects.filter(username=username).first().email:
                send_mail(subject='验证码', message=message, from_email=None,
                          recipient_list=emailBox, fail_silently=False)
                return HttpResponse('验证码发送成功')
            else:
                return HttpResponse('邮箱错误')
        else:
            return HttpResponse('邮箱空')

    return HttpResponseRedirect('/LM/loginLocMana/')


# 修改授权信息
@csrf_exempt
def get_authIp_info(request):
    if request.method == 'POST':
        username = request.user
        position_id = request.POST['id']
        ip = position.objects.filter(user=username, id=position_id).first().ip
        authData = Login_location_auth.objects.filter(username=username, ip=ip).first()
        return render(request, 'loginLocationMana.html', {'authData': authData})

    return HttpResponse(0)

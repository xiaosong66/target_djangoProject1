import datetime
import json
import traceback

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from riskWarning.models import userRisk
from .form import createNewUser
from .get_before_months import getMonth
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail
from authorizationManage.models import position, Login_location_auth
from django.core.cache import cache
from riskWarning.securityMethod.checkPdStrength import checkPdStrength


# 登录认证
# 使用session记录登录用户的信息
def record_loginInfo(request, user_obj, username):
    # 登录用户
    auth.login(request, user_obj)
    # 使用session存储用户登录情况
    user = User.objects.get(username=username)
    request.session['is_login'] = True
    request.session['user_id'] = user.id
    request.session['username'] = user.username


# 保存授权的IP信息
def save_auth_ip(username, ip, if_auth_login=True):
    data = Login_location_auth(username=username, ip=ip, if_auth_login=if_auth_login)
    data.save()
    # 保存登录ip到授权数据库中
    ipInfo = Login_location_auth.objects.filter(ip=ip)
    if ipInfo.count() == 0:
        IpData = Login_location_auth(username=username, ip=ip, auth_start_time=datetime.datetime.now(), if_auth_login=True)
        IpData.save()


# 判断用户登录失败的次数是否大于五次
def judge_loginFailure_num_gt5(username):
    # 获取用户已经登录失败的次数
    userInfo_obj = userInfo.objects.filter(username=username)
    loginFailureNum = userInfo_obj.first().login_failure_num
    if loginFailureNum < 5:
        loginFailureNum += 1
        userInfo_obj.update(login_failure_num=loginFailureNum)
        return False, userInfo_obj
    else:
        return True, userInfo_obj


# 添加用户的登录信息
def add_log_info(username, location, ip, loginTag=True, logInfo=None):
    if loginTag:
        if_log_success = True
        # 修改最后登录成功时间
        # print(now())
        try:
            userInfo.objects.filter(username=username).update(last_login=datetime.datetime.now())
        except:
            pass
    else:
        if_log_success = False

    data = position(user=username, ip=ip, location=location, if_log_success=if_log_success, logInfo=logInfo)
    data.save()


# 登录授权
@csrf_exempt
def loginAUTH(request):
    if request.method == "GET":
        return render(request, "login.html")

    username = request.POST["username"]
    password = request.POST["pwd"]
    logIP = request.POST["ip"]
    location = request.POST["location"]
    # 获取当前时间是否在授权时间之间
    now = datetime.datetime.now()
    # valid_num = request.POST.get("valid_num")
    # keep_str = request.session.get("keep_str")
    # if keep_str.upper() == valid_num.upper():
    try:
        # 登录认证的是否成功，认证成功判断是否被授权登录
        # 授权登录判断是否在授权时间
        # 第一次登录直接登录成功
        userExistTag = User.objects.filter(username=username).count()
        if userExistTag != 0:
            user_obj = auth.authenticate(username=username, password=password)
            # 无论认证成功都要记录登录失败信息
            # 认证成功返回用户名，认证失败返回None
            # 判断用户登录失败的次数是否大于五次, 大于就直接输出登录错误
            gt5_Tag, userInfo_obj = judge_loginFailure_num_gt5(username)
            if gt5_Tag:
                loginFailure_days_Tag = userInfo_obj.first().loginFailure_days_Tag
                loginFailure_days = userInfo_obj.first().loginFailure_days
                if not loginFailure_days_Tag:
                    # 保存用户风险信息
                    userRisk(username=username, time=now, level="warn", riskDescribe="账户锁定登录一天").save()
                    userInfo_obj.update(if_auth_login=False, loginFailure_days=(loginFailure_days + 1),
                                        loginFailure_days_Tag=True)
                add_log_info(username, location, logIP, False, "登录账户锁定")
                return HttpResponse("登录失败次数大于5次")

            # 登录认证成功
            if user_obj is not None:
                cache.set('neededVerifyCode' + username, user_obj)  # 缓存机制，用于登录未授权情况缓存，无须重复验证

                # 授权管理,获取授权的ip地址信息
                authIP_obj = Login_location_auth.objects.filter(username=username, ip=logIP).first()

                # 登录认证成功且授权ip不空，就将授权时间取出，否则查看是否第一次登录
                if authIP_obj is not None:
                    authStartTime = authIP_obj.auth_start_time
                    authEndTime = authIP_obj.auth_end_time

                    if authEndTime is not None:
                        if authIP_obj.if_auth_login & (now > authStartTime) & (now < authEndTime):  # 被授权登录
                            record_loginInfo(request, user_obj, username)  # 记录登录信息
                            userInfo_obj.update(login_failure_num=0)  # 更新登录失败信息
                            # 检测密码强度,并保存到数据库
                            checkPdStrength(username=username, password=password)
                            # 保存用户信息
                            add_log_info(username, location, logIP, True, "常用IP登录成功")
                            return HttpResponse('ok')
                    else:
                        if authIP_obj.if_auth_login & (now > authStartTime):
                            record_loginInfo(request, user_obj, username)
                            userInfo_obj.update(login_failure_num=0)
                            # 检测密码强度,并保存到数据库
                            checkPdStrength(username=username, password=password)
                            # 保存用户信息
                            add_log_info(username, location, logIP, True, "常用IP登录成功")
                            return HttpResponse('ok')
                        elif not authIP_obj.if_auth_login:
                            return HttpResponse('未被授权的登录IP地址')
                        elif (now < authStartTime) & authIP_obj.if_auth_login:
                            return HttpResponse('授权登录时间已过,继续登录请验证邮箱')
                        else:
                            add_log_info(username, location, logIP, False, "登录验证失败")
                            return HttpResponse('登录验证失败')
                # 登录认证成功，但是授权ip认证失败
                # 或者第一次在该IP登录
                else:
                    authIP_obj_num = Login_location_auth.objects.filter(username=username).count()
                    userInfo_num = userInfo.objects.filter(username=username).count()
                    # 查看是否有个人信息记录
                    if userInfo_num == 0:
                        save_user_info(request, 1)
                    # 第一次登录, 直接登录成功, 写入session信息
                    # 并且写入用户个人信息
                    if authIP_obj_num == 0:
                        save_auth_ip(username, logIP, True)
                        record_loginInfo(request, user_obj, username)
                        request.session['email'] = 'no'
                        # 检测密码强度,并保存到数据库
                        checkPdStrength(username=username, password=password)
                        add_log_info(username, location, logIP, True, "首次登录IP")
                        return HttpResponse('ok')
                    # 非第一次登陆
                    else:
                        return HttpResponse('未被授权的登录IP地址')
            else:
                add_log_info(username, location, logIP, False, "登录验证失败")
                return HttpResponse('用户不存在或者密码错误')
        else:
            return HttpResponse("用户不存在或者密码错误")
    except AttributeError:
        traceback.print_exc()
        add_log_info(username, location, logIP, False, "登录验证失败")
        return HttpResponse('用户不存在或者密码错误')


# 创建新用户
def createUser(request):
    if request.method == 'POST':
        form = createNewUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            # 保存用户信息
            userInfo(username=username, email=email).save()

            messages.info(request, "注册成功")
            return HttpResponseRedirect("/lg/login/")
    else:
        form = createNewUser()
    return render(request, 'register.html', {'form': form})


# 注销登录
def logOut(request):
    # return logout_then_login(request, "/lg/login/")
    auth.logout(request)
    request.session.flush()
    # logout(request)
    return HttpResponseRedirect('/lg/login/')


# 获取用户信息
def get_user_info(request, tag=True):
    username = request.user
    userData = User.objects.filter(username=username).first()
    registerDate = userData.date_joined
    userType = '0'
    if userData.is_superuser:
        userType = '1'
    data = userInfo.objects.filter(username=username).first()
    if not tag:
        return data, registerDate, userType
    else:
        return render(request, 'individualInfo.html',
                      {'userInfo': data,
                       'registerDate': registerDate,
                       'userType': userType
                       }
                      )


# 保存用户信息
def save_user_info(request, Tag=0):
    # 第一次登录
    if Tag == 1:
        username = request.POST.get('username')
        userInfo(username=username).save()
    else:
        username = request.user
        phoneNum = request.POST.get('phoneNum')
        email = request.POST.get('email')
        userInfo.objects.filter(username=username).update(phone_number=phoneNum, email=email)
        data, registerDate, userType = get_user_info(request, tag=False)
        return render(request, 'individualInfo.html',
                      {'userInfo': data,
                       'registerDate': registerDate,
                       'userType': userType
                       }
                      )


# 发送邮件
@csrf_exempt
def sendMessage(request, type=None):  # 发送邮件并返回验证码
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
        if (type == 'rt') or (type == 'loginVerify'):  # 注册
            to_email = request.POST.get('email')
            emailBox = [to_email]
            send_mail(subject='验证码', message=message, from_email=None,
                      recipient_list=emailBox, fail_silently=False)
            return HttpResponse('验证码发送成功')
        else:  # 非注册
            to_email = request.POST.get('myEmail')
            emailBox = [to_email]
            username = request.user
            if to_email == userInfo.objects.filter(username=username).first().email:
                send_mail(subject='验证码', message=message, from_email=None,
                          recipient_list=emailBox, fail_silently=False)
                return HttpResponse('验证码发送成功')
            else:
                return HttpResponse('邮箱错误')

    return HttpResponseRedirect('/lg/login/')


# login页面异地登录验证码验证
def verifyAuthCode(request):
    if request.method == 'POST':
        verifyCode = request.POST.get('authCode')
        username = request.POST.get('username')
        logIP = request.POST.get('ip')
        location = request.POST['location']
        email = request.POST.get('email')
        user_email = userInfo.objects.filter(username=username).first()
        # print(cache.get('neededVerifyCode' + username))
        # user_email.email必须这么访问
        if (verifyCode == cache.get("verifyCode")) & (email == user_email.email):
            # 删除验证码缓存
            # cache.delete("verifyCode")
            # 保存用户登录IP
            authIP_obj = Login_location_auth.objects.filter(username=username, ip=logIP)
            if authIP_obj.count() == 0:
                Login_location_auth(username=username, ip=logIP, if_auth_login=True, auth_start_time=datetime.datetime.now()).save()
            else:
                authIP_obj.update(auth_end_time=None, if_auth_login=True)
            # 待验证验证码的用户，登录用户写入session
            record_loginInfo(request, cache.get('neededVerifyCode' + username), username)
            add_log_info(username, location, logIP, True, "验证码验证成功登录")
            userInfo_obj = userInfo.objects.filter(username=username).update(login_failure_num=0, loginFailure_days=0,
                                                                             loginFailure_days_Tag=False)
            return HttpResponse('验证码验证成功')
        else:
            add_log_info(username, location, logIP, False, "验证码验证失败")
            return HttpResponse('验证码验证失败')

    return HttpResponseRedirect('/lg/login/')


# 获取登录信息  生成并学习  常用登录地
# 改成使用定时分析，比较好
@login_required(login_url='/lg/login/')
def statistics_log_info(request, tag=True):
    if request.method == 'POST':
        locationInfo = {}
        ipInfo = {}
        now = datetime.datetime.today()
        # 得到两个月前的日期
        before = getMonth(now)
        username = request.user

        # 获取常用IP
        ipKinds = position.objects.filter(user=username, log_time__range=(before, now)).values("ip").distinct()
        # print(ipKinds)
        for obj in ipKinds:
            ip = obj['ip']
            ipNum = position.objects.filter(user=username, log_time__range=(before, now), ip=ip).all().count()
            if ip not in ipInfo:
                ipInfo[ip] = ipNum
        ipInfo_sort = sorted(ipInfo.items(), key=lambda x: x[1], reverse=True)
        # 更新用户常用IP
        userInfo.objects.filter(username=username).update(common_login_ip=ipInfo_sort[0][0])
        # print(ipInfo_sort)

        log_data = position.objects.filter(user=username, log_time__range=(before, now))
        if tag:
            for i in log_data:
                if i.location not in locationInfo:
                    locationInfo[i.location] = 1
                else:
                    locationInfo[i.location] += 1
            locationInfo_sort = sorted(locationInfo.items(), key=lambda x: x[1], reverse=True)
            # print(locationInfo_sort)

            # ipInfo_sort = sorted(ipInfo.items(), key=lambda x: x[1], reverse=True)
            # print(ipInfo_sort)
            # 更新用户常用登录位置
            userInfo.objects.filter(username=username).update(common_login_location=locationInfo_sort[0][0])
            return HttpResponse(json.dumps(locationInfo_sort, ensure_ascii=False))
        else:
            return log_data, before, now

    return HttpResponse('获取地址信息失败')


# index页面简略查看
@login_required(login_url='/lg/login/')
def log_info(request):
    if request.method == 'POST':
        logInfo = []
        positionInfo = []
        logNum = []
        log_data, before, now = statistics_log_info(request, False)
        for i in log_data:
            if i.location not in positionInfo:
                positionInfo.append(i.location)
            try:
                logNum[positionInfo.index(i.location)] += 1
            except IndexError:
                logNum.append(1)

        logInfo.append(positionInfo)
        logInfo.append(logNum)
        print(logInfo)
        return HttpResponse(json.dumps(logInfo, ensure_ascii=False))

    return HttpResponse('获取地址信息失败')


# 修改密码
def modify_PD(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # nowPD = request.POST.get('now_password')
        newPD = request.POST.get('new_password')
        repeatNewPD = request.POST.get('repeat_new_password')
        verifyCode = request.POST.get('authCode')
        # 验证密码的，没必要
        # user_obj = auth.authenticate(username=username, password=nowPD)
        if verifyCode == cache.get("verifyCode"):
            if repeatNewPD == newPD:
                User.objects.filter(username=username).update(password=make_password(newPD))
                cache.delete("verifyCode")
                return HttpResponse('密码修改成功')
            else:
                return HttpResponse('修改失败')
        else:
            return HttpResponse('验证码错误')

    return HttpResponseRedirect('/lg/indiInfo/')


# 检测用户的信息是否完整
@login_required(login_url='/lg/login/')
def judge_userInfo_integrity(request):
    if request.method == 'POST':
        username = request.user
        email = userInfo.objects.filter(username=username).first().email
        if email is None:
            request.session['email'] = 'No'
        else:
            request.session['email'] = 'Yes'

        return HttpResponse('1')

    return HttpResponse('0')

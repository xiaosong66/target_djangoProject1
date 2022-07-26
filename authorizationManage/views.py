import datetime
import re

from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now

from authorizationManage.models import *
from login.models import userInfo
from propertyManage.models import individual_property


# Create your views here.
# 获取登录授权信息
def get_auth_ip(request, Tag=False):
    if request.method == 'POST':
        user = request.user
        data = Login_location_auth.objects.filter(username=user)
        if Tag:
            return data
        return render(request, 'authorization.html', {'ipAllData': data})

    return HttpResponseRedirect('/AM/authorization/')


# 修改登录ip授权信息
def modify_auth_IP(request):
    if request.method == 'POST':
        IPid = request.POST.get('IPid')
        username = request.POST.get('username')
        ip = request.POST.get('M_auth_ip')
        auth_start_time = request.POST.get('M_auth_start_time')
        auth_end_time = request.POST.get('M_auth_end_time')
        if auth_start_time != '':
            auth_start_time = datetime.datetime.strptime(auth_start_time, '%Y-%m-%dT%H:%M')
        else:
            auth_start_time = None
        if auth_end_time != '':
            auth_end_time = datetime.datetime.strptime(auth_end_time, '%Y-%m-%dT%H:%M')
        else:
            auth_end_time = None

        if_auth_login = True
        if request.POST.get('if_authLogin') == '0':
            if_auth_login = False

        authIP_obj = Login_location_auth.objects.filter(id=IPid, username=username)
        if authIP_obj is not None:
            authIP_obj.update(ip=ip, auth_start_time=auth_start_time,
                              auth_end_time=auth_end_time, if_auth_login=if_auth_login)

        data = get_auth_ip(request, True)
        return render(request, 'authorization.html', {'ipAllData': data})

    return HttpResponse('授权ip修改失败')


# 新增登录ip信息
def add_new_authIP(request):
    if request.method == 'POST':
        auth_start_time = request.POST.get('M_auth_start_time')
        auth_end_time = request.POST.get('M_auth_end_time')
        auth_ip = request.POST.get('M_auth_ip')
        username = request.user
        if_authLogin = request.POST.get('if_authLogin')

        if auth_ip == '':
            return HttpResponse('授权ip为空')
        if auth_start_time == '':
            auth_start_time = now()
        else:
            auth_start_time = datetime.datetime.strptime(auth_start_time, '%Y-%m-%dT%H:%M')
            if datetime.datetime.now() > auth_start_time:
                auth_start_time = now()
        if auth_end_time == '':
            auth_end_time = None
        else:
            auth_end_time = datetime.datetime.strptime(auth_end_time, '%Y-%m-%dT%H:%M')
            if datetime.datetime.now() > auth_end_time:
                auth_end_time = now()

        if auth_end_time < auth_start_time:
            auth_end_time = auth_start_time

        ipData = Login_location_auth(username=username, ip=auth_ip,
                                     if_auth_login=True if if_authLogin == '1' else False,
                                     auth_start_time=auth_start_time,
                                     auth_end_time=auth_end_time
                                     )
        ipData.save()

        data = get_auth_ip(request, True)
        return render(request, 'authorization.html', {'ipAllData': data})

    return HttpResponse('0')


# 删除一条已经存在的IP
def delete_auth_ip(request):
    if request.method == 'POST':
        will_IP_id = request.POST.get('will_IP_id')
        username = request.user
        Login_location_auth.objects.filter(id=will_IP_id, username=username).delete()

        data = get_auth_ip(request, True)
        return render(request, 'authorization.html', {'ipAllData': data})

    return HttpResponse('删除失败')


# 删除选中的所有IP授权
def delete_selectAll_IP(request):
    if request.method == 'POST':
        username = request.user
        chd_id = re.findall(r'\d+', request.POST.get('chk_id'))

        for i in chd_id:
            Login_location_auth.objects.filter(username=username, id=i).delete()

        data = get_auth_ip(request, True)
        return render(request, 'authorization.html', {'ipAllData': data})

    return HttpResponse('数据删除失败')


'''   -----------------        资产管理  --------------------    '''


# 资产授权信息 property_auth 数据库
# index页面和授权页面的函数
def get_propertyAuth_info(request, Tag=False):
    if request.method == 'POST':
        user = request.user
        data = property_auth.objects.filter(original_user=user).order_by('-share_start_time')
        num = data.count()
        tag = request.POST.get('tag')
        if Tag:
            return data

        if tag == '1':
            return render(request, 'authorization.html', {'propertyAllData': data, 'num': num})
        else:
            return render(request, 'index.html', {'allData': data.first()})

    return HttpResponseRedirect('index/')


# 共享资产
# 资产管理页面的功能
def add_share_info(request):
    if request.method == "POST":
        username = request.user
        propertyID = request.POST.get('id')
        share_users = request.POST.get('M_share_users')
        start_share_time = request.POST.get('M_start_share_time')
        end_share_time = request.POST.get('M_end_share_time')
        fileDescribe = request.POST.get('fileDescribe')
        # print(end_share_time)
        data = property_auth(individualProperty_id=propertyID, original_user=username,
                             share_start_time=start_share_time, share_end_time=end_share_time,
                             share_users=share_users, fileDescribe=fileDescribe,
                             )
        data.save()
        return HttpResponse('共享文件成功')
    return HttpResponse('共享文件失败')


# 删除一条资产授权
def delete_auth_property(request):
    if request.method == 'POST':
        delete_property_id = request.POST.get('delete_property_id')
        username = request.user

        property_auth.objects.filter(id=delete_property_id, original_user=username).delete()

        data = get_propertyAuth_info(request, True)
        return render(request, 'authorization.html', {'propertyAllData': data})

    return HttpResponse('删除失败')


# 修改资产授权信息
def modify_auth_property(request):
    if request.method == 'POST':
        username = request.user
        modify_id = request.POST.get('id')
        shared_username = request.POST.get('shared_username')
        M_share_start_time = request.POST.get('M_share_start_time')
        M_share_end_time = request.POST.get('M_share_end_time')
        sharedFile_describe = request.POST.get('sharedFile_describe')

        obj = property_auth.objects.filter(original_user=username, id=modify_id)
        if obj is not None:
            obj.update(share_users=shared_username, share_start_time=M_share_start_time,
                       share_end_time=M_share_end_time, fileDescribe=sharedFile_describe)

            data = get_propertyAuth_info(request, True)
            return render(request, 'authorization.html', {'propertyAllData': data})

    return HttpResponse('修改失败')


# 删除选中的所有资产授权
def delete_selectAll_properties(request):
    if request.method == 'POST':
        username = request.user
        chd_id = re.findall(r'\d+', request.POST.get('chk_id'))

        for i in chd_id:
            property_auth.objects.filter(original_user=username, id=i).delete()

        data = get_propertyAuth_info(request, True)
        return render(request, 'authorization.html', {'propertyAllData': data})

    return HttpResponse('数据删除失败')

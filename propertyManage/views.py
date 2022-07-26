import os
import traceback

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.contrib import messages
from django.core import serializers  # 用来处理json格式数据，格式化成json数据
import json
import re
import filetype
from login.models import userInfo
from authorizationManage.models import property_auth
from django.http import StreamingHttpResponse
from .otherFunc.judgeFileTypeAndOperate import *


# Create your views here.
# 手动保存文件
def handle_uploaded_file(f, username):
    # 用户文件目录
    myPath = os.path.join(BASE_DIR, 'media', username)
    if not os.path.exists(myPath):
        os.mkdir(myPath)

    # 文件名字目录
    fileName = f.name

    if ('jpeg' in fileName) or ('jpg' in fileName):
        fileName1, fileName2 = re.split('\.', fileName)
        fileName = fileName1 + '.' + 'png'

    filePath = os.path.join(myPath, fileName)

    if not os.path.exists(filePath):
        with open(os.path.join(myPath, fileName), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return 1, filePath, fileName
    else:
        return 0, filePath, fileName


# 新增数据 ajax方式
@login_required(login_url='/lg/login')
def add_data(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/PM/property/')

    username = request.user
    fileDescribe = request.POST.get("describe")
    secondPD = userInfo.objects.filter(username=username).first().second_password
    if (secondPD == '') or (secondPD is None):
        return HttpResponse("未设置二次密码")
    # 文件、采用单独保存的方法
    myFile = request.FILES['myFile']

    # 文件类型
    try:
        fileType = filetype.guess(myFile).mime
    except AttributeError:
        # filetype不能识别文本类型数据
        fileType = os.path.splitext(myFile.name)[-1]

    # 保存文件，自定义保存路径
    operateCode, filePath, fileName = handle_uploaded_file(myFile, str(username))
    # operateCode用于判断文件是否存在
    if operateCode == 1:
        # 描述
        describe = ''
        if (fileDescribe == '') or (fileDescribe is None):
            fileDescribe = '无'
        describe = '文件名称：' + fileName + '\n' + '其他：' + fileDescribe
        if request.POST.get("if_backup") == '1':
            backup = True
        else:
            backup = False
        try:
            if request.POST.get("if_encrypt") == '1':
                # 判断文件类型然后采用合适的方式加密
                # 主要有PDF、word、 PPT、 Excel、 TXT
                # 1表示加密
                print(filePath)
                judgeFileType(filePath, secondPD, fileType, 1)
                encryption = True
            else:
                encryption = False

            data = individual_property(user=username, type=fileType, describe=describe,
                                       backup=backup, encryption=encryption,
                                       fileName=fileName, filePath=filePath
                                       )
            data.save()
        except:
            traceback.print_exc()
            try:
                os.remove(filePath)
            finally:
                return HttpResponse("上传失败")

        alldata = get_all_data(request, tag=False)
        return render(request, 'property.html', {'allData': alldata})  # HttpResponseRedirect可以防止表单重复提交，也可以使用ajax方式
    else:
        return HttpResponse('文件已存在')


# 取得所有数据
@login_required(login_url='/lg/login')
def get_all_data(request, tag=True):
    if request.method == 'GET':
        return HttpResponseRedirect('/PM/property/')
    inquireUser = request.user
    response = individual_property.objects.filter(user=inquireUser)
    if response is None:
        return HttpResponse("无查询结果！")
    else:
        # jsonData = serializers.serialize('json', response)
        # request.session['queryResult'] = jsonData
        if not tag:
            return response
        else:
            return render(request, 'property.html', {'allData': response})


# 查询数据
@login_required(login_url='/lg/login')
def search_data(request):
    response = ''
    tag = 'Share'
    if request.method == 'GET':
        return HttpResponseRedirect('/PM/property/')

    username = request.user
    # 过滤器，搜索类别
    searchType = request.POST.get('searchType')

    # 搜索内容
    inquireContent = request.POST.get('inquireContent')

    if searchType == '资产类型':
        response = individual_property.objects.filter(type__contains=inquireContent, user=username)
    elif searchType == '描述' or searchType == '':
        response = individual_property.objects.filter(describe__contains=inquireContent, user=username)
    elif searchType == '被共享资产':
        tag = "NoShare"
        sharedProperties = property_auth.objects.filter(share_users__contains=username)
        id_list = []
        for obj in sharedProperties:
            id_list.append(obj.individualProperty_id)
        response = individual_property.objects.filter(id__in=id_list)
    elif searchType == '' and inquireContent == '':
        response = get_all_data(request, tag=False)
    else:
        return HttpResponseRedirect('/PM/property/')

    if response is None or response == '':
        return HttpResponse("无查询结果！")
    else:
        # share_tag 临时解决分享问题
        return render(request, 'property.html', {'allData': response, 'share_tag': tag})


# 删除所有选中的数据
@login_required(login_url='/lg/login')
def deleteAll(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/PM/property/')

    chd_id = re.findall(r'\d+', request.POST.get('chk_id'))
    user = request.user
    for i in chd_id:
        deleteObj = individual_property.objects.filter(user=user, id=i).first()
        os.remove(deleteObj.filePath)
        deleteObj.delete()

    data = get_all_data(request, tag=False)
    return render(request, 'property.html', {'allData': data})


# 删除其中一条数据
@login_required(login_url='/lg/login')
@csrf_exempt
def deleteOne(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/PM/property/')

    delete_ID = request.POST.get("delete_id")
    user = request.user
    deleteObj = individual_property.objects.filter(id=delete_ID, user=user).first()
    filePath = deleteObj.filePath
    # 删除对应文件
    if os.path.exists(filePath):
        os.remove(filePath)
    # 删除数据库内容
    deleteObj.delete()

    data = get_all_data(request, tag=False)
    return render(request, 'property.html', {'allData': data})


# 修改数据
@login_required(login_url='/lg/login')
def editOne(request):
    if request.method == 'POST':
        editID = request.POST.get('editID')
        # editUser = request.POST.get('editUser')
        # filePath = request.POST.get('filePath')

        # modifyTime = request.POST.get('modifyTime')   # 2022年3月8日 16:38
        # modifyTime_fm = datetime.date(*map(int, modifyTime.split('年/月/日/:/')))
        username = request.user
        describe = request.POST.get('describe')
        backup = True
        encryption = True
        secondPD = userInfo.objects.filter(username=username).first().second_password
        if (secondPD == '') or (secondPD is None):
            return HttpResponse("未设置二次密码")

        if request.POST.get('if-backup') == '0':
            backup = False

        if request.POST.get('if-encrypt') == '0':
            # 如果原本为加密了的，就解密，否则不执行
            if individual_property.objects.filter(id=editID).first().encryption:
                propertyObj = individual_property.objects.filter(user=username, id=editID).first()
                judgeFileType(propertyObj.filePath, secondPD, propertyObj.type, 0)
            encryption = False
        else:
            if not individual_property.objects.filter(id=editID).first().encryption:
                propertyObj = individual_property.objects.filter(user=username, id=editID).first()
                judgeFileType(propertyObj.filePath, secondPD, propertyObj.type, 1)

        individual_property.objects.filter(id=editID).update(describe=describe,
                                                             backup=backup, encryption=encryption)
        data = get_all_data(request, tag=False)
        return render(request, 'property.html', {'allData': data})

    return HttpResponseRedirect('/PM/property/')


# 下载文件
# 安全改进，用户名映射uid进行验证
@csrf_exempt
@login_required(login_url='/lg/login')
def downloadFile(request):
    if request.method == "POST":
        fileId = request.POST.get('id')
        username = request.user
        obj = individual_property.objects.filter(id=fileId, user=username).first()

        fileName = obj.fileName
        filePath = obj.filePath

        response = FileResponse(open(filePath, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName).encode('utf-8').decode(
            'ISO-8859-1')
        return response
    return HttpResponse('请求失败')


# 检测是否设置了二次密码
@login_required(login_url='/lg/login')
@csrf_exempt
def judge_make_secondPD(request):
    if request.method == 'POST':
        username = request.user
        second_password = userInfo.objects.filter(username=username).first().second_password
        if (second_password is None) or (second_password == ''):
            return HttpResponse("未设置二次密码")
        return HttpResponse("已设置二次密码")

    return HttpResponse(0)


# 设置二次密码
@csrf_exempt
@login_required(login_url='/lg/login')
def setSecondPD(request):
    if request.method == 'POST':
        code = request.POST['code']
        authCode = cache.get("verifyCode")
        if code == authCode:
            username = request.user
            secondPD = request.POST['secondPD']
            re_secondPD = request.POST['re_secondPD']
            if secondPD == re_secondPD:
                userInfo.objects.filter(username=username).update(second_password=secondPD)
                cache.delete("verifyCode")
                return HttpResponse("设置成功")
            else:
                return HttpResponse("两次密码不相同")
        else:
            return HttpResponse('验证码错误')
    return HttpResponse(0)

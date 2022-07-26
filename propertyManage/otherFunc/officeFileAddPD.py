# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 10:53
# @Author  : xiaosong
# @File    : officeFileAddPD.py
# @Software: PyCharm
import os
import time
import win32com.client
import pythoncom
from pptx import Presentation

from target_djangoProject1.settings import BASE_DIR


# office加密码和去除密码
def officeEncryption(path, password):
    # fileType的选项： Word.Application, Excel.Application, PowerPoint.Application
    # 若加密保存.docx时，覆盖原文件，则无法成功添加密码。但是保存为另一个文件名，则可以添加密码。
    # 因此将A存为B，删A，再将B改为A。
    wordType = ['docx', 'doc']
    excelType = ['xlsx', 'xlsx', 'csv']
    pptType = ['ppt', 'pptx', 'pps', 'ppsx', ' ppa', 'ppam', 'pot', 'potx', 'thmx']
    fileType = ''
    dirname, tempName = os.path.split(path)
    print(dirname)
    # print(path)
    # 判断文件类型
    for item in wordType:
        if item in tempName:
            fileType = 'Word.Application'
        break

    if fileType == '':
        for item in excelType:
            if item in tempName:
                fileType = 'Excel.Application'
            break

    if fileType == '':
        for item in pptType:
            if item in tempName:
                fileType = 'PowerPoint.Application'
            break

    path_temp = os.path.join(dirname, tempName)
    while os.path.exists(path_temp):
        tempName = f'{len(tempName)}' + tempName
        path_temp = os.path.join(dirname, tempName)

    def encryption(fp, pt, pw):
        global workContent, office_app
        try:
            pythoncom.CoInitialize()
            # print(fileType)
            office_app = win32com.client.Dispatch(fileType)
            office_app.DisplayAlerts = 0  # 不警告
            if fileType == 'Word.Application':
                # print(fp)
                office_app.Visible = 0  # 不显示
                workContent = office_app.Documents.Open(fp, False, False, False, '')
                workContent.SaveAs2(pt, None, False, pw)
                # os.remove(path)  # 删除原文件
                # os.rename(path_temp, path)  # 改临时文件名称为原文件名称
                workContent.Close()
                office_app.Quit()
            elif fileType == "Excel.Application":
                office_app.Visible = 0  # 不显示
                workContent = office_app.Workbooks.Open(fp, False, False, None, '')
                workContent.SaveAs(pt, None, pw)
                os.remove(path)  # 删除原文件
                os.rename(path_temp, path)  # 改临时文件名称为原文件名称
                workContent.Close()
                office_app.Quit()
            elif fileType == "PowerPoint.Application":
                workContent = office_app.Presentations.open(fp, False, False, False)
                workContent.Password = pw
                workContent.Save()
                workContent.Close()
                office_app.Quit()
        finally:
            time.sleep(0.5)
    encryption(path, path_temp, password)


def officeDecryption(path, password):
    # fileType的选项： Word.Application, Excel.Application, PowerPoint.Application
    # 若加密保存.docx时，覆盖原文件，则无法成功添加密码。但是保存为另一个文件名，则可以添加密码。
    # 因此将A存为B，删A，再将B改为A。
    wordType = ['docx', 'doc']
    excelType = ['xlsx', 'xlsx', 'csv']
    pptType = ['ppt', 'pptx', 'pps', 'ppsx', ' ppa', 'ppam', 'pot', 'potx', 'thmx']
    fileType = ''
    dirname, tempName = os.path.split(path)
    # 判断文件类型
    for item in wordType:
        if item in tempName:
            fileType = 'Word.Application'
        break

    if fileType == '':
        for item in excelType:
            if item in tempName:
                fileType = 'Excel.Application'
            break

    if fileType == '':
        for item in pptType:
            if item in tempName:
                fileType = 'PowerPoint.Application'
            break

    path_temp = os.path.join(dirname, tempName)
    while os.path.exists(path_temp):
        tempName = f'{len(tempName)}' + tempName
        path_temp = os.path.join(dirname, tempName)

    def decryption(fp, pt, pw):
        pythoncom.CoInitialize()
        global workContent
        # print(fileType)
        office_app = win32com.client.Dispatch(fileType)
        office_app.DisplayAlerts = 0  # 不警告
        if fileType == 'Word.Application':
            office_app.Visible = 0  # 不显示
            workContent = office_app.Documents.Open(fp, False, False, False, pw)
            workContent.SaveAs2(pt, None, False, pw)
            # os.remove(path)  # 删除原文件
            # os.rename(path_temp, path)  # 改临时文件名称为原文件名称
            workContent.Close()
            office_app.Quit()
            time.sleep(0.5)
        elif fileType == "Excel.Application":
            office_app.Workbooks.Visible = 0  # 不显示
            workContent = office_app.Workbooks.Open(fp, False, False, None, pw)
            workContent.SaveAs(pt, None, '')
            # os.remove(path)  # 删除原文件
            # os.rename(path_temp, path)  # 改临时文件名称为原文件名称
            workContent.Close()
            office_app.Quit()
            time.sleep(0.5)
        elif fileType == "PowerPoint.Application":
            office_app.__setattr__("Password", pw)
            workContent = office_app.Presentations.open(fp, False, False, False)
            workContent.Password = ''
            workContent.Save()
            workContent.Close()
            office_app.Quit()
            time.sleep(0.5)

    decryption(path, path_temp, password)


if __name__ == '__main__':
    key = '12345'  # 加密解密密匙
    # fileDir = os.path.join(BASE_DIR, 'media/hongsong/', "1.pptx")  # 指定路径不包含子路径
    # fileDir = os.path.join(BASE_DIR, 'media/hongsong/', "1.xlsx")  # 指定路径不包含子路径
    fileDir = os.path.join(BASE_DIR, 'media/hongsong/', "test.docx")  # 指定路径不包含子路径
    # officeDecryption(fileDir, key)
    officeEncryption(fileDir, key)

    print('encryption success')
